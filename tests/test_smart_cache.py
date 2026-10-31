"""
Comprehensive Test Suite for Smart Build-Cache Invalidation Engine.
Verifies hashing normalization, restore-key chains, path filtering, and eviction.
Author: Saksham Singh (24BTRAO035)
"""
import os
import tempfile
import time
import pytest
from src.cache_engine.hasher import ContentHasher
from src.cache_engine.key_generator import CacheKeyGenerator
from src.cache_engine.dependency_graph import ChangeDetector, ImpactDomain
from src.cache_engine.cache_manager import SmartCacheManager, LookupStatus


def test_hasher_normalization_comments_and_order():
    """
    Validates that comments, blank lines, and line re-ordering do NOT falsely invalidate the cache.
    """
    with tempfile.NamedTemporaryFile("w+", delete=False) as f1, tempfile.NamedTemporaryFile("w+", delete=False) as f2:
        try:
            # File 1: Unsorted with comments and whitespaces
            f1.write("# Dependencies\nfastapi==0.115.8  \n\n# Web server\nuvicorn==0.34.0\npydantic==2.10.6\n")
            f1.flush()

            # File 2: Alphabetical order, different comments and extra blank lines
            f2.write("pydantic==2.10.6\n# Different comment\nfastapi==0.115.8\nuvicorn==0.34.0\n\n")
            f2.flush()

            hash1 = ContentHasher.hash_manifest_normalized(f1.name)
            hash2 = ContentHasher.hash_manifest_normalized(f2.name)

            assert hash1 == hash2, f"Hashes must match despite order/comment changes: {hash1} vs {hash2}"
        finally:
            os.remove(f1.name)
            os.remove(f2.name)


def test_hasher_invalidates_on_version_bump():
    """
    Validates that changing a package version triggers a genuine cache invalidation.
    """
    with tempfile.NamedTemporaryFile("w+", delete=False) as f1, tempfile.NamedTemporaryFile("w+", delete=False) as f2:
        try:
            f1.write("fastapi==0.115.8\nuvicorn==0.34.0\n")
            f1.flush()

            f2.write("fastapi==0.116.0\nuvicorn==0.34.0\n")
            f2.flush()

            hash1 = ContentHasher.hash_manifest_normalized(f1.name)
            hash2 = ContentHasher.hash_manifest_normalized(f2.name)

            assert hash1 != hash2, "Version bump must produce distinct hash to invalidate stale cache"
        finally:
            os.remove(f1.name)
            os.remove(f2.name)


def test_cache_key_generation_and_fallbacks():
    """
    Verifies primary key generation and hierarchical fallback restore keys.
    """
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        try:
            f.write("pytest==9.2.0\n")
            f.flush()

            gen = CacheKeyGenerator(os_name="Linux", runtime="py312", branch="feature/fast-ci")
            hierarchy = gen.generate_keys(f.name)

            assert hierarchy.primary_key.startswith("smartci-linux-py312-feature-fast-ci-")
            assert len(hierarchy.restore_keys) == 3
            assert hierarchy.restore_keys[0] == "smartci-linux-py312-feature-fast-ci-"
            assert hierarchy.restore_keys[1] == "smartci-linux-py312-"
            assert hierarchy.restore_keys[2] == "smartci-linux-"
        finally:
            os.remove(f.name)


def test_path_change_impact_detection():
    """
    Verifies path-based invalidation boundaries.
    """
    # Docs only -> Skip
    assert ChangeDetector.evaluate_impact(["README.md", "docs/architecture.png"]) == ImpactDomain.DOCS_ONLY
    assert ChangeDetector.should_skip_pipeline(["README.md"]) is True

    # Tests only -> Reuse compilation cache, run test suites
    assert ChangeDetector.evaluate_impact(["tests/test_cart.py"]) == ImpactDomain.TESTS_ONLY

    # Application source -> Recompile app bytecode
    assert ChangeDetector.evaluate_impact(["src/core/pricing.py"]) == ImpactDomain.SRC_ONLY

    # Dependency manifest -> Invalidate dependency cache
    assert ChangeDetector.evaluate_impact(["requirements.txt", "src/core/pricing.py"]) == ImpactDomain.MANIFEST_CHANGED

    # Dockerfile -> Invalidate container layers
    assert ChangeDetector.evaluate_impact(["Dockerfile"]) == ImpactDomain.DOCKER_CHANGED


def test_smart_cache_manager_lifecycle():
    """
    Validates Cold Miss -> Put -> Warm Exact Hit -> Partial Restore-Key Hit -> TTL Expire.
    """
    mgr = SmartCacheManager(max_capacity_mb=500.0, ttl_seconds=2.0)

    key_v1 = "smartci-linux-py312-main-aaaa1111"
    key_v2 = "smartci-linux-py312-main-bbbb2222"
    restore_keys = ["smartci-linux-py312-main-", "smartci-linux-py312-"]

    # 1. Cold query -> Miss
    decision1 = mgr.query(key_v1, restore_keys)
    assert decision1.status == LookupStatus.MISS

    # 2. Store built artifact
    mgr.put(key_v1, size_mb=150.0, payload={"packages": "fastapi,uvicorn"})

    # 3. Exact warm query -> Exact Hit
    decision2 = mgr.query(key_v1, restore_keys)
    assert decision2.status == LookupStatus.EXACT_HIT
    assert decision2.matched_key == key_v1
    assert decision2.time_saved_seconds > 0

    # 4. New commit with updated dependency -> Partial Hit via restore-key prefix
    decision3 = mgr.query(key_v2, restore_keys)
    assert decision3.status == LookupStatus.PARTIAL_HIT
    assert decision3.matched_key == key_v1

    # 5. Verify hit ratio calculation
    # 3 total queries, 1 exact hit + 1 partial hit = 2/3 = 66.67%
    assert mgr.hit_ratio_percentage() == 66.67

    # 6. Test TTL Expiration
    time.sleep(2.1)
    decision4 = mgr.query(key_v1, restore_keys=None)
    assert decision4.status == LookupStatus.INVALIDATED


def test_cache_lru_eviction():
    """
    Validates LRU eviction when cache exceeds capacity threshold.
    """
    mgr = SmartCacheManager(max_capacity_mb=100.0)
    mgr.put("entry-1", size_mb=60.0)
    mgr.put("entry-2", size_mb=30.0)

    # Size is 90MB, fits within 100MB
    assert mgr.current_size_mb() == 90.0

    # Adding 30MB entry forces eviction of oldest ("entry-1")
    mgr.put("entry-3", size_mb=30.0)
    assert "entry-1" not in mgr._storage
    assert "entry-2" in mgr._storage
    assert "entry-3" in mgr._storage
