package dev.xolo.celestialdominion.events;

import dev.xolo.celestialdominion.content.ModItems;
import net.minecraft.core.Holder;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.phys.AABB;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.living.LivingKnockBackEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

public final class GameplayEvents {
    private static final String FLIGHT_GRANTED_KEY = "celestial_dominion_granted_flight";

    private GameplayEvents() {}

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) {
            return;
        }

        if (player.tickCount % 20 != 0) {
            return;
        }

        boolean solar = hasFullSet(
                player,
                ModItems.SOLAR_HELMET.get(),
                ModItems.SOLAR_CHESTPLATE.get(),
                ModItems.SOLAR_LEGGINGS.get(),
                ModItems.SOLAR_BOOTS.get()
        );

        boolean abyssal = hasFullSet(
                player,
                ModItems.ABYSSAL_HELMET.get(),
                ModItems.ABYSSAL_CHESTPLATE.get(),
                ModItems.ABYSSAL_LEGGINGS.get(),
                ModItems.ABYSSAL_BOOTS.get()
        );

        boolean celestial = hasFullSet(
                player,
                ModItems.CELESTIAL_HELMET.get(),
                ModItems.CELESTIAL_CHESTPLATE.get(),
                ModItems.CELESTIAL_LEGGINGS.get(),
                ModItems.CELESTIAL_BOOTS.get()
        );

        if (solar || celestial) {
            applyEffect(player, MobEffects.FIRE_RESISTANCE, 260, 0);
            applyEffect(player, MobEffects.STRENGTH, 260, celestial ? 3 : 2);
            applyEffect(player, MobEffects.HASTE, 260, 1);
            applyEffect(player, MobEffects.SPEED, 260, 1);

            ServerLevel level = (ServerLevel) player.level();
            level.sendParticles(
                    ParticleTypes.FLAME,
                    player.getX(), player.getY() + 1.0, player.getZ(),
                    5, 0.45, 0.7, 0.45, 0.01
            );
        }

        if (abyssal || celestial) {
            applyEffect(player, MobEffects.RESISTANCE, 260, celestial ? 3 : 2);
            applyEffect(player, MobEffects.REGENERATION, 260, 1);
            applyEffect(player, MobEffects.ABSORPTION, 260, celestial ? 4 : 2);

            ServerLevel level = (ServerLevel) player.level();
            level.sendParticles(
                    ParticleTypes.SOUL,
                    player.getX(), player.getY() + 1.0, player.getZ(),
                    4, 0.4, 0.7, 0.4, 0.01
            );

            AABB aura = player.getBoundingBox().inflate(celestial ? 9.0 : 6.0);
            for (LivingEntity target : level.getEntitiesOfClass(
                    LivingEntity.class,
                    aura,
                    entity -> entity != player && entity.isAlive() && entity.isPickable()
            )) {
                applyEffect(target, MobEffects.SLOWNESS, 50, celestial ? 4 : 2);
                target.setTicksFrozen(Math.max(
                        target.getTicksFrozen(),
                        celestial ? 100 : 40
                ));
            }
        }

        updateCelestialFlight(player, celestial);
    }

    @SubscribeEvent
    public static void onDamageTaken(LivingDamageEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer victim)) {
            return;
        }

        boolean solar = hasFullSet(
                victim,
                ModItems.SOLAR_HELMET.get(),
                ModItems.SOLAR_CHESTPLATE.get(),
                ModItems.SOLAR_LEGGINGS.get(),
                ModItems.SOLAR_BOOTS.get()
        );

        boolean celestial = hasFullSet(
                victim,
                ModItems.CELESTIAL_HELMET.get(),
                ModItems.CELESTIAL_CHESTPLATE.get(),
                ModItems.CELESTIAL_LEGGINGS.get(),
                ModItems.CELESTIAL_BOOTS.get()
        );

        if (!solar && !celestial) {
            return;
        }

        if (event.getSource().getEntity() instanceof LivingEntity attacker && attacker != victim) {
            attacker.setRemainingFireTicks((celestial ? 12 : 8) * 20);
        }
    }

    @SubscribeEvent
    public static void onKnockback(LivingKnockBackEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) {
            return;
        }

        boolean abyssal = hasFullSet(
                player,
                ModItems.ABYSSAL_HELMET.get(),
                ModItems.ABYSSAL_CHESTPLATE.get(),
                ModItems.ABYSSAL_LEGGINGS.get(),
                ModItems.ABYSSAL_BOOTS.get()
        );

        boolean celestial = hasFullSet(
                player,
                ModItems.CELESTIAL_HELMET.get(),
                ModItems.CELESTIAL_CHESTPLATE.get(),
                ModItems.CELESTIAL_LEGGINGS.get(),
                ModItems.CELESTIAL_BOOTS.get()
        );

        if (abyssal || celestial) {
            event.setCanceled(true);
        }
    }

    private static void updateCelestialFlight(ServerPlayer player, boolean wearingCelestial) {
        var abilities = player.getAbilities();
        CompoundTag persistentData = player.getPersistentData();

        if (wearingCelestial) {
            if (!abilities.mayfly && !player.isCreative() && !player.isSpectator()) {
                persistentData.putBoolean(FLIGHT_GRANTED_KEY, true);
            }

            abilities.mayfly = true;
            abilities.setFlyingSpeed(0.12F);
            player.onUpdateAbilities();
            return;
        }

        boolean flightWasGrantedByThisMod =
                persistentData.getBooleanOr(FLIGHT_GRANTED_KEY, false);

        if (flightWasGrantedByThisMod && !player.isCreative() && !player.isSpectator()) {
            abilities.mayfly = false;
            abilities.flying = false;
            abilities.setFlyingSpeed(0.05F);
            player.onUpdateAbilities();
        }

        persistentData.remove(FLIGHT_GRANTED_KEY);
    }

    private static boolean hasFullSet(
            ServerPlayer player,
            Item helmet,
            Item chestplate,
            Item leggings,
            Item boots
    ) {
        return player.getItemBySlot(EquipmentSlot.HEAD).is(helmet)
                && player.getItemBySlot(EquipmentSlot.CHEST).is(chestplate)
                && player.getItemBySlot(EquipmentSlot.LEGS).is(leggings)
                && player.getItemBySlot(EquipmentSlot.FEET).is(boots);
    }

    private static void applyEffect(
            LivingEntity entity,
            Holder<MobEffect> effect,
            int duration,
            int amplifier
    ) {
        entity.addEffect(new MobEffectInstance(
                effect,
                duration,
                amplifier,
                true,
                false,
                true
        ));
    }
}
