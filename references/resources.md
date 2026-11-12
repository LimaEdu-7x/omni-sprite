# Recursos integrados à omni-sprite

As URLs vieram de resultados de busca; abra e verifique antes de depender delas. Skills da comunidade são de terceiros e não foram auditadas: leia o SKILL.md antes de instalar.

## Sites (aprendizado, paletas, assets)
| # | Site | Use para |
|---|---|---|
| 1 | https://lospec.com/palette-list | Paletas por número de cores/tag; download `.hex` por paleta |
| 2 | https://lospec.com/pixel-art-tutorials | Tutoriais por tópico (sombra, dithering, animação) |
| 3 | https://www.aseprite.org/docs/ | Manual oficial do Aseprite (modo indexado, tags, slices) |
| 4 | https://www.aseprite.org/api/ | API de scripts Lua (scripts em lote além do MCP) |
| 5 | https://www.slynyrd.com/blog | "Pixelblog": lições longas e estruturadas (personagens, tiles, cenas) |
| 6 | https://saint11.art/blog/pixel-art-tutorials/ | Tutoriais animados curtos sobre movimento e acabamento |
| 7 | https://derekyu.com/makegames/pixelart.html | Introdução clássica: contornos, rampas de cor, dithering |
| 8 | https://pixeljoint.com | Galeria da comunidade para referência de estilo |
| 9 | https://michafrar.itch.io/pixel-logic | Guia "Pixel Logic": linhas limpas, aglomerados, sombra |
| 10 | https://itch.io/game-assets/tag-pixel-art | Referência de pacotes de sprites prontos (estude, não copie) |
| 11 | https://opengameart.org | Assets gratuitos com licença indicada |
| 12 | https://www.pixilart.com ou https://www.pixelation.org | Crítica/inspiração da comunidade (verifique se estão no ar) |

## Skills e servidores da comunidade para estudar ou compor
| # | Nome | Origem | O que aproveitar |
|---|---|---|---|
| 1 | pixel-art | omer-metin/skills-for-antigravity | Dithering + paleta limitada |
| 2 | pixel-art-sprites | omer-metin/skills-for-antigravity | Fluxos de spritesheet e tileset |
| 3 | pixel-art-studio | AnastasiyaW/codex-claude-code-config | Nota de qualidade por script (enviar ≥ 80, corrigir 60–80, refazer < 60) |
| 4 | pixel-art-studio | gamezxz | Sprites desenhados por código com Python/Pillow (plano B sem Aseprite) |
| 5 | pixel-art-exporter | willibrandon/pixel-plugin | Formatos de exportação por motor de jogo |
| 6 | pixel-art-sprites | AbsolutelySkilled | Estrutura dos ciclos de andar/ataque/idle |
| 7 | creating-sprites | riccardogrin/skills | Checklist de criação de sprite |
| 8 | pixel-art-advisor | listagem claudskills.com | Prompts de revisão em formato de conselho |
| 9 | diivi/aseprite-mcp | github.com/diivi/aseprite-mcp | MCP alternativo em Python (servidor reserva) |
| 10 | rkdfx/aseprite-mcp | github.com/rkdfx/aseprite-mcp | Alternativa baseada em scripts Lua |
| 11 | willibrandon/pixel-mcp | github.com/willibrandon/pixel-mcp | **Servidor obrigatório** usado por esta skill (MIT) |

## Skills de direção, pose e animação (adicionadas)
| # | Nome | Origem | O que aproveitar |
|---|---|---|---|
| 1 | character-sprite | paulrobello/claude-office | Convenção de 8 direções (S, SW, W, NW, N, NE, E, SE) |
| 2 | tinyworld-25d-template-sprites | jasonkneen/tiny-world-builder | Usar linhas laterais reais em vez de espelhar quando o desenho é assimétrico |
| 3 | animated-spritesheets | listagem claudskills.com | Flag de direção com trava de perfil lateral para L/O |
| 4 | generate2dsprite | 0x0funky/agent-sprite-forge | Declarar vista (lateral / top-down / 3/4) e layout de grade logo de início |
| 5 | sprite-forge | tdimino/claude-code-minoan | Desenhar membros como blocos distintos para os ciclos moverem independentemente |
| 6 | pixel-art-animator | willibrandon/pixel-plugin | Andar de 4 frames a 100 ms como ciclo mínimo viável |
| 7 | sprite-sheet | summerengine/summer | Sheets horizontais de linha fixa, mesmo personagem |
| 8 | scenario-sprite-animation | scenario-labs/skills | Prompts de animação por ciclo |
| 9 | animate-frames | 392fyc/mercury-claude-skills | Checklists de animação quadro a quadro |
| 10 | game-animation-frames | scomofo (listagem skills.rest) | Tabelas de contagem de frames e tempo |

Leia cada SKILL.md antes de depender delas; estas notas vêm de páginas de listagem.

Mais referências: https://www.slynyrd.com/blog/2026/1/26/side-view-run-n-gun (Pixelblog 60, andar lateral de 8 frames), https://itch.io/blog/526535/pixel-art-walk-cycle-animation, https://opengameart.org/content/knight-walking.

## Como foram integradas
- Sites 1–2, 7, 9 alimentam `palette-workflow.md` e as regras de `styles.md`.
- Sites 3–4 cobrem tarefas que o MCP não faz: escreva um script Lua e rode `aseprite -b --script arquivo.lua`.
- Sites 5–6 alimentam `animation.md`.
- A ideia de nota da skill 3 virou `quality-checklist.md`.
- A skill 4 é o plano B quando o Aseprite não está disponível: desenhar com Pillow, mesmos estilos.
