# Celestial Dominion

Minecraft Java Edition **26.3** / NeoForge **26.3.0.101** / Java **25**.

## Build
Install JDK 25 and Gradle 9.2.1, then run:

```sh
./gradlew build
```

The jar is written to `build/libs/`. GitHub Actions installs Pillow, generates the textures, builds the project and uploads the jar as an Actions artifact.

## Current gameplay
- Solar Overlord, Abyssal Sovereign and Celestial Ascendant armor and swords.
- Distinct armor defense/toughness/knockback resistance and sword damage/speed.
- Solar dash/shockwave and Abyssal pull/freeze/heal abilities; Celestial sword combines both.
- Full-set buffs and flight for the fusion armor.
- Three custom ore blocks, ingots, smithing-template/catalyst items and 32x32 generated item/block textures.

## World generation and progression
- Solar Ore: ultra-rare veins in Overworld deepslate near bedrock (Y -63 to -48).
- Abyssal Ore: ultra-rare veins in Nether base stone (Y 4 to 24).
- Celestial Ore: exceptionally rare veins in End stone (Y 4 to 22).
- Each ore drops its matching ingot. Silk-touch/fortune-specific loot behavior can be added as a balancing pass.
- Solar/Abyssal smithing: Netherite equipment + matching custom template + matching ingot. Templates are duplicated from a Netherite Upgrade Template, seven diamonds, one Netherite Ingot and one matching rare ingot (produces two).
- Celestial Catalyst: crafted from four Solar Ingots, four Abyssal Ingots and one Celestial Ingot. Celestial fusion: Solar equipment + matching Abyssal equipment in the template slot + Celestial Catalyst in the addition slot.

## Build caveat
The project includes data-driven world generation, loot tables and all 15 smithing transformations.
- Solar full set retaliates by igniting attackers.
- Abyssal and Celestial full sets slow/freeze nearby living entities.
- Abyssal and Celestial full sets cancel player knockback.
- Celestial flight is enabled without forcing the player to remain airborne.
- Armor durability comes from the large ArmorMaterial durability multipliers rather than a small fixed override. It still needs a real Java 25 / NeoForge 26.3 build and in-game validation; no successful compile is claimed from this environment. GitHub Actions performs that build after push.
