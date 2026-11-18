package dev.xolo.celestialdominion.item;

import java.util.List;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

public final class AbilitySwordItem extends Item {
    public enum Mode {
        SOLAR,
        ABYSSAL,
        CELESTIAL
    }

    private final Mode mode;

    public AbilitySwordItem(Properties properties, Mode mode) {
        super(properties.stacksTo(1).fireResistant());
        this.mode = mode;
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);

        if (player.getCooldowns().isOnCooldown(stack)) {
            return InteractionResult.FAIL;
        }

        int cooldown = mode == Mode.CELESTIAL ? 500 : 700;
        player.getCooldowns().addCooldown(stack, cooldown);

        if (!level.isClientSide()) {
            ServerLevel serverLevel = (ServerLevel) level;

            if (mode == Mode.SOLAR || mode == Mode.CELESTIAL) {
                solarAbility(serverLevel, player);
            }

            if (mode == Mode.ABYSSAL || mode == Mode.CELESTIAL) {
                abyssalAbility(serverLevel, player);
            }
        }

        return InteractionResult.SUCCESS;
    }

    private static void solarAbility(ServerLevel level, Player player) {
        Vec3 look = player.getLookAngle();
        player.setDeltaMovement(look.scale(2.2).add(0.0, 0.25, 0.0));

        AABB area = player.getBoundingBox().inflate(7.0);
        List<LivingEntity> targets = level.getEntitiesOfClass(
                LivingEntity.class,
                area,
                target -> target != player && target.isAlive() && target.isPickable()
        );

        var damageSource = level.damageSources().playerAttack(player);

        for (LivingEntity target : targets) {
            if (target.hurtServer(level, damageSource, 26.0F)) {
                target.setRemainingFireTicks(8 * 20);
                target.knockback(
                        1.8,
                        player.getX() - target.getX(),
                        player.getZ() - target.getZ(),
                        damageSource,
                        26.0F
                );
            }
        }

        level.sendParticles(
                ParticleTypes.FLAME,
                player.getX(), player.getY() + 1.0, player.getZ(),
                72, 4.0, 1.5, 4.0, 0.12
        );
        level.sendParticles(
                ParticleTypes.EXPLOSION,
                player.getX(), player.getY() + 1.0, player.getZ(),
                4, 2.0, 1.0, 2.0, 0.05
        );
    }

    private void abyssalAbility(ServerLevel level, Player player) {
        AABB area = player.getBoundingBox().inflate(11.0);
        List<LivingEntity> targets = level.getEntitiesOfClass(
                LivingEntity.class,
                area,
                target -> target != player && target.isAlive() && target.isPickable()
        );

        for (LivingEntity target : targets) {
            Vec3 pull = player.position().subtract(target.position()).normalize().scale(1.15);
            target.push(pull.x, 0.35, pull.z);
            target.hurtServer(level, level.damageSources().magic(), 22.0F);
            target.setTicksFrozen(Math.max(target.getTicksFrozen(), 180));
            target.setDeltaMovement(target.getDeltaMovement().scale(0.15));
        }

        player.heal(mode == Mode.CELESTIAL ? 16.0F : 10.0F);

        level.sendParticles(
                ParticleTypes.SNOWFLAKE,
                player.getX(), player.getY() + 1.0, player.getZ(),
                80, 6.0, 2.0, 6.0, 0.08
        );
        level.sendParticles(
                ParticleTypes.PORTAL,
                player.getX(), player.getY() + 1.0, player.getZ(),
                48, 5.0, 2.0, 5.0, 0.3
        );
    }
}
