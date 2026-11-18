#!/usr/bin/env python3
"""Fast resource validation for Celestial Dominion; no Minecraft launch required."""
from pathlib import Path
import json
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources"
ASSETS = ROOT / "assets/celestial_dominion"
ERRORS = []


def fail(message):
    ERRORS.append(message)


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None


def check_png(path, expected=None):
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if expected and image.size != expected:
                fail(f"{path.relative_to(ROOT)}: expected {expected}, got {image.size}")
            return image.size
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid PNG: {exc}")
        return None


def main():
    # Parse every JSON resource, not just the newly generated files.
    for path in ROOT.rglob("*.json"):
        read_json(path)

    # All relic item models must be genuine cuboid models, not generated sprites.
    materials = ("solar", "abyssal", "celestial")
    kinds = ("pickaxe", "axe", "shovel", "hoe", "multitool", "sword")
    for material in materials:
        for kind in kinds:
            name = f"{material}_{kind}"
            model_path = ASSETS / "models/item" / f"{name}.json"
            item_path = ASSETS / "items" / f"{name}.json"
            texture_path = ASSETS / "textures/item" / f"{name}.png"
            meta_path = ASSETS / "textures/item" / f"{name}.png.mcmeta"
            model = read_json(model_path) if model_path.exists() else None
            item = read_json(item_path) if item_path.exists() else None
            if model:
                elements = model.get("elements", [])
                if len(elements) < 6:
                    fail(f"{name}: expected 3D cuboid geometry, found {len(elements)} elements")
                if model.get("parent") != "minecraft:item/handheld":
                    fail(f"{name}: handheld model parent missing")
                for element in elements:
                    for face in element.get("faces", {}).values():
                        uv = face.get("uv", [])
                        if len(uv) != 4 or min(uv) < 0 or max(uv) > 64:
                            fail(f"{name}: UV coordinates outside the 64x64 animation frame: {uv}")
            if item and item.get("model", {}).get("model") != f"celestial_dominion:item/{name}":
                fail(f"{name}: client item does not point to its 3D model")
            size = check_png(texture_path)
            if size != (64, 512):
                fail(f"{name}: expected an 8-frame 64x64 vertical animation sheet")
            meta = read_json(meta_path) if meta_path.exists() else None
            if not meta or meta.get("animation", {}).get("width") != 64 or meta.get("animation", {}).get("height") != 64:
                fail(f"{name}: animation metadata must declare 64x64 frames")

    # Ingredients and smithing relics also use 3D cuboids rather than flat icons.
    for name in ("solar_ingot", "abyssal_ingot", "celestial_ingot",
                 "solar_smithing_template", "abyssal_smithing_template",
                 "celestial_catalyst"):
        model_path = ASSETS / "models/item" / f"{name}.json"
        item_path = ASSETS / "items" / f"{name}.json"
        model = read_json(model_path) if model_path.exists() else None
        item = read_json(item_path) if item_path.exists() else None
        if not model or len(model.get("elements", [])) < 3:
            fail(f"{name}: expected a 3D cuboid model")
        if model and model.get("parent") != "minecraft:item/handheld":
            fail(f"{name}: flat generated parent would draw a sprite behind the cuboids")
        if not item or item.get("model", {}).get("model") != f"celestial_dominion:item/{name}":
            fail(f"{name}: client item does not point to its cuboid model")

    # Material textures must be valid native armor UV atlases.
    for material in materials:
        for layer in ("humanoid", "humanoid_leggings", "humanoid_baby"):
            check_png(ASSETS / "textures/entity/equipment" / layer / f"{material}.png", (64, 32) if layer != "humanoid_baby" else (64, 64))

    # Smithing progression is required for every tool type and tier.
    recipes = ROOT / "data/celestial_dominion/recipe"
    for material in materials:
        for kind in ("pickaxe", "axe", "shovel", "hoe", "multitool"):
            path = recipes / f"{material}_{kind}.json"
            recipe = read_json(path) if path.exists() else None
            if not recipe or recipe.get("type") != "minecraft:smithing_transform":
                fail(f"missing smithing recipe: {material}_{kind}")

    if ERRORS:
        print(f"ASSET VALIDATION FAILED ({len(ERRORS)} issue(s))")
        for error in ERRORS:
            print(" -", error)
        return 1
    print("ASSET VALIDATION PASSED")
    print(" - all JSON resources parse")
    print(" - 18 animated relic models and 6 ingredient models contain 3D cuboid geometry")
    print(" - all 18 animated texture sheets and metadata are valid")
    print(" - 9 armor atlas files have expected dimensions")
    print(" - all 15 tool smithing recipes exist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
