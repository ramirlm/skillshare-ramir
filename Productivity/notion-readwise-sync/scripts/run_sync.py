#!/usr/bin/env python3
"""Compatibility wrapper for legacy invocations.

Historically the sync entrypoint is a shell script. This file intentionally allows:
  - python3 run_sync.py
to execute the same flow as run_sync.sh.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SH = ROOT / "run_sync.sh"

if __name__ == "__main__":
    cmd = ["bash", str(SH)]
    env = os.environ.copy()
    env.setdefault("NOTION_API_KEY", os.environ.get("NOTION_API_KEY", ""))
    rc = subprocess.call(cmd, env=env)
    raise SystemExit(rc)
