"""
Cache Manager Orchestration & Decision Engine.
Implements exact key lookups, hierarchical restore-key resolution, eviction, and telemetry.
Author: Saksham Singh (24BTRAO035)
"""
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


class LookupStatus(Enum):
    EXACT_HIT = auto()       # Exact key match: 100% cache warm hit
    PARTIAL_HIT = auto()     # Fallback restore-key matched: partial delta hit
    MISS = auto()            # Cache miss: cold build required
    INVALIDATED = auto()     # Stale or purged: forced rebuild


@dataclass
class CacheEntry:
    key: str
    size_mb: float
    created_at: float
    last_accessed: float
    payload: Dict[str, str] = field(default_factory=dict)
    access_count: int = 0


@dataclass
class CacheDecision:
    status: LookupStatus
    matched_key: Optional[str]
    time_saved_seconds: float
    bandwidth_saved_mb: float
    action_description: str


class SmartCacheManager:
    """
    Simulates and orchestrates local and CI runner cache storage.
    Enforces maximum capacity (MB) and Least-Recently-Used (LRU) pruning.
    Tracks quantitative efficiency metrics.
    """

    def __init__(self, max_capacity_mb: float = 1000.0, ttl_seconds: float = 86400 * 7):
        self.max_capacity_mb = max_capacity_mb
        self.ttl_seconds = ttl_seconds
        self._storage: Dict[str, CacheEntry] = {}
        
        # Telemetry counters
        self.total_lookups: int = 0
        self.exact_hits: int = 0
        self.partial_hits: int = 0
        self.misses: int = 0
        self.total_time_saved_sec: float = 0.0
        self.total_bandwidth_saved_mb: float = 0.0

    def put(self, key: str, size_mb: float, payload: Optional[Dict[str, str]] = None) -> CacheEntry:
        """Stores or overwrites a cache entry. Evicts LRU entries if capacity exceeded."""
        self._evict_if_needed(incoming_size_mb=size_mb)
        now = time.time()
        entry = CacheEntry(
            key=key,
            size_mb=size_mb,
            created_at=now,
            last_accessed=now,
            payload=payload or {},
            access_count=1
        )
        self._storage[key] = entry
        return entry

    def query(self, primary_key: str, restore_keys: Optional[List[str]] = None) -> CacheDecision:
        """
        Queries cache using exact key first, then searches restore-key prefixes in order.
        """
        self.total_lookups += 1
        now = time.time()

        # Step 1: Check exact match
        if primary_key in self._storage:
            entry = self._storage[primary_key]
            # Check TTL
            if (now - entry.created_at) > self.ttl_seconds:
                del self._storage[primary_key]
                self.misses += 1
                return CacheDecision(
                    status=LookupStatus.INVALIDATED,
                    matched_key=None,
                    time_saved_seconds=0.0,
                    bandwidth_saved_mb=0.0,
                    action_description=f"Entry expired via TTL ({self.ttl_seconds}s); invalidated."
                )

            entry.last_accessed = now
            entry.access_count += 1
            self.exact_hits += 1
            time_saved = 45.0  # Approx savings for 100% warm pip cache
            bw_saved = entry.size_mb
            self.total_time_saved_sec += time_saved
            self.total_bandwidth_saved_mb += bw_saved
            return CacheDecision(
                status=LookupStatus.EXACT_HIT,
                matched_key=primary_key,
                time_saved_seconds=time_saved,
                bandwidth_saved_mb=bw_saved,
                action_description=f"Exact match on key '{primary_key}'. Reusing full cache."
            )

        # Step 2: Fallback to ordered restore-keys (Prefix matching)
        if restore_keys:
            for prefix in restore_keys:
                for existing_key, entry in sorted(self._storage.items(), key=lambda kv: kv[1].last_accessed, reverse=True):
                    if existing_key.startswith(prefix):
                        entry.last_accessed = now
                        entry.access_count += 1
                        self.partial_hits += 1
                        time_saved = 32.0  # Savings for partial reuse (only installing delta)
                        bw_saved = entry.size_mb * 0.75
                        self.total_time_saved_sec += time_saved
                        self.total_bandwidth_saved_mb += bw_saved
                        return CacheDecision(
                            status=LookupStatus.PARTIAL_HIT,
                            matched_key=existing_key,
                            time_saved_seconds=time_saved,
                            bandwidth_saved_mb=bw_saved,
                            action_description=f"Partial restore-key matched prefix '{prefix}' -> '{existing_key}'. Reusing base dependencies and downloading delta."
                        )

        # Step 3: Cache Miss
        self.misses += 1
        return CacheDecision(
            status=LookupStatus.MISS,
            matched_key=None,
            time_saved_seconds=0.0,
            bandwidth_saved_mb=0.0,
            action_description="Cache miss. Performing cold installation and saving new cache entry."
        )

    def current_size_mb(self) -> float:
        return sum(e.size_mb for e in self._storage.values())

    def _evict_if_needed(self, incoming_size_mb: float) -> None:
        """Evicts oldest accessed entries when storage limit is exceeded."""
        while (self.current_size_mb() + incoming_size_mb) > self.max_capacity_mb and self._storage:
            oldest_key = min(self._storage.keys(), key=lambda k: self._storage[k].last_accessed)
            del self._storage[oldest_key]

    def hit_ratio_percentage(self) -> float:
        if self.total_lookups == 0:
            return 0.0
        return round(((self.exact_hits + self.partial_hits) / self.total_lookups) * 100.0, 2)
