# Celestial Dominion playtest checklist

Run the automated checks before launching:

```sh
python -m pip install pillow
python scripts/generate_textures.py
python scripts/generate_relic_assets.py
python scripts/test_assets.py
./gradlew build
```

The Python test suite validates resource JSON, vanilla item-model parents, sprite dimensions, armor/wing atlases, animation metadata, recipe presence and the intended stat ordering. It cannot validate the visual quality of the sprites or combat in a running client.

## Client visual checks

1. Launch Minecraft 26.3 with the built JAR and NeoForge 26.3.
2. Press `F3 + T` once after entering a world to reload generated resources.
3. Give yourself the weapons and tools:

```mcfunction
/give @p celestial_dominion:solar_sword
/give @p celestial_dominion:abyssal_sword
/give @p celestial_dominion:celestial_sword
/give @p celestial_dominion:solar_pickaxe
/give @p celestial_dominion:solar_axe
/give @p celestial_dominion:solar_shovel
/give @p celestial_dominion:solar_hoe
/give @p celestial_dominion:solar_multitool
/give @p celestial_dominion:abyssal_pickaxe
/give @p celestial_dominion:abyssal_axe
/give @p celestial_dominion:abyssal_shovel
/give @p celestial_dominion:abyssal_hoe
/give @p celestial_dominion:abyssal_multitool
/give @p celestial_dominion:celestial_pickaxe
/give @p celestial_dominion:celestial_axe
/give @p celestial_dominion:celestial_shovel
/give @p celestial_dominion:celestial_hoe
/give @p celestial_dominion:celestial_multitool
```

4. Check first-person, third-person front/back, offhand, GUI and dropped-item views. Each sprite must read immediately as its intended vanilla tool or weapon at normal inventory scale: pickaxe head, axe blade, shovel spade, hoe tine, sword blade and Omnitool head. Confirm vanilla-sized transforms and no clipping.
5. Hold each tier for at least 10 seconds. Check the material-specific palette and restrained Solar ember, Abyssal rift and Celestial star-map details without losing the underlying tool silhouette. Verify material-colored aura particles in both main hand and offhand. Item sprites are intentionally static; armor wings use native texture animation.
6. Equip each full armor set. Check the pixel-art base armor UVs and transparent ornamental overlay, then inspect the material-specific animated wings from behind and from the side. Also check a normal and slim player skin.
7. Test baby humanoid armor rendering separately; the baby atlas is a separate resource path and should not break adult armor.

## Combat role checks

- **Solar:** equip the full set and verify Fire Resistance, Strength III, Haste II and Speed II. Hit a nearby hostile mob and verify fiery retaliation. The sword should be the highest-damage non-Celestial path.
- **Abyssal:** equip the full set and verify Resistance III, Regeneration II and Absorption III. Check knockback resistance and the nearby slow/freeze aura. Its sword has lower raw damage than Solar but a stronger control/heal ability.
- **Celestial:** equip the full set and verify flight plus both Solar and Abyssal effects. The sword should execute both abilities and use the shorter fusion cooldown.

Sword ability cooldowns are 35 seconds for Solar/Abyssal and 25 seconds for Celestial. Compare damage on the same target type and difficulty; do not compare hits on differently armored mobs.

## Tool and Omnitool checks

Use a fresh survival world or a test area with expendable blocks.

- Pickaxe: stone, deepslate, diamond ore and ancient debris; confirm expected drops.
- Axe: logs, stripped logs and copper oxidation/wax states.
- Shovel: dirt path, campfire dousing and shovel-minable blocks.
- Hoe: dirt/coarse dirt/rooted dirt and crop tilling.
- Omnitool: repeat each of the above with one item; confirm it never performs area mining and loses durability normally.

## World generation checks

Run each feature in its intended dimension:

```mcfunction
/place feature celestial_dominion:solar_ore ~ ~ ~
/place feature celestial_dominion:abyssal_ore ~ ~ ~
/place feature celestial_dominion:celestial_ore ~ ~ ~
```

- Solar Ore: Overworld.
- Abyssal Ore: Nether.
- Celestial Ore: End.

Natural generation is separate from the feature-placement test. To test natural generation, create fresh chunks in each dimension and inspect the configured Y ranges; existing chunks are not retroactively populated.

## Regression record

When reporting a visual or balance issue, include:
- Minecraft and NeoForge versions
- Client log and latest.log
- Which material, item, hand and view mode were used
- Whether the issue appears in a fresh world
- A screenshot of the held item or worn armor, preferably with F3 hidden and a second screenshot with F3 visible
