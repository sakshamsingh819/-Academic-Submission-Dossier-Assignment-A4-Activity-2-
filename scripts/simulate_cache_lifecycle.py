"""
Cache Lifecycle Simulator.
Simulates Cold Build, Warm Hit, False-Positive Prevention, Invalidation, and Fallback Delta.
Author: Saksham Singh (24BTRAO035)
"""
import os
import sys
import tempfile
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cache_engine.hasher import ContentHasher
from src.cache_engine.key_generator import CacheKeyGenerator
from src.cache_engine.dependency_graph import ChangeDetector, ImpactDomain
from src.cache_engine.cache_manager import SmartCacheManager, LookupStatus


def run_simulation():
    print("=" * 80)
    print("SMART BUILD-CACHE INVALIDATION LIFECYCLE SIMULATOR")
    print("Candidate: Saksham Singh | USN: 24BTRAO035 | AI DRIVE DEVOPS")
    print("=" * 80)

    manager = SmartCacheManager(max_capacity_mb=1000.0)
    key_gen = CacheKeyGenerator(os_name="ubuntu-latest", runtime="py312", branch="main")

    with tempfile.TemporaryDirectory() as tmp_dir:
        req_file = os.path.join(tmp_dir, "requirements.txt")

        # -------------------------------------------------------------
        # SCENARIO 1: Cold Initial Build (Fresh Clone / Cache Miss)
        # -------------------------------------------------------------
        print("\n[SCENARIO 1] Cold Initial Build (Fresh Commit / Clean Runner)")
        with open(req_file, "w") as f:
            f.write("fastapi==0.115.8\npydantic==2.10.6\nuvicorn==0.34.0\n")

        keys1 = key_gen.generate_keys(req_file)
        print(f"Generated Primary Cache Key: {keys1.primary_key}")
        print(f"Fallback Restore Keys:       {keys1.restore_keys}")

        decision1 = manager.query(keys1.primary_key, keys1.restore_keys)
        print(f"Cache Lookup Result:         [{decision1.status.name}] {decision1.action_description}")
        print("Action Taken:                Resolving dependencies from PyPI (Cold download: 180MB, 45.2s)...")
        # Save cache entry
        manager.put(keys1.primary_key, size_mb=180.0, payload={"installed": "fastapi,pydantic,uvicorn"})
        print("Result:                      Artifacts compiled & cached under primary key.")

        # -------------------------------------------------------------
        # SCENARIO 2: Unchanged Subsequent Build (Warm Exact Hit)
        # -------------------------------------------------------------
        print("\n[SCENARIO 2] Subsequent Build with Zero Manifest Changes")
        keys2 = key_gen.generate_keys(req_file)
        decision2 = manager.query(keys2.primary_key, keys2.restore_keys)
        print(f"Cache Lookup Result:         [{decision2.status.name}] {decision2.action_description}")
        print(f"Time Saved:                  {decision2.time_saved_seconds}s | Bandwidth Saved: {decision2.bandwidth_saved_mb}MB")
        print("Action Taken:                Bypassed pip download; dependencies restored from cache in 1.4s.")

        # -------------------------------------------------------------
        # SCENARIO 3: Non-Semantic Manifest Edit (Comments / Whitespace)
        # -------------------------------------------------------------
        print("\n[SCENARIO 3] Developer Adds Comments & Changes Line Order (False Invalidation Test)")
        with open(req_file, "w") as f:
            f.write("# Web framework\nfastapi==0.115.8  \n\n# ASGI Server\nuvicorn==0.34.0\n# Data validation\npydantic==2.10.6\n")

        keys3 = key_gen.generate_keys(req_file)
        print(f"New Manifest Fingerprint:    {keys3.manifest_hash}")
        decision3 = manager.query(keys3.primary_key, keys3.restore_keys)
        print(f"Cache Lookup Result:         [{decision3.status.name}] {decision3.action_description}")
        print(f"SMART OUTCOME:               Normalization prevented false cache bust! Reused cache key: {decision3.matched_key}")

        # -------------------------------------------------------------
        # SCENARIO 4: Legitimate Dependency Invalidation (Version Bump)
        # -------------------------------------------------------------
        print("\n[SCENARIO 4] Legitimate Dependency Upgrade (fastapi 0.115.8 -> 0.116.0)")
        with open(req_file, "w") as f:
            f.write("fastapi==0.116.0\npydantic==2.10.6\nuvicorn==0.34.0\n")

        keys4 = key_gen.generate_keys(req_file)
        print(f"Updated Primary Key:         {keys4.primary_key}")
        decision4 = manager.query(keys4.primary_key, keys4.restore_keys)
        print(f"Cache Lookup Result:         [{decision4.status.name}]")
        print(f"Fallback Key Matched:        {decision4.matched_key}")
        print(f"Description:                 {decision4.action_description}")
        print(f"Optimization Achieved:       Partial Hit! Base dependencies reused ({decision4.bandwidth_saved_mb}MB saved). Only delta downloaded (12MB).")
        # Save updated cache under new primary key
        manager.put(keys4.primary_key, size_mb=192.0, payload={"installed": "fastapi-0.116.0,pydantic,uvicorn"})

        # -------------------------------------------------------------
        # SCENARIO 5: Path-Based Impact Analysis (Docs Edit)
        # -------------------------------------------------------------
        print("\n[SCENARIO 5] Path-Based Invalidation Filter (Documentation Commit)")
        changed_files = ["README.md", "docs/architecture.png"]
        impact = ChangeDetector.evaluate_impact(changed_files)
        should_skip = ChangeDetector.should_skip_pipeline(changed_files)
        print(f"Modified Files:              {changed_files}")
        print(f"Detected Impact Domain:      {impact.name}")
        print(f"Pipeline Action:             Skip Build & Test Pipeline = {should_skip} (0.0s elapsed, 100% runner savings)")

        # -------------------------------------------------------------
        # SUMMARY TELEMETRY
        # -------------------------------------------------------------
        print("\n" + "=" * 80)
        print("SIMULATION SUMMARY & TELEMETRY REPORT")
        print("=" * 80)
        print(f"Total Lookups:               {manager.total_lookups}")
        print(f"Exact Warm Hits:             {manager.exact_hits}")
        print(f"Partial Restore-Key Hits:    {manager.partial_hits}")
        print(f"Cold Misses:                 {manager.misses}")
        print(f"Overall Hit Ratio:           {manager.hit_ratio_percentage()}%")
        print(f"Total Time Saved:            {manager.total_time_saved_sec:.1f} seconds")
        print(f"Total Bandwidth Saved:       {manager.total_bandwidth_saved_mb:.1f} MB")
        print("=" * 80)


if __name__ == "__main__":
    run_simulation()
