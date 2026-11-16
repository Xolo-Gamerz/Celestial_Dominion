package dev.xolo.celestialdominion.item;

import java.util.List;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

public final class AbilitySwordItem extends Item {
    public enum Mode { SOLAR, ABYSSAL, CELESTIAL }
    private final Mode mode;

    public AbilitySwordItem(Properties properties, Mode mode) {
        super(properties.stacksTo(1).fireResistant());
        this.mode = mode;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.getCooldowns().isOnCooldown(this)) return InteractionResultHolder.fail(stack);
        player.getCooldowns().addCooldown(this, mode == Mode.CELESTIAL ? 500 : 700);
        if (!level.isClientSide) {
            ServerLevel server = (ServerLevel) level;
            if (mode == Mode.SOLAR || mode == Mode.CELESTIAL) solar(server, player);
            if (mode == Mode.ABYSSAL || mode == Mode.CELESTIAL) abyssal(server, player);
        }
        return InteractionResultHolder.success(stack);
    }

    private void solar(ServerLevel level, Player player) {
        Vec3 look = player.getLookAngle();
        player.setDeltaMovement(look.scale(2.2).add(0, 0.25, 0));
        player.hurtMarked = true;
        AABB area = player.getBoundingBox().inflate(7.0);
        List<LivingEntity> targets = level.getEntitiesOfClass(LivingEntity.class, area,
                e -> e != player && e.isAlive() && e.isPickable());
        for (LivingEntity target : targets) {
            target.hurtServer(level, level.damageSources().playerAttack(player), 26.0F);
            target.setSecondsOnFire(8);
            target.knockback(1.8, player.getX() - target.getX(), player.getZ() - target.getZ());
        }
        level.sendParticles(ParticleTypes.FLAME, player.getX(), player.getY() + 1, player.getZ(), 180, 4, 1.5, 4, 0.12);
        level.sendParticles(ParticleTypes.EXPLOSION, player.getX(), player.getY() + 1, player.getZ(), 8, 2, 1, 2, 0.05);
    }

    private void abyssal(ServerLevel level, Player player) {
        AABB area = player.getBoundingBox().inflate(11.0);
        List<LivingEntity> targets = level.getEntitiesOfClass(LivingEntity.class, area,
                e -> e != player && e.isAlive() && e.isPickable());
        for (LivingEntity target : targets) {
            Vec3 pull = player.position().subtract(target.position()).normalize().scale(1.15);
            target.push(pull.x, 0.35, pull.z);
            target.hurtServer(level, level.damageSources().magic(), 22.0F);
            target.setTicksFrozen(Math.max(target.getTicksFrozen(), 180));
            target.setDeltaMovement(target.getDeltaMovement().scale(0.15));
        }
        player.heal(mode == Mode.CELESTIAL ? 16.0F : 10.0F);
        level.sendParticles(ParticleTypes.SNOWFLAKE, player.getX(), player.getY() + 1, player.getZ(), 220, 6, 2, 6, 0.08);
        level.sendParticles(ParticleTypes.PORTAL, player.getX(), player.getY() + 1, player.getZ(), 140, 5, 2, 5, 0.3);
    }
}
