package dev.xolo.celestialdominion;

import dev.xolo.celestialdominion.content.ModBlocks;
import dev.xolo.celestialdominion.content.ModCreativeTabs;
import dev.xolo.celestialdominion.content.ModItems;
import dev.xolo.celestialdominion.events.GameplayEvents;
import dev.xolo.celestialdominion.events.ItemTooltipEvents;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;

@Mod(CelestialDominion.MOD_ID)
public final class CelestialDominion {
    public static final String MOD_ID = "celestial_dominion";

    public CelestialDominion(IEventBus modBus) {
        ModBlocks.BLOCKS.register(modBus);
        ModItems.ITEMS.register(modBus);
        ModCreativeTabs.TABS.register(modBus);
        NeoForge.EVENT_BUS.register(GameplayEvents.class);
        NeoForge.EVENT_BUS.register(ItemTooltipEvents.class);
    }
}
