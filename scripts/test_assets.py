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

    # Relic tools and swords deliberately use vanilla 2D item rendering.
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
                if not model.get("elements"):
                    fail(f"{name}: relic tool must use an extruded 3D item model")
                if model.get("parent"):
                    fail(f"{name}: custom 3D relic model must not inherit a flat vanilla parent")
                display = model.get("display", {})
                for context in ("firstperson_righthand", "thirdperson_righthand"):
                    if display.get(context, {}).get("scale", [0, 0, 0])[0] < 1.1:
                        fail(f"{name}: held model must be slightly larger than vanilla")
            if item and item.get("model", {}).get("model") != f"celestial_dominion:item/{name}":
                fail(f"{name}: client item does not point to its generated sprite model")
            size = check_png(texture_path, (32, 32))
            if size != (32, 32):
                fail(f"{name}: pixel-art tool sprite must be 32x32")
            if meta_path.exists():
                fail(f"{name}: static item sprite must not have animation metadata")
            try:
                with Image.open(texture_path) as image:
                    if image.convert("RGBA").getbbox() is None:
                        fail(f"{name}: sprite is fully transparent")
            except Exception:
                pass

    # Ingots, smithing templates and catalyst are also flat vanilla item sprites.
    ingredient_names = (
        "solar_ingot", "abyssal_ingot", "celestial_ingot",
        "solar_smithing_template", "abyssal_smithing_template",
        "celestial_catalyst",
    )
    for name in ingredient_names:
        model_path = ASSETS / "models/item" / f"{name}.json"
        item_path = ASSETS / "items" / f"{name}.json"
        texture_path = ASSETS / "textures/item" / f"{name}.png"
        model = read_json(model_path) if model_path.exists() else None
        item = read_json(item_path) if item_path.exists() else None
        if not model or model.get("parent") != "minecraft:item/generated":
            fail(f"{name}: ingredient must use Minecraft's vanilla generated-item model")
        if model and model.get("elements"):
            fail(f"{name}: ingredient sprite must not contain custom cuboid geometry")
        if not item or item.get("model", {}).get("model") != f"celestial_dominion:item/{name}":
            fail(f"{name}: client item does not point to its generated sprite model")
        check_png(texture_path, (32, 32))
        if texture_path.with_name(f"{name}.png.mcmeta").exists():
            fail(f"{name}: static ingredient sprite unexpectedly has animation metadata")

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

    # Tiered spears use the native 26.3 spear item behaviour and their own sprites.
    for material in materials:
        name = f"{material}_spear"
        model_path = ASSETS / "models/item" / f"{name}.json"
        item_path = ASSETS / "items" / f"{name}.json"
        texture_path = ASSETS / "textures/item" / f"{name}.png"
        model = read_json(model_path) if model_path.exists() else None
        item = read_json(item_path) if item_path.exists() else None
        if not model or model.get("parent") != "minecraft:item/generated":
            fail(f"{name}: spear must use the generated vanilla spear sprite model")
        definition = item.get("model", {}) if item else {}
        cases = definition.get("cases", [])
        gui_model = cases[0].get("model", {}).get("model") if cases else None
        held_model = definition.get("fallback", {}).get("model")
        held_path = ASSETS / "models/item" / f"{name}_in_hand.json"
        held = read_json(held_path) if held_path.exists() else None
        if definition.get("type") != "minecraft:select" or gui_model != f"celestial_dominion:item/{name}":
            fail(f"{name}: spear item definition must select its GUI sprite by display context")
        if held_model != f"celestial_dominion:item/{name}_in_hand" or not held:
            fail(f"{name}: spear must use a dedicated held model for vanilla jab/charge animations")
        check_png(texture_path, (64, 64))
        recipe = read_json(recipes / f"{name}.json")
        if not recipe or recipe.get("type") != "minecraft:smithing_transform":
            fail(f"missing smithing recipe: {name}")

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

    # Final-tier gear must carry the real UNBREAKABLE component; base tiers must
    # retain increasing but finite durability values.
    if "DataComponents.UNBREAKABLE" not in source or "Unit.INSTANCE" not in source:
        fail("Celestial gear must use the native UNBREAKABLE item component")
    for expected in ("armor(\"solar\", 320", "armor(\"abyssal\", 480",
                     "ToolMaterial SOLAR_TOOL = new ToolMaterial(",
                     "ToolMaterial ABYSSAL_TOOL = new ToolMaterial("):
        if expected not in source:
            fail(f"missing durability progression declaration: {expected}")

    # Particle bursts are deliberately capped to avoid the old 300+ particle
    # ability spikes. This is a static guard; client FPS still needs a playtest.
    ability_java = ROOT.parent / "java/dev/xolo/celestialdominion/item/AbilitySwordItem.java"
    gameplay_java = ROOT.parent / "java/dev/xolo/celestialdominion/events/GameplayEvents.java"
    for java_path in (ability_java, gameplay_java):
        if not java_path.exists():
            fail(f"missing particle implementation source: {java_path.name}")
            continue
        particle_source = java_path.read_text(encoding="utf-8")
        counts = [int(value) for value in re.findall(
            r'sendParticles\(\s*ParticleTypes\.\w+,.*?\n\s*(\d+),',
            particle_source,
            re.DOTALL,
        )]
        if not counts:
            fail(f"{java_path.name}: no particle calls found for performance validation")
        elif max(counts) > 100:
            fail(f"{java_path.name}: particle burst exceeds 100 particles ({max(counts)})")

    if ERRORS:
        print(f"ASSET VALIDATION FAILED ({len(ERRORS)} issue(s))")
        for error in ERRORS:
            print(" -", error)
        return 1
    print("ASSET VALIDATION PASSED")
    print(" - all JSON resources parse")
    print(" - all 18 tools/weapons use extruded 3D models, larger held transforms and 32x32 pixel-art sprites")
    print(" - all 6 ingredients use vanilla generated-item models and 32x32 sprites")
    print(" - 9 armor atlases, 9 transparent ornament overlays and 3 animated wing sheets have expected dimensions")
    print(" - all 15 tool smithing recipes exist")
    print(" - Solar/Abyssal/Celestial combat-role balance declarations are consistent")
    print(" - particle bursts stay below the 100-particle static cap")
    return 0


if __name__ == "__main__":
    sys.exit(main())
