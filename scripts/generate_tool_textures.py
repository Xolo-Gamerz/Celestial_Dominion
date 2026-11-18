#!/usr/bin/env python3
"""Generate animated 64px pixel-art tool relics.

The vertical PNG sheets and .mcmeta are consumed by Minecraft's native texture
animation system. There is no per-frame Java renderer, shader, or particle loop.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/assets/celestial_dominion/textures/item"
PALETTES = {
    "solar": {
        "outline": (38, 12, 16, 255), "dark": (91, 25, 19, 255),
        "metal": (179, 61, 24, 255), "light": (255, 137, 35, 255),
        "gold": (255, 205, 84, 255), "shine": (255, 247, 191, 255),
    },
    "abyssal": {
        "outline": (8, 8, 24, 255), "dark": (31, 26, 64, 255),
        "metal": (74, 55, 125, 255), "light": (137, 89, 207, 255),
        "gold": (53, 224, 222, 255), "shine": (206, 255, 255, 255),
    },
    "celestial": {
        "outline": (24, 26, 52, 255), "dark": (70, 76, 116, 255),
        "metal": (151, 160, 194, 255), "light": (218, 224, 245, 255),
        "gold": (255, 207, 103, 255), "shine": (255, 255, 244, 255),
    },
}
KINDS = ("pickaxe", "axe", "shovel", "hoe", "multitool")


def poly(draw, points, fill, outline, width=1):
    draw.polygon(points, fill=fill)
    draw.line(points + [points[0]], fill=outline, width=width, joint="curve")


def line(draw, points, fill, width=1):
    draw.line(points, fill=fill, width=width, joint="curve")


def draw_head(draw, kind, p, frame):
    o, d, m, h, g, w = (p[k] for k in ("outline", "dark", "metal", "light", "gold", "shine"))
    if kind == "pickaxe":
        poly(draw, [(5,17),(12,10),(24,14),(47,4),(58,10),(43,23),(29,20),(17,27),(9,24)], m, o, 3)
        poly(draw, [(8,17),(14,13),(25,17),(47,8),(53,11),(41,18),(28,17),(17,23)], h, g)
        line(draw, [(13,17),(24,19),(45,11)], w, 2)
        poly(draw, [(46,5),(58,10),(43,23),(45,16)], g, o)
    elif kind == "axe":
        poly(draw, [(17,8),(34,8),(50,13),(59,22),(57,36),(48,43),(39,34),(30,27),(21,29),(13,38),(7,31),(10,19)], m, o, 3)
        poly(draw, [(18,12),(34,12),(49,17),(54,23),(49,33),(42,30),(33,22),(21,22),(13,30)], h, g)
        line(draw, [(17,17),(32,17),(47,22)], w, 2)
        poly(draw, [(49,17),(58,22),(55,34),(48,40),(45,30)], g, o)
    elif kind == "shovel":
        poly(draw, [(24,7),(42,7),(52,18),(49,39),(33,51),(17,39),(14,18)], m, o, 3)
        poly(draw, [(27,12),(40,12),(47,20),(44,36),(33,44),(22,36),(19,20)], h, g)
        poly(draw, [(28,17),(38,17),(41,25),(33,35),(25,25)], d, o)
        line(draw, [(25,20),(33,27),(41,20)], w, 2)
    elif kind == "hoe":
        poly(draw, [(8,9),(17,5),(27,13),(36,9),(48,12),(57,20),(51,28),(39,22),(30,26),(20,18),(12,20)], m, o, 3)
        poly(draw, [(13,10),(18,9),(28,16),(38,13),(48,16),(53,20),(49,23),(38,18),(29,22),(19,15)], h, g)
        line(draw, [(17,12),(28,19),(39,16),(49,20)], w, 2)
        poly(draw, [(8,9),(17,5),(21,12),(13,18)], g, o)
    else:
        # Four-edged relic head: pick teeth, axe crescent, spade point and hoe wings.
        poly(draw, [(5,12),(16,5),(26,12),(32,3),(39,12),(53,6),(61,16),(55,27),
                    (47,25),(43,40),(32,34),(21,42),(18,29),(8,31),(3,21)], m, o, 3)
        poly(draw, [(10,14),(17,10),(27,17),(32,10),(39,18),(51,11),(56,17),
                    (50,23),(43,21),(39,32),(32,27),(23,34),(21,24),(11,25),(8,19)], h, g)
        line(draw, [(13,17),(23,21),(32,15),(41,22),(51,17)], w, 2)
        poly(draw, [(32,9),(39,18),(32,27),(25,18)], g, o)


def draw_frame(material, kind, frame):
    p = PALETTES[material]
    o, d, m, h, g, w = (p[k] for k in ("outline", "dark", "metal", "light", "gold", "shine"))
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)

    # Haft, pommel, grip wraps and forged collar.
    line(dr, [(17,58),(49,16)], o, 10)
    line(dr, [(18,56),(48,17)], d, 7)
    line(dr, [(19,54),(47,18)], m, 3)
    line(dr, [(20,53),(45,20)], h, 1)
    for i in range(4):
        x, y = 20 + i * 5, 53 - i * 6
        line(dr, [(x-3,y+3),(x+2,y-2)], g, 2)
    poly(dr, [(13,57),(18,53),(23,57),(21,63),(15,63)], m, o, 2)
    dr.point((18,58), fill=w)
    draw_head(dr, kind, p, frame)

    # A different animated signature for each tier.
    if material == "solar":
        # Flame tongues flicker around the head; a bright ember travels along the edge.
        shift = frame % 4
        for x, y in ((7,5),(54,2),(57,35),(5,34)):
            poly(dr, [(x,y+8),(x+2,y+3+shift),(x+5,y+7),(x+3,y+12)], h, g)
            dr.point((x+3,y+7), fill=w if frame % 2 else g)
        ex = 13 + ((frame * 7) % 38)
        ey = 13 + ((frame * 3) % 9)
        dr.rectangle((ex,ey,ex+2,ey+2), fill=w)
    elif material == "abyssal":
        # A slow cyan rift pulse, not particles.
        radius = 4 + (frame % 4)
        dr.ellipse((31-radius, 15-radius, 31+radius, 15+radius), outline=g, width=2)
        dr.ellipse((29,13,33,17), fill=w)
        line(dr, [(7,43),(12,38),(16,40)], g, 2)
        line(dr, [(48,47),(53,42),(57,44)], h, 2)
    else:
        # A celestial sigil and rotating star glints.
        dr.ellipse((26,9,38,21), outline=g, width=1)
        dr.ellipse((29,12,35,18), outline=w, width=1)
        for i in range(4):
            x = 8 + ((frame * 9 + i * 13) % 49)
            y = 5 + ((frame * 5 + i * 11) % 47)
            line(dr, [(x-2,y),(x+2,y)], w, 1)
            line(dr, [(x,y-2),(x,y+2)], g, 1)

    # Shared gem at the collar, colored by material.
    poly(dr, [(44,28),(48,25),(52,28),(50,34),(46,34)], g, o, 1)
    dr.point((48,29), fill=w)
    return im


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for material in PALETTES:
        for kind in KINDS:
            sheet = Image.new("RGBA", (64, 64 * 8), (0, 0, 0, 0))
            for frame in range(8):
                sheet.paste(draw_frame(material, kind, frame), (0, frame * 64))
            filename = f"{material}_{kind}.png"
            sheet.save(ROOT / filename, optimize=True)
            metadata = {"animation": {"width": 64, "height": 64, "frametime": 3, "interpolate": False}}
            (ROOT / f"{filename}.mcmeta").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
