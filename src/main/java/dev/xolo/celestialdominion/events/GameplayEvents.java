package dev.xolo.celestialdominion.events;

import dev.xolo.celestialdominion.content.ModItems;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.phys.AABB;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.living.LivingKnockBackEvent;

public final class GameplayEvents {
    private GameplayEvents() {}

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player) || player.tickCount % 20 != 0) return;

        boolean solar = full(player, ModItems.SOLAR_HELMET.get(), ModItems.SOLAR_CHESTPLATE.get(),
                ModItems.SOLAR_LEGGINGS.get(), ModItems.SOLAR_BOOTS.get());
        boolean abyssal = full(player, ModItems.ABYSSAL_HELMET.get(), ModItems.ABYSSAL_CHESTPLATE.get(),
                ModItems.ABYSSAL_LEGGINGS.get(), ModItems.ABYSSAL_BOOTS.get());
        boolean celestial = full(player, ModItems.CELESTIAL_HELMET.get(), ModItems.CELESTIAL_CHESTPLATE.get(),
                ModItems.CELESTIAL_LEGGINGS.get(), ModItems.CELESTIAL_BOOTS.get());

        if (solar || celestial) {
            effect(player, MobEffects.FIRE_RESISTANCE, 260, 0);
            effect(player, MobEffects.STRENGTH, 260, celestial ? 3 : 2);
            effect(player, MobEffects.HASTE, 260, 1);
            effect(player, MobEffects.SPEED, 260, 1);
            ((ServerLevel) player.level()).sendParticles(ParticleTypes.FLAME,
                    player.getX(), player.getY() + 1, player.getZ(), 5, .45, .7, .45, .01);
        }

        if (abyssal || celestial) {
            effect(player, MobEffects.RESISTANCE, 260, celestial ? 3 : 2);
            effect(player, MobEffects.REGENERATION, 260, 1);
            effect(player, MobEffects.ABSORPTION, 260, celestial ? 4 : 2);
            ((ServerLevel) player.level()).sendParticles(ParticleTypes.SOUL,
                    player.getX(), player.getY() + 1, player.getZ(), 4, .4, .7, .4, .01);

            // The Abyssal aura controls nearby hostile living entities without damaging them.
            AABB aura = player.getBoundingBox().inflate(celestial ? 9.0 : 6.0);
            for (LivingEntity target : player.level().getEntitiesOfClass(LivingEntity.class, aura,
                    entity -> entity != player && entity.isAlive() && entity.isPickable())) {
                effect(target, MobEffects.SLOWNESS, 50, celestial ? 4 : 2);
                target.setTicksFrozen(Math.max(target.getTicksFrozen(), celestial ? 100 : 40));
            }
        }

        if (celestial) {
            player.getAbilities().mayfly = true;
            player.getAbilities().setFlyingSpeed(0.12F);
            player.onUpdateAbilities();
        } else if (!player.isCreative() && !player.isSpectator() && player.getAbilities().mayfly) {
            // Do not revoke flight from creative/spectator players.
            player.getAbilities().mayfly = false;
            player.getAbilities().flying = false;
            player.onUpdateAbilities();
        }
    }


    @SubscribeEvent
    public static void onDamageTaken(LivingDamageEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer victim)) return;
        boolean solar = full(victim, ModItems.SOLAR_HELMET.get(), ModItems.SOLAR_CHESTPLATE.get(),
                ModItems.SOLAR_LEGGINGS.get(), ModItems.SOLAR_BOOTS.get());
        boolean celestial = full(victim, ModItems.CELESTIAL_HELMET.get(), ModItems.CELESTIAL_CHESTPLATE.get(),
                ModItems.CELESTIAL_LEGGINGS.get(), ModItems.CELESTIAL_BOOTS.get());
        if (!solar && !celestial) return;
        if (event.getSource().getEntity() instanceof LivingEntity attacker && attacker != victim) {
            attacker.setSecondsOnFire(celestial ? 12 : 8);
        }
    }

    @SubscribeEvent
    public static void onKnockback(LivingKnockBackEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        boolean abyssal = full(player, ModItems.ABYSSAL_HELMET.get(), ModItems.ABYSSAL_CHESTPLATE.get(),
                ModItems.ABYSSAL_LEGGINGS.get(), ModItems.ABYSSAL_BOOTS.get());
        boolean celestial = full(player, ModItems.CELESTIAL_HELMET.get(), ModItems.CELESTIAL_CHESTPLATE.get(),
                ModItems.CELESTIAL_LEGGINGS.get(), ModItems.CELESTIAL_BOOTS.get());
        if (abyssal || celestial) event.setCanceled(true);
    }

    private static boolean full(ServerPlayer p, Item helmet, Item chest, Item legs, Item boots) {
        return p.getItemBySlot(EquipmentSlot.HEAD).is(helmet)
                && p.getItemBySlot(EquipmentSlot.CHEST).is(chest)
                && p.getItemBySlot(EquipmentSlot.LEGS).is(legs)
                && p.getItemBySlot(EquipmentSlot.FEET).is(boots);
    }

    private static void effect(LivingEntity entity,
            net.minecraft.core.Holder<net.minecraft.world.effect.MobEffect> effect,
            int duration, int amplifier) {
        entity.addEffect(new MobEffectInstance(effect, duration, amplifier, true, false, true));
    }
}
