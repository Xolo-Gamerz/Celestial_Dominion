#!/usr/bin/env python3
"""Generate Celestial Dominion's 32x32 item art and 64x32 armor atlases.

Only Pillow is required. Run from any directory; output paths are resolved from
this script, so the GitHub Actions workflow and local runs produce identical files.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import random

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/assets/celestial_dominion"

# Each set has its own material identity: forged embersteel, abyssal obsidian,
# and ivory-gold astral alloy. These palettes are deliberately not recolors of
# one another: their silhouettes and motifs also differ.
PALETTES = {
    "solar": {
        "shadow": (48, 12, 22, 255), "base": (116, 27, 25, 255),
        "mid": (204, 66, 24, 255), "accent": (255, 166, 35, 255),
        "shine": (255, 225, 135, 255), "white": (255, 248, 211, 255),
    },
    "abyssal": {
        "shadow": (8, 9, 24, 255), "base": (31, 25, 61, 255),
        "mid": (76, 48, 117, 255), "accent": (25, 202, 213, 255),
        "shine": (119, 247, 246, 255), "white": (220, 255, 255, 255),
    },
    "celestial": {
        "shadow": (70, 56, 105, 255), "base": (190, 190, 221, 255),
        "mid": (232, 229, 247, 255), "accent": (244, 190, 65, 255),
        "shine": (255, 245, 188, 255), "white": (255, 255, 255, 255),
    },
}
MATERIALS = tuple(PALETTES)
PIECES = ("helmet", "chestplate", "leggings", "boots")


def rgba(c):
    return c if len(c) == 4 else (*c, 255)


def draw_gem(draw, cx, cy, radius, colors):
    x, y, r = cx, cy, radius
    draw.polygon([(x, y-r), (x+r, y-r//3), (x+r//2, y+r), (x-r//2, y+r), (x-r, y-r//3)],
                 fill=colors[1], outline=colors[3])
    draw.line((x, y-r+1, x, y+r-1), fill=colors[3])
    draw.point((x-1, y-r//3), fill=colors[2])


def make_armor_icon(material, piece):
    p = PALETTES[material]
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    outline, base, mid, accent, shine, white = (p[k] for k in ("shadow", "base", "mid", "accent", "shine", "white"))

    if piece == "helmet":
        # A proper helmet silhouette, with set-specific crest / crown profile.
        d.polygon([(7, 11), (8, 6), (13, 3), (19, 3), (24, 6), (26, 12),
                   (24, 22), (21, 26), (11, 26), (8, 22)], fill=base, outline=shine)
        d.polygon([(9, 11), (12, 6), (20, 6), (24, 11), (22, 14), (10, 14)], fill=mid)
        d.rectangle((9, 15, 23, 18), fill=outline)
        d.line((10, 14, 22, 14), fill=accent, width=2)
        d.rectangle((12, 16, 14, 17), fill=white)
        d.rectangle((18, 16, 20, 17), fill=white)
        d.line((10, 21, 22, 21), fill=accent)
        if material == "solar":
            d.polygon([(12, 6), (10, 1), (15, 4), (16, 0), (18, 4), (23, 1), (21, 7)], fill=accent, outline=shine)
            d.point((16, 9), fill=white)
        elif material == "abyssal":
            d.polygon([(8, 10), (3, 7), (7, 15), (9, 17)], fill=accent, outline=shine)
            d.polygon([(24, 10), (29, 7), (25, 15), (23, 17)], fill=accent, outline=shine)
            d.ellipse((14, 8, 18, 12), fill=accent, outline=white)
        else:
            d.polygon([(16, 0), (18, 5), (23, 6), (18, 8), (16, 13), (14, 8), (9, 6), (14, 5)], fill=accent, outline=white)
            d.point((16, 17), fill=white)

    elif piece == "chestplate":
        d.polygon([(8, 6), (13, 4), (19, 4), (24, 6), (29, 12), (26, 17),
                   (24, 27), (8, 27), (6, 17), (3, 12)], fill=base, outline=shine)
        d.polygon([(8, 7), (13, 6), (16, 9), (19, 6), (24, 7), (25, 13), (21, 16),
                   (11, 16), (7, 13)], fill=mid, outline=accent)
        d.polygon([(7, 14), (15, 16), (16, 25), (9, 24)], fill=base, outline=accent)
        d.polygon([(25, 14), (17, 16), (16, 25), (23, 24)], fill=base, outline=accent)
        d.line((16, 10, 16, 24), fill=shine, width=2)
        if material == "solar":
            d.ellipse((12, 12, 20, 20), fill=accent, outline=white)
            d.ellipse((14, 14, 18, 18), fill=white)
            for a, b in [(16, 9), (16, 22), (10, 16), (22, 16)]: d.point((a, b), fill=shine)
        elif material == "abyssal":
            d.ellipse((10, 12, 22, 21), fill=outline, outline=accent)
            d.ellipse((14, 13, 18, 19), fill=accent, outline=white)
            d.point((16, 16), fill=white)
        else:
            draw_gem(d, 16, 16, 6, (outline, accent, mid, white))
            d.line((6, 11, 9, 14), fill=white)
            d.line((26, 11, 23, 14), fill=white)

    elif piece == "leggings":
        d.polygon([(8, 4), (24, 4), (25, 11), (22, 15), (23, 28), (17, 29),
                   (16, 17), (15, 29), (9, 28), (10, 15), (7, 11)], fill=base, outline=shine)
        d.rectangle((8, 5, 24, 9), fill=mid, outline=accent)
        d.line((16, 10, 16, 26), fill=accent, width=2)
        d.line((10, 15, 14, 16, 14, 24), fill=shine)
        d.line((22, 15, 18, 16, 18, 24), fill=shine)
        d.rectangle((10, 17, 14, 20), fill=mid, outline=accent)
        d.rectangle((18, 17, 22, 20), fill=mid, outline=accent)
        if material == "solar":
            d.rectangle((13, 5, 19, 8), fill=accent)
            d.point((16, 6), fill=white)
            d.line((10, 24, 14, 26), fill=accent)
            d.line((18, 26, 22, 24), fill=accent)
        elif material == "abyssal":
            d.line((9, 11, 13, 14, 11, 17, 14, 20), fill=accent, width=2)
            d.line((23, 11, 19, 14, 21, 17, 18, 20), fill=accent, width=2)
        else:
            d.polygon([(16, 11), (18, 15), (22, 16), (18, 18), (16, 22), (14, 18), (10, 16), (14, 15)], fill=accent, outline=white)

    elif piece == "boots":
        # Two distinct boots, not a recolored chestplate silhouette.
        d.polygon([(5, 5), (14, 5), (14, 20), (12, 23), (14, 26), (13, 29),
                   (3, 29), (2, 26), (5, 22)], fill=base, outline=shine)
        d.polygon([(18, 5), (27, 5), (27, 22), (30, 26), (29, 29),
                   (19, 29), (18, 26), (20, 23)], fill=base, outline=shine)
        d.line((6, 7, 12, 7, 12, 19), fill=mid, width=2)
        d.line((20, 7, 26, 7, 26, 19), fill=mid, width=2)
        d.rectangle((3, 26, 13, 28), fill=accent)
        d.rectangle((19, 26, 29, 28), fill=accent)
        if material == "solar":
            d.line((6, 14, 12, 17), fill=shine, width=2)
            d.line((20, 17, 26, 14), fill=shine, width=2)
            d.point((8, 22), fill=white); d.point((24, 22), fill=white)
        elif material == "abyssal":
            d.line((5, 12, 10, 16, 8, 19), fill=accent, width=2)
            d.line((27, 12, 22, 16, 24, 19), fill=accent, width=2)
            d.point((9, 22), fill=white); d.point((23, 22), fill=white)
        else:
            d.polygon([(9, 11), (11, 15), (14, 16), (11, 18), (9, 21), (7, 18), (4, 16), (7, 15)], fill=accent)
            d.polygon([(23, 11), (25, 15), (28, 16), (25, 18), (23, 21), (21, 18), (18, 16), (21, 15)], fill=accent)
    return im


def make_sword(material):
    p = PALETTES[material]
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    dark, base, mid, accent, shine, white = (p[k] for k in ("shadow", "base", "mid", "accent", "shine", "white"))
    d.polygon([(23, 1), (29, 4), (13, 23), (9, 20)], fill=shine, outline=dark)
    d.polygon([(23, 2), (26, 4), (12, 21), (11, 19)], fill=white)
    d.line((10, 20, 5, 27), fill=accent, width=3)
    d.line((7, 17, 15, 25), fill=mid, width=3)
    d.line((4, 26, 8, 29), fill=dark, width=3)
    d.rectangle((4, 27, 8, 30), fill=base, outline=shine)
    if material == "solar":
        d.point((24, 3), fill=accent); d.line((18, 8, 21, 10), fill=accent, width=2)
    elif material == "abyssal":
        d.line((17, 9, 21, 7, 22, 10), fill=accent, width=2); d.point((15, 15), fill=white)
    else:
        d.polygon([(20, 5), (22, 8), (25, 9), (22, 11), (20, 14), (18, 11), (15, 9), (18, 8)], fill=accent)
    return im


def make_ingot(material):
    p = PALETTES[material]; im = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(4, 10), (22, 5), (29, 11), (26, 23), (9, 27), (3, 20)], fill=p["base"], outline=p["shine"])
    d.polygon([(6, 11), (22, 7), (26, 12), (10, 16)], fill=p["mid"])
    d.polygon([(10, 17), (26, 13), (24, 21), (9, 25), (5, 20)], fill=p["accent"])
    d.line((7, 12, 22, 8), fill=p["white"], width=2)
    d.line((10, 23, 23, 19), fill=p["shine"])
    return im


def make_template(material):
    p = PALETTES[material]; im = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 3, 27, 28), radius=2, fill=p["shadow"], outline=p["shine"], width=2)
    d.rectangle((7, 6, 24, 25), fill=p["base"], outline=p["accent"])
    d.rectangle((10, 9, 21, 22), fill=p["mid"], outline=p["shine"])
    if material == "solar":
        d.ellipse((12, 11, 20, 19), fill=p["accent"], outline=p["white"])
        d.line((16, 8, 16, 23), fill=p["shine"]); d.line((9, 15, 23, 15), fill=p["shine"])
    elif material == "abyssal":
        d.ellipse((10, 11, 22, 20), fill=p["shadow"], outline=p["accent"])
        d.ellipse((14, 12, 18, 19), fill=p["accent"], outline=p["white"])
    else:
        draw_gem(d, 16, 15, 7, (p["shadow"], p["accent"], p["mid"], p["white"]))
    d.line((8, 26, 23, 26), fill=p["shine"])
    return im


def make_catalyst():
    p = PALETTES["celestial"]; im = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(16, 1), (25, 9), (29, 17), (16, 30), (3, 17), (7, 9)], fill=p["shadow"], outline=p["white"])
    d.polygon([(16, 4), (23, 10), (25, 17), (16, 26), (7, 17), (9, 10)], fill=p["accent"], outline=p["shine"])
    d.polygon([(16, 7), (21, 12), (16, 22), (11, 12)], fill=p["white"])
    d.point((16, 14), fill=p["mid"])
    return im


def make_ore_block(material):
    p = PALETTES[material]; rng = random.Random(2603 + list(MATERIALS).index(material))
    im = Image.new("RGBA", (16, 16), p["shadow"]); d = ImageDraw.Draw(im)
    # Deep, irregular host rock; each ore has its own crystal geometry.
    for y in range(16):
        for x in range(16):
            n = rng.randrange(5)
            if n == 0: d.point((x, y), fill=p["base"])
            elif n == 1: d.point((x, y), fill=(p["base"][0]//2, p["base"][1]//2, p["base"][2]//2, 255))
    if material == "solar":
        for pts in [[(2,3),(3,2),(4,3),(3,4)],[(10,2),(11,3),(12,4),(11,5)],[(6,10),(7,9),(8,10),(7,12)],[(12,12),(13,11),(14,12),(13,14)]]:
            d.polygon(pts, fill=p["accent"], outline=p["shine"])
        d.point((3,3), fill=p["white"]); d.point((11,3), fill=p["white"])
    elif material == "abyssal":
        d.line((1,3,4,6,3,9,6,12), fill=p["accent"], width=2)
        d.line((9,1,12,4,11,7,14,10), fill=p["mid"], width=2)
        d.ellipse((6,5,10,9), fill=p["accent"], outline=p["white"])
        d.point((8,7), fill=p["shadow"])
    else:
        d.line((2,2,6,6,9,4,13,8), fill=p["accent"], width=2)
        d.line((1,12,5,9,8,12,12,10), fill=p["shine"], width=1)
        d.polygon([(11,2),(12,5),(15,6),(12,7),(11,10),(10,7),(7,6),(10,5)], fill=p["white"])
    return im


def make_armor_atlas(material, layer):
    p = PALETTES[material]
    im = Image.new("RGBA", (64, 32), p["shadow"])
    d = ImageDraw.Draw(im)
    # Fine plate grain, bevels and seams across the 64x32 humanoid UV atlas.
    for x in range(0, 64, 8):
        d.rectangle((x, 0, min(63, x+7), 31), fill=p["base"] if (x//8)%2 == 0 else p["shadow"])
        d.line((x, 0, x, 31), fill=p["mid"], width=1)
    for y in range(0, 32, 8):
        d.line((0, y, 63, y), fill=p["mid"], width=1)
    # Armor plates, distinct panel treatment for each UV texture family.
    if layer == "humanoid_leggings":
        d.rectangle((2, 2, 61, 29), fill=p["base"], outline=p["shine"])
        d.rectangle((5, 4, 58, 8), fill=p["mid"], outline=p["accent"])
        d.line((16, 9, 16, 28), fill=p["accent"], width=2)
        d.line((31, 9, 31, 28), fill=p["shine"], width=1)
        d.line((47, 9, 47, 28), fill=p["accent"], width=2)
        for x in (8, 24, 40, 56):
            d.rectangle((x-2, 13, x+2, 20), fill=p["mid"], outline=p["shine"])
    elif layer == "humanoid_baby":
        d.rectangle((1, 1, 62, 30), fill=p["base"], outline=p["shine"])
        d.rectangle((4, 4, 59, 27), fill=p["mid"], outline=p["accent"])
        d.line((4, 5, 59, 26), fill=p["shine"], width=1)
        d.line((59, 5, 4, 26), fill=p["accent"], width=1)
    else:
        d.rectangle((1, 1, 62, 30), fill=p["base"], outline=p["shine"])
        d.rectangle((4, 4, 59, 27), fill=p["mid"], outline=p["accent"])
        d.line((4, 8, 59, 8), fill=p["shine"], width=1)
        d.line((4, 23, 59, 23), fill=p["shadow"], width=2)
        for x in (8, 24, 40, 56):
            d.rectangle((x-2, 11, x+2, 20), fill=p["base"], outline=p["shine"])
    # Set-specific insignia: sunburst, abyssal eye, or eight-point star.
    for cx in (12, 32, 52):
        cy = 16
        if material == "solar":
            d.ellipse((cx-3, cy-3, cx+3, cy+3), fill=p["accent"], outline=p["white"])
            d.line((cx, cy-6, cx, cy+6), fill=p["shine"])
            d.line((cx-6, cy, cx+6, cy), fill=p["shine"])
        elif material == "abyssal":
            d.ellipse((cx-5, cy-3, cx+5, cy+3), fill=p["shadow"], outline=p["accent"])
            d.ellipse((cx-1, cy-2, cx+1, cy+2), fill=p["shine"])
        else:
            d.polygon([(cx,cy-6),(cx+2,cy-2),(cx+6,cy),(cx+2,cy+2),(cx,cy+6),(cx-2,cy+2),(cx-6,cy),(cx-2,cy-2)],
                      fill=p["accent"], outline=p["white"])
    # Sparse glints keep the 64x32 map readable in motion.
    rng = random.Random(800 + list(MATERIALS).index(material)*13 + len(layer))
    for _ in range(34):
        x, y = rng.randrange(64), rng.randrange(32)
        d.point((x, y), fill=p["shine"] if rng.random() < .5 else p["mid"])
    return im


def main():
    (ROOT / "textures/item").mkdir(parents=True, exist_ok=True)
    (ROOT / "textures/block").mkdir(parents=True, exist_ok=True)

    for material in MATERIALS:
        for piece in PIECES:
            make_armor_icon(material, piece).save(ROOT / "textures/item" / f"{material}_{piece}.png")
        make_sword(material).save(ROOT / "textures/item" / f"{material}_sword.png")
        make_ingot(material).save(ROOT / "textures/item" / f"{material}_ingot.png")
        if material != "celestial":
            make_template(material).save(ROOT / "textures/item" / f"{material}_smithing_template.png")
        make_ore_block(material).save(ROOT / "textures/block" / f"{material}_ore.png")
        for layer in ("humanoid", "humanoid_leggings", "humanoid_baby"):
            out = ROOT / "textures/entity/equipment" / layer / f"{material}.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            atlas = make_armor_atlas(material, layer)
            if layer == "humanoid_baby":
                # 26.1+ uses a dedicated 64x64 baby-humanoid equipment atlas.
                # Preserve the UV art in the upper atlas and mirror its mapped
                # surfaces into the lower half instead of stretching the UVs.
                baby = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
                baby.paste(atlas, (0, 0))
                baby.paste(atlas, (0, 32))
                atlas = baby
            atlas.save(out)
    make_catalyst().save(ROOT / "textures/item" / "celestial_catalyst.png")


if __name__ == "__main__":
    main()
