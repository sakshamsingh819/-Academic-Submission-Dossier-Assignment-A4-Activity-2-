"""
Content-Addressable Hashing Module for Smart Build-Cache Invalidation.
Provides deterministic, normalized cryptographic SHA-256 fingerprinting.
Author: Saksham Singh (24BTRAO035)
"""
import hashlib
import os
from pathlib import Path
from typing import List, Union


class ContentHasher:
    """
    Computes cryptographic fingerprints of dependency manifests and source files.
    Applies normalization to eliminate false-positive cache invalidations caused by
    comments, whitespace variations, or non-semantic line reordering.
    """

    @staticmethod
    def hash_file_raw(file_path: Union[str, Path]) -> str:
        """Computes exact byte-level SHA-256 hash of a file."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Target file does not exist: {file_path}")

        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def hash_manifest_normalized(file_path: Union[str, Path]) -> str:
        """
        Normalizes dependency files (e.g., requirements.txt) before hashing:
        1. Strips comment lines (# ...)
        2. Strips leading/trailing whitespace
        3. Filters out blank lines
        4. Sorts dependencies alphabetically to avoid line-order churn
        Returns an invariant 16-character SHA-256 fingerprint.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Manifest file not found: {file_path}")

        normalized_lines: List[str] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                cleaned = line.strip()
                # Exclude comments and blank lines
                if not cleaned or cleaned.startswith("#"):
                    continue
                # Normalize inline comments: e.g. "package==1.0 # note" -> "package==1.0"
                cleaned = cleaned.split("#")[0].strip()
                normalized_lines.append(cleaned)

        # Sort lines deterministically
        normalized_lines.sort()
        payload = "\n".join(normalized_lines).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:16]

    @classmethod
    def hash_composite(cls, file_paths: List[Union[str, Path]]) -> str:
        """
        Computes a combined fingerprint across multiple manifest files
        (e.g., requirements.txt + pyproject.toml + Dockerfile).
        """
        combined_hasher = hashlib.sha256()
        for fp in sorted(file_paths, key=lambda p: str(p)):
            p = Path(fp)
            if p.is_file():
                file_hash = cls.hash_manifest_normalized(p)
                combined_hasher.update(f"{p.name}:{file_hash};".encode("utf-8"))
        return combined_hasher.hexdigest()[:16]

    @staticmethod
    def hash_directory(directory_path: Union[str, Path], extension: str = ".py") -> str:
        """
        Computes a deterministic hash over all files with given extension in a directory.
        Files are processed in sorted order.
        """
        dir_p = Path(directory_path)
        if not dir_p.is_dir():
            raise NotADirectoryError(f"Directory not found: {directory_path}")

        hasher = hashlib.sha256()
        matching_files = sorted(dir_p.rglob(f"*{extension}"))
        for file_p in matching_files:
            rel_path = file_p.relative_to(dir_p)
            hasher.update(str(rel_path).encode("utf-8"))
            with open(file_p, "rb") as f:
                while chunk := f.read(32768):
                    hasher.update(chunk)
        return hasher.hexdigest()[:16]
