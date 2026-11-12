#!/usr/bin/env bash
# Builds Aseprite from source (Linux / macOS). Output: ~/.aseprite-build/build/bin/aseprite
# Needs: git cmake ninja, a C++ toolchain, and the system libs listed in Aseprite's INSTALL.md.
# Aseprite is source-available (EULA): build for your own use; do not redistribute the binary.
# Usage: ./build-aseprite.sh [tag] [root-dir]
set -euo pipefail
TAG="${1:-}"; ROOT="${2:-$HOME/.aseprite-build}"
for t in git cmake ninja; do command -v "$t" >/dev/null || { echo "Missing tool: $t" >&2; exit 1; }; done
mkdir -p "$ROOT"; SRC="$ROOT/aseprite-src"; SKIA="$ROOT/deps/skia"
if [ -z "$TAG" ]; then
  TAG="$(git ls-remote --tags --refs https://github.com/aseprite/aseprite.git 'v1.3.*' | sed 's#.*refs/tags/##' | grep -E '^v1\.3\.[0-9]+(\.[0-9]+)?$' | sort -V | tail -1)"
fi
echo "Aseprite tag: $TAG"
[ -d "$SRC" ] || git clone --recursive --depth 1 --branch "$TAG" https://github.com/aseprite/aseprite.git "$SRC"
SKIA_TAG="$(grep -oE 'aseprite/skia/releases/tag/m[0-9]+-[0-9a-f]+' "$SRC/INSTALL.md" | head -1 | sed 's#.*/tag/##')"
[ -n "$SKIA_TAG" ] || { echo "Could not read the Skia tag from INSTALL.md" >&2; exit 1; }
case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)  ZIP="Skia-Linux-Release-x64-libstdc++.zip"; LIBDIR="out/Release-x64" ;;
  Darwin-arm64)  ZIP="Skia-macOS-Release-arm64.zip";          LIBDIR="out/Release-arm64" ;;
  Darwin-x86_64) ZIP="Skia-macOS-Release-x64.zip";            LIBDIR="out/Release-x64" ;;
  *) echo "Unsupported platform; follow $SRC/INSTALL.md" >&2; exit 1 ;;
esac
if [ ! -f "$SKIA/$LIBDIR/libskia.a" ]; then
  mkdir -p "$SKIA"
  curl -fsSL "https://github.com/aseprite/skia/releases/download/$SKIA_TAG/$ZIP" -o "$ROOT/skia.zip"
  unzip -q -o "$ROOT/skia.zip" -d "$SKIA"; rm "$ROOT/skia.zip"
fi
mkdir -p "$ROOT/build"; cd "$ROOT/build"
EXTRA=()
if [ "$(uname -s)" = Darwin ]; then EXTRA=(-DCMAKE_OSX_ARCHITECTURES="$(uname -m)" -DCMAKE_OSX_DEPLOYMENT_TARGET=11.0); fi
cmake -DCMAKE_BUILD_TYPE=Release -DLAF_BACKEND=skia -DSKIA_DIR="$SKIA" \
  -DSKIA_LIBRARY_DIR="$SKIA/$LIBDIR" -DSKIA_LIBRARY="$SKIA/$LIBDIR/libskia.a" "${EXTRA[@]}" -G Ninja "$SRC"
ninja aseprite
echo "OK: $ROOT/build/bin/aseprite"
