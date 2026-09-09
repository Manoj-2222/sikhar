"""Sikhar test suite."""
import sys
from pathlib import Path

# Ensure src/ is in sys.path when running unittest directly
src_path = str(Path(__file__).resolve().parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
