#!/usr/bin/env bash
# Imprime o caminho de um executável do Aseprite e sai com 0; sai com 2 (sem imprimir nada) se não achar.
for c in "${ASEPRITE_PATH:-}" "$(command -v aseprite || true)" \
  "/Applications/Aseprite.app/Contents/MacOS/aseprite" \
  "$HOME/Library/Application Support/Steam/steamapps/common/Aseprite/Aseprite.app/Contents/MacOS/aseprite" \
  "$HOME/.steam/steam/steamapps/common/Aseprite/aseprite" \
  "$HOME/.local/share/Steam/steamapps/common/Aseprite/aseprite" \
  "$HOME/.aseprite-build/build/bin/aseprite"; do
  if [ -n "$c" ] && [ -x "$c" ]; then echo "$c"; exit 0; fi
done
exit 2
