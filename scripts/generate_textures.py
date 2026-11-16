#!/usr/bin/env python3
"""Generate only crisp 32x32 PNG textures for Celestial Dominion."""
from pathlib import Path
from PIL import Image, ImageDraw
import random

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/assets/celestial_dominion"
random.seed(2603)
PALETTES = {
    "solar": ((91,16,24),(201,63,24),(255,174,35),(255,244,180)),
    "abyssal": ((15,13,31),(67,39,104),(38,218,231),(191,250,255)),
    "celestial": ((232,237,255),(245,193,72),(129,74,194),(255,255,255)),
}
NAMES = [
    "solar_ingot","abyssal_ingot","celestial_ingot","solar_smithing_template","abyssal_smithing_template",
    "celestial_catalyst","solar_ore","abyssal_ore","celestial_ore","solar_sword","abyssal_sword","celestial_sword",
    "solar_helmet","solar_chestplate","solar_leggings","solar_boots","abyssal_helmet","abyssal_chestplate",
    "abyssal_leggings","abyssal_boots","celestial_helmet","celestial_chestplate","celestial_leggings","celestial_boots"
]

def make_texture(name):
    key = "celestial" if name.startswith("celestial") else "solar" if name.startswith("solar") else "abyssal"
    c0,c1,c2,c3 = PALETTES[key]
    image = Image.new("RGBA",(32,32),(0,0,0,0))
    d = ImageDraw.Draw(image)
    if name.endswith("_ore"):
        d.rectangle((0,0,31,31),fill=(48,45,49,255))
        for _ in range(42):
            x,y=random.randrange(32),random.randrange(32)
            c=random.choice((c1,c2,c3))
            d.rectangle((x,y,min(31,x+1),min(31,y+1)),fill=(*c,255))
        d.rectangle((2,2,29,29),outline=(*c0,255))
    elif name.endswith("_ingot") or "template" in name or name.endswith("_catalyst"):
        d.polygon([(4,9),(23,5),(29,12),(26,24),(8,27),(3,19)],fill=(*c1,255),outline=(*c3,255))
        d.line((7,12,22,9,26,13),fill=(*c3,255),width=2)
        d.line((8,22,23,20),fill=(*c0,255),width=2)
        if "template" in name or name.endswith("_catalyst"):
            d.rectangle((13,13,18,18),fill=(*c2,255))
    elif name.endswith("_sword"):
        d.polygon([(22,2),(27,7),(13,23),(9,19)],fill=(*c3,255),outline=(*c0,255))
        d.line((9,19,5,27),fill=(*c1,255),width=3)
        d.line((7,17,15,25),fill=(*c2,255),width=3)
        d.point((24,4),fill=(255,255,255,255))
    else:
        d.polygon([(9,3),(16,6),(23,3),(28,9),(25,15),(27,28),(16,30),(5,28),(7,15),(4,9)],
                  fill=(*c0,255),outline=(*c3,255))
        d.polygon([(9,8),(16,11),(23,8),(21,15),(16,18),(11,15)],fill=(*c1,255))
        d.line((16,7,16,27),fill=(*c2,255),width=2)
        d.point((16,13),fill=(*c3,255))
        d.line((7,23,12,26,20,26,25,23),fill=(*c2,255),width=2)
    return image

def main():
    for name in NAMES:
        image = make_texture(name)
        if name.endswith("_ore"):
            out = ROOT / "textures/block" / f"{name}.png"
        else:
            out = ROOT / "textures/item" / f"{name}.png"
        out.parent.mkdir(parents=True,exist_ok=True)
        image.save(out,"PNG",optimize=False)
    # Armor UV layers are generated once per material, not overwritten by each inventory icon.
    for material in PALETTES:
        layer1 = make_texture(f"{material}_chestplate")
        layer2 = make_texture(f"{material}_leggings")
        for layer, image in ((1, layer1), (2, layer2)):
            armor = ROOT / "textures/models/armor" / f"{material}_layer_{layer}.png"
            armor.parent.mkdir(parents=True,exist_ok=True)
            image.save(armor,"PNG",optimize=False)

if __name__ == "__main__":
    main()
