#!/usr/bin/env python3
"""Fail when a tracked source URL still carries an X/Twitter session token."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


SECRET_QUERY = re.compile(r"(?:[?&]|%3f|%26)xsec_token(?:=|%3d)[^&\"\s]+", re.IGNORECASE)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    files = subprocess.check_output(
        ["git", "-C", str(root), "ls-files", "-z"], text=False
    ).split(b"\0")
    findings: list[str] = []
    for raw_path in files:
        if not raw_path:
            continue
        path = root / os_fsdecode(raw_path)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if SECRET_QUERY.search(text):
            findings.append(str(path.relative_to(root)))
    if findings:
        print("xsec_token query values found in: " + ", ".join(sorted(findings)))
        return 1
    print("no xsec_token query values found in tracked files")
    return 0


def os_fsdecode(value: bytes) -> str:
    return value.decode(sys.getfilesystemencoding() or "utf-8", errors="surrogateescape")


if __name__ == "__main__":
    raise SystemExit(main())
