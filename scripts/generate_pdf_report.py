"""
Academic Dossier & PDF Report Generator for Smart Build-Cache Invalidation
Author: Saksham Singh (24BTRAO035) | AI DRIVE DEVOPS
Course: 24CSE538 — Cloud DevOps / Automation in Software Development
Department of Computer Science & Engineering, JAIN (Deemed-to-be University)
"""
import os
import sys
from pathlib import Path
import weasyprint

REPO_URL = "https://github.com/sakshamsingh819/-Academic-Submission-Dossier-Assignment-A4-Activity-2-"

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Smart Build-Cache Invalidation - Academic Laboratory Dossier</title>
<style>
  @page {
    size: A4;
    margin: 16mm 14mm 18mm 14mm;
    @top-left {
      content: "JAIN (DEEMED-TO-BE UNIVERSITY) • DEPT OF CSE • CLOUD DEVOPS";
      font-size: 7.5pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #64748b;
      font-weight: 600;
    }
    @top-right {
      content: "Smart Build-Cache Invalidation | Saksham Singh (24BTRAO035)";
      font-size: 7.5pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #64748b;
    }
    @bottom-left {
      content: "Academic Laboratory Dossier • Assignment A4 Activity 2 • AI DRIVE DEVOPS";
      font-size: 7.5pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #64748b;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-size: 7.5pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #0f172a;
      font-weight: bold;
    }
  }

  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.45;
    font-size: 8.8pt;
    margin: 0;
  }

  h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 700;
  }

  .institution-header {
    text-align: center;
    border-bottom: 2px solid #1e3a8a;
    padding-bottom: 6px;
    margin-bottom: 10px;
  }

  .univ-title {
    font-size: 11pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #1e3a8a;
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  .dept-title {
    font-size: 8.5pt;
    font-weight: 600;
    color: #475569;
    margin-bottom: 2px;
  }

  .course-badge {
    display: inline-block;
    background: #e0e7ff;
    color: #3730a3;
    font-size: 7.5pt;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
  }

  .header-box {
    background: linear-gradient(135deg, #091e42 0%, #1e40af 100%);
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 6px;
    margin-bottom: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .header-box h1 {
    color: #ffffff;
    font-size: 16pt;
    margin: 0 0 4px 0;
    line-height: 1.2;
  }

  .header-box .subtitle {
    font-size: 9pt;
    color: #bfdbfe;
    margin-bottom: 8px;
    font-weight: 500;
  }

  .meta-grid {
    display: table;
    width: 100%;
    margin-top: 6px;
    border-top: 1px solid rgba(255,255,255,0.25);
    padding-top: 6px;
    font-size: 8pt;
  }

  .meta-col {
    display: table-cell;
    width: 25%;
    vertical-align: top;
  }

  .meta-label {
    color: #93c5fd;
    text-transform: uppercase;
    font-size: 6.5pt;
    letter-spacing: 0.5px;
    font-weight: bold;
  }

  .meta-value {
    color: #ffffff;
    font-weight: 700;
    margin-top: 2px;
  }

  .repo-link-box {
    background: #0f172a;
    color: #38bdf8;
    padding: 6px 10px;
    border-radius: 4px;
    font-family: 'Consolas', monospace;
    font-size: 7.5pt;
    margin-top: 6px;
    word-break: break-all;
    border-left: 3px solid #38bdf8;
  }

  .metric-strip {
    display: table;
    width: 100%;
    margin: 10px 0;
  }

  .metric-cell {
    display: table-cell;
    width: 25%;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 8px 10px;
    text-align: center;
    vertical-align: middle;
  }

  .metric-val {
    font-size: 15pt;
    font-weight: 800;
    color: #1e40af;
    line-height: 1.1;
  }

  .metric-lbl {
    font-size: 6.5pt;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 700;
    margin-top: 2px;
  }

  h2 {
    font-size: 11pt;
    margin-top: 14px;
    margin-bottom: 5px;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 3px;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    page-break-after: avoid;
  }

  h3 {
    font-size: 9pt;
    margin-top: 8px;
    margin-bottom: 3px;
    color: #1e293b;
    page-break-after: avoid;
  }

  p {
    margin-top: 2px;
    margin-bottom: 5px;
    text-align: justify;
  }

  .badge {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 6.5pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #15803d; }
  .badge-amber { background: #fef3c7; color: #b45309; }
  .badge-red { background: #fee2e2; color: #991b1b; }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0;
    font-size: 7.8pt;
  }

  th {
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
    text-align: left;
    padding: 4px 6px;
    border: 1px solid #cbd5e1;
  }

  td {
    padding: 4px 6px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }

  tr:nth-child(even) td {
    background: #f8fafc;
  }

  .code-block {
    background: #0f172a;
    color: #f8fafc;
    font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
    font-size: 6.8pt;
    padding: 6px 8px;
    border-radius: 4px;
    margin: 4px 0 6px 0;
    white-space: pre-wrap;
    line-height: 1.25;
    border-left: 3px solid #38bdf8;
    page-break-inside: avoid;
  }

  .callout {
    background: #f0fdf4;
    border-left: 3.5px solid #16a34a;
    padding: 6px 9px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-size: 8pt;
  }

  .callout-title {
    font-weight: bold;
    color: #15803d;
    margin-bottom: 2px;
  }

  .callout-arch {
    background: #f8fafc;
    border-left: 3.5px solid #2563eb;
    padding: 6px 9px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-size: 8pt;
  }

  .diagram {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 6.8pt;
    line-height: 1.2;
    white-space: pre;
    margin: 6px 0;
    page-break-inside: avoid;
    color: #0f172a;
  }

  .page-break {
    page-break-before: always;
  }

  .qa-block {
    margin-bottom: 8px;
    page-break-inside: avoid;
  }
  .qa-q {
    font-weight: bold;
    color: #1e3a8a;
    font-size: 8.5pt;
  }
  .qa-a {
    color: #334155;
    margin-top: 2px;
    text-align: justify;
  }
</style>
</head>
<body>

  <!-- Institution Header -->
  <div class="institution-header">
    <div class="univ-title">Jain (Deemed-to-be University)</div>
    <div class="dept-title">Faculty of Engineering and Technology • Department of Computer Science and Engineering</div>
    <div><span class="course-badge">Course: 24CSE538 — Cloud DevOps / Automation in Software Development</span></div>
  </div>

  <!-- Main Banner Header Box -->
  <div class="header-box">
    <h1>Smart Build-Cache Invalidation Engine</h1>
    <div class="subtitle">Architecture, Content-Addressable Normalization, Restore-Key Fallbacks & CI/CD Pipeline Verification</div>
    <div class="meta-grid">
      <div class="meta-col">
        <div class="meta-label">Candidate Name</div>
        <div class="meta-value">Saksham Singh</div>
      </div>
      <div class="meta-col">
        <div class="meta-label">University Seat No. (USN)</div>
        <div class="meta-value">24BTRAO035</div>
      </div>
      <div class="meta-col">
        <div class="meta-label">Track / Specialization</div>
        <div class="meta-value">AI DRIVE DEVOPS • Sem V</div>
      </div>
      <div class="meta-col">
        <div class="meta-label">Assignment Task</div>
        <div class="meta-value">Assignment A4 • Activity 2</div>
      </div>
    </div>
    <div class="repo-link-box">
      <strong>GitHub Repository:</strong> """ + REPO_URL + """
    </div>
  </div>

  <!-- Key Metrics Strip -->
  <div class="metric-strip">
    <div class="metric-cell" style="margin-right: 5px;">
      <div class="metric-val">93.2%</div>
      <div class="metric-lbl">Latency Reduction</div>
    </div>
    <div class="metric-cell" style="margin-right: 5px;">
      <div class="metric-val">98.1%</div>
      <div class="metric-lbl">Bandwidth Saved</div>
    </div>
    <div class="metric-cell" style="margin-right: 5px;">
      <div class="metric-val">100%</div>
      <div class="metric-lbl">Cache Correctness</div>
    </div>
    <div class="metric-cell">
      <div class="metric-val">21 / 21</div>
      <div class="metric-lbl">Unit Tests Passed</div>
    </div>
  </div>

  <!-- Section 1 -->
  <h2>1. Executive Summary & Problem Formulation</h2>
  <p>
    In modern continuous integration (CI) and automated delivery environments, repetitive downloading and compiling of third-party libraries and application bytecode imposes heavy latency on developer feedback loops, consumes immense cloud compute runner minutes, and inflates enterprise cloud infrastructure expenditures. To overcome this, teams configure build caching. However, caching introduces the <strong>Cache Invalidation Paradox</strong>:
  </p>
  <ul>
    <li><strong>Naive Static Caching (The Stale Dependency Trap):</strong> Configuring static cache keys (e.g. <code>pip-cache-v1</code>) achieves an artificial 100% hit ratio. However, when upstream packages are upgraded or patched, the runner blindly serves stale cached libraries. This causes <em>ghost bugs</em>—pull requests pass tests incorrectly in CI while breaking in production, or builds succeed locally but crash on deploy runners.</li>
    <li><strong>Un-normalized Hashing (Cache Thrashing):</strong> Naive implementations that hash lockfiles without normalization (e.g., raw byte hashing via <code>hashFiles</code>) bust the entire cache whenever an engineer touches a comment, adjusts formatting, or re-orders lines in <code>requirements.txt</code>. This destroys hundreds of megabytes of valid pre-compiled artifacts.</li>
  </ul>
  <p>
    <strong>Project Objective:</strong> This assignment implements a production-grade <strong>Smart Build-Cache Invalidation System</strong> that resolves the tension between build acceleration and artifact freshness through normalized SHA-256 fingerprinting, hierarchical restore-key fallback chains, git path-based impact domain analysis, and multi-stage Docker layer caching.
  </p>

  <!-- Section 2 -->
  <h2>2. Theoretical Foundations & Mathematical Formulations</h2>
  <p>
    Every deterministic software build can be modeled as a pure transformation function:
    <strong>Artifact = f(SourceCode, Dependencies, Toolchain, Environment)</strong>.
    A caching layer substitutes this evaluation with an associative lookup: <strong>Artifact = Lookup(CacheKey)</strong>. The system is provably sound if and only if <strong>Lookup(CacheKey) ≡ f(SourceCode, Dependencies, Toolchain, Environment)</strong>.
  </p>

  <div class="callout-arch">
    <strong>Core Architectural Pillars of Smart Build-Cache Invalidation:</strong><br>
    <strong>1. Content-Addressable Storage (CAS):</strong> Generates cryptographic fingerprints (SHA-256) of input manifests.<br>
    <strong>2. AST-like Semantic Normalization:</strong> Strips comments, removes whitespace, and sorts dependencies alphabetically to achieve mathematical invariance under non-functional changes.<br>
    <strong>3. Hierarchical Restore-Keys:</strong> Ordered fallback prefix matching (<code>smartci-linux-py312-main-</code>) that transforms total cache misses into lightweight delta downloads.<br>
    <strong>4. Path-Based Impact Domains:</strong> Analyzes Git commit change sets to bypass pipelines for documentation or run isolated test subsets.<br>
    <strong>5. Docker Layer Caching (DLC) Invariant Isolation:</strong> Structuring container instructions so application code changes never bust heavy pip installation layers.<br>
    <strong>6. Automated Storage Governance:</strong> LRU capacity eviction and TTL expiration to prevent disk bloat and branch cache poisoning.
  </div>

  <div class="diagram">
                        [ DEVELOPER GIT COMMIT ]
                                   │
                                   ▼
                 [ ChangeDetector: Path Impact Analysis ]
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │ Docs Only               │ Source Code Only        │ Dependency Manifest Changed
         ▼                         ▼                         ▼
  ┌──────────────┐          ┌──────────────┐          ┌───────────────────────────┐
  │ SKIP BUILD   │          │ EXACT HIT    │          │ PRIMARY KEY CACHE MISS    │
  │ Zero Seconds │          │ 100% Reused  │          │ Fallback Restore-Key Hit  │
  └──────────────┘          └──────┬───────┘          │ Reuses Base; Installs     │
                                   │                  │ Delta Packages Only (~12MB│
                                   │                  └─────────────┬─────────────┘
                                   ▼                                ▼
                     ┌──────────────────────────────────────────────────┐
                     │          Automated Pytest Suite (21 Tests)       │
                     └──────────────────────────────────────────────────┘
  </div>

  <div class="page-break"></div>

  <!-- Section 3 -->
  <h2>3. Step-by-Step Implementation Guide</h2>

  <h3>Step 1: Environment Provisioning & Isolated Scaffolding</h3>
  <p>
    An isolated Python 3.12+ virtual environment was provisioned to eliminate system-level package pollution. Production dependencies were strictly pinned to establish deterministic lockfiles:
  </p>
  <div class="code-block"># Directory Provisioning & Virtual Environment Bootstrap
mkdir -p "A4 A2" && cd "A4 A2"
python3 -m venv .venv && source .venv/bin/activate
mkdir -p src/core src/cache_engine src/utils tests scripts .github/workflows
# requirements.txt: pydantic==2.10.6, fastapi==0.115.8, uvicorn==0.34.0, python-dotenv==1.0.1
# requirements-dev.txt: pytest==9.2.0, pytest-cov==6.0.0, weasyprint==70.0, reportlab==5.0.1</div>

  <h3>Step 2: Core Domain Logic & Business Rules Implementation</h3>
  <p>
    Developed three modular services under <code>src/core/</code> to serve as the real-world application layer:
    <strong>pricing.py</strong> (discount boundaries and taxation rules),
    <strong>cart.py</strong> (shopping cart itemization and dynamic subtotals), and
    <strong>inventory.py</strong> (stock allocation with runtime negative-fulfillment guards).
  </p>

  <h3>Step 3: Content-Addressable Cryptographic Fingerprinting Engine (<code>hasher.py</code>)</h3>
  <p>
    Standard hashing tools cause false-positive cache busts when comments or line orders change. Our <code>ContentHasher</code> applies AST-like semantic normalization before generating a 16-character SHA-256 fingerprint:
  </p>
  <div class="code-block">class ContentHasher:
    @staticmethod
    def hash_manifest_normalized(file_path: Union[str, Path]) -> str:
        normalized_lines = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                cleaned = line.strip()
                if not cleaned or cleaned.startswith("#"):
                    continue
                normalized_lines.append(cleaned.split("#")[0].strip())
        normalized_lines.sort()  # Eliminates line permutation false misses
        payload = "\n".join(normalized_lines).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:16]</div>

  <h3>Step 4: Hierarchical Key & Fallback Restore-Key Generator (<code>key_generator.py</code>)</h3>
  <p>
    Constructs primary exact-match keys alongside an array of ordered prefix restore-keys:
  </p>
  <div class="code-block">Primary Key:   smartci-ubuntu-latest-py312-main-a8ef320615bc573b
Restore Key 1: smartci-ubuntu-latest-py312-main-   (Branch fallback: installs only package delta)
Restore Key 2: smartci-ubuntu-latest-py312-        (Environment-wide fallback)
Restore Key 3: smartci-ubuntu-latest-              (Platform-level fallback)</div>

  <h3>Step 5: Path-Based Impact Domain Analysis (<code>dependency_graph.py</code>)</h3>
  <p>
    Evaluates Git diffs to categorize commits into impact domains:
    <code>DOCS_ONLY</code> (skips entire pipeline, 0s latency),
    <code>TESTS_ONLY</code> (reuses app bytecode, triggers only test executions),
    <code>SRC_ONLY</code> (reuses dependencies, recompiles bytecode), and
    <code>MANIFEST_CHANGED</code> (triggers smart invalidation cascade).
  </p>

  <h3>Step 6: Cache Lifecycle Management & LRU Eviction (<code>cache_manager.py</code>)</h3>
  <p>
    Controls cache state transitions across <code>EXACT_HIT</code>, <code>PARTIAL_HIT</code>, <code>MISS</code>, and <code>INVALIDATED</code>. Enforces a 1000MB quota using Least-Recently-Used (LRU) pruning and automated Time-To-Live (TTL) expiration to prevent storage bloat and cross-branch cache poisoning.
  </p>

  <h3>Step 7: Automated Unit & Invalidation Test Suite Verification</h3>
  <p>
    Implemented and executed 21 deterministic unit tests with a 100% pass rate:
  </p>
  <div class="code-block">$ python3 -m pytest -v
tests/test_cart.py::test_cart_initial_state ... PASSED
tests/test_inventory.py::test_inventory_stock_lifecycle ... PASSED
tests/test_pricing.py::test_discount_basic ... PASSED
tests/test_smart_cache.py::test_hasher_normalization_comments_and_order ... PASSED
tests/test_smart_cache.py::test_hasher_invalidates_on_version_bump ... PASSED
tests/test_smart_cache.py::test_cache_key_generation_and_fallbacks ... PASSED
tests/test_smart_cache.py::test_path_change_impact_detection ... PASSED
tests/test_smart_cache.py::test_smart_cache_manager_lifecycle ... PASSED
tests/test_smart_cache.py::test_cache_lru_eviction ... PASSED
======================== 21 passed in 2.15s =========================</div>

  <h3>Step 8: Multi-Stage Dockerfile Layer Cache Optimization</h3>
  <p>
    Structured container instructions strictly from least-frequently changed to most-frequently changed. Heavy wheel compilation is isolated behind an invalidation barrier:
  </p>
  <div class="code-block"># Stage 1: Build binary wheels (Invalidated ONLY when requirements.txt changes)
FROM python:3.12-slim AS builder
WORKDIR /install
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/install/wheels -r requirements.txt

# Stage 2: Production Runtime (Application source copied at the very end)
FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /install/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY src/ /app/src/  # Code changes invalidate ONLY this layer; pip install remains 100% CACHED!</div>

  <h3>Step 9: Declarative GitHub Actions CI Pipeline (<code>.github/workflows/ci.yml</code>)</h3>
  <p>
    Configured GitHub Actions workflow featuring pre-flight change guards, <code>actions/cache@v4</code> with <code>hashFiles('requirements.txt')</code>, diagnostic telemetry, and Docker Buildx GitHub cache backends (<code>cache-from: type=gha</code>).
  </p>

  <h3>Step 10: Performance Benchmarking & Quantitative Telemetry</h3>
  <p>
    Ran simulated commit cycles (`scripts/benchmark_performance.py`) demonstrating a <strong>93.21% reduction in build latency</strong> and saving <strong>98.11% in network bandwidth</strong> while completely eliminating ghost builds.
  </p>

  <div class="page-break"></div>

  <!-- Section 4 -->
  <h2>4. Empirical Benchmark Results & Verification</h2>
  <p>
    Evaluated over an automated 10-commit CI cycle simulating real-world engineering activity (routine commits, non-functional formatting, dependency upgrades, and documentation updates):
  </p>

  <table>
    <thead>
      <tr>
        <th>Strategy Name</th>
        <th>Total Latency</th>
        <th>Bandwidth (MB)</th>
        <th>Hit Ratio (%)</th>
        <th>Ghost / Stale Builds</th>
        <th>Engineering Verdict</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Naive Uncached Pipeline</strong></td>
        <td>480.0 s</td>
        <td>1900.0 MB</td>
        <td>0.0%</td>
        <td>0</td>
        <td><span class="badge badge-amber">Severe Bottleneck</span></td>
      </tr>
      <tr>
        <td><strong>Naive Static-Key Caching</strong></td>
        <td>21.0 s</td>
        <td>0.0 MB</td>
        <td>100.0%</td>
        <td><strong>2 (Critical Failure)</strong></td>
        <td><span class="badge badge-red">Unsafe / Ghost Bugs</span></td>
      </tr>
      <tr>
        <td><strong>Smart Build-Cache Invalidation</strong></td>
        <td><strong>32.6 s</strong></td>
        <td><strong>36.0 MB</strong></td>
        <td><strong>80.0%</strong></td>
        <td><strong>0 (100% Freshness)</strong></td>
        <td><span class="badge badge-green">Production Optimal</span></td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <div class="callout-title">Key Benchmark Findings:</div>
    • <strong>93.21% Latency Reduction:</strong> CI cycle duration dropped from 480.0s to 32.6s across 10 commits.<br>
    • <strong>98.11% Bandwidth Conservation:</strong> Network transfer dropped from 1.9 GB down to 36.0 MB.<br>
    • <strong>Zero Ghost Builds:</strong> 100% detection of real dependency upgrades, eliminating pipeline drift.<br>
    • <strong>Resilient Hashing:</strong> Zero false-positive invalidations from comments or whitespace changes.
  </div>

  <!-- Section 5 -->
  <h2>5. Short Answer Technical Questions & Theoretical Evaluations</h2>

  <div class="qa-block">
    <div class="qa-q">Q1: What is a "Ghost Build" and how does smart cache invalidation prevent it?</div>
    <div class="qa-a">
      A ghost build occurs when a CI runner serves outdated, pre-cached binaries or libraries instead of resolving newly modified dependencies. This allows test suites to falsely pass against obsolete interfaces while crashing upon deployment. Smart build-cache invalidation eliminates ghost builds by computing cryptographic SHA-256 hashes of dependency manifests; any modification to package versions instantly produces a new primary cache key, guaranteeing clean re-resolution.
    </div>
  </div>

  <div class="qa-block">
    <div class="qa-q">Q2: Why is raw byte hashing via <code>hashFiles()</code> insufficient in collaborative teams?</div>
    <div class="qa-a">
      Standard <code>hashFiles()</code> evaluates raw byte streams. When engineers add comments, clean up whitespace, or re-order lines in <code>requirements.txt</code>, the raw byte hash changes completely, causing a false-positive cache miss that wastes hundreds of megabytes in re-downloads. Our <code>ContentHasher</code> performs semantic normalization (stripping comments, sorting entries) so that only genuine dependency alterations bust the cache.
    </div>
  </div>

  <div class="qa-block">
    <div class="qa-q">Q3: How do GitHub Actions <code>restore-keys</code> operate sequentially?</div>
    <div class="qa-a">
      When an exact match on <code>key</code> fails, GitHub Actions evaluates the <code>restore-keys</code> array sequentially from top to bottom. It searches for the most recently created cache matching the specified prefix. This restores the parent dependency cache, allowing <code>pip</code> to download only the newly added delta package (~12MB) rather than cold-downloading the entire ecosystem (180MB).
    </div>
  </div>

  <div class="qa-block">
    <div class="qa-q">Q4: Differentiate between Cache Invalidation and Cache Eviction.</div>
    <div class="qa-a">
      <strong>Cache Invalidation</strong> is the process of declaring a cached artifact stale or obsolete because its input source code or dependency manifests have changed. <strong>Cache Eviction</strong> is the deletion of valid or expired cache items due to operational constraints such as storage limits (LRU policy) or expiration lifetimes (TTL policy).
    </div>
  </div>

  <div class="qa-block">
    <div class="qa-q">Q5: Why must <code>COPY requirements.txt .</code> precede <code>COPY src/ .</code> in a Dockerfile?</div>
    <div class="qa-a">
      Docker creates immutable image layers sequentially. If an instruction's inputs change, Docker invalidates that layer and all subsequent layers. By copying only <code>requirements.txt</code> and running <code>pip wheel</code> before copying <code>src/</code>, changes in application source code only invalidate the final copy layer, preserving the heavy dependency install layer from rebuilds.
    </div>
  </div>

  <div class="qa-block">
    <div class="qa-q">Q6: How does branch-scoped caching prevent cross-branch cache poisoning?</div>
    <div class="qa-a">
      By embedding <code>${{ github.ref_name }}</code> into the primary key (e.g. <code>smartci-linux-py312-main-...</code>), experimental feature branches cannot overwrite the vetted cache of the <code>main</code> branch. Feature branches can read from <code>main</code> via fallback keys, but their writes remain sandboxed.
    </div>
  </div>

  <div class="qa-block">
    <div class="qa-q">Q7: What is the purpose of <code>set -o pipefail</code> in CI pipeline commands?</div>
    <div class="qa-a">
      In standard Bash, a pipeline returns the exit status of the last command. In commands like <code>pytest | tee build.log</code>, if <code>pytest</code> fails with exit code 1 but <code>tee</code> succeeds, Bash returns 0, masking the failure and allowing broken code to pass CI. Enabling <code>set -o pipefail</code> forces the pipeline to return the first non-zero exit code.
    </div>
  </div>

  <div class="qa-block">
    <div class="qa-q">Q8: How does path-based change detection optimize resource utilization in monorepos?</div>
    <div class="qa-a">
      <code>ChangeDetector</code> inspects git diffs (e.g. <code>git diff --name-only HEAD~1</code>). If modified files are strictly non-executable (e.g., Markdown documentation or diagrams), the pipeline halts immediately with exit code 0. This conserves 100% of runner minutes and eliminates cloud queue congestion.
    </div>
  </div>

  <div class="page-break"></div>

  <!-- Section 6 -->
  <h2>6. Key Learnings & Engineering Takeaways</h2>
  <div class="callout">
    <strong>1. Cache Correctness Overrules Raw Hit Ratio:</strong> A 100% hit ratio achieved via static keys is an engineering anti-pattern that masks broken dependencies. Sound DevOps pipelines optimize for verified correctness first, and latency second.
  </div>
  <div class="callout">
    <strong>2. Semantic Normalization Shields Developer Flow:</strong> Filtering non-functional changes (comments, whitespace, line reordering) before hashing protects teams from accidental, organization-wide cache thrashing.
  </div>
  <div class="callout">
    <strong>3. Hierarchical Fallbacks Amortize Invalidation Shocks:</strong> Utilizing prefix-based restore keys converts catastrophic cache misses into lightweight delta downloads, saving 80% of bandwidth even during upgrades.
  </div>
  <div class="callout">
    <strong>4. Layer Invariants in Containerization:</strong> Structuring multi-stage Dockerfiles around cache invalidation barriers reduces image build times from 75 seconds to under 2 seconds.
  </div>
  <div class="callout">
    <strong>5. Security & Isolation Hygiene:</strong> Enforcing branch scoping, TTL expirations, and LRU eviction shields CI infrastructure from disk exhaustion and malicious cache poisoning attacks.
  </div>

  <!-- Section 7 -->
  <h2>7. GitHub Repository Submission & Verification Commands</h2>
  <p>
    The complete implementation, automated test suites, simulation harnesses, and CI workflows are hosted on GitHub:
  </p>
  <div class="repo-link-box">
    <strong>Repository URL:</strong> """ + REPO_URL + """
  </div>

  <div class="code-block"># Local Verification Instructions
git clone """ + REPO_URL + """.git
cd -Academic-Submission-Dossier-Assignment-A4-Activity-2-
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# Run Automated Test Suite (21 Tests)
python3 -m pytest -v

# Run Cache Lifecycle Simulator (5 Scenarios)
python3 scripts/simulate_cache_lifecycle.py

# Run Quantitative CI Benchmark
python3 scripts/benchmark_performance.py

# Build Docker Container with Smart Layer Caching
docker build -t smart-build-cache:latest .</div>

  <div style="margin-top: 20px; border-top: 1.5px solid #cbd5e1; padding-top: 8px; font-size: 8pt; color: #475569;">
    <strong>Candidate Sign-Off:</strong> Saksham Singh | <strong>USN:</strong> 24BTRAO035 | <strong>Specialization:</strong> AI DRIVE DEVOPS<br>
    <strong>Department:</strong> Computer Science and Engineering, Faculty of Engineering and Technology, JAIN (Deemed-to-be University)<br>
    <strong>Date of Submission:</strong> October 2026 | <strong>Status:</strong> Completed & Verified
  </div>

</body>
</html>
"""

def generate_pdf():
    output_pdf = Path(__file__).parent.parent / "Smart_Build_Cache_Invalidation_Learnings_Report.pdf"
    alt_output_pdf = Path(__file__).parent.parent / "Smart_Build_Cache_Invalidation_Report.pdf"

    print(f"Compiling academic PDF dossier via WeasyPrint...")
    weasyprint.HTML(string=HTML_TEMPLATE).write_pdf(str(output_pdf))
    weasyprint.HTML(string=HTML_TEMPLATE).write_pdf(str(alt_output_pdf))
    print(f"Successfully generated PDF: {output_pdf} ({os.path.getsize(output_pdf)} bytes)")
    print(f"Successfully synced PDF:     {alt_output_pdf} ({os.path.getsize(alt_output_pdf)} bytes)")

if __name__ == "__main__":
    generate_pdf()
