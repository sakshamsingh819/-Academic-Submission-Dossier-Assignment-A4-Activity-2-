# Smart Build-Cache Invalidation Engine & CI/CD Pipeline

[![CI Pipeline](https://github.com/sakshamsingh819/-Academic-Submission-Dossier-Assignment-A4-Activity-2-/actions/workflows/ci.yml/badge.svg)](https://github.com/sakshamsingh819/-Academic-Submission-Dossier-Assignment-A4-Activity-2-)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Pytest Tests](https://img.shields.io/badge/tests-21%20passed-brightgreen.svg)](tests/)
[![Cache Invalidation](https://img.shields.io/badge/cache%20freshness-100%25-success.svg)](src/cache_engine/)

> **Academic Submission Dossier — Assignment A4 / Activity 2**  
> **Course:** Automation in Software Development 
> **Candidate:** Saksham Singh  
> **USN:** `24BTRAO035`  
> **Specialization:** Artificial Intelligence & AI Driven DevOps  
> **Institution:** School of Computer Science and Engineering, Faculty of Engineering and Technology, JAIN (Deemed-to-be University)

---

## 1. Executive Summary & Problem Formulation

In modern DevOps and continuous integration (CI) workflows, caching dependencies and compilation artifacts is essential to keep developer feedback loops fast. However, naive caching strategies lead to severe engineering failures:

1. **Naive No-Cache Approach:** Every single commit downloads and compiles packages from scratch. This wastes substantial runner compute minutes, creates bottlenecked delivery pipelines, and incurs high cloud infrastructure costs.
2. **Naive Static Caching:** Reusing static cache keys (e.g., `deps-cache-v1`) creates **"ghost bugs"** and pipeline drift. When dependencies or transitive libraries change, the static cache supplies outdated binaries, resulting in false passes or unreproducible local vs. CI bugs.
3. **False Invalidation Thrashing:** In crude hashing systems, touching a single comment or whitespace line in `requirements.txt` invalidates the entire cache, wasting hundreds of megabytes of downloads.

### The Solution: Smart Build-Cache Invalidation
This project implements an intelligent, content-addressable build-cache invalidation architecture featuring:
* **Normalized Cryptographic Hashing (SHA-256):** Filters comments, line permutations, and formatting to prevent false cache busts.
* **Hierarchical Restore-Key Chains:** Falls back to prefix-matched caches to download *only the delta* on legitimate package updates.
* **Path-Based Impact Boundary Filtering:** Skips entire build and test pipelines when only documentation or non-executable assets are touched.
* **Docker Multi-Stage Layer Ordering:** Structures container instructions so heavy dependency layers remain 100% cached when source code changes.
* **Automated TTL & LRU Pruning:** Prevents cache storage bloat and branch cache poisoning.

---

## 2. Architecture & Invalidation Flowchart

```text
                                 [ Developer Commit ]
                                          │
                                          ▼
                         [ Path Impact Analyzer (ChangeDetector) ]
                                          │
             ┌────────────────────────────┼───────────────────────────┐
             │ Docs Only                  │ Source Only               │ Manifest Changed
             ▼                            ▼                           ▼
    ┌─────────────────┐          ┌─────────────────┐         ┌─────────────────────────┐
    │  SKIP PIPELINE  │          │ Exact Hit: Full │         │ Primary Key Miss        │
    │  Zero Runner    │          │ Dependency Cache│         │ Fallback Restore-Key    │
    │  Minutes Used   │          │ Reused (100%)   │         │ Matched (Partial Hit)   │
    └─────────────────┘          └────────┬────────┘         └────────────┬────────────┘
                                          │                               │
                                          │                               ▼
                                          │                   ┌────────────────────────┐
                                          │                   │ Download ONLY Delta    │
                                          │                   │ Dependencies (~12MB)   │
                                          │                   └───────────┬────────────┘
                                          ▼                               ▼
                                ┌──────────────────────────────────────────────────────┐
                                │             Automated Pytest Suite (21 Tests)        │
                                └─────────────────────────┬────────────────────────────┘
                                                          ▼
                                ┌──────────────────────────────────────────────────────┐
                                │       Save Updated Primary Cache Key for Future Hits │
                                └──────────────────────────────────────────────────────┘
```

---

## 3. Comparative Benchmark Results

Evaluated over an automated 10-commit continuous integration simulation cycle:

| Strategy | Total Build Latency | Total Bandwidth Consumed | Hit Ratio (%) | Stale / Ghost Builds |
| :--- | :---: | :---: | :---: | :---: |
| **Naive Uncached Pipeline** | 480.0 s | 1900.0 MB | 0.0% | 0 |
| **Naive Static-Key Caching** | 21.0 s | 0.0 MB | 100.0% | **2 (Critical Flaw)** |
| **Smart Build-Cache Invalidation** | **32.6 s** | **36.0 MB** | **80.0%** | **0 (100% Freshness)** |

### Quantitative Efficiency Achievements
* **93.21% Reduction in CI Execution Latency** (from 480s down to 32.6s).
* **98.11% Reduction in Network Transfer Volume** (from 1900MB down to 36.0MB).
* **Zero Ghost Builds (100% Invalidation Correctness)**: Guaranteed detection of every real dependency change.
* **100% Resiliency against False Invalidation**: Non-semantic comment and whitespace updates do not invalidate the cache.

---

## 4. Project File Structure

```text
.
├── .github/
│   └── workflows/
│       ├── ci.yml                     # Production CI workflow with smart cache & Docker caching
│       └── cache-benchmark.yml        # Automated performance benchmark workflow
├── src/
│   ├── __init__.py
│   ├── core/                          # Business Domain Microservices
│   │   ├── __init__.py
│   │   ├── pricing.py                 # Discount & tax rules with boundary constraints
│   │   ├── cart.py                    # Transaction aggregations & item management
│   │   └── inventory.py               # Stock allocation & concurrency guards
│   ├── cache_engine/                  # Smart Build-Cache Invalidation Core
│   │   ├── __init__.py
│   │   ├── hasher.py                  # Normalized SHA-256 cryptographic fingerprinting
│   │   ├── key_generator.py           # Primary keys & hierarchical fallback restore-keys
│   │   ├── dependency_graph.py        # Path-based change impact analyzer
│   │   └── cache_manager.py           # LRU, TTL, and cache telemetry orchestration
│   └── utils/
│       ├── __init__.py
│       └── logger.py                  # Structured audit logger
├── tests/                             # Comprehensive Automated Unit & Regression Suites
│   ├── __init__.py
│   ├── test_pricing.py
│   ├── test_cart.py
│   ├── test_inventory.py
│   └── test_smart_cache.py            # Rigorous tests for normalization, fallbacks & eviction
├── scripts/
│   ├── simulate_cache_lifecycle.py    # Visual step-by-step simulator for all 5 cache scenarios
│   ├── benchmark_performance.py       # Benchmark script generating quantitative metrics
│   └── generate_pdf_report.py         # Academic PDF Dossier generator using WeasyPrint
├── Dockerfile                         # Production multi-stage Dockerfile with smart layer caching
├── .dockerignore                      # Context filter preventing accidental layer cache busts
├── requirements.txt                   # Pinned application dependencies
├── requirements-dev.txt               # Development & test tooling
├── pyproject.toml                     # Modern build manifest
├── .gitignore                         # Comprehensive ignore file
├── README.md                          # Repository documentation
├── Smart_Build_Cache_Invalidation_Learnings.md # Comprehensive learning document
└── Smart_Build_Cache_Invalidation_Report.pdf   # Publication-ready academic report PDF
```

---

## 5. Quickstart & Local Verification

### 1. Clone & Set Up Virtual Environment
```bash
git clone <YOUR_REPO_URL>
cd "A4 A2"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 2. Run All Automated Pytest Suites (21 Tests)
```bash
python3 -m pytest -v
```

### 3. Run the Smart Cache Lifecycle Simulator
```bash
python3 scripts/simulate_cache_lifecycle.py
```

### 4. Run Quantitative CI Performance Benchmarks
```bash
python3 scripts/benchmark_performance.py
```

### 5. Generate the Academic PDF Submission Dossier
```bash
python3 scripts/generate_pdf_report.py
```

---

## 6. Author Information
* **Student Name:** Saksham Singh
* **USN:** `24BTRAO035`
* **Department:** Computer Science and Engineering
* **Specialization:** Artificial Intelligence / AI Driven DevOps
* **Course:** Automation in Software Development (`24CSE538`)
* **Institution:** JAIN (Deemed-to-be University), Bangalore
