package dev.xolo.celestialdominion.content;

import dev.xolo.celestialdominion.CelestialDominion;
import dev.xolo.celestialdominion.item.AbilitySwordItem;
import java.util.EnumMap;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ToolMaterial;
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
            String assetName,
            int durability,
            int helmet,
            int chest,
            int legs,
            int boots,
            float toughness,
            float knockbackResistance
    ) {
        Map<ArmorType, Integer> defense = new EnumMap<>(ArmorType.class);
        defense.put(ArmorType.HELMET, helmet);
        defense.put(ArmorType.CHESTPLATE, chest);
        defense.put(ArmorType.LEGGINGS, legs);
        defense.put(ArmorType.BOOTS, boots);
        defense.put(ArmorType.BODY, chest);

        return new ArmorMaterial(
                durability,
                defense,
                30,
                SoundEvents.ARMOR_EQUIP_NETHERITE,
                toughness,
                knockbackResistance,
                REPAIR_TAG,
                asset(assetName)
        );
    }

    private static final ArmorMaterial SOLAR_ARMOR =
            armor("solar", 160, 8, 14, 11, 8, 8.0F, 0.35F);
    private static final ArmorMaterial ABYSSAL_ARMOR =
            armor("abyssal", 220, 10, 18, 14, 10, 14.0F, 0.65F);
    private static final ArmorMaterial CELESTIAL_ARMOR =
            armor("celestial", 320, 14, 24, 18, 14, 22.0F, 1.0F);

    private static final ToolMaterial SOLAR_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 12000, 16.0F, 12.0F, 30, REPAIR_TAG);
    private static final ToolMaterial ABYSSAL_TOOL = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL, 18000, 14.0F, 18.0F, 30, REPAIR_TAG);
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

    public static final DeferredItem<Item> SOLAR_TEMPLATE =
            ITEMS.registerSimpleItem("solar_smithing_template");
    public static final DeferredItem<Item> ABYSSAL_TEMPLATE =
            ITEMS.registerSimpleItem("abyssal_smithing_template");
    public static final DeferredItem<Item> CELESTIAL_CATALYST =
            ITEMS.registerSimpleItem("celestial_catalyst");

    public static final DeferredItem<Item> SOLAR_HELMET =
            armorItem("solar_helmet", SOLAR_ARMOR, ArmorType.HELMET);
    public static final DeferredItem<Item> SOLAR_CHESTPLATE =
            armorItem("solar_chestplate", SOLAR_ARMOR, ArmorType.CHESTPLATE);
    public static final DeferredItem<Item> SOLAR_LEGGINGS =
            armorItem("solar_leggings", SOLAR_ARMOR, ArmorType.LEGGINGS);
    public static final DeferredItem<Item> SOLAR_BOOTS =
            armorItem("solar_boots", SOLAR_ARMOR, ArmorType.BOOTS);

    public static final DeferredItem<Item> ABYSSAL_HELMET =
            armorItem("abyssal_helmet", ABYSSAL_ARMOR, ArmorType.HELMET);
    public static final DeferredItem<Item> ABYSSAL_CHESTPLATE =
            armorItem("abyssal_chestplate", ABYSSAL_ARMOR, ArmorType.CHESTPLATE);
    public static final DeferredItem<Item> ABYSSAL_LEGGINGS =
            armorItem("abyssal_leggings", ABYSSAL_ARMOR, ArmorType.LEGGINGS);
    public static final DeferredItem<Item> ABYSSAL_BOOTS =
            armorItem("abyssal_boots", ABYSSAL_ARMOR, ArmorType.BOOTS);

    public static final DeferredItem<Item> CELESTIAL_HELMET =
            armorItem("celestial_helmet", CELESTIAL_ARMOR, ArmorType.HELMET);
    public static final DeferredItem<Item> CELESTIAL_CHESTPLATE =
            armorItem("celestial_chestplate", CELESTIAL_ARMOR, ArmorType.CHESTPLATE);
    public static final DeferredItem<Item> CELESTIAL_LEGGINGS =
            armorItem("celestial_leggings", CELESTIAL_ARMOR, ArmorType.LEGGINGS);
    public static final DeferredItem<Item> CELESTIAL_BOOTS =
            armorItem("celestial_boots", CELESTIAL_ARMOR, ArmorType.BOOTS);

    public static final DeferredItem<Item> SOLAR_SWORD = ITEMS.registerItem(
            "solar_sword",
            properties -> new AbilitySwordItem(
                    properties.sword(SOLAR_TOOL, 24.0F, -1.2F),
                    AbilitySwordItem.Mode.SOLAR
            )
    );
    public static final DeferredItem<Item> ABYSSAL_SWORD = ITEMS.registerItem(
            "abyssal_sword",
            properties -> new AbilitySwordItem(
                    properties.sword(ABYSSAL_TOOL, 19.0F, -1.5F),
                    AbilitySwordItem.Mode.ABYSSAL
            )
    );
    public static final DeferredItem<Item> CELESTIAL_SWORD = ITEMS.registerItem(
            "celestial_sword",
            properties -> new AbilitySwordItem(
                    properties.sword(CELESTIAL_TOOL, 34.0F, -0.8F),
                    AbilitySwordItem.Mode.CELESTIAL
            )
    );

    private static DeferredItem<Item> armorItem(
            String id, ArmorMaterial material, ArmorType type
    ) {
        return ITEMS.registerItem(
                id,
                properties -> new Item(properties.humanoidArmor(material, type).fireResistant())
        );
    }

    private ModItems() {}
}
