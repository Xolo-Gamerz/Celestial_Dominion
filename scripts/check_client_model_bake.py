#!/usr/bin/env python3
"""Fail CI when a real NeoForge client resource reload reports item model bake errors."""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: check_client_model_bake.py <latest.log>")

log_path = Path(sys.argv[1])
if not log_path.is_file():
    raise SystemExit(f"Client smoke test did not produce a log: {log_path}")

text = log_path.read_text(encoding="utf-8", errors="replace")
errors = [
    r"Unable to bake item model",
    r"Cannot compute translucency out of bounds",
    r"Failed to load model",
    r"Exception loading model",
    r"Error loading model",
]
found = []
for pattern in errors:
    for match in re.finditer(pattern, text, re.IGNORECASE):
        line = text.count("\n", 0, match.start()) + 1
        excerpt = text[match.start():text.find("\n", match.start())]
        found.append(f"line {line}: {excerpt[:300]}")

if found:
    print(f"CLIENT MODEL BAKE FAILED ({len(found)} model-loading error(s))")
    for item in found:
        print(" -", item)
    raise SystemExit(1)

if "Reloading ResourceManager" not in text:
    raise SystemExit("Client log did not reach resource reload; model-bake smoke test is inconclusive")

print("CLIENT MODEL BAKE PASSED")
print(" - NeoForge client reached resource reload")
print(" - no item model bake, cuboid UV/translucency, or model loading errors found")
