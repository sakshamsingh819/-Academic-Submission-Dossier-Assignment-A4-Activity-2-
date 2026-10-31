"""
Dependency Graph and Path-Based Impact Domain Analysis.
Determines granular invalidation boundaries based on changed files in a commit.
Author: Saksham Singh (24BTRAO035)
"""
from enum import Enum, auto
from pathlib import Path
from typing import List, Set


class ImpactDomain(Enum):
    DOCS_ONLY = auto()         # Only markdown/docs changed -> Skip CI build entirely
    TESTS_ONLY = auto()        # Only test suites changed -> Reuse dependencies & build cache
    SRC_ONLY = auto()          # Core source changed -> Reuse dependencies, recompile bytecode
    MANIFEST_CHANGED = auto()  # Lockfile/requirements changed -> Invalidate dependency cache
    DOCKER_CHANGED = auto()    # Dockerfile changed -> Invalidate container layer cache
    FULL_REBUILD = auto()      # Multiple mixed domains or unknown config changed


class ChangeDetector:
    """
    Evaluates modified file paths to infer the minimal required invalidation scope.
    Avoids unnecessary rebuilds of unchanged pipeline layers.
    """

    DOCS_EXTENSIONS = {".md", ".rst", ".txt", ".png", ".jpg", ".jpeg", ".svg"}
    MANIFEST_FILES = {"requirements.txt", "requirements-dev.txt", "pyproject.toml", "setup.py", "Pipfile"}
    DOCKER_FILES = {"dockerfile", ".dockerignore", "docker-compose.yml"}

    @classmethod
    def evaluate_impact(cls, changed_paths: List[str]) -> ImpactDomain:
        if not changed_paths:
            return ImpactDomain.DOCS_ONLY

        paths = [Path(p) for p in changed_paths]
        names = {p.name.lower() for p in paths}

        # Check for manifest alterations (highest impact on caching)
        if any(name in cls.MANIFEST_FILES for name in names):
            return ImpactDomain.MANIFEST_CHANGED

        # Check for Docker configuration changes
        if any(name in cls.DOCKER_FILES for name in names):
            return ImpactDomain.DOCKER_CHANGED

        # Check if all files are documentation / non-code
        all_docs = True
        for p in paths:
            if p.suffix.lower() not in cls.DOCS_EXTENSIONS and "docs" not in p.parts:
                all_docs = False
                break
        if all_docs:
            return ImpactDomain.DOCS_ONLY

        # Check if changes are confined exclusively to test files
        all_tests = True
        for p in paths:
            parts = [part.lower() for part in p.parts]
            if "tests" not in parts and not p.name.startswith("test_"):
                all_tests = False
                break
        if all_tests:
            return ImpactDomain.TESTS_ONLY

        # Check if changes are confined to application source
        all_src = True
        for p in paths:
            parts = [part.lower() for part in p.parts]
            if "src" not in parts:
                all_src = False
                break
        if all_src:
            return ImpactDomain.SRC_ONLY

        return ImpactDomain.FULL_REBUILD

    @classmethod
    def should_skip_pipeline(cls, changed_paths: List[str]) -> bool:
        """Returns True if the entire CI run can safely skip code compilation/testing."""
        return cls.evaluate_impact(changed_paths) == ImpactDomain.DOCS_ONLY
