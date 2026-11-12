#!/usr/bin/env bash
# Instala o pixel-mcp (MIT, github.com/willibrandon/pixel-mcp, de willibrandon) e o registra no Claude Code.
# Uso: ./install-mcp.sh [/caminho/aseprite] [v0.5.0]
# Sem caminho, detecta o Aseprite sozinho; se não achar, imprime ASEPRITE_NOT_FOUND e sai com código 2.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ASEPRITE="${1:-$("$HERE/find-aseprite.sh" || true)}"
VERSION="${2:-v0.5.0}"
if [ -z "$ASEPRITE" ] || [ ! -x "$ASEPRITE" ]; then echo "ASEPRITE_NOT_FOUND"; exit 2; fi

OS="$(uname -s)"; ARCH="$(uname -m)"
case "$OS-$ARCH" in
  Linux-x86_64) T="Linux_x86_64" ;; Linux-aarch64|Linux-arm64) T="Linux_arm64" ;;
  Darwin-x86_64) T="Darwin_x86_64" ;; Darwin-arm64) T="Darwin_arm64" ;;
  *) echo "Plataforma sem suporte: $OS-$ARCH" >&2; exit 1 ;;
esac
VER="${VERSION#v}"
DIR="$HOME/.claude/mcp/pixel-mcp"; mkdir -p "$DIR"
ARCHIVE="pixel-mcp_${VER}_${T}.tar.gz"
BASE="https://github.com/willibrandon/pixel-mcp/releases/download/$VERSION"
curl -fsSL "$BASE/$ARCHIVE" -o "$DIR/$ARCHIVE"
curl -fsSL "$BASE/checksums.txt" -o "$DIR/checksums.txt"
EXPECTED="$(grep "$ARCHIVE" "$DIR/checksums.txt" | awk '{print $1}')"
ACTUAL="$( (sha256sum "$DIR/$ARCHIVE" 2>/dev/null || shasum -a 256 "$DIR/$ARCHIVE") | awk '{print $1}')"
[ "$EXPECTED" = "$ACTUAL" ] || { echo "Checksum SHA-256 não confere" >&2; exit 1; }
tar -xzf "$DIR/$ARCHIVE" -C "$DIR"

CFG="$HOME/.config/pixel-mcp"; mkdir -p "$CFG"
cat > "$CFG/config.json" <<JSON
{"aseprite_path": "$ASEPRITE", "temp_dir": "/tmp/pixel-mcp", "timeout": 60, "log_level": "info", "log_file": "", "enable_timing": false}
JSON
claude mcp add --scope user aseprite -- "$DIR/pixel-mcp"
echo "Pronto. Reinicie o cliente e rode: claude mcp list"
