package dev.xolo.celestialdominion.content;

import dev.xolo.celestialdominion.CelestialDominion;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/** The mod's discoverability surface: every registered item is exposed here. */
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
                        output.accept(ModItems.SOLAR_HELMET.get());
                        output.accept(ModItems.SOLAR_CHESTPLATE.get());
                        output.accept(ModItems.SOLAR_LEGGINGS.get());
                        output.accept(ModItems.SOLAR_BOOTS.get());
                        output.accept(ModItems.SOLAR_SWORD.get());
                        output.accept(ModItems.ABYSSAL_HELMET.get());
                        output.accept(ModItems.ABYSSAL_CHESTPLATE.get());
                        output.accept(ModItems.ABYSSAL_LEGGINGS.get());
                        output.accept(ModItems.ABYSSAL_BOOTS.get());
                        output.accept(ModItems.ABYSSAL_SWORD.get());
                        output.accept(ModItems.CELESTIAL_HELMET.get());
                        output.accept(ModItems.CELESTIAL_CHESTPLATE.get());
                        output.accept(ModItems.CELESTIAL_LEGGINGS.get());
                        output.accept(ModItems.CELESTIAL_BOOTS.get());
                        output.accept(ModItems.CELESTIAL_SWORD.get());
                    })
                    .build());

    private ModCreativeTabs() {}
}
