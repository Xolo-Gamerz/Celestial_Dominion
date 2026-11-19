package dev.xolo.celestialdominion.content;

import dev.xolo.celestialdominion.CelestialDominion;
import dev.xolo.celestialdominion.item.AbilitySwordItem;
import dev.xolo.celestialdominion.item.CelestialMultitoolItem;
import net.minecraft.util.Unit;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import net.minecraft.core.HolderSet;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.component.Tool;
import net.minecraft.world.item.component.AttackRange;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModItems {
    public static final DeferredRegister.Items ITEMS =
            DeferredRegister.createItems(CelestialDominion.MOD_ID);

    private static final TagKey<Item> REPAIR_TAG = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(CelestialDominion.MOD_ID, "repairs_celestial_gear")
    );
    private static final TagKey<Block> INCORRECT_FOR_CELESTIAL_TOOL = TagKey.create(
            Registries.BLOCK,
            Identifier.fromNamespaceAndPath(CelestialDominion.MOD_ID, "incorrect_for_celestial_tool")
    );

    private static ResourceKey<EquipmentAsset> asset(String name) {
        return ResourceKey.create(
                EquipmentAssets.ROOT_ID,
                Identifier.fromNamespaceAndPath(CelestialDominion.MOD_ID, name)
        );
    }

    private static ArmorMaterial armor(
            String assetName, int durability, int helmet, int chest, int legs, int boots,
            float toughness, float knockbackResistance
    ) {
        Map<ArmorType, Integer> defense = new EnumMap<>(ArmorType.class);
        defense.put(ArmorType.HELMET, helmet);
        defense.put(ArmorType.CHESTPLATE, chest);
        defense.put(ArmorType.LEGGINGS, legs);
        defense.put(ArmorType.BOOTS, boots);
        defense.put(ArmorType.BODY, chest);
        return new ArmorMaterial(durability, defense, 30, SoundEvents.ARMOR_EQUIP_NETHERITE,
                toughness, knockbackResistance, REPAIR_TAG, asset(assetName));
    }

    private static final ArmorMaterial SOLAR_ARMOR = armor("solar", 320, 9, 15, 11, 8, 2.5F, 0.05F);
    private static final ArmorMaterial ABYSSAL_ARMOR = armor("abyssal", 480, 13, 21, 16, 12, 4.0F, 0.20F);
    private static final ArmorMaterial CELESTIAL_ARMOR = armor("celestial", 640, 16, 26, 20, 16, 5.0F, 0.25F);

    private static final ToolMaterial SOLAR_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 24000, 16.0F, 8.0F, 30, REPAIR_TAG);
    private static final ToolMaterial ABYSSAL_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 36000, 18.0F, 2.0F, 30, REPAIR_TAG);
    private static final ToolMaterial CELESTIAL_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 48000, 22.0F, 12.0F, 40, REPAIR_TAG);

    // Mining tools share each tier's speed, durability and repair material, but not sword-level damage.
    private static final ToolMaterial SOLAR_MINING_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 12000, 16.0F, 5.0F, 30, REPAIR_TAG);
    private static final ToolMaterial ABYSSAL_MINING_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 18000, 18.0F, 2.0F, 30, REPAIR_TAG);
    private static final ToolMaterial CELESTIAL_MINING_TOOL = new ToolMaterial(
            INCORRECT_FOR_CELESTIAL_TOOL, 48000, 22.0F, 6.0F, 40, REPAIR_TAG);

    public static final DeferredItem<Item> SOLAR_ORE_ITEM = ITEMS.registerItem(
            "solar_ore", properties -> new BlockItem(ModBlocks.SOLAR_ORE.get(), properties));
    public static final DeferredItem<Item> ABYSSAL_ORE_ITEM = ITEMS.registerItem(
            "abyssal_ore", properties -> new BlockItem(ModBlocks.ABYSSAL_ORE.get(), properties));
    public static final DeferredItem<Item> CELESTIAL_ORE_ITEM = ITEMS.registerItem(
            "celestial_ore", properties -> new BlockItem(ModBlocks.CELESTIAL_ORE.get(), properties));

    public static final DeferredItem<Item> SOLAR_INGOT = ITEMS.registerSimpleItem("solar_ingot");
    public static final DeferredItem<Item> ABYSSAL_INGOT = ITEMS.registerSimpleItem("abyssal_ingot");
    public static final DeferredItem<Item> CELESTIAL_INGOT = ITEMS.registerSimpleItem("celestial_ingot");
    public static final DeferredItem<Item> SOLAR_TEMPLATE = ITEMS.registerSimpleItem("solar_smithing_template");
    public static final DeferredItem<Item> ABYSSAL_TEMPLATE = ITEMS.registerSimpleItem("abyssal_smithing_template");
    public static final DeferredItem<Item> CELESTIAL_CATALYST = ITEMS.registerSimpleItem("celestial_catalyst");

    public static final DeferredItem<Item> SOLAR_HELMET = armorItem("solar_helmet", SOLAR_ARMOR, ArmorType.HELMET);
    public static final DeferredItem<Item> SOLAR_CHESTPLATE = armorItem("solar_chestplate", SOLAR_ARMOR, ArmorType.CHESTPLATE);
    public static final DeferredItem<Item> SOLAR_LEGGINGS = armorItem("solar_leggings", SOLAR_ARMOR, ArmorType.LEGGINGS);
    public static final DeferredItem<Item> SOLAR_BOOTS = armorItem("solar_boots", SOLAR_ARMOR, ArmorType.BOOTS);
    public static final DeferredItem<Item> ABYSSAL_HELMET = armorItem("abyssal_helmet", ABYSSAL_ARMOR, ArmorType.HELMET);
    public static final DeferredItem<Item> ABYSSAL_CHESTPLATE = armorItem("abyssal_chestplate", ABYSSAL_ARMOR, ArmorType.CHESTPLATE);
    public static final DeferredItem<Item> ABYSSAL_LEGGINGS = armorItem("abyssal_leggings", ABYSSAL_ARMOR, ArmorType.LEGGINGS);
    public static final DeferredItem<Item> ABYSSAL_BOOTS = armorItem("abyssal_boots", ABYSSAL_ARMOR, ArmorType.BOOTS);
    public static final DeferredItem<Item> CELESTIAL_HELMET = armorItem("celestial_helmet", CELESTIAL_ARMOR, ArmorType.HELMET);
    public static final DeferredItem<Item> CELESTIAL_CHESTPLATE = armorItem("celestial_chestplate", CELESTIAL_ARMOR, ArmorType.CHESTPLATE);
    public static final DeferredItem<Item> CELESTIAL_LEGGINGS = armorItem("celestial_leggings", CELESTIAL_ARMOR, ArmorType.LEGGINGS);
    public static final DeferredItem<Item> CELESTIAL_BOOTS = armorItem("celestial_boots", CELESTIAL_ARMOR, ArmorType.BOOTS);

    public static final DeferredItem<Item> SOLAR_SWORD = ITEMS.registerItem("solar_sword",
            p -> new AbilitySwordItem(p.sword(SOLAR_TOOL, 10.0F, -1.2F), AbilitySwordItem.Mode.SOLAR));
    public static final DeferredItem<Item> ABYSSAL_SWORD = ITEMS.registerItem("abyssal_sword",
            p -> new AbilitySwordItem(p.sword(ABYSSAL_TOOL, 12.0F, -1.6F), AbilitySwordItem.Mode.ABYSSAL));
    public static final DeferredItem<Item> CELESTIAL_SWORD = ITEMS.registerItem("celestial_sword",
            p -> new AbilitySwordItem(unbreakable(p.sword(CELESTIAL_TOOL, 13.0F, -1.0F)), AbilitySwordItem.Mode.CELESTIAL));

    // Dedicated tools retain vanilla mining rules, enchantment compatibility and block interactions.
    public static final DeferredItem<Item> SOLAR_PICKAXE = ITEMS.registerItem("solar_pickaxe", p -> new Item(p.pickaxe(SOLAR_MINING_TOOL, 1.0F, -2.6F).fireResistant()));
    public static final DeferredItem<Item> SOLAR_AXE = ITEMS.registerItem("solar_axe", p -> new Item(p.axe(SOLAR_MINING_TOOL, 5.0F, -2.6F).fireResistant()));
    public static final DeferredItem<Item> SOLAR_SHOVEL = ITEMS.registerItem("solar_shovel", p -> new Item(p.shovel(SOLAR_MINING_TOOL, 1.0F, -2.6F).fireResistant()));
    public static final DeferredItem<Item> SOLAR_HOE = ITEMS.registerItem("solar_hoe", p -> new Item(p.hoe(SOLAR_MINING_TOOL, 0.0F, -0.6F).fireResistant()));

    public static final DeferredItem<Item> ABYSSAL_PICKAXE = ITEMS.registerItem("abyssal_pickaxe", p -> new Item(p.pickaxe(ABYSSAL_MINING_TOOL, 2.0F, -3.0F).fireResistant()));
    public static final DeferredItem<Item> ABYSSAL_AXE = ITEMS.registerItem("abyssal_axe", p -> new Item(p.axe(ABYSSAL_MINING_TOOL, 6.0F, -3.2F).fireResistant()));
    public static final DeferredItem<Item> ABYSSAL_SHOVEL = ITEMS.registerItem("abyssal_shovel", p -> new Item(p.shovel(ABYSSAL_MINING_TOOL, 2.0F, -3.2F).fireResistant()));
    public static final DeferredItem<Item> ABYSSAL_HOE = ITEMS.registerItem("abyssal_hoe", p -> new Item(p.hoe(ABYSSAL_MINING_TOOL, 1.0F, -1.2F).fireResistant()));

    public static final DeferredItem<Item> CELESTIAL_PICKAXE = ITEMS.registerItem("celestial_pickaxe", p -> new Item(unbreakable(p.pickaxe(CELESTIAL_MINING_TOOL, 3.0F, -2.4F)).fireResistant()));
    public static final DeferredItem<Item> CELESTIAL_AXE = ITEMS.registerItem("celestial_axe", p -> new Item(unbreakable(p.axe(CELESTIAL_MINING_TOOL, 7.0F, -2.4F)).fireResistant()));
    public static final DeferredItem<Item> CELESTIAL_SHOVEL = ITEMS.registerItem("celestial_shovel", p -> new Item(unbreakable(p.shovel(CELESTIAL_MINING_TOOL, 3.0F, -2.4F)).fireResistant()));
    public static final DeferredItem<Item> CELESTIAL_HOE = ITEMS.registerItem("celestial_hoe", p -> new Item(unbreakable(p.hoe(CELESTIAL_MINING_TOOL, 2.0F, -0.4F)).fireResistant()));

    // Native Minecraft spear behaviour: jab, charge, reach and vanilla spear animations.
    public static final DeferredItem<Item> SOLAR_SPEAR = ITEMS.registerItem("solar_spear",
            p -> new Item(p.spear(SOLAR_TOOL, 0.90F, 1.15F, 0.45F, 2.5F, 8.5F, 5.0F, 5.1F, 8.75F, 4.6F)
                    .component(DataComponents.ATTACK_RANGE, new AttackRange(2.0F, 5.25F, 2.0F, 7.25F, 0.3F, 1.0F)).fireResistant()));
    public static final DeferredItem<Item> ABYSSAL_SPEAR = ITEMS.registerItem("abyssal_spear",
            p -> new Item(p.spear(ABYSSAL_TOOL, 1.00F, 1.20F, 0.42F, 2.5F, 8.5F, 5.0F, 5.1F, 8.75F, 4.6F)
                    .component(DataComponents.ATTACK_RANGE, new AttackRange(2.0F, 5.25F, 2.0F, 7.25F, 0.3F, 1.0F)).fireResistant()));
    public static final DeferredItem<Item> CELESTIAL_SPEAR = ITEMS.registerItem("celestial_spear",
            p -> new Item(unbreakable(p.spear(CELESTIAL_TOOL, 0.80F, 1.30F, 0.40F, 2.5F, 8.5F, 5.0F, 5.1F, 8.75F, 4.6F)
                    .component(DataComponents.ATTACK_RANGE, new AttackRange(2.0F, 5.25F, 2.0F, 7.25F, 0.3F, 1.0F))).fireResistant()));

    public static final DeferredItem<Item> SOLAR_MULTITOOL = ITEMS.registerItem("solar_multitool",
            p -> new CelestialMultitoolItem(multitoolProperties(p, SOLAR_MINING_TOOL, 1.0F, -2.7F)));
    public static final DeferredItem<Item> ABYSSAL_MULTITOOL = ITEMS.registerItem("abyssal_multitool",
            p -> new CelestialMultitoolItem(multitoolProperties(p, ABYSSAL_MINING_TOOL, 2.0F, -2.7F)));
    public static final DeferredItem<Item> CELESTIAL_MULTITOOL = ITEMS.registerItem("celestial_multitool",
            p -> new CelestialMultitoolItem(unbreakable(multitoolProperties(p, CELESTIAL_MINING_TOOL, 3.0F, -2.6F))));

    private static Item.Properties unbreakable(Item.Properties properties) {
        return properties.component(DataComponents.UNBREAKABLE, Unit.INSTANCE);
    }

    private static Item.Properties multitoolProperties(Item.Properties properties, ToolMaterial material,
                                                        float damage, float speed) {
        return (material == CELESTIAL_MINING_TOOL ? unbreakable(properties) : properties).pickaxe(material, damage, speed)
                .delayedComponent(DataComponents.TOOL, context -> {
                    var blocks = context.lookupOrThrow(Registries.BLOCK);
                    return new Tool(List.of(
                            Tool.Rule.deniesDrops(blocks.getOrThrow(material.incorrectBlocksForDrops())),
                            Tool.Rule.minesAndDrops(blocks.getOrThrow(BlockTags.MINEABLE_WITH_PICKAXE), material.speed()),
                            Tool.Rule.minesAndDrops(blocks.getOrThrow(BlockTags.MINEABLE_WITH_AXE), material.speed()),
                            Tool.Rule.minesAndDrops(blocks.getOrThrow(BlockTags.MINEABLE_WITH_SHOVEL), material.speed()),
                            Tool.Rule.minesAndDrops(blocks.getOrThrow(BlockTags.MINEABLE_WITH_HOE), material.speed())
                    ), 1.0F, 1, false);
                });
    }

    private static DeferredItem<Item> armorItem(String id, ArmorMaterial material, ArmorType type) {
        return ITEMS.registerItem(id,
                properties -> new Item((material == CELESTIAL_ARMOR ? unbreakable(properties) : properties).humanoidArmor(material, type).fireResistant()));
    }

    private ModItems() {}
}
