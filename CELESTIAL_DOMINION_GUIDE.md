# Celestial Dominion — player guide

Celestial Dominion is a three-stage endgame progression. The item registry IDs stay stable, but the in-game names and tooltips now describe the relics and their abilities.

## Finding the items

- Open the **Celestial Dominion** creative tab.
- In JEI, search `@celestial` to filter the mod. Search `&celestial_dominion:` to search registry IDs if your JEI version supports the registry-ID prefix.
- Every item is explicitly added to the custom tab. JEI does not need to be a required dependency of this mod.

## Ore locations

| Ore | Dimension | Replaceable block | Height | Generation |
|---|---|---|---:|---|
| Solar Ore | Overworld | Deepslate | Y -63 to -48 | Rare, small veins |
| Abyssal Ore | Nether | Nether base stone | Y 4 to 24 | Very rare, small veins |
| Celestial Ore | The End | End Stone | Y 4 to 22 | Extremely rare, tiny veins |

**Important:** natural world generation only runs when a chunk is first generated. Updating the mod does not retroactively populate chunks you have already explored. Test in newly generated terrain or a new world.

### Operator test commands

These commands are for a creative/operator test world. Run each in the matching dimension:

```mcfunction
/place feature celestial_dominion:solar_ore ~ ~ ~
/place feature celestial_dominion:abyssal_ore ~ ~ ~
/place feature celestial_dominion:celestial_ore ~ ~ ~
```

The placed feature includes a rarity filter, so a single `/place feature` attempt can legitimately place nothing. Repeat the command if you are testing the feature manually. These commands test feature placement; they do not prove that a previously generated chunk was retroactively populated.

You can also verify that the blocks themselves exist independently of world generation:

```mcfunction
/setblock ~ ~ ~ celestial_dominion:solar_ore
/setblock ~ ~ ~ celestial_dominion:abyssal_ore
/setblock ~ ~ ~ celestial_dominion:celestial_ore
```

## Progression

1. Mine Solar Ore in deep Overworld deepslate and obtain Solarite Ingots.
2. Duplicate the Solar Smithing Template using its recipe, then upgrade Netherite gear into Solar Regalia.
3. Find Abyssal Ore in the Nether, refine it into Abyssal Ingots, and duplicate the Abyssal Smithing Template.
4. Upgrade Netherite gear into Abyssal Regalia.
5. Find Celestial Ore in the End and refine it into Celestial Ingots.
6. Craft the Celestial Catalyst. Use the Abyssal piece as the smithing template, the matching Solar piece as the base, and the Catalyst as the addition to ascend that piece to Celestial gear.

The Celestial sword and spear follow the same final-stage smithing progression as the armor. Solar and Abyssal spears are upgraded from Netherite Spears with their matching smithing templates and ingots; the Celestial Spear is forged by combining the Solar Spear, Abyssal Spear template, and Celestial Catalyst.

## Set blessings

### Solar Regalia — First Dawn

Wear all four Solar armor pieces for Fire Resistance, Strength III, Haste II, and Speed II. Living attackers that damage you are set on fire. Solar armor is the aggressive, mobility-focused path.

**Dawnrender — Solar Rupture:** right-click to lunge forward and strike nearby enemies with a fiery area burst. Targets take 13 hearts of damage, burn for 8 seconds, and are knocked back. Cooldown: 35 seconds.

### Abyssal Regalia — Drowned King

Wear all four Abyssal armor pieces for Resistance III, Regeneration II, and Absorption III. Nearby living enemies are slowed and frozen; the wearer is immune to knockback. Abyssal armor is the control and survival path.

**Eventide — Event Horizon:** right-click to pull nearby enemies inward, deal 11 magic damage, freeze them for 9 seconds, and restore 5 hearts. Cooldown: 35 seconds.

### Celestial Ascendant — Firmament

Wear all four Celestial pieces to combine the Solar and Abyssal blessings and gain flight. The full set also grants Strength IV, Resistance IV, Regeneration II, Absorption V, Fire Resistance, Haste II, and Speed II. Nearby enemies are frozen, attackers are scorched, and knockback is prevented.

**Genesis — Genesis:** right-click to unleash both Solar Rupture and Event Horizon together and restore 8 hearts. Cooldown: 25 seconds.

## Notes

- Armor and sword abilities are server-side gameplay effects; they do not require shaders.
- The custom armor textures are 64x32 atlases for the humanoid, leggings, and baby-humanoid equipment layers. Item icons are separate 32x32 sprites.
- Solar and Abyssal armor/tool durability is substantially increased over the previous release. Celestial armor, swords, tools, multitool and spear carry Minecraft's native Unbreakable component.
- The Celestial set is intentionally the final, extremely powerful tier. It is not balanced as a PvP equipment set.
