#!/usr/bin/env python3
"""Generate vanilla-style, pixel-art item sprites and flat Minecraft item models.

The tools deliberately use Minecraft's normal 2D handheld rendering path.
There are no custom cuboids, oversized display transforms, shaders, or runtime
renderers. Artwork is original and generated at native 32x32 pixel resolution.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/assets/celestial_dominion"
MODELS = ROOT / "models/item"
TEXTURES = ROOT / "textures/item"

PALETTES = {
    "solar": {
        "outline": (48, 14, 18, 255), "handle": (103, 35, 25, 255),
        "handle_light": (170, 75, 37, 255), "metal_dark": (132, 48, 24, 255),
        "metal": (220, 105, 34, 255), "edge": (255, 190, 73, 255),
        "shine": (255, 239, 177, 255), "gem": (255, 111, 35, 255),
    },
    "abyssal": {
        "outline": (10, 12, 28, 255), "handle": (38, 31, 67, 255),
        "handle_light": (77, 62, 119, 255), "metal_dark": (48, 42, 89, 255),
        "metal": (104, 79, 158, 255), "edge": (63, 218, 220, 255),
        "shine": (203, 255, 255, 255), "gem": (25, 178, 198, 255),
    },
    "celestial": {
        "outline": (47, 48, 70, 255), "handle": (112, 116, 148, 255),
        "handle_light": (173, 178, 204, 255), "metal_dark": (143, 151, 184, 255),
        "metal": (218, 221, 238, 255), "edge": (255, 211, 111, 255),
        "shine": (255, 255, 242, 255), "gem": (255, 226, 151, 255),
    },
}

KINDS = ("pickaxe", "axe", "shovel", "hoe", "multitool", "sword")


def line(draw, points, fill, width=1):
    draw.line(points, fill=fill, width=width)


def outlined_polygon(draw, points, fill, outline):
    draw.polygon(points, fill=fill, outline=outline)


def draw_handle(draw, p, start=(7, 27), end=(22, 12), width=4):
    # Dark pixel outline, wooden core and one restrained highlight.
    line(draw, [start, end], p["outline"], width + 2)
    line(draw, [start, end], p["handle"], width)
    line(draw, [(start[0]+1, start[1]-1), (end[0]+1, end[1]-1)],
         p["handle_light"], 1)
    draw.point((start[0], start[1]-1), fill=p["edge"])


def draw_pickaxe(draw, p):
    # Broad, unmistakable pick head with two tapered tips.
    outlined_polygon(draw,
        [(4, 7), (8, 4), (13, 6), (18, 7), (24, 3), (28, 5),
         (26, 10), (19, 12), (13, 10), (8, 13), (5, 11)],
        p["metal_dark"], p["outline"])
    outlined_polygon(draw,
        [(6, 7), (9, 6), (14, 8), (19, 9), (24, 5), (26, 6),
         (25, 8), (19, 11), (13, 9), (8, 11)],
        p["metal"], p["outline"])
    line(draw, [(8, 7), (14, 9), (19, 10), (24, 7)], p["shine"], 1)
    draw.point((25, 6), fill=p["edge"])


def draw_axe(draw, p):
    # Heavy wedge on one side of the haft, like a vanilla axe sprite.
    outlined_polygon(draw,
        [(8, 5), (16, 4), (23, 7), (28, 12), (27, 18), (22, 20),
         (17, 16), (12, 12), (7, 12), (5, 9)],
        p["metal_dark"], p["outline"])
    outlined_polygon(draw,
        [(10, 7), (16, 6), (22, 9), (26, 13), (25, 16), (22, 17),
         (17, 13), (12, 10), (8, 10)],
        p["metal"], p["outline"])
    line(draw, [(10, 7), (17, 9), (23, 14)], p["shine"], 1)
    line(draw, [(22, 17), (25, 16), (26, 13)], p["edge"], 1)


def draw_shovel(draw, p):
    # Narrow neck and broad spade head.
    outlined_polygon(draw,
        [(11, 3), (21, 3), (27, 8), (26, 16), (21, 21),
         (11, 21), (6, 16), (5, 8)],
        p["metal_dark"], p["outline"])
    outlined_polygon(draw,
        [(12, 5), (20, 5), (24, 9), (23, 15), (19, 19),
         (13, 19), (9, 15), (8, 9)],
        p["metal"], p["outline"])
    outlined_polygon(draw, [(13, 7), (19, 7), (22, 10), (16, 16), (10, 10)],
                     p["metal_dark"], p["edge"])
    line(draw, [(13, 8), (17, 12)], p["shine"], 1)


def draw_hoe(draw, p):
    # Thin horizontal tine and a short downward hook.
    outlined_polygon(draw,
        [(5, 5), (10, 3), (16, 6), (22, 6), (27, 9), (26, 14),
         (21, 15), (16, 11), (11, 11), (8, 15), (4, 13)],
        p["metal_dark"], p["outline"])
    outlined_polygon(draw,
        [(7, 6), (10, 5), (16, 8), (22, 8), (25, 10), (24, 12),
         (21, 12), (15, 10), (10, 9), (7, 12)],
        p["metal"], p["outline"])
    line(draw, [(8, 6), (16, 9), (23, 10)], p["shine"], 1)


def draw_multitool(draw, p):
    # A recognizable pick head with a compact axe blade on the right.
    outlined_polygon(draw,
        [(3, 8), (7, 4), (13, 7), (18, 8), (24, 4), (28, 7),
         (25, 12), (19, 13), (13, 11), (8, 14), (4, 12)],
        p["metal_dark"], p["outline"])
    outlined_polygon(draw,
        [(5, 8), (8, 6), (14, 9), (19, 10), (24, 6), (26, 8),
         (24, 10), (19, 12), (13, 10), (8, 12)],
        p["metal"], p["outline"])
    outlined_polygon(draw, [(20, 12), (27, 11), (29, 16), (25, 20), (21, 17)],
                     p["metal_dark"], p["outline"])
    line(draw, [(7, 8), (14, 10), (19, 11), (24, 8)], p["shine"], 1)
    draw.point((27, 15), fill=p["edge"])


def draw_sword(draw, p):
    # Blade, fuller, crossguard and grip; the diagonal sword silhouette stays
    # readable in the inventory and at normal GUI scale.
    outlined_polygon(draw, [(22, 2), (28, 5), (12, 24), (8, 21)],
                     p["metal_dark"], p["outline"])
    outlined_polygon(draw, [(23, 4), (26, 5), (12, 21), (10, 20)],
                     p["metal"], p["outline"])
    line(draw, [(23, 4), (13, 18)], p["shine"], 1)
    line(draw, [(8, 19), (17, 27)], p["outline"], 4)
    line(draw, [(8, 19), (17, 27)], p["edge"], 2)
    line(draw, [(6, 24), (12, 18)], p["outline"], 3)
    line(draw, [(7, 24), (11, 20)], p["metal"], 1)
    outlined_polygon(draw, [(14, 25), (18, 28), (15, 31), (11, 28)],
                     p["handle"], p["outline"])
    draw.point((25, 5), fill=p["edge"])


def draw_signature(draw, material, p, kind):
    # A few pixels, not a large glowing blob: lore identity without destroying
    # the vanilla item silhouette.
    if kind == "sword":
        draw.point((20, 8), fill=p["gem"])
        draw.point((18, 10), fill=p["edge"])
    elif kind == "pickaxe":
        draw.point((15, 7), fill=p["gem"])
    elif kind == "axe":
        draw.point((21, 10), fill=p["gem"])
    elif kind == "shovel":
        draw.point((16, 11), fill=p["gem"])
    elif kind == "hoe":
        draw.point((17, 8), fill=p["gem"])
    else:
        draw.point((17, 8), fill=p["gem"])
        draw.point((24, 15), fill=p["edge"])
    if material == "solar":
        draw.point((kind != "sword" and 12 or 19, 5), fill=p["edge"])
    elif material == "abyssal":
        draw.point((kind != "sword" and 19 or 16, 13), fill=p["shine"])
    else:
        draw.point((kind != "sword" and 14 or 22, 6), fill=p["shine"])


def make_tool_sprite(material, kind):
    p = PALETTES[material]
    image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if kind == "sword":
        draw_sword(draw, p)
    else:
        draw_handle(draw, p)
        if kind == "pickaxe":
            draw_pickaxe(draw, p)
        elif kind == "axe":
            draw_axe(draw, p)
        elif kind == "shovel":
            draw_shovel(draw, p)
        elif kind == "hoe":
            draw_hoe(draw, p)
        else:
            draw_multitool(draw, p)

    draw_signature(draw, material, p, kind)
    return image


def flat_model(item_id, handheld):
    texture = f"celestial_dominion:item/{item_id}"
    if not handheld:
        return {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": texture},
        }

    # A thick, pixel-art extrusion: the transparent silhouette stays crisp in
    # the GUI while the item has visible physical depth in first/third person.
    return {
        "textures": {"layer0": texture, "particle": texture},
        "elements": [{
            "from": [1, 1, 7],
            "to": [15, 15, 9],
            "faces": {
                "north": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
                "south": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
                "east": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
                "west": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
                "up": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
                "down": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
            },
        }],
        "display": {
            "thirdperson_righthand": {
                "rotation": [0, -90, 55], "translation": [0, 4, 1],
                "scale": [1.12, 1.12, 1.12],
            },
            "thirdperson_lefthand": {
                "rotation": [0, 90, -55], "translation": [0, 4, 1],
                "scale": [1.12, 1.12, 1.12],
            },
            "firstperson_righthand": {
                "rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13],
                "scale": [1.18, 1.18, 1.18],
            },
            "firstperson_lefthand": {
                "rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13],
                "scale": [1.18, 1.18, 1.18],
            },
            "gui": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [1, 1, 1]},
            "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.65, 0.65, 0.65]},
            "fixed": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [0.8, 0.8, 0.8]},
        },
    }



def make_spear_sprite(material):
    p = PALETTES[material]
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    line(draw, [(13,58),(49,13)], p["outline"], 10)
    line(draw, [(14,57),(48,14)], p["handle"], 7)
    line(draw, [(15,55),(47,15)], p["handle_light"], 3)
    for i in range(4):
        x, y = 17 + i * 4, 53 - i * 5
        line(draw, [(x-3,y+3),(x+2,y-2)], p["edge"], 2)
    outlined_polygon(draw, [(8,56),(14,52),(19,57),(16,63),(10,62)],
                     p["metal_dark"], p["outline"])
    outlined_polygon(draw, [(40,20),(47,10),(53,12),(46,24)],
                     p["metal_dark"], p["outline"])
    if material == "solar":
        outlined_polygon(draw, [(49,2),(62,8),(57,17),(49,25),(43,17)],
                         p["metal_dark"], p["outline"])
        outlined_polygon(draw, [(50,4),(58,9),(54,16),(49,21),(46,16)],
                         p["metal"], p["edge"])
        outlined_polygon(draw, [(47,14),(39,10),(43,19),(49,20)],
                         p["gem"], p["outline"])
        outlined_polygon(draw, [(55,15),(61,19),(54,18)], p["edge"], p["outline"])
        draw.point((54,8), fill=p["shine"])
    elif material == "abyssal":
        outlined_polygon(draw, [(50,2),(62,8),(57,17),(50,24),(44,17),(47,9)],
                         p["metal_dark"], p["outline"])
        outlined_polygon(draw, [(51,4),(59,9),(55,16),(50,21),(47,16)],
                         p["edge"], p["shine"])
        outlined_polygon(draw, [(47,14),(40,8),(43,19)],
                         p["metal"], p["outline"])
        line(draw, [(50,21),(44,26)], p["edge"], 2)
        draw.point((54,8), fill=p["shine"])
    else:
        outlined_polygon(draw, [(52,2),(61,8),(56,17),(51,24),(45,17),(48,8)],
                         p["metal_dark"], p["outline"])
        outlined_polygon(draw, [(52,4),(58,9),(55,16),(51,21),(48,16)],
                         p["metal"], p["edge"])
        outlined_polygon(draw, [(52,5),(56,9),(52,14),(49,9)],
                         p["shine"], p["edge"])
        outlined_polygon(draw, [(48,14),(41,12),(45,20)],
                         p["gem"], p["outline"])
    for x, y in ((25,45),(31,38),(37,31)):
        draw.point((x,y), fill=p["gem"])
        draw.point((x+1,y-1), fill=p["shine"])
    return image

def main():
    MODELS.mkdir(parents=True, exist_ok=True)
    TEXTURES.mkdir(parents=True, exist_ok=True)

    for material in PALETTES:
        for kind in KINDS:
            item_id = f"{material}_{kind}"
            make_tool_sprite(material, kind).save(TEXTURES / f"{item_id}.png", optimize=True)
            (MODELS / f"{item_id}.json").write_text(
                json.dumps(flat_model(item_id, handheld=True), indent=2) + "\n",
                encoding="utf-8",
            )
            meta = TEXTURES / f"{item_id}.png.mcmeta"
            if meta.exists():
                meta.unlink()

        # Ingredients use vanilla's generated-item renderer, not cuboids.
        for item_id in (f"{material}_ingot", f"{material}_smithing_template"):
            if item_id.endswith("smithing_template") and material == "celestial":
                continue
            (MODELS / f"{item_id}.json").write_text(
                json.dumps(flat_model(item_id, handheld=False), indent=2) + "\n",
                encoding="utf-8",
            )

    catalyst = "celestial_catalyst"
    (MODELS / f"{catalyst}.json").write_text(
        json.dumps(flat_model(catalyst, handheld=False), indent=2) + "\n",
        encoding="utf-8",
    )

    # Native 26.3 spears need a GUI model and a dedicated held model so the
    # vanilla jab/charge animations and display-context switching remain intact.
    item_definitions = ROOT / "items"
    item_definitions.mkdir(parents=True, exist_ok=True)
    for material in PALETTES:
        spear = f"{material}_spear"
        make_spear_sprite(material).save(TEXTURES / f"{spear}.png", optimize=True)
        (MODELS / f"{spear}.json").write_text(
            json.dumps(flat_model(spear, handheld=False), indent=2) + "\n",
            encoding="utf-8",
        )
        held_model = {
            "parent": "minecraft:item/netherite_spear_in_hand",
            "textures": {"layer0": f"celestial_dominion:item/{spear}"},
        }
        (MODELS / f"{spear}_in_hand.json").write_text(
            json.dumps(held_model, indent=2) + "\n",
            encoding="utf-8",
        )
        definition = {
            "model": {
                "type": "minecraft:select",
                "property": "minecraft:display_context",
                "cases": [{
                    "when": ["gui", "ground", "fixed", "on_shelf"],
                    "model": {"type": "minecraft:model", "model": f"celestial_dominion:item/{spear}"},
                }],
                "fallback": {"type": "minecraft:model", "model": f"celestial_dominion:item/{spear}_in_hand"},
            },
            "swap_animation_scale": 1.95,
        }
        (item_definitions / f"{spear}.json").write_text(
            json.dumps(definition, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
