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

# Send ICCCM WM_DELETE_WINDOW directly to the GLFW client. There is no
# window manager inside xvfb-run, so EWMH window-manager close requests cannot
# be handled here. The helper verifies that the client advertises this protocol
# before sending it; GLFW turns it into its normal window-close callback.
JVM_LIST="$(jcmd -l 2>&1)" || fail "Could not enumerate JVMs with jcmd: $JVM_LIST"
echo "JVMs visible to jcmd:"
printf '%s\n' "$JVM_LIST"
mapfile -t CLIENT_PIDS < <(
  printf '%s\n' "$JVM_LIST" |
    awk '$0 ~ /minecraft-patched|net\.neoforged\.devlaunch\.Main|clientRunVmArgs/ { print $1 }'
)
[ "${#CLIENT_PIDS[@]}" -eq 1 ] || {
  echo "Java process table:"
  ps -eo pid,ppid,args | grep -E '[j]ava|[g]radle' || true
  fail "Expected exactly one NeoForge client JVM from jcmd -l; found ${#CLIENT_PIDS[@]}."
}
CLIENT_PID="${CLIENT_PIDS[0]}"

command -v xdotool >/dev/null 2>&1 || fail "xdotool is required to locate the Minecraft window."
mapfile -t CLIENT_WINDOWS < <(xdotool search --onlyvisible --pid "$CLIENT_PID" 2>/dev/null || true)
[ "${#CLIENT_WINDOWS[@]}" -eq 1 ] || fail "Expected exactly one visible X11 window for client PID $CLIENT_PID; found ${#CLIENT_WINDOWS[@]}."
CLIENT_WINDOW="${CLIENT_WINDOWS[0]}"
echo "Requesting ICCCM WM_DELETE_WINDOW for Minecraft PID $CLIENT_PID (window $CLIENT_WINDOW)."
python scripts/send_x11_close.py "$CLIENT_WINDOW" || fail "Could not send graceful WM_DELETE_WINDOW request to Minecraft window."

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
