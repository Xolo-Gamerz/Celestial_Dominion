#!/usr/bin/env python3
"""Validate a real NeoForge client resource reload and reject model/resource errors."""
from pathlib import Path
import re
import sys

ERROR_PATTERNS = (
    r"Unable to bake item model",
    r"Cannot compute translucency out of bounds",
    r"Failed to load model",
    r"Exception loading model",
    r"Error loading model",
    r"Unable to load model",
    r"Couldn't load model",
    r"Missing texture",
    r"Missing model",
    r"FileNotFoundException:.*celestial_dominion",
)
RELOAD_MARKER = "Reloading ResourceManager"
ATLAS_MARKER = "minecraft/TextureAtlas"


def inspect_log(text):
    found = []
    for pattern in ERROR_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line = text.count("\n", 0, match.start()) + 1
            excerpt = text[match.start():text.find("\n", match.start())]
            found.append(f"line {line}: {excerpt[:300]}")

    missing = []
    if RELOAD_MARKER not in text:
        missing.append("client never began a resource reload")
    if not re.search(r"TextureAtlas.*Created:", text):
        missing.append("client never logged texture-atlas creation after resource reload")
    return found, missing


def self_test():
    clean = (
        "[Render thread/INFO] [minecraft/ReloadableResourceManager]: "
        "Reloading ResourceManager: vanilla, mod/celestial_dominion\n"
        "[Render thread/INFO] [net.minecraft.client.renderer.texture.TextureAtlas/]: Created: "
        "512x512x0 minecraft:textures/atlas/blocks.png-atlas\n"
    )
    found, missing = inspect_log(clean)
    assert not found and not missing, "clean smoke log should pass"

    for pattern in ERROR_PATTERNS:
        sample = clean + "\n[Worker-ResourceReload/WARN] " + pattern.replace(r"\s", " ")
        found, missing = inspect_log(sample)
        assert found, f"checker failed to reject injected error: {pattern}"

    found, missing = inspect_log("client started but no reload")
    assert missing, "checker should reject a client that never reloads resources"

    no_atlas = clean.split("[Render thread/INFO] [minecraft/TextureAtlas]")[0]
    found, missing = inspect_log(no_atlas)
    assert any("texture-atlas" in item for item in missing), "checker should require atlas creation"
    print("CLIENT LOG CHECKER SELF-TEST PASSED")
    print(f" - {len(ERROR_PATTERNS)} model/resource error signatures rejected")
    print(" - missing resource reload and missing texture-atlas creation rejected")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
        return 0
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_client_model_bake.py <latest.log> | --self-test")

    log_path = Path(sys.argv[1])
    if not log_path.is_file():
        raise SystemExit(f"Client smoke test did not produce a log: {log_path}")

    text = log_path.read_text(encoding="utf-8", errors="replace")
    found, missing = inspect_log(text)
    if found or missing:
        print(f"CLIENT RESOURCE SMOKE TEST FAILED ({len(found)} model/resource error(s), {len(missing)} missing milestone(s))")
        for item in missing:
            print(" -", item)
        for item in found:
            print(" -", item)
        return 1

    print("CLIENT RESOURCE SMOKE TEST PASSED")
    print(" - NeoForge client began resource reload")
    print(" - texture atlas creation was logged")
    print(" - no model bake, missing texture, missing model or resource-loading errors found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
