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

# Select the largest visible top-level X11 window instead of relying on
# title/class metadata. Minecraft's SDL/LWJGL title varies across versions.
window_id=""
largest_area=0
while IFS= read -r candidate; do
  [ -n "$candidate" ] || continue
  geometry="$(xdotool getwindowgeometry --shell "$candidate" 2>/dev/null || true)"
  width="$(printf '%s\\n' "$geometry" | sed -n 's/^WIDTH=//p')"
  height="$(printf '%s\\n' "$geometry" | sed -n 's/^HEIGHT=//p')"
  [[ "$width" =~ ^[0-9]+$ && "$height" =~ ^[0-9]+$ ]] || continue
  area=$((width * height))
  if (( area > largest_area && width >= 320 && height >= 240 )); then
    largest_area=$area
    window_id="$candidate"
  fi
done < <(xdotool search --onlyvisible --name '.*' 2>/dev/null || true)

[ -n "$window_id" ] || fail "No visible Minecraft-sized X11 window found on DISPLAY=$DISPLAY."
echo "Closing visible client window $window_id ($largest_area pixels)."

# This image's xdotool version does not provide windowquit. Focus the
# SDL window and send a real XTEST Alt+F4 key chord instead of destroying
# the X11 window (which leaves the client process running).
xdotool windowfocus "$window_id" || fail "Could not focus the Minecraft window."
xdotool key --clearmodifiers alt+F4 || fail "Could not send the Minecraft quit shortcut."
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
