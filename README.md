# Celestial Dominion

Minecraft Java Edition **26.3** / NeoForge **26.3.0.103** / Java **25**.

## Build
Install JDK 25 and Gradle 9.2.1, then generate assets and build:

```sh
python -m pip install pillow
python scripts/generate_textures.py
python scripts/generate_relic_assets.py
python scripts/test_assets.py
./gradlew build
```

The jar is written to `build/libs/`. GitHub Actions installs Pillow, generates the textures, builds the project and uploads the jar as an Actions artifact.

## Current gameplay
- Solar Overlord, Abyssal Sovereign and Celestial Ascendant armor, swords, pickaxes, axes, shovels, hoes and Omnitools.
- Solar: offence-first armor and sword profile; strong Strength and a fiery retaliation aura.
- Abyssal: defence-first armor, high toughness/knockback resistance, regeneration and crowd control; its sword trades raw damage for control.
- Celestial: combines both paths, with the strongest armor and the combined sword abilities.
- Solar dash/shockwave and Abyssal pull/freeze/heal abilities; Celestial sword combines both.
- Full-set buffs and flight for the fusion armor.
- Three custom ore blocks, ingots, smithing-template/catalyst items, distinct vanilla-style pixel-art tool silhouettes and material-themed visual effects.

## World generation and progression
- Solar Ore: ultra-rare veins in Overworld deepslate near bedrock (Y -63 to -48).
- Abyssal Ore: ultra-rare veins in Nether base stone (Y 4 to 24).
- Celestial Ore: exceptionally rare veins in End stone (Y 4 to 22).
- Each ore drops its matching ingot. Silk-touch/fortune-specific loot behavior can be added as a balancing pass.
- Solar/Abyssal smithing: Netherite equipment + matching custom template + matching ingot. Templates are duplicated from a Netherite Upgrade Template, seven diamonds, one Netherite Ingot and one matching rare ingot (produces two).
- Celestial Catalyst: crafted from four Solar Ingots, four Abyssal Ingots and one Celestial Ingot. Celestial fusion: Solar equipment + matching Abyssal equipment in the template slot + Celestial Catalyst in the addition slot.

## Tool progression
- Solar tools and the Solar Omnitool are smithing upgrades from Netherite using the Solar Smithing Template and Solar Ingot.
- Abyssal tools and the Abyssal Omnitool are smithing upgrades from Netherite using the Abyssal Smithing Template and Abyssal Ingot.
- Celestial tools are the final fusion: the matching Solar tool is the base, the matching Abyssal tool occupies the template slot, and the Celestial Catalyst is the addition.
- Each Omnitool combines pickaxe, axe, shovel and hoe mining rules and supports log stripping, copper scraping/unwaxing, dirt pathing, campfire dousing and tilling. It is intentionally a single-block tool: no area mining or tick-driven particles.
- Tools and swords use Minecraft's vanilla 2D handheld item models and original 32x32 pixel-art sprites. Pickaxe, axe, shovel, hoe, Omnitool and sword silhouettes stay recognizable at inventory scale; each material adds a restrained signature palette and a few lore-specific pixels. Vanilla display transforms are inherited instead of enlarging custom geometry. Material motion is supplied by the low-frequency held-item aura and animated armor wings.
- Held relics emit at most two tiny material particles per hand every five ticks on the server; no per-frame Java renderer or shader is used.
- Each armor set now uses a base plate texture plus a transparent ornamental overlay, with distinct Solar sun-forging, Abyssal rift and Celestial star-map motifs. Each set also includes material-themed animated 3D wings through Minecraft's built-in `WINGS` equipment layer. Ore blocks remain full 3D block models; ingots, templates and the catalyst use vanilla generated-item models with original flat pixel-art sprites.

## Automated asset tests
`docs/PLAYTEST_CHECKLIST.md` contains repeatable in-game checks for held models, animated wings, combat roles, tools, and ore generation.

`python scripts/test_assets.py` parses every resource JSON, verifies all 18 tool/weapon sprites use vanilla handheld models and all six ingredients use vanilla generated-item models, checks texture dimensions and armor/wing atlas dimensions, and confirms all 15 tool smithing recipes exist. GitHub Actions then launches the NeoForge client under Xvfb, waits for resource reload and texture-atlas creation to settle, and fails on model-bake, missing-texture, missing-model or resource-loading errors.

## Build caveat
The project includes data-driven world generation, loot tables and all 15 smithing transformations. CI now performs a headless client resource-reload smoke test in addition to compilation. This catches model-bake errors that a Java compile and JSON parser cannot see, but it does not replace a human visual/combat playtest.
- Solar full set retaliates by igniting attackers.
- Abyssal and Celestial full sets slow/freeze nearby living entities.
- Abyssal and Celestial full sets cancel player knockback.
- Celestial flight is enabled without forcing the player to remain airborne.
- Armor durability comes from the large ArmorMaterial durability multipliers rather than a small fixed override. GitHub Actions runs the Java 25 / NeoForge 26.3 build and asset regression checks. A successful CI build still needs to be followed by an in-game client playtest for model transforms, armor wings and combat feel.
