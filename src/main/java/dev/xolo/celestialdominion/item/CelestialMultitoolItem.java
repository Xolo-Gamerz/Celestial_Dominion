package dev.xolo.celestialdominion.item;

import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.common.ItemAbilities;
import net.neoforged.neoforge.common.ItemAbility;

/**
 * A four-discipline tool. Mining/drop rules are supplied by its Tool component;
 * this class exposes and executes the vanilla axe, shovel and hoe transformations.
 */
public final class CelestialMultitoolItem extends Item {
    public CelestialMultitoolItem(Properties properties) {
        super(properties.stacksTo(1).fireResistant());
    }

    @Override
    public boolean canPerformAction(ItemStack stack, ItemAbility ability) {
        return ItemAbilities.DEFAULT_AXE_ACTIONS.contains(ability)
                || ItemAbilities.DEFAULT_SHOVEL_ACTIONS.contains(ability)
                || ItemAbilities.HOE_TILL == ability;
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos pos = context.getClickedPos();
        BlockState original = level.getBlockState(pos);
        ItemStack stack = context.getItemInHand();

        ItemAbility[] actions = {
                ItemAbilities.AXE_STRIP,
                ItemAbilities.AXE_SCRAPE,
                ItemAbilities.AXE_WAX_OFF,
                ItemAbilities.SHOVEL_FLATTEN,
                ItemAbilities.SHOVEL_DOUSE,
                ItemAbilities.HOE_TILL
        };
        SoundEvents[] sounds = {
                SoundEvents.AXE_STRIP,
                SoundEvents.AXE_SCRAPE,
                SoundEvents.AXE_WAX_OFF,
                SoundEvents.SHOVEL_FLATTEN,
                SoundEvents.FIRE_EXTINGUISH,
                SoundEvents.HOE_TILL
        };

        for (int i = 0; i < actions.length; i++) {
            Optional<BlockState> modified = Optional.ofNullable(
                    original.getToolModifiedState(context, actions[i], false));
            if (modified.isEmpty() || modified.get() == original) {
                continue;
            }

            if (!level.isClientSide()) {
                level.setBlock(pos, modified.get(), 11);
                level.playSound(context.getPlayer(), pos, sounds[i], SoundSource.BLOCKS, 1.0F, 1.0F);
                if (context.getPlayer() != null) {
                    stack.hurtAndBreak(1, context.getPlayer(), context.getHand());
                }
            }
            return InteractionResult.SUCCESS;
        }
        return super.useOn(context);
    }
}
