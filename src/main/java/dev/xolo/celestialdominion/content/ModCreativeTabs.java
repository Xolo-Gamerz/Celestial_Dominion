package dev.xolo.celestialdominion.content;

import dev.xolo.celestialdominion.CelestialDominion;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, CelestialDominion.MOD_ID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> CELESTIAL_DOMINION =
            TABS.register("celestial_dominion", () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.celestial_dominion"))
                    .icon(() -> ModItems.CELESTIAL_SWORD.get().getDefaultInstance())
                    .displayItems((parameters, output) -> {
                        output.accept(ModItems.SOLAR_ORE_ITEM.get());
                        output.accept(ModItems.ABYSSAL_ORE_ITEM.get());
                        output.accept(ModItems.CELESTIAL_ORE_ITEM.get());
                        output.accept(ModItems.SOLAR_INGOT.get());
                        output.accept(ModItems.ABYSSAL_INGOT.get());
                        output.accept(ModItems.CELESTIAL_INGOT.get());
                        output.accept(ModItems.SOLAR_TEMPLATE.get());
                        output.accept(ModItems.ABYSSAL_TEMPLATE.get());
                        output.accept(ModItems.CELESTIAL_CATALYST.get());
                        addArmorAndWeapons(output);
                        addTools(output,
                                ModItems.SOLAR_PICKAXE.get(), ModItems.SOLAR_AXE.get(),
                                ModItems.SOLAR_SHOVEL.get(), ModItems.SOLAR_HOE.get(),
                                ModItems.SOLAR_MULTITOOL.get());
                        addTools(output,
                                ModItems.ABYSSAL_PICKAXE.get(), ModItems.ABYSSAL_AXE.get(),
                                ModItems.ABYSSAL_SHOVEL.get(), ModItems.ABYSSAL_HOE.get(),
                                ModItems.ABYSSAL_MULTITOOL.get());
                        addTools(output,
                                ModItems.CELESTIAL_PICKAXE.get(), ModItems.CELESTIAL_AXE.get(),
                                ModItems.CELESTIAL_SHOVEL.get(), ModItems.CELESTIAL_HOE.get(),
                                ModItems.CELESTIAL_MULTITOOL.get());
                    }).build());

    private static void addArmorAndWeapons(CreativeModeTab.Output output) {
        output.accept(ModItems.SOLAR_HELMET.get()); output.accept(ModItems.SOLAR_CHESTPLATE.get());
        output.accept(ModItems.SOLAR_LEGGINGS.get()); output.accept(ModItems.SOLAR_BOOTS.get());
        output.accept(ModItems.SOLAR_SWORD.get()); output.accept(ModItems.SOLAR_SPEAR.get());
        output.accept(ModItems.ABYSSAL_HELMET.get()); output.accept(ModItems.ABYSSAL_CHESTPLATE.get());
        output.accept(ModItems.ABYSSAL_LEGGINGS.get()); output.accept(ModItems.ABYSSAL_BOOTS.get());
        output.accept(ModItems.ABYSSAL_SWORD.get()); output.accept(ModItems.ABYSSAL_SPEAR.get());
        output.accept(ModItems.CELESTIAL_HELMET.get()); output.accept(ModItems.CELESTIAL_CHESTPLATE.get());
        output.accept(ModItems.CELESTIAL_LEGGINGS.get()); output.accept(ModItems.CELESTIAL_BOOTS.get());
        output.accept(ModItems.CELESTIAL_SWORD.get()); output.accept(ModItems.CELESTIAL_SPEAR.get());
    }

    private static void addTools(CreativeModeTab.Output output, net.minecraft.world.item.Item pickaxe,
                                 net.minecraft.world.item.Item axe, net.minecraft.world.item.Item shovel,
                                 net.minecraft.world.item.Item hoe, net.minecraft.world.item.Item multitool) {
        output.accept(pickaxe); output.accept(axe); output.accept(shovel);
        output.accept(hoe); output.accept(multitool);
    }

    private ModCreativeTabs() {}
}
