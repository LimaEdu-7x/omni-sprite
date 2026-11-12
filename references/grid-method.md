# Método da grade (ASCII → pixels)

Escreva o sprite como texto; cada caractere é um índice da paleta. `.` = transparente.

```
..kkkk..
.kHHHHk.
kHLLMMSk
.kMMSSk.
..kkkk..
```
Exemplo de legenda: `k`=contorno `H`=brilho `L`=luz `M`=meio `S`=sombra.

Converter:
```
python scripts/grid_to_pixels.py sprite.txt --legend legend.json --ox 0 --oy 0 > pixels.json
```
`legend.json` mapeia caracteres para hex: `{"k":"#1a1c2c","H":"#f4f4f4","L":"#94b0c2","M":"#566c86","S":"#333c57"}`.
Saída: lista `[{"x":0,"y":0,"color":"#rrggbb"}, ...]`, no formato aceito por `draw_pixels` (confirmado no schema do pixel-mcp 0.5.0). Envie em blocos de até 10 000 pixels.

Dicas: desenhe metade e espelhe (`--mirror-x`) em objetos simétricos, depois acrescente os detalhes assimétricos à mão; mantenha cada grade com até 64 colunas para ficar legível e divida sprites maiores em partes com `--ox/--oy`.
