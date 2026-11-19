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
grep -Eq "Using graphics backend (Vulkan|OpenGL)" "$LOG" || fail "Minecraft did not initialize a graphics backend."

# xvfb-run exports DISPLAY only to its child process. This script runs inside
# that child, so xdotool talks to the exact X server hosting Minecraft.
window_id=""
for _ in $(seq 1 40); do
  while IFS= read -r candidate; do
    [ -n "$candidate" ] || continue
    window_name="$(xdotool getwindowname "$candidate" 2>/dev/null || true)"
    window_class="$(xdotool getwindowclassname "$candidate" 2>/dev/null || true)"
    if [[ "$window_name $window_class" =~ [Mm]inecraft|[Ll][Ww][Jj][Gg][Ll] ]]; then
      window_id="$candidate"
      break
    fi
  done < <(xdotool search --name '.*' 2>/dev/null || true)
  [ -n "$window_id" ] && break
  sleep 0.25
done
[ -n "$window_id" ] || fail "Could not identify Minecraft's X11 window on DISPLAY=$DISPLAY."

xdotool windowclose "$window_id" || fail "Could not send the Minecraft window-close event."
set +e
for _ in $(seq 1 30); do
  kill -0 "$PID" 2>/dev/null || break
  sleep 1
done
if kill -0 "$PID" 2>/dev/null; then
  fail "Minecraft did not shut down gracefully within 30 seconds."
fi
wait "$PID"
status=$?
set -e
cat "$SMOKE"
[ "$status" -eq 0 ] || fail "Gradle/client exited with status $status after graceful window close."
python scripts/check_client_model_bake.py "$LOG"
