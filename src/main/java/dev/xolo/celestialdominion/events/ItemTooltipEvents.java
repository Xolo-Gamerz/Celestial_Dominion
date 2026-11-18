package dev.xolo.celestialdominion.events;

import dev.xolo.celestialdominion.content.ModItems;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;

/** Adds concise lore and exact gameplay instructions to every custom item. */
public final class ItemTooltipEvents {
    private ItemTooltipEvents() {}

    @SubscribeEvent
    public static void onItemTooltip(ItemTooltipEvent event) {
        ItemStack stack = event.getItemStack();

        if (stack.is(ModItems.SOLAR_ORE_ITEM.get())) {
            line(event, "tooltip.celestial_dominion.solar_ore.lore", ChatFormatting.GOLD);
            line(event, "tooltip.celestial_dominion.solar_ore.where", ChatFormatting.GRAY);
            line(event, "tooltip.celestial_dominion.ore.new_chunks", ChatFormatting.DARK_GRAY);
        } else if (stack.is(ModItems.ABYSSAL_ORE_ITEM.get())) {
            line(event, "tooltip.celestial_dominion.abyssal_ore.lore", ChatFormatting.DARK_AQUA);
            line(event, "tooltip.celestial_dominion.abyssal_ore.where", ChatFormatting.GRAY);
            line(event, "tooltip.celestial_dominion.ore.new_chunks", ChatFormatting.DARK_GRAY);
        } else if (stack.is(ModItems.CELESTIAL_ORE_ITEM.get())) {
            line(event, "tooltip.celestial_dominion.celestial_ore.lore", ChatFormatting.LIGHT_PURPLE);
            line(event, "tooltip.celestial_dominion.celestial_ore.where", ChatFormatting.GRAY);
            line(event, "tooltip.celestial_dominion.ore.new_chunks", ChatFormatting.DARK_GRAY);
        } else if (stack.is(ModItems.SOLAR_INGOT.get())) {
            line(event, "tooltip.celestial_dominion.solar_ingot", ChatFormatting.GOLD);
        } else if (stack.is(ModItems.ABYSSAL_INGOT.get())) {
            line(event, "tooltip.celestial_dominion.abyssal_ingot", ChatFormatting.AQUA);
        } else if (stack.is(ModItems.CELESTIAL_INGOT.get())) {
            line(event, "tooltip.celestial_dominion.celestial_ingot", ChatFormatting.LIGHT_PURPLE);
        } else if (stack.is(ModItems.SOLAR_TEMPLATE.get())) {
            line(event, "tooltip.celestial_dominion.solar_template", ChatFormatting.GOLD);
        } else if (stack.is(ModItems.ABYSSAL_TEMPLATE.get())) {
            line(event, "tooltip.celestial_dominion.abyssal_template", ChatFormatting.DARK_AQUA);
        } else if (stack.is(ModItems.CELESTIAL_CATALYST.get())) {
            line(event, "tooltip.celestial_dominion.celestial_catalyst", ChatFormatting.LIGHT_PURPLE);
        } else if (isSolarArmor(stack)) {
            line(event, "tooltip.celestial_dominion.solar_armor.lore", ChatFormatting.GOLD);
            line(event, "tooltip.celestial_dominion.solar_armor.bonus", ChatFormatting.YELLOW);
        } else if (isAbyssalArmor(stack)) {
            line(event, "tooltip.celestial_dominion.abyssal_armor.lore", ChatFormatting.DARK_AQUA);
            line(event, "tooltip.celestial_dominion.abyssal_armor.bonus", ChatFormatting.AQUA);
        } else if (isCelestialArmor(stack)) {
            line(event, "tooltip.celestial_dominion.celestial_armor.lore", ChatFormatting.LIGHT_PURPLE);
            line(event, "tooltip.celestial_dominion.celestial_armor.bonus", ChatFormatting.GOLD);
        } else if (stack.is(ModItems.SOLAR_SWORD.get())) {
            line(event, "tooltip.celestial_dominion.solar_sword.lore", ChatFormatting.GOLD);
            line(event, "tooltip.celestial_dominion.solar_sword.ability", ChatFormatting.YELLOW);
            line(event, "tooltip.celestial_dominion.sword.cooldown_35", ChatFormatting.GRAY);
        } else if (stack.is(ModItems.ABYSSAL_SWORD.get())) {
            line(event, "tooltip.celestial_dominion.abyssal_sword.lore", ChatFormatting.DARK_AQUA);
            line(event, "tooltip.celestial_dominion.abyssal_sword.ability", ChatFormatting.AQUA);
            line(event, "tooltip.celestial_dominion.sword.cooldown_35", ChatFormatting.GRAY);
        } else if (stack.is(ModItems.CELESTIAL_SWORD.get())) {
            line(event, "tooltip.celestial_dominion.celestial_sword.lore", ChatFormatting.LIGHT_PURPLE);
            line(event, "tooltip.celestial_dominion.celestial_sword.ability", ChatFormatting.GOLD);
            line(event, "tooltip.celestial_dominion.sword.cooldown_25", ChatFormatting.GRAY);
        }
    }

    private static boolean isSolarArmor(ItemStack stack) {
        return stack.is(ModItems.SOLAR_HELMET.get()) || stack.is(ModItems.SOLAR_CHESTPLATE.get())
                || stack.is(ModItems.SOLAR_LEGGINGS.get()) || stack.is(ModItems.SOLAR_BOOTS.get());
    }

    private static boolean isAbyssalArmor(ItemStack stack) {
        return stack.is(ModItems.ABYSSAL_HELMET.get()) || stack.is(ModItems.ABYSSAL_CHESTPLATE.get())
                || stack.is(ModItems.ABYSSAL_LEGGINGS.get()) || stack.is(ModItems.ABYSSAL_BOOTS.get());
    }

    private static boolean isCelestialArmor(ItemStack stack) {
        return stack.is(ModItems.CELESTIAL_HELMET.get()) || stack.is(ModItems.CELESTIAL_CHESTPLATE.get())
                || stack.is(ModItems.CELESTIAL_LEGGINGS.get()) || stack.is(ModItems.CELESTIAL_BOOTS.get());
    }

    private static void line(ItemTooltipEvent event, String translationKey, ChatFormatting color) {
        event.getToolTip().add(Component.translatable(translationKey).withStyle(color));
    }
}
