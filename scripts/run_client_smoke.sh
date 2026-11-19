#!/usr/bin/env bash
# Run inside xvfb-run so the controller and Minecraft share the same DISPLAY.
set -euo pipefail

LOG=run/logs/latest.log
SMOKE="${RUNNER_TEMP:-/tmp}/client-smoke.log"
rm -f "$LOG" "$SMOKE"

timeout --signal=TERM --kill-after=10s 240s ./gradlew runClient --console=plain >"$SMOKE" 2>&1 &
PID=$!

fail() {
  echo "::error::$1"
  tail -n 160 "$SMOKE" 2>/dev/null || true
  tail -n 160 "$LOG" 2>/dev/null || true
  kill "$PID" 2>/dev/null || true
  exit 1
}

# Poll frequently; the client log is small and local. No two-second blind delay.
deadline=$((SECONDS + 190))
reload_seen=0
while (( SECONDS < deadline )); do
  if grep -q "Reloading ResourceManager" "$LOG" 2>/dev/null; then
    reload_seen=1
    break
  fi
  if grep -Eiq "Vulkan is not supported|Failed to create backend Vulkan|Failed to create Vulkan (instance|device)|No Vulkan devices" "$LOG" "$SMOKE" 2>/dev/null; then
    fail "Minecraft Vulkan graphics backend failed."
  fi
  kill -0 "$PID" 2>/dev/null || break
  sleep 0.25
done
[ "$reload_seen" -eq 1 ] || fail "Client exited or timed out before resource reload."

# Wait until all atlas creation has settled (three 250ms stable samples).
atlas_deadline=$((SECONDS + 60))
last_atlas_count=0
stable_samples=0
while (( SECONDS < atlas_deadline )); do
  atlas_count="$(grep -c "TextureAtlas.*Created:" "$LOG" 2>/dev/null || true)"
  if (( atlas_count > 0 )); then
    if [ "$atlas_count" = "$last_atlas_count" ]; then
      stable_samples=$((stable_samples + 1))
    else
      stable_samples=0
      last_atlas_count="$atlas_count"
    fi
    (( stable_samples >= 3 )) && break
  fi
  sleep 0.25
done
(( stable_samples >= 3 )) || fail "Texture-atlas creation did not complete (last observed count: $last_atlas_count)."
grep -Eq "Using graphics backend Vulkan," "$LOG" || fail "Minecraft did not initialize the Vulkan graphics backend."

# Validate the actual client log before shutting the client down. The self-test
# above only validates the checker implementation, not this run's resources.
python scripts/check_client_model_bake.py "$LOG" || fail "Client resource/model validation failed."

# Xvfb is intentionally run without a window manager, so Alt+F4 has no WM to
# handle it. Ask the running JVM to exit through the JDK attach mechanism;
# this executes normal JVM shutdown hooks and lets Gradle finish runClient.
# NeoForge's actual client main class is launcher/version dependent, so do
# not identify it by a hard-coded net.minecraft main-class command-line match.
# jcmd reports the main class for every attach-visible JVM in this container.
JVM_LIST="$(jcmd -l 2>&1)" || fail "Could not enumerate JVMs with jcmd: $JVM_LIST"
echo "JVMs visible to jcmd:"
printf '%s\n' "$JVM_LIST"
mapfile -t CLIENT_PIDS < <(
  printf '%s\n' "$JVM_LIST" |
    awk 'NF >= 2 && $2 !~ /GradleDaemon|GradleWrapperMain|sun\.tools\.jcmd\.JCmd/ { print $1 }'
)
[ "${#CLIENT_PIDS[@]}" -eq 1 ] || {
  echo "Java process table:"
  ps -eo pid,ppid,args | grep -E '[j]ava|[g]radle' || true
  fail "Expected exactly one non-Gradle client JVM from jcmd -l; found ${#CLIENT_PIDS[@]}."
}
CLIENT_PID="${CLIENT_PIDS[0]}"
echo "Requesting graceful JVM shutdown for client PID $CLIENT_PID after successful resource validation."
jcmd "$CLIENT_PID" VM.exit || fail "Could not request client JVM shutdown through jcmd."

set +e
for _ in $(seq 1 30); do
  kill -0 "$PID" 2>/dev/null || break
  sleep 1
done
if kill -0 "$PID" 2>/dev/null; then
  fail "Gradle did not finish after the Minecraft JVM shutdown request."
fi
wait "$PID"
status=$?
set -e
cat "$SMOKE"
[ "$status" -eq 0 ] || fail "Gradle/client exited with status $status after validated JVM shutdown."
