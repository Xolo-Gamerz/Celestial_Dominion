package dev.xolo.celestialdominion.content;

import dev.xolo.celestialdominion.CelestialDominion;
import dev.xolo.celestialdominion.item.AbilitySwordItem;
import dev.xolo.celestialdominion.item.CelestialMultitoolItem;
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

    private static final ArmorMaterial SOLAR_ARMOR = armor("solar", 160, 8, 14, 11, 8, 8.0F, 0.35F);
    private static final ArmorMaterial ABYSSAL_ARMOR = armor("abyssal", 220, 10, 18, 14, 10, 14.0F, 0.65F);
    private static final ArmorMaterial CELESTIAL_ARMOR = armor("celestial", 320, 14, 24, 18, 14, 22.0F, 1.0F);

    private static final ToolMaterial SOLAR_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 12000, 16.0F, 12.0F, 30, REPAIR_TAG);
    private static final ToolMaterial ABYSSAL_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 18000, 18.0F, 18.0F, 30, REPAIR_TAG);
    private static final ToolMaterial CELESTIAL_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 30000, 22.0F, 24.0F, 40, REPAIR_TAG);

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
            p -> new AbilitySwordItem(p.sword(SOLAR_TOOL, 24.0F, -1.2F), AbilitySwordItem.Mode.SOLAR));
    public static final DeferredItem<Item> ABYSSAL_SWORD = ITEMS.registerItem("abyssal_sword",
            p -> new AbilitySwordItem(p.sword(ABYSSAL_TOOL, 19.0F, -1.5F), AbilitySwordItem.Mode.ABYSSAL));
    public static final DeferredItem<Item> CELESTIAL_SWORD = ITEMS.registerItem("celestial_sword",
            p -> new AbilitySwordItem(p.sword(CELESTIAL_TOOL, 34.0F, -0.8F), AbilitySwordItem.Mode.CELESTIAL));

    // Dedicated tools retain vanilla mining rules, enchantment compatibility and block interactions.
    public static final DeferredItem<Item> SOLAR_PICKAXE = ITEMS.registerItem("solar_pickaxe", p -> new Item(p.pickaxe(SOLAR_TOOL, 8.0F, -2.8F).fireResistant()));
    public static final DeferredItem<Item> SOLAR_AXE = ITEMS.registerItem("solar_axe", p -> new Item(p.axe(SOLAR_TOOL, 10.0F, -3.0F).fireResistant()));
    public static final DeferredItem<Item> SOLAR_SHOVEL = ITEMS.registerItem("solar_shovel", p -> new Item(p.shovel(SOLAR_TOOL, 7.0F, -3.0F).fireResistant()));
    public static final DeferredItem<Item> SOLAR_HOE = ITEMS.registerItem("solar_hoe", p -> new Item(p.hoe(SOLAR_TOOL, 5.0F, -1.0F).fireResistant()));

    public static final DeferredItem<Item> ABYSSAL_PICKAXE = ITEMS.registerItem("abyssal_pickaxe", p -> new Item(p.pickaxe(ABYSSAL_TOOL, 9.0F, -2.8F).fireResistant()));
    public static final DeferredItem<Item> ABYSSAL_AXE = ITEMS.registerItem("abyssal_axe", p -> new Item(p.axe(ABYSSAL_TOOL, 11.0F, -3.0F).fireResistant()));
    public static final DeferredItem<Item> ABYSSAL_SHOVEL = ITEMS.registerItem("abyssal_shovel", p -> new Item(p.shovel(ABYSSAL_TOOL, 8.0F, -3.0F).fireResistant()));
    public static final DeferredItem<Item> ABYSSAL_HOE = ITEMS.registerItem("abyssal_hoe", p -> new Item(p.hoe(ABYSSAL_TOOL, 6.0F, -1.0F).fireResistant()));

    public static final DeferredItem<Item> CELESTIAL_PICKAXE = ITEMS.registerItem("celestial_pickaxe", p -> new Item(p.pickaxe(CELESTIAL_TOOL, 12.0F, -2.8F).fireResistant()));
    public static final DeferredItem<Item> CELESTIAL_AXE = ITEMS.registerItem("celestial_axe", p -> new Item(p.axe(CELESTIAL_TOOL, 14.0F, -3.0F).fireResistant()));
    public static final DeferredItem<Item> CELESTIAL_SHOVEL = ITEMS.registerItem("celestial_shovel", p -> new Item(p.shovel(CELESTIAL_TOOL, 10.0F, -3.0F).fireResistant()));
    public static final DeferredItem<Item> CELESTIAL_HOE = ITEMS.registerItem("celestial_hoe", p -> new Item(p.hoe(CELESTIAL_TOOL, 8.0F, -1.0F).fireResistant()));

    public static final DeferredItem<Item> SOLAR_MULTITOOL = ITEMS.registerItem("solar_multitool",
            p -> new CelestialMultitoolItem(multitoolProperties(p, SOLAR_TOOL, 10.0F, -2.7F)));
    public static final DeferredItem<Item> ABYSSAL_MULTITOOL = ITEMS.registerItem("abyssal_multitool",
            p -> new CelestialMultitoolItem(multitoolProperties(p, ABYSSAL_TOOL, 11.0F, -2.7F)));
    public static final DeferredItem<Item> CELESTIAL_MULTITOOL = ITEMS.registerItem("celestial_multitool",
            p -> new CelestialMultitoolItem(multitoolProperties(p, CELESTIAL_TOOL, 14.0F, -2.6F)));

    private static Item.Properties multitoolProperties(Item.Properties properties, ToolMaterial material,
                                                        float damage, float speed) {
        return properties.pickaxe(material, damage, speed)
                .delayedComponent(DataComponents.TOOL, context -> {
                    var blocks = context.lookup(Registries.BLOCK);
                    return new Tool(List.of(
                            Tool.Rule.deniesDrops(blocks.getOrThrow(BlockTags.INCORRECT_FOR_NETHERITE_TOOL)),
                            Tool.Rule.minesAndDrops(blocks.getOrThrow(BlockTags.MINEABLE_WITH_PICKAXE), material.speed()),
                            Tool.Rule.minesAndDrops(blocks.getOrThrow(BlockTags.MINEABLE_WITH_AXE), material.speed()),
                            Tool.Rule.minesAndDrops(blocks.getOrThrow(BlockTags.MINEABLE_WITH_SHOVEL), material.speed()),
                            Tool.Rule.minesAndDrops(blocks.getOrThrow(BlockTags.MINEABLE_WITH_HOE), material.speed())
                    ), 1.0F, 1, false);
                });
    }

    private static DeferredItem<Item> armorItem(String id, ArmorMaterial material, ArmorType type) {
        return ITEMS.registerItem(id,
                properties -> new Item(properties.humanoidArmor(material, type).fireResistant()));
    }

    private ModItems() {}
}
