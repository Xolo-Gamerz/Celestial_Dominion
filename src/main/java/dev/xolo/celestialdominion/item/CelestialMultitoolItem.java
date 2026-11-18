package dev.xolo.celestialdominion.item;

import net.minecraft.core.component.BlockTransformer;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.component.BlockTransformers;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;

/**
 * The Omnitool combines the vanilla axe, shovel and hoe block-transformer
 * registries. Its multi-category Tool component supplies the mining behavior.
 */
public final class CelestialMultitoolItem extends Item {
    public CelestialMultitoolItem(Properties properties) {
        super(properties.stacksTo(1).fireResistant());
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        var transformers = level.registryAccess().lookupOrThrow(Registries.BLOCK_TRANSFORMER);

        InteractionResult result = apply(context, transformers.getOrThrow(BlockTransformers.AXE).value());
        if (result.consumesAction()) return result;

        result = apply(context, transformers.getOrThrow(BlockTransformers.SHOVEL).value());
        if (result.consumesAction()) return result;

        result = apply(context, transformers.getOrThrow(BlockTransformers.HOE).value());
        if (result.consumesAction()) return result;

        return super.useOn(context);
    }

    private static InteractionResult apply(UseOnContext context, BlockTransformer transformer) {
        return transformer.transformBlock(context);
    }
}
