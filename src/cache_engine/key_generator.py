"""
Cache Key Generator and Hierarchy Module.
Constructs primary exact-match keys and ordered prefix restore-keys for CI pipelines.
Author: Saksham Singh (24BTRAO035)
"""
from dataclasses import dataclass, field
from typing import List
from .hasher import ContentHasher


@dataclass
class CacheKeyHierarchy:
    primary_key: str
    restore_keys: List[str]
    manifest_hash: str
    scope_branch: str
    os_name: str
    runtime: str


class CacheKeyGenerator:
    """
    Generates structured, hierarchical cache keys compliant with GitHub Actions
    and modern continuous integration caching specifications.
    """
    PREFIX = "smartci"

    def __init__(self, os_name: str = "linux", runtime: str = "py312", branch: str = "main"):
        self.os_name = os_name.lower()
        self.runtime = runtime.lower()
        self.branch = branch.replace("/", "-")

    def generate_keys(self, manifest_path: str) -> CacheKeyHierarchy:
        """
        Builds a primary exact key and tiered fallback restore keys.
        
        Example:
          Primary:      smartci-linux-py312-main-a1b2c3d4e5f67890
          Restore Key 1: smartci-linux-py312-main-
          Restore Key 2: smartci-linux-py312-
          Restore Key 3: smartci-linux-
        """
        manifest_hash = ContentHasher.hash_manifest_normalized(manifest_path)
        
        primary_key = f"{self.PREFIX}-{self.os_name}-{self.runtime}-{self.branch}-{manifest_hash}"
        
        restore_keys = [
            f"{self.PREFIX}-{self.os_name}-{self.runtime}-{self.branch}-",
            f"{self.PREFIX}-{self.os_name}-{self.runtime}-",
            f"{self.PREFIX}-{self.os_name}-",
        ]
        
        return CacheKeyHierarchy(
            primary_key=primary_key,
            restore_keys=restore_keys,
            manifest_hash=manifest_hash,
            scope_branch=self.branch,
            os_name=self.os_name,
            runtime=self.runtime
        )
