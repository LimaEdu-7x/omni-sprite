# Estilos prontos

Cada estilo fixa: nível de tela, cores, contorno, sombreamento, dithering e antialiasing. Escolha um; não misture, a menos que o usuário peça. Os slugs de paleta apontam para `https://lospec.com/palette-list/<slug>`.

| # | Estilo | Tela (car.) | Cores | Contorno | Sombreamento | Dither | AA | Paletas sugeridas |
|---|---|---|---|---|---|---|---|---|
| 1 | `gameboy-4` | 32–64 | 4 (rampa verde) | nenhum/1 tom | chapado, 1 degrau | nenhum | não | `nintendo-gameboy-bgb` |
| 2 | `nes-8bit` | 32–64 | ≤16, 3 por sprite + transparente | preto 1px | chapado, 2 degraus | nenhum | não | `nes`/`pico-8` |
| 3 | `snes-16bit` | 64–96 | 16–32 | escuro com mudança de matiz, 1px | 3 degraus, cell shading | xadrez leve só em áreas grandes | raro | `endesga-32`, `db32` |
| 4 | `gba-chunky` | 64–96 | 24–40 | seletivo (escuro, não preto) | 3–4 degraus, saturado | nenhum | manual em curvas | `apollo`, `sweetie-16`+ |
| 5 | `arcade-neo` | 128–192 | 48–64 | contorno escuro grosso de espessura variável | 4–5 degraus, hard cel + brilho especular | pouco | sim | `aap-64`, `resurrect-64` |
| 6 | **`hd-pixel`** (padrão) | 128–256 | 32–64 | seletivo/colorido, mais claro no lado iluminado | 4–5 degraus + luz de contorno + luz rebatida | só textura | sim | `resurrect-64`, `aap-64`, `apollo` |
| 7 | `dark-fantasy` | 96–192 | 24–40 pouco saturadas, 1 acento | fino e escuro, nenhum na borda iluminada | alto contraste, luz de contorno forte, névoa por dither | sim (pedra, tecido) | sim | estilo `blk-neo`, `lospec500` |
| 8 | `cyberpunk-neon` | 128–192 | 32–48: base escura + 3 matizes neon | contorno colorido (brilho neon) | 3 degraus + rampas emissivas | scanline/bayer para brilho | sim | paletas com tag `cyberpunk` |
| 9 | `cute-chibi` | 64–128 | 16–32 pastel | colorido (tom mais escuro do preenchimento) | 2–3 degraus suaves | nenhum | sim | paletas com tag `pastel` |
| 10 | `isometric` | tile 64×32 (2:1), objetos 128 | 24–48 | seletivo | 3 faces: topo claro, esquerda média, direita escura (fixo) | só textura | regra de linha 2:1 (corrida de 2px) | `endesga-32` |
| 11 | `lineless-painterly` | 128–256 | 48–64 | nenhum; a forma vem do valor | 5 degraus, aglomerados suaves | dither de ruído para misturar | sim | `resurrect-64` |
| 12 | `1-bit` | 64–256 | 2 | – | só dither (Bayer / hachura) | pesado | não | `1bit-monitor-glow` |

## Regras para todos os estilos
- Uma única fonte de luz. Mantenha em todo frame/tile de um conjunto de assets.
- Rampas com mudança de matiz: sombras para azul/roxo, luzes para amarelo (inverta para noite/neon).
- Contraste de valor máximo no ponto focal (rosto/arma); mínimo em fundo/longe.
- Colinha de materiais: metal = faixas duras + brilho especular nítido; tecido = 3 degraus suaves + aglomerados de dobras; pele = rampa quente com vermelho nas sombras; pedra = dither/aglomerados + lascas; folhagem = tufos, 3 verdes + borda amarela; água = linhas horizontais de onda, faixas de luz; vidro = poucos pixels de brilho.
- Olhos: 2–4 px, um pixel de brilho; não delineie de preto rostos em dark fantasy.
- Nunca use `#000000` ou `#ffffff` puros, exceto em 1-bit/NES.
- Tiles: contínuos (*seamless*) — imagine uma repetição 3×3, confira se as bordas coincidem; faça 3–4 variações para evitar repetição.
- Amplie só por múltiplos inteiros com vizinho mais próximo (x2, x3, x4…).
