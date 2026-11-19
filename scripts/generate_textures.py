#!/usr/bin/env python3
"""Generate Celestial Dominion's 32x32 item art and 64x32 armor atlases.

Only Pillow is required. Run from any directory; output paths are resolved from
this script, so the GitHub Actions workflow and local runs produce identical files.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import random
import json

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


def make_wings(material, frame=0):
    """64x32 texture for the built-in humanoid WingsLayer (elytra geometry)."""
    p = PALETTES[material]
    im = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    outline, base, mid, accent, shine, white = (
        p[k] for k in ("shadow", "base", "mid", "accent", "shine", "white")
    )
    # Two swept feather/energy vanes around the center hinge.
    d.polygon([(30, 2), (24, 4), (15, 7), (4, 15), (2, 24), (10, 27),
               (19, 23), (27, 17), (31, 13)], fill=base, outline=shine)
    d.polygon([(34, 2), (40, 4), (49, 7), (60, 15), (62, 24), (54, 27),
               (45, 23), (37, 17), (33, 13)], fill=base, outline=shine)
    d.polygon([(29, 5), (22, 8), (12, 14), (7, 21), (14, 22),
               (23, 17), (30, 11)], fill=mid, outline=accent)
    d.polygon([(35, 5), (42, 8), (52, 14), (57, 21), (50, 22),
               (41, 17), (34, 11)], fill=mid, outline=accent)
    # Raised vane ridges and luminous edge seams.
    d.line((29, 7, 21, 12, 12, 19, 6, 22), fill=shine, width=2)
    d.line((35, 7, 43, 12, 52, 19, 58, 22), fill=shine, width=2)
    d.line((28, 11, 20, 18, 14, 23), fill=accent, width=2)
    d.line((36, 11, 44, 18, 50, 23), fill=accent, width=2)
    d.polygon([(29, 1), (35, 1), (37, 8), (32, 15), (27, 8)],
              fill=accent, outline=white)
    d.rectangle((30, 4, 33, 10), fill=white)
    # Material signature.
    if material == "solar":
        shift = frame % 4
        for x in (7, 14, 21, 43, 50, 57):
            d.line((x, 18-shift, x+2, 13-shift), fill=shine, width=2)
            d.point((x+2, 12-shift), fill=white)
    elif material == "abyssal":
        pulse = frame % 3
        for x in (8, 17, 24, 40, 47, 56):
            d.ellipse((x-1-pulse, 15-pulse, x+2+pulse, 18+pulse), fill=accent, outline=white)
        d.line((8, 25, 20, 20-pulse, 28, 15), fill=white, width=1)
        d.line((56, 25, 44, 20-pulse, 36, 15), fill=white, width=1)
    else:
        for i, (x, y) in enumerate(((8, 17), (18, 12), (24, 19), (56, 17), (46, 12), (40, 19))):
            shift = (frame + i) % 3 - 1
            d.line((x-2, y+shift, x+2, y+shift), fill=white, width=1)
            d.line((x, y-2+shift, x, y+2+shift), fill=accent, width=1)
    return im


def make_armor_overlay(material, layer):
    """Transparent trim placed only on real humanoid armor UV islands."""
    p = PALETTES[material]
    im = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bright = (*p["shine"][:3], 245)
    accent = (*p["accent"][:3], 235)
    white = (*p["white"][:3], 255)

    def seam(points, color=bright):
        d.line(points, fill=color, width=1)

    def diamond(cx, cy, color=accent):
        d.polygon([(cx, cy-2), (cx+2, cy), (cx, cy+2), (cx-2, cy)], fill=color)

    if layer == "humanoid_leggings":
        # Front-facing leg panels and small knee/ankle details.
        for x in (4, 20):
            seam((x, 22, x, 29), accent)
            seam((x+3, 22, x+3, 29), bright)
            diamond(x+2, 24, white)
            seam((x-1, 30, x+4, 30), bright)
        return im

    # Helmet front face (8,8)-(15,15): crest is deliberately tiny.
    if material == "solar":
        diamond(12, 11, white)
        seam((12, 8, 12, 10), bright)
        seam((9, 11, 11, 11), accent)
        seam((13, 11, 15, 11), accent)
    elif material == "abyssal":
        d.ellipse((10, 10, 14, 13), outline=accent, width=1)
        d.point((12, 11), fill=white)
    else:
        diamond(12, 11, white)
        d.point((10, 13), fill=accent)
        d.point((14, 9), fill=accent)

    # Chest insignia on the front torso UV (20,20)-(27,31).
    if material == "solar":
        d.ellipse((22, 23, 25, 26), outline=white, width=1)
        seam((23, 21, 23, 28), bright)
        seam((20, 24, 27, 24), accent)
    elif material == "abyssal":
        d.ellipse((21, 24, 26, 27), outline=accent, width=1)
        d.ellipse((23, 24, 24, 26), fill=white)
    else:
        diamond(23, 25, white)
        seam((21, 23, 25, 27), accent)
        seam((25, 23, 21, 27), accent)

    # Repeated, restrained trim on arm and leg faces, not across unused UVs.
    for x in (42, 46, 50, 54):
        seam((x, 23, x, 28), accent)
        d.point((x, 29), fill=white)
    for x in (4, 8, 12):
        seam((x, 23, x, 28), bright if material == "celestial" else accent)
    return im


def make_armor_atlas(material, layer):
    """Paint original pixel-art plates into Minecraft's 64x32 armor UV net."""
    p = PALETTES[material]
    im = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    outline, base, mid, accent, shine, white = (
        p[k] for k in ("shadow", "base", "mid", "accent", "shine", "white")
    )

    def face_box(rect, fill, edge=outline):
        d.rectangle(rect, fill=fill, outline=edge)

    def panel(rect, inset=1):
        x0, y0, x1, y1 = rect
        face_box(rect, base)
        if x1 - x0 > 3 and y1 - y0 > 3:
            d.rectangle((x0+inset, y0+inset, x1-inset, y1-inset),
                        fill=mid, outline=accent)
        d.line((x0+1, y0+1, x1-1, y0+1), fill=shine)

    if layer == "humanoid_leggings":
        # Layer 2 is two leg cuboids: 4x12 side/front/back faces plus caps.
        for x in (0, 16):
            panel((x+4, 16, x+7, 19), 0)
            panel((x+8, 16, x+11, 19), 0)
            for face_x in (x, x+4, x+8, x+12):
                panel((face_x, 20, face_x+3, 31))
            # Knee plate and boot cuff sit on the front face.
            d.rectangle((x+4, 22, x+7, 25), fill=base, outline=shine)
            d.line((x+4, 28, x+7, 28), fill=accent, width=1)
            d.point((x+5, 23), fill=white)
        return im

    # Helmet: two 8x8 caps and four 8x8 side faces.
    panel((8, 0, 15, 7))
    panel((16, 0, 23, 7))
    for x in (0, 8, 16, 24):
        panel((x, 8, x+7, 15))
    # Front visor/face plate.
    d.rectangle((9, 11, 14, 13), fill=outline, outline=accent)
    d.point((10, 12), fill=white)
    d.point((13, 12), fill=white)

    # Torso: caps and four wrapped 8x12 / 4x12 body faces.
    panel((20, 16, 27, 19), 0)
    panel((28, 16, 35, 19), 0)
    for rect in ((16, 20, 19, 31), (20, 20, 27, 31),
                 (28, 20, 31, 31), (32, 20, 39, 31)):
        panel(rect)
    # Chest plate silhouette and central material emblem.
    d.polygon([(21, 21), (26, 21), (27, 25), (24, 30),
               (20, 25)], fill=base, outline=shine)
    if material == "solar":
        d.ellipse((22, 23, 25, 26), fill=accent, outline=white)
        d.point((23, 24), fill=white)
    elif material == "abyssal":
        d.ellipse((21, 24, 26, 27), fill=outline, outline=accent)
        d.point((23, 25), fill=white)
    else:
        d.polygon([(23, 22), (25, 25), (23, 28), (21, 25)],
                  fill=accent, outline=white)

    # Arm cuboid faces; cuff and seam details remain aligned to the UV net.
    panel((44, 16, 47, 19), 0)
    panel((48, 16, 51, 19), 0)
    for rect in ((40, 20, 43, 31), (44, 20, 47, 31),
                 (48, 20, 51, 31), (52, 20, 55, 31)):
        panel(rect)
    d.rectangle((44, 28, 47, 30), fill=accent, outline=shine)
    d.rectangle((4, 28, 7, 30), fill=accent, outline=shine)
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
        wings = ROOT / "textures/entity/equipment/wings" / f"{material}.png"
        wings.parent.mkdir(parents=True, exist_ok=True)
        wing_sheet = Image.new("RGBA", (64, 32 * 8), (0, 0, 0, 0))
        for frame in range(8):
            wing_sheet.paste(make_wings(material, frame), (0, frame * 32))
        wing_sheet.save(wings)
        (wings.parent / f"{material}.png.mcmeta").write_text(
            json.dumps({"animation": {"width": 64, "height": 32, "frametime": 4}}, indent=2) + "\n",
            encoding="utf-8",
        )
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
            overlay = make_armor_overlay(material, layer)
            if layer == "humanoid_baby":
                baby_overlay = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
                baby_overlay.paste(overlay, (0, 0))
                baby_overlay.paste(overlay, (0, 32))
                overlay = baby_overlay
            overlay_path = ROOT / "textures/entity/equipment" / layer / f"{material}_ornament.png"
            overlay.save(overlay_path)
    make_catalyst().save(ROOT / "textures/item" / "celestial_catalyst.png")


if __name__ == "__main__":
    main()
