package dev.xolo.celestialdominion.content;

import dev.xolo.celestialdominion.CelestialDominion;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;

public final class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(CelestialDominion.MOD_ID);

    public static final DeferredBlock<Block> SOLAR_ORE = BLOCKS.registerSimpleBlock(
            "solar_ore", BlockBehaviour.Properties.ofFullCopy(Blocks.ANCIENT_DEBRIS).strength(65.0F, 1200.0F));
    public static final DeferredBlock<Block> ABYSSAL_ORE = BLOCKS.registerSimpleBlock(
            "abyssal_ore", BlockBehaviour.Properties.ofFullCopy(Blocks.ANCIENT_DEBRIS).strength(70.0F, 1200.0F));
    public static final DeferredBlock<Block> CELESTIAL_ORE = BLOCKS.registerSimpleBlock(
            "celestial_ore", BlockBehaviour.Properties.ofFullCopy(Blocks.ANCIENT_DEBRIS).strength(85.0F, 1200.0F));

    private ModBlocks() {}
}
