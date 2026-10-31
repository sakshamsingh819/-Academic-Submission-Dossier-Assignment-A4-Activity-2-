# ==============================================================================
# SMART BUILD-CACHE OPTIMIZED DOCKERFILE
# Architecture: Multi-Stage Layer Caching with Invariant Isolation
# Candidate: Saksham Singh (USN: 24BTRAO035) | AI DRIVE DEVOPS
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build & Dependency Resolution Layer (Infrequent Invalidation)
# ------------------------------------------------------------------------------
FROM python:3.12-slim AS builder

# Establish isolated build context
WORKDIR /install

# Install system compilation utilities if required (cached across all application builds)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# SMART CACHE INSTRUCTION 1: Copy ONLY dependency manifests
# This isolates the heavy compilation and download step from volatile application source changes.
COPY requirements.txt .

# Compile wheels into dedicated wheelhouse directory
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir=/install/wheels -r requirements.txt

# ------------------------------------------------------------------------------
# Stage 2: Minimal Distroless / Slim Production Runtime (High Cache Reuse)
# ------------------------------------------------------------------------------
FROM python:3.12-slim AS runner

# Environmental tuning for containerized Python execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# SMART CACHE INSTRUCTION 2: Install pre-built wheels from Stage 1
COPY --from=builder /install/wheels /wheels
COPY --from=builder /install/requirements.txt .
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# SMART CACHE INSTRUCTION 3: Copy volatile source code at the VERY LAST layer
# When code in src/ changes, layers 1 through 4 remain 100% CACHED!
COPY src/ /app/src/

# Security Hardening: Non-root execution
RUN useradd -u 10001 -m appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Healthcheck to verify runtime integrity
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

ENTRYPOINT ["python3", "-m", "pytest", "tests/"]
