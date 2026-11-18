#!/usr/bin/env python3
"""Generate native, low-overhead animated tool icons for Celestial Dominion.

Minecraft animates these PNG sheets itself. No Java render loop, shaders, or
per-tick particle emitter is required. Each texture is eight 32x32 frames.
"""
from pathlib import Path
import json
import math
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/assets/celestial_dominion/textures/item"
PALETTES = {
    "solar": ((53, 13, 15, 255), (168, 43, 18, 255), (255, 111, 24, 255), (255, 205, 75, 255), (255, 246, 188, 255)),
    "abyssal": ((8, 9, 25, 255), (40, 31, 77, 255), (102, 60, 160, 255), (32, 225, 224, 255), (198, 255, 255, 255)),
    "celestial": ((42, 36, 78, 255), (142, 135, 190, 255), (225, 218, 245, 255), (255, 203, 91, 255), (255, 255, 239, 255)),
}
TOOLS = ("pickaxe", "axe", "shovel", "hoe", "multitool")


def polygon(draw, points, fill, outline):
    draw.polygon(points, fill=fill, outline=outline)


def draw_tool(material, kind, frame):
    shadow, base, mid, accent, glow = PALETTES[material]
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pulse = (frame % 4)
    # Shared forged haft; each tool has a deliberately different head silhouette.
    d.line((9, 27, 23, 9), fill=shadow, width=5)
    d.line((9, 26, 22, 9), fill=base, width=3)
    d.line((10, 24, 21, 10), fill=glow, width=1)
    if kind == "pickaxe":
        polygon(d, [(4, 9), (8, 5), (15, 8), (24, 2), (29, 6), (19, 14), (12, 12), (7, 14)], mid, glow)
        d.line((7, 9, 14, 10, 24, 5), fill=accent, width=2)
    elif kind == "axe":
        polygon(d, [(7, 4), (17, 3), (26, 7), (27, 14), (21, 17), (17, 12), (12, 10), (8, 14), (5, 10)], mid, glow)
        polygon(d, [(8, 6), (17, 5), (23, 8), (18, 10), (12, 9)], accent, glow)
    elif kind == "shovel":
        polygon(d, [(19, 3), (27, 6), (24, 17), (17, 21), (12, 16), (14, 8)], mid, glow)
        d.line((17, 7, 22, 9, 20, 16), fill=accent, width=2)
    elif kind == "hoe":
        d.line((7, 8, 24, 25), fill=base, width=4)
        polygon(d, [(3, 6), (6, 3), (15, 11), (12, 14)], mid, glow)
        polygon(d, [(5, 3), (13, 7), (10, 11), (3, 7)], accent, glow)
    else:
        # A four-pronged relic head: pick teeth, axe blade, spade point and tilling edge.
        polygon(d, [(3, 5), (10, 2), (15, 7), (21, 1), (29, 5), (26, 13),
                    (21, 12), (18, 19), (12, 14), (7, 17), (4, 11)], mid, glow)
        d.line((6, 7, 12, 10, 19, 6, 25, 8), fill=accent, width=2)
        d.point((17, 10), fill=glow)
    # Material-specific animated energy, kept inside the icon (no runtime particles).
    if material == "solar":
        for i in range(3):
            x = 5 + ((frame * 3 + i * 9) % 23)
            y = 3 + ((frame * 2 + i * 7) % 9)
            d.point((x, y), fill=glow if i == pulse % 3 else accent)
        d.line((13, 20, 15, 17, 17, 19), fill=accent, width=1)
    elif material == "abyssal":
        cx, cy = 17, 9
        r = 2 + (frame % 3)
        d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=accent, width=1)
        d.point((cx, cy), fill=glow)
        d.line((4, 18 + frame % 3, 7, 15 + frame % 3), fill=accent, width=1)
    else:
        cx, cy = 17, 8
        d.line((cx, cy-4, cx, cy+4), fill=glow, width=1)
        d.line((cx-4, cy, cx+4, cy), fill=glow, width=1)
        d.point((5 + frame * 3 % 22, 4 + frame * 5 % 12), fill=accent)
    # Small animated highlight on the grip pommel.
    d.ellipse((7, 24, 11, 28), fill=accent if frame % 2 else glow, outline=glow)
    return im


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for material in PALETTES:
        for kind in TOOLS:
            sheet = Image.new("RGBA", (32, 32 * 8), (0, 0, 0, 0))
            for frame in range(8):
                sheet.paste(draw_tool(material, kind, frame), (0, frame * 32))
            stem = f"{material}_{kind}"
            sheet.save(ROOT / f"{stem}.png", optimize=True)
            (ROOT / f"{stem}.png.mcmeta").write_text(json.dumps({
                "animation": {"width": 32, "height": 32, "frametime": 3, "interpolate": True}
            }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
