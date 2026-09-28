#!/usr/bin/env python
"""Minimal setup.py that only checks system dependencies."""

import shutil
import sys

# Check system dependencies at import time
SYSTEM_DEPS = ["fzf", "ffmpeg", "yq", "lsof", "v4l2-ctl"]

missing = []
print("Checking system dependencies...")
for dep in SYSTEM_DEPS:
    if shutil.which(dep) is None:
        missing.append(dep)
        print(f"{dep} - NOT FOUND")
    else:
        print(f"{dep} - OK")

if missing:
    print(f"\nERROR: Missing required system dependencies: {', '.join(missing)}")
    print("\nPlease install the missing dependencies and try again:")
    print("Ubuntu/Debian: sudo apt install " + ' '.join(missing))
    print("macOS: brew install " + ' '.join(missing))
    sys.exit(1)

print("All system dependencies satisfied!")

# Import and use setuptools normally - pyproject.toml handles the rest
from setuptools import setup
setup()
