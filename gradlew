#!/usr/bin/env sh
set -eu
VERSION="9.2.1"
GRADLE_USER_HOME="${GRADLE_USER_HOME:-$HOME/.gradle}"
DIST_DIR="$GRADLE_USER_HOME/wrapper/dists/gradle-$VERSION-bin/celestial-bootstrap"
GRADLE_BIN="$DIST_DIR/gradle-$VERSION/bin/gradle"
if [ ! -x "$GRADLE_BIN" ]; then
  mkdir -p "$DIST_DIR"
  ARCHIVE="$DIST_DIR/gradle-$VERSION-bin.zip"
  echo "Downloading Gradle $VERSION..."
  if command -v curl >/dev/null 2>&1; then
    curl -fL "https://services.gradle.org/distributions/gradle-$VERSION-bin.zip" -o "$ARCHIVE"
  elif command -v wget >/dev/null 2>&1; then
    wget -O "$ARCHIVE" "https://services.gradle.org/distributions/gradle-$VERSION-bin.zip"
  else
    echo "curl or wget is required to bootstrap Gradle." >&2
    exit 1
  fi
  unzip -q -o "$ARCHIVE" -d "$DIST_DIR"
  rm -f "$ARCHIVE"
fi
exec "$GRADLE_BIN" "$@"
