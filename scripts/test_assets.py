#!/usr/bin/env python3
"""Fast resource validation for Celestial Dominion; no Minecraft launch required."""
from pathlib import Path
import json
import re
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

    # Material textures and transparent ornamental overlays must match each
    # equipment layer's native UV dimensions.
    for material in materials:
        equipment = read_json(ASSETS / "equipment" / f"{material}.json")
        layers = equipment.get("layers", {}) if equipment else {}
        for layer in ("humanoid", "humanoid_leggings", "humanoid_baby"):
            expected = (64, 32) if layer != "humanoid_baby" else (64, 64)
            check_png(ASSETS / "textures/entity/equipment" / layer / f"{material}.png", expected)
            check_png(ASSETS / "textures/entity/equipment" / layer / f"{material}_ornament.png", expected)
            expected_layers = [
                {"texture": f"celestial_dominion:{material}"},
                {"texture": f"celestial_dominion:{material}_ornament"},
            ]
            if layers.get(layer) != expected_layers:
                fail(f"{material}: {layer} must have a base texture plus its ornate overlay")

        if layers.get("wings") != [{"texture": f"celestial_dominion:{material}"}]:
            fail(f"{material}: missing material-specific WingsLayer texture")
        wing_path = ASSETS / "textures/entity/equipment/wings" / f"{material}.png"
        check_png(wing_path, (64, 256))
        wing_meta = read_json(wing_path.with_name(f"{material}.png.mcmeta"))
        if not wing_meta or wing_meta.get("animation", {}).get("width") != 64 or wing_meta.get("animation", {}).get("height") != 32:
            fail(f"{material}: wing animation metadata must declare 64x32 frames")

    # Smithing progression is required for every tool type and tier.
    recipes = ROOT / "data/celestial_dominion/recipe"
    for material in materials:
        for kind in ("pickaxe", "axe", "shovel", "hoe", "multitool"):
            path = recipes / f"{material}_{kind}.json"
            recipe = read_json(path) if path.exists() else None
            if not recipe or recipe.get("type") != "minecraft:smithing_transform":
                fail(f"missing smithing recipe: {material}_{kind}")

    # Static balance regression checks: Solar is the damage path, Abyssal
    # is the durability/defence path, and Celestial is the final fusion.
    java_items = ROOT.parent / "java/dev/xolo/celestialdominion/content/ModItems.java"
    source = java_items.read_text(encoding="utf-8") if java_items.exists() else ""
    if not source:
        fail("ModItems.java missing; cannot validate combat-role configuration")
    else:
        def armor_stats(material):
            match = re.search(
                rf'armor\("{material}",\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)F,\s*([\d.]+)F\)',
                source,
            )
            if not match:
                fail(f"{material}: armor stats declaration not found")
                return (0, 0, 0)
            values = [float(value) for value in match.groups()]
            return (sum(values[1:5]), values[5], values[6], values[0])

        solar_armor = armor_stats("solar")
        abyssal_armor = armor_stats("abyssal")
        celestial_armor = armor_stats("celestial")
        if not (abyssal_armor[0] > solar_armor[0]
                and abyssal_armor[1] > solar_armor[1]
                and abyssal_armor[2] > solar_armor[2]):
            fail("Abyssal armor must exceed Solar defense, toughness and knockback resistance")
        if not (celestial_armor[0] > abyssal_armor[0]
                and celestial_armor[1] > abyssal_armor[1]
                and celestial_armor[2] >= abyssal_armor[2]):
            fail("Celestial armor must exceed Abyssal defense/toughness and retain its resistance")
        if not (abyssal_armor[3] > solar_armor[3] and celestial_armor[3] > abyssal_armor[3]):
            fail("Armor durability must progress Solar < Abyssal < Celestial")

        def material_bonus(name):
            match = re.search(
                rf'ToolMaterial {name} = new ToolMaterial\(\s*[^,]+,\s*\d+,\s*[\d.]+F,\s*([\d.]+)F',
                source,
            )
            if not match:
                fail(f"{name}: ToolMaterial declaration not found")
                return 0.0
            return float(match.group(1))

        def harvest_tag(name):
            match = re.search(
                rf'ToolMaterial {name} = new ToolMaterial\(\s*([^,]+)',
                source,
            )
            if not match:
                fail(f"{name}: harvest-tier declaration not found")
                return ""
            return match.group(1).strip()

        def material_speed(name):
            match = re.search(
                rf'ToolMaterial {name} = new ToolMaterial\(\s*[^,]+,\s*\d+,\s*([\d.]+)F',
                source,
            )
            if not match:
                fail(f"{name}: mining speed declaration not found")
                return 0.0
            return float(match.group(1))
        def sword_damage(name, material):
            match = re.search(
                rf'p\.sword\({material},\s*([\d.]+)F,\s*-[\d.]+F\)',
                source,
            )
            if not match:
                fail(f"{name}: sword damage declaration not found")
                return 0.0
            return float(match.group(1)) + material_bonus(material)

        solar_sword = sword_damage("Solar", "SOLAR_TOOL")
        abyssal_sword = sword_damage("Abyssal", "ABYSSAL_TOOL")
        celestial_sword = sword_damage("Celestial", "CELESTIAL_TOOL")
        if not (solar_sword > abyssal_sword and celestial_sword > solar_sword):
            fail("Sword damage must follow Solar offence > Abyssal control and Celestial fusion")

        solar_mining = material_bonus("SOLAR_MINING_TOOL")
        abyssal_mining = material_bonus("ABYSSAL_MINING_TOOL")
        celestial_mining = material_bonus("CELESTIAL_MINING_TOOL")
        if not (solar_mining > abyssal_mining and celestial_mining > solar_mining):
            fail("Mining-tool damage bonus must follow Solar offence > Abyssal and Celestial fusion")
        solar_speed = material_speed("SOLAR_MINING_TOOL")
        abyssal_speed = material_speed("ABYSSAL_MINING_TOOL")
        celestial_speed = material_speed("CELESTIAL_MINING_TOOL")
        if not (abyssal_speed > solar_speed and celestial_speed > abyssal_speed):
            fail("Mining speed must progress Solar < Abyssal < Celestial")
        if harvest_tag("SOLAR_MINING_TOOL") != "BlockTags.INCORRECT_FOR_NETHERITE_TOOL":
            fail("Solar tools must retain at least Netherite harvest capability")
        if harvest_tag("ABYSSAL_MINING_TOOL") != "BlockTags.INCORRECT_FOR_NETHERITE_TOOL":
            fail("Abyssal tools must retain Netherite harvest capability")
        if harvest_tag("CELESTIAL_MINING_TOOL") != "INCORRECT_FOR_CELESTIAL_TOOL":
            fail("Celestial tools must use the custom final harvest tier")

    if ERRORS:
        print(f"ASSET VALIDATION FAILED ({len(ERRORS)} issue(s))")
        for error in ERRORS:
            print(" -", error)
        return 1
    print("ASSET VALIDATION PASSED")
    print(" - all JSON resources parse")
    print(" - 18 animated relic models and 6 ingredient models contain 3D cuboid geometry")
    print(" - all 18 animated texture sheets and metadata are valid")
    print(" - 9 armor atlases, 9 transparent ornament overlays and 3 animated wing sheets have expected dimensions")
    print(" - all 15 tool smithing recipes exist")
    print(" - Solar/Abyssal/Celestial combat-role balance declarations are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
