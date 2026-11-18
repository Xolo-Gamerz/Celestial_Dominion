package dev.xolo.celestialdominion.item;

import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.common.ItemAbility;

/**
 * The Omnitool combines the mining Tool component with all vanilla axe,
 * shovel and hoe block transformations. Mining/drop rules live in the item
 * component; this class only dispatches the right-click transformations.
 */
public final class CelestialMultitoolItem extends Item {
    private static final ItemAbility AXE_STRIP = ItemAbility.get("axe_strip");
    private static final ItemAbility AXE_SCRAPE = ItemAbility.get("axe_scrape");
    private static final ItemAbility AXE_WAX_OFF = ItemAbility.get("axe_wax_off");
    private static final ItemAbility SHOVEL_FLATTEN = ItemAbility.get("shovel_flatten");
    private static final ItemAbility SHOVEL_DOUSE = ItemAbility.get("shovel_douse");
    private static final ItemAbility HOE_TILL = ItemAbility.get("hoe_till");

    private static final ItemAbility[] ACTIONS = {
            AXE_STRIP, AXE_SCRAPE, AXE_WAX_OFF,
            SHOVEL_FLATTEN, SHOVEL_DOUSE, HOE_TILL
    };

    public CelestialMultitoolItem(Properties properties) {
        super(properties.stacksTo(1).fireResistant());
    }

    @Override
    public boolean canPerformAction(ItemStack stack, ItemAbility ability) {
        for (ItemAbility action : ACTIONS) {
            if (action == ability) return true;
        }
        return false;
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos pos = context.getClickedPos();
        BlockState original = level.getBlockState(pos);
        ItemStack stack = context.getItemInHand();

        for (ItemAbility action : ACTIONS) {
            BlockState modified = original.getToolModifiedState(context, action, true);
            if (modified == null || modified == original) continue;

            if (!level.isClientSide()) {
                // Ask the block to perform its normal transformation with simulate=false.
                modified = original.getToolModifiedState(context, action, false);
                if (modified == null || modified == original) continue;
                level.setBlock(pos, modified, 11);
                if (context.getPlayer() != null) {
                    stack.hurtAndBreak(1, context.getPlayer(), context.getHand());
                }
            }
            return InteractionResult.SUCCESS;
        }
        return super.useOn(context);
    }
}
