#!/usr/bin/env python3
"""Generate Celestial Dominion's 3D item geometry and animated material atlases.

Uses vanilla cuboid item models: no custom render loop, shaders, or per-frame
Java work. Minecraft's sprite animation system advances the 8-frame textures.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/assets/celestial_dominion"
MODELS = ROOT / "models/item"
TEXTURES = ROOT / "textures/item"

PALETTES = {
    "solar": {"outline": (43, 13, 17, 255), "dark": (100, 29, 20, 255),
              "metal": (183, 61, 25, 255), "light": (255, 139, 37, 255),
              "gold": (255, 207, 82, 255), "white": (255, 247, 196, 255)},
    "abyssal": {"outline": (8, 9, 25, 255), "dark": (29, 25, 62, 255),
                "metal": (76, 57, 128, 255), "light": (133, 89, 203, 255),
                "gold": (45, 222, 220, 255), "white": (211, 255, 255, 255)},
    "celestial": {"outline": (37, 38, 66, 255), "dark": (94, 101, 139, 255),
                  "metal": (176, 184, 211, 255), "light": (229, 232, 247, 255),
                  "gold": (255, 207, 105, 255), "white": (255, 255, 248, 255)},
}
KINDS = ("pickaxe", "axe", "shovel", "hoe", "multitool", "sword")


def face(uv):
    return {side: {"uv": uv, "texture": "#layer0"} for side in
            ("north", "south", "east", "west", "up", "down")}


def cube(a, b, uv, name=None):
    # UV coordinates are pixel coordinates on the 64x64 animation frame.
    # Each cuboid uses a dedicated atlas region so haft, forged head and gem
    # do not all sample the same four pixels.
    return {"from": a, "to": b, "faces": face(uv)}


def add_gem(elements, x=7, y=11, z=5):
    elements.append(cube([x, y, z], [x+2, y+2, z+2], [4, 8, 8, 12]))


def tool_elements(kind):
    e = []
    # Octagonal-looking haft: three overlapping bevelled cuboids and a pommel.
    e += [
        cube([7, 0, 7], [9, 13, 9], [2, 1, 13, 62]),
        cube([6.5, 1, 7.2], [7.5, 12, 8.8], [2, 1, 13, 62]),
        cube([8.5, 1, 7.2], [9.5, 12, 8.8], [2, 1, 13, 62]),
        cube([6, 0, 6], [10, 1.5, 10], [19, 32, 34, 46]),
        cube([7, 10, 6], [9, 11, 10], [19, 32, 34, 46]),
    ]
    if kind == "pickaxe":
        e += [cube([2, 12, 6], [14, 14, 10], [16, 0, 63, 31]),
              cube([1, 11, 6], [4, 15, 10], [16, 0, 63, 31]),
              cube([12, 11, 6], [15, 15, 10], [16, 0, 63, 31]),
              cube([5, 13, 5], [11, 15, 11], [19, 32, 34, 46])]
    elif kind == "axe":
        e += [cube([8, 10, 6], [15, 15, 10], [16, 0, 63, 31]),
              cube([10, 12, 5], [15, 14, 11], [16, 0, 63, 31]),
              cube([7, 12, 6], [10, 14, 10], [16, 0, 63, 31]),
              cube([8, 13, 5], [11, 15, 11], [19, 32, 34, 46])]
    elif kind == "shovel":
        e += [cube([5, 12, 5], [11, 16, 11], [16, 0, 63, 31]),
              cube([6, 13, 4], [10, 16, 12], [16, 0, 63, 31]),
              cube([7, 14, 4], [9, 16, 12], [19, 32, 34, 46])]
    elif kind == "hoe":
        e += [cube([8, 12, 6], [15, 14, 10], [16, 0, 63, 31]),
              cube([10, 11, 6], [14, 15, 10], [16, 0, 63, 31]),
              cube([8, 13, 5], [11, 15, 11], [19, 32, 34, 46])]
    else:
        # The Omnitool has a pick crown, an axe blade, and a spade/hoe edge.
        e += [cube([2, 12, 6], [14, 14, 10], [16, 0, 63, 31]),
              cube([1, 11, 6], [4, 15, 10], [16, 0, 63, 31]),
              cube([12, 11, 6], [15, 15, 10], [16, 0, 63, 31]),
              cube([9, 9, 5], [15, 13, 11], [16, 0, 63, 31]),
              cube([5, 13, 5], [11, 16, 11], [16, 0, 63, 31]),
              cube([7, 13, 4], [9, 16, 12], [19, 32, 34, 46])]
    add_gem(e)
    return e


def sword_elements():
    return [
        cube([7, 0, 7], [9, 4, 9], [2, 1, 13, 62]),
        cube([5, 3, 6], [11, 5, 10], [19, 32, 34, 46]),
        cube([7, 4, 7], [9, 6, 9], [19, 32, 34, 46]),
        cube([6, 6, 6], [10, 15, 10], [16, 0, 63, 31]),
        cube([5.5, 7, 7], [6.5, 14, 9], [16, 0, 63, 31]),
        cube([9.5, 7, 7], [10.5, 14, 9], [16, 0, 63, 31]),
        cube([7, 14, 6], [9, 16, 10], [16, 0, 63, 31]),
        cube([7, 1, 6], [9, 3, 10], [19, 32, 34, 46]),
        cube([6, 0, 6], [10, 1, 10], [19, 32, 34, 46]),
        cube([6, 5, 5], [10, 7, 11], [19, 32, 34, 46]),
    ]


def display():
    return {
        "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 3.4, 1.2], "scale": [1.35, 1.35, 1.35]},
        "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 3.4, 1.2], "scale": [1.35, 1.35, 1.35]},
        "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.1, 3.2, 1.1], "scale": [1.45, 1.45, 1.45]},
        "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.1, 3.2, 1.1], "scale": [1.45, 1.45, 1.45]},
        "gui": {"rotation": [20, -35, 0], "translation": [0, 0, 0], "scale": [1.1, 1.1, 1.1]},
        "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.9, 0.9, 0.9]},
        "fixed": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [1.0, 1.0, 1.0]},
    }


def model_json(item_id, elements, handheld=True):
    return {
        "parent": "minecraft:item/handheld",
        "textures": {"layer0": f"celestial_dominion:item/{item_id}"},
        "elements": elements,
        "display": display(),
    }


def draw_atlas(material, kind, frame):
    p = PALETTES[material]
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    o, dark, metal, light, gold, white = (p[k] for k in ("outline", "dark", "metal", "light", "gold", "white"))

    # Haft UV tile: full-height faceted shaft, wrapped in a material-specific grip.
    d.rectangle((2, 1, 13, 62), fill=o)
    d.rectangle((4, 1, 11, 62), fill=dark)
    d.rectangle((6, 1, 9, 62), fill=metal)
    d.line((5, 2, 5, 61), fill=light, width=1)
    d.line((10, 2, 10, 61), fill=gold, width=1)
    for y in range(8, 61, 8):
        d.line((3, y, 12, y-2), fill=gold, width=2)
    d.rectangle((2, 57, 13, 63), fill=metal, outline=white)
    d.point((7, 59), fill=white)

    # Tool head / blade atlas tile. Distinct profiles, bevels and a strong edge highlight.
    if kind == "sword":
        d.polygon([(20, 29), (24, 2), (34, 0), (44, 2), (60, 29), (40, 25), (32, 31)], fill=o)
        d.polygon([(24, 26), (28, 4), (34, 2), (42, 4), (56, 26), (40, 22), (32, 28)], fill=metal)
        d.polygon([(29, 23), (32, 5), (35, 4), (52, 25), (40, 21)], fill=light)
        d.line((34, 5, 48, 23), fill=white, width=2)
    elif kind == "pickaxe":
        d.polygon([(17, 15), (24, 3), (40, 9), (57, 1), (63, 8), (49, 23), (34, 18), (22, 29)], fill=o)
        d.polygon([(20, 14), (26, 7), (40, 13), (57, 5), (60, 9), (47, 19), (34, 15), (24, 24)], fill=metal)
        d.line((24, 13, 40, 16, 56, 9), fill=white, width=2)
    elif kind == "axe":
        d.polygon([(18, 3), (36, 4), (51, 10), (62, 21), (58, 29), (46, 27), (36, 19), (25, 25), (16, 18)], fill=o)
        d.polygon([(21, 6), (36, 7), (50, 13), (58, 21), (53, 25), (44, 22), (34, 15), (25, 21), (20, 16)], fill=metal)
        d.line((23, 8, 39, 12, 54, 21), fill=white, width=2)
    elif kind == "shovel":
        d.polygon([(29, 1), (47, 1), (61, 12), (56, 27), (39, 31), (22, 27), (16, 12)], fill=o)
        d.polygon([(31, 4), (45, 4), (56, 13), (51, 24), (39, 28), (26, 24), (21, 13)], fill=metal)
        d.polygon([(32, 7), (44, 7), (50, 14), (39, 24), (28, 14)], fill=light)
        d.line((30, 10, 39, 18, 48, 10), fill=white, width=2)
    elif kind == "hoe":
        d.polygon([(18, 4), (32, 1), (45, 7), (60, 8), (62, 19), (49, 22), (37, 15), (25, 22), (16, 15)], fill=o)
        d.polygon([(20, 7), (32, 4), (45, 10), (57, 11), (58, 17), (48, 18), (36, 12), (25, 19), (20, 14)], fill=metal)
        d.line((22, 8, 34, 8, 48, 14, 57, 14), fill=white, width=2)
    else:
        d.polygon([(17, 11), (25, 1), (35, 9), (42, 0), (51, 10), (63, 7), (60, 23),
                   (50, 27), (44, 20), (36, 31), (27, 21), (19, 27), (15, 19)], fill=o)
        d.polygon([(20, 12), (26, 6), (35, 14), (42, 5), (50, 14), (59, 11), (56, 20),
                   (49, 23), (43, 17), (36, 26), (28, 17), (21, 23), (18, 18)], fill=metal)
        d.line((21, 13, 35, 18, 42, 10, 55, 16), fill=white, width=2)

    # Gem tile and rune tile.
    d.polygon([(24, 33), (30, 32), (34, 37), (31, 45), (24, 46), (19, 40)], fill=o, outline=white)
    d.polygon([(25, 34), (29, 34), (32, 38), (29, 43), (25, 43), (22, 39)], fill=gold)
    d.line((25, 35, 28, 38), fill=white, width=2)
    d.rectangle((34, 33, 62, 62), fill=dark, outline=metal)
    for i in range(4):
        x = 38 + i * 6
        d.line((x, 38, x+3, 42, x, 47), fill=gold, width=2)
        d.point((x+2, 54), fill=light)
    if material == "solar":
        # Flickering ember tongues and hot sparks.
        shift = frame % 4
        for x in (18, 29, 43, 55):
            d.polygon([(x, 1+shift), (x+2, 7+shift), (x+4, 2+shift), (x+3, 11+shift)], fill=light)
        d.line((18, 28, 25, 24, 30, 28), fill=gold, width=2)
    elif material == "abyssal":
        # A slow rift pulse and cyan arc.
        d.ellipse((43-frame%3, 36-frame%2, 54+frame%3, 47+frame%2), outline=gold, width=2)
        d.line((18, 28, 25, 23, 31, 27), fill=gold, width=2)
        d.point((48, 41), fill=white)
    else:
        # Rotating constellation points.
        for i in range(4):
            x = 37 + ((frame*5 + i*7) % 25)
            y = 36 + ((frame*3 + i*9) % 25)
            d.line((x-2, y, x+2, y), fill=white, width=1)
            d.line((x, y-2, x, y+2), fill=gold, width=1)
    return im


def make_template_model(item_id):
    return model_json(item_id, [
        cube([2, 1, 7], [14, 15, 9], [0, 0, 32, 32], "plate"),
        cube([3, 2, 6], [13, 14, 7], [0, 0, 32, 32]),
        cube([5, 4, 5], [11, 12, 6], [0, 0, 32, 32]),
        cube([6, 6, 4], [10, 10, 7], [0, 0, 32, 32]),
    ], False)


def main():
    MODELS.mkdir(parents=True, exist_ok=True)
    TEXTURES.mkdir(parents=True, exist_ok=True)
    for material in PALETTES:
        for kind in KINDS:
            item_id = f"{material}_{kind}"
            elements = sword_elements() if kind == "sword" else tool_elements(kind)
            (MODELS / f"{item_id}.json").write_text(
                json.dumps(model_json(item_id, elements), indent=2) + "\n", encoding="utf-8")
            sheet = Image.new("RGBA", (64, 64*8), (0, 0, 0, 0))
            for frame in range(8):
                sheet.paste(draw_atlas(material, kind, frame), (0, frame*64))
            name = f"{item_id}.png"
            sheet.save(TEXTURES / name, optimize=True)
            (TEXTURES / f"{name}.mcmeta").write_text(json.dumps({
                "animation": {"width": 64, "height": 64, "frametime": 3, "interpolate": False}
            }, indent=2) + "\n", encoding="utf-8")

        # 3D, beveled ingots, templates and the final catalyst.
        (MODELS / f"{material}_ingot.json").write_text(json.dumps(model_json(
            f"{material}_ingot", [
                cube([2, 5, 5], [14, 11, 11], [0, 0, 32, 32]),
                cube([3, 6, 4], [13, 10, 12], [0, 0, 32, 32]),
                cube([4, 7, 3], [12, 9, 13], [0, 0, 32, 32]),
            ], False), indent=2) + "\n", encoding="utf-8")
        template_id = f"{material}_smithing_template"
        if material != "celestial":
            (MODELS / f"{template_id}.json").write_text(json.dumps(
                make_template_model(template_id), indent=2) + "\n", encoding="utf-8")
    (MODELS / "celestial_catalyst.json").write_text(json.dumps(model_json(
        "celestial_catalyst", [
            cube([3, 2, 6], [13, 14, 10], [0, 0, 32, 32], "crystal"),
            cube([5, 4, 5], [11, 12, 11], [0, 0, 32, 32]),
            cube([7, 6, 4], [9, 10, 12], [0, 0, 32, 32]),
        ], False), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
