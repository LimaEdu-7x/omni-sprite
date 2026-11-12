#!/usr/bin/env bash
# Instalação em um comando: copia as skills para ~/.claude/skills e instala/registra o servidor MCP do Aseprite.
# Uso: ./install.sh [/caminho/aseprite]
# Se o Aseprite não for encontrado, as skills são instaladas mesmo assim; no primeiro uso a IA oferece compilá-lo.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"; mkdir -p "$DEST"
for s in "$HERE"/skills/*/; do
  n="$(basename "$s")"
  if [ "$n" = "grill-me" ] && [ -d "$DEST/$n" ]; then echo "grill-me já instalada, pulando"; continue; fi
  rm -rf "${DEST:?}/$n"; cp -r "$s" "$DEST/$n"; echo "skill instalada: $n"
done
chmod +x "$DEST"/omni-sprite/scripts/*.sh 2>/dev/null || true
"$HERE/skills/omni-sprite/scripts/install-mcp.sh" ${1:+"$1"}; rc=$?
if [ "$rc" = 2 ]; then
  echo "Aseprite não encontrado. As skills estão instaladas. Peça um sprite à sua IA: ela oferecerá compilar o Aseprite do código-fonte,"
  echo "ou instale o Aseprite você mesmo e rode de novo: ./install.sh /caminho/aseprite"
elif [ "$rc" != 0 ]; then exit "$rc"; fi
