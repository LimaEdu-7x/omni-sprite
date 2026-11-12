---
name: sprite
argument-hint: "[descrição do sprite] [--tamanho S|M|L|XL|cena] [--estilo hd-pixel|snes|gba|...] [--anim idle,walk,attack] [--paleta slug|#hex] [--vista lateral|3-4|frontal|iso]"
user-invocable: true
description: Cria sprites, tilesets e animações de pixel art grandes e detalhadas no Aseprite pelo servidor pixel-mcp. Use quando o usuário pedir sprite, personagem, tile, ícone, cena de pixel art, spritesheet, ciclo de animação ou um estilo específico (8-bit, 16-bit, GBA, HD pixel, dark fantasy, cyberpunk, isométrico). Also triggers on English requests for sprites, pixel art, sprite sheets and animation cycles. Impõe níveis de resolução, paleta primeiro, direção travada, camadas e revisão visual para que o resultado não fique pequeno e chapado.
---

# OmniSprite 🎮✨ — comando `/sprite`

Fluxo cirúrgico de pixel art sobre o servidor `pixel-mcp` do Aseprite (catálogo de ferramentas: `references/mcp-tools.md`). Responda ao usuário no idioma dele.

## Comando `/sprite`
Uso: `/sprite [descrição] [flags]`. Sem argumentos, pergunte o que criar.

| Flag | Efeito |
|---|---|
| `--tamanho S\|M\|L\|XL\|cena` | nível de tamanho (padrão `L`, 128×128) |
| `--estilo <preset>` | um dos 12 estilos de `references/styles.md` (padrão `hd-pixel`) |
| `--vista lateral\|3-4\|frontal\|iso` | vista travada (padrão lateral, voltado para a direita) |
| `--anim idle,walk,attack,...` | ciclos a animar (receitas em `references/animation.md`) |
| `--paleta <slug-lospec\|#hex,#hex\|ref:caminho>` | paleta dada, do Lospec ou derivada de uma imagem |
| `--doctor` | só diagnostica: Aseprite encontrado? MCP registrado? (passos do item 0) |
| `--compilar` | força o fluxo de compilar o Aseprite do código-fonte (item 0.4a) |

Flags informadas dispensam a pergunta correspondente do briefing; o que faltar vai para a rodada de `grill-me`. Ex.: `/sprite cavaleiro dark fantasy --tamanho L --anim idle,walk,attack`.

## 0. Pré-requisitos (plug and play; verifique uma vez e corrija o que faltar)
1. **As ferramentas MCP estão visíveis?** (`create_canvas`, `draw_pixels`, `export_sprite`…). Se sim, vá ao passo 1.
2. **Se não, encontre o Aseprite:** rode `scripts/find-aseprite.ps1` (Windows) ou `scripts/find-aseprite.sh`. Saída 0 imprime o caminho; saída 2 = não encontrado.
3. **Aseprite encontrado →** rode `scripts/install-mcp.ps1` / `.sh` (detecta sozinho, baixa a versão fixa do `pixel-mcp`, confere o SHA-256 e registra). Peça ao usuário para reiniciar o cliente e continue.
4. **Aseprite NÃO encontrado →** pergunte ao usuário (uma pergunta, com opções); não assuma:
   - *"O Aseprite não está instalado. Quer que eu baixe o código dele do GitHub, compile e configure? (precisa de git, CMake, Ninja e um compilador C++; leva cerca de 10–40 min; a licença do Aseprite permite compilar para uso pessoal, não redistribuir o binário.)"*
   - Opções: **(a) Sim, compile para mim** (recomendado) · **(b) Eu instalo sozinho** (Steam / aseprite.org / itch.io; pago, apoia o desenvolvedor) · **(c) Pular o Aseprite** e usar o plano B com Python/Pillow (sem arquivo `.aseprite`, mesmas regras de estilo).
   - Em (a): rode `scripts/build-aseprite.ps1` (Windows) ou `scripts/build-aseprite.sh`. Se faltar um pré-requisito, diga qual e ofereça instalá-lo com o gerenciador de pacotes da plataforma (winget / brew / apt) **depois de perguntar**. Em caso de falha, siga `references/build-aseprite.md`. Ao terminar, execute o passo 3.
5. Nunca desenhe antes de fechar o briefing (seção 1). Respostas faltando → pergunte, ou use o padrão e diga qual.

## 1. Briefing (use `grill-me` se estiver instalada)
Faça as perguntas abaixo como uma rodada curta de `grill-me` (todas as perguntas independentes juntas, cada uma com resposta recomendada, para "sim" aceitar); se a skill não existir, pergunte normalmente. Pergunte só o que falta.

| Pergunta | Padrão se sem resposta |
|---|---|
| O que é, em uma frase + clima? | – |
| Onde será usado (gênero do jogo, UI, impressão)? Câmera: lateral / 3/4 top-down / isométrica / frontal | vista lateral |
| Estilo (veja `references/styles.md`) | `hd-pixel` |
| Nível de tamanho (tabela abaixo) | `L` |
| Animação? quais ciclos | nenhuma |
| Paleta: dada / escolher no Lospec / derivar de referência | derivar com a skill `color` (`/color`) se existir, senão Lospec |

## 2. Níveis de tamanho (vá além do "tamanho de ícone"; continue sendo pixel art)
| Nível | Tela | Uso típico | Cores |
|---|---|---|---|
| S | 32×32 | itens, ícones | 8–16 |
| M | 64×64 | personagens pequenos, props | 16–24 |
| **L** | **128×128** | personagens principais, props detalhados | 24–40 |
| XL | 192×192 / 256×256 | retratos de herói, chefes | 32–64 |
| Cena | 320×180 ou 480×270 | cenários, key art | 32–64 |

Regra: o pixel é **quadrado e nunca escalado com valor não inteiro**. Detalhe vem de mais pixels, não de desfoque. Se o usuário pedir "mais detalhe", suba um nível antes de adicionar ruído.

## 3. Paleta primeiro
1. Escolha/derive a paleta (`references/palette-workflow.md`; hex do Lospec: `https://lospec.com/palette-list/<slug>.hex`).
2. `create_canvas` em modo de cor **indexado**, depois `set_palette`. Ordene a paleta do escuro ao claro dentro de cada rampa (`sort_palette` por matiz e depois luminância, se preciso).
3. Monte **rampas**, não cores soltas: 3–5 degraus por material (sombra, meio, luz, brilho), com mudança de matiz (sombras → mais frias/saturadas, luzes → mais quentes). Confira com `analyze_palette_harmonies`.
4. Passe `use_palette: true` nas chamadas de desenho para cada pixel se ajustar à paleta.

## 3b. Orientação e pose (trave antes de desenhar; veja `references/orientation-and-pose.md`)
Declare `view` (lateral / 3/4 / frontal / isométrica), `facing` (desenhe vistas laterais voltadas para a direita), direção da luz, qual mão segura qual prop e para onde capa/cabelo caem. Regras: membros do lado da câmera na frente do torso, os do lado oposto atrás, cabeça voltada para a direção do olhar, capas presas nas costas e na camada mais baixa, um prop por mão, à frente do corpo. Para qualquer coisa animada, **monte o esqueleto primeiro**: juntas + IK de 2 ossos, depois as formas (`rig.py` em https://github.com/LimaEdu-7x/omni-sprite/tree/main/examples/knight). Faça os testes de silhueta/espelho/sobreposição após o primeiro render.

## 4. Ordem de construção (camadas, sempre nesta ordem)
Crie camadas de baixo para cima com `add_layer`: `bg`, `shadow-cast`, `base`, `shade`, `light`, `detail`, `outline`, `fx`.
1. **Silhueta** – preencha a forma toda com uma cor escura chapada em `base`. Leia em 1×: se não for reconhecível como silhueta, refaça. Assimetria forte, separação clara de cabeça/torso/membros, espaço negativo legível.
2. **Cores chapadas** – um tom médio por material com `fill_area` / `draw_rectangle` / `draw_circle` / `draw_contour`.
3. **Sombra de forma** – escolha UMA direção de luz (padrão: superior esquerda). Use `apply_shading` (estilo *hard* para nítido, *smooth* para HD) em `shade`/`light`; adicione luz de contorno seletiva no lado oposto à luz principal.
4. **Textura e detalhe** – `draw_with_dither` só onde o estilo permitir (veja estilos); `draw_pixels` manual para olhos, costuras, fivelas, brilhos. Agrupe pixels; evite pixels soltos (ruído) e "serrilhado" (degraus irregulares nas linhas).
5. **Contorno** – `apply_outline` e depois ajuste à mão: contorno seletivo (cor mais escura com mudança de matiz, não preto puro) para HD; contorno escuro completo para 8/16-bit; nenhum para "sem contorno".
6. **Antialiasing** – `suggest_antialiasing` em curvas/diagonais (pule em 1-bit/NES).
7. **FX** – brilho, faíscas, sombra no chão em `fx`/`shadow-cast`.

Para formas orgânicas complexas use o **método da grade**: escreva o sprite como grade ASCII (um caractere = índice da paleta), converta com `scripts/grid_to_pixels.py` em um lote de `draw_pixels` (veja `references/grid-method.md`). Áreas grandes com ferramentas de forma, detalhes com a grade.

## 5. Ciclo de renderizar e revisar (obrigatório)
Após cada etapa importante: `export_sprite` PNG → cópia com `scale_sprite` ×4 (nearest) ou PNG ampliado → **olhe a imagem** (Read no PNG). Passe o checklist de `references/quality-checklist.md`. Corrija o pior defeito e renderize de novo. No máximo 3 ciclos por etapa; depois relate o que sobrou.

## 6. Animação (quando pedida)
Siga `references/animation.md`: poses-chave primeiro, depois intermediárias, 8–12 fps (`set_frame_duration` 80–125 ms), uma tag por ciclo (`create_tag`: idle, walk, run, attack, hurt, death), `duplicate_frame` + edição, `link_cel` para partes estáticas, pivô/pés travados na mesma linha de pixels. Exporte com `export_sprite` (GIF de prévia) e `export_spritesheet` (+JSON).

## 7. Entrega
Salve o `.aseprite` (`save_as`), exporte PNG 1×, PNG de prévia ×4 e, para animação, GIF + sheet + JSON. Informe: tamanho da tela, nome/número de cores da paleta, direção da luz, estilo e caminhos dos arquivos.

## Armadilhas (verificadas no pixel-mcp 0.5.0)
- `create_canvas` devolve JSON `{"file_path": ...}`; esse caminho é o `sprite_path` de todas as outras ferramentas. Não há parâmetro de nome; use `save_as` para nomear.
- **Use barras normais** em `output_path` (`C:/Users/eu/saida.png`). Barras invertidas quebram o Lua gerado (`\U` é lido como escape) e falham com "invalid character 'U'".
- `scale_sprite` altera o sprite **no lugar**: faça `save_as` de uma cópia, escale a cópia e exporte.
- Números de frame começam em 1 (`export_sprite` com frame 0 = todos).
- `draw_pixels` recebe `[{x,y,color}]`, até ~10 000 por chamada; é o que `grid_to_pixels.py` gera.
- Ao falar com o servidor por stdio: JSON-RPC por linha, escreva bytes com `\n` (CRLF falha com "invalid trailing data").
- Um exemplo completo (esqueleto → partes sombreadas → camadas → exportações) está em https://github.com/LimaEdu-7x/omni-sprite/tree/main/examples/knight.

## Referências extras (carregue sob demanda)
- `references/build-aseprite.md` – compilar o Aseprite do código-fonte e resolver falhas.
- `references/orientation-and-pose.md` – vista/lado de olhar, camadas perto/longe, rigs, conjuntos de direções.
- `references/styles.md` – 12 estilos com regras exatas.
- `references/palette-workflow.md` – rampas, mudança de matiz, paletas do Lospec, orçamento de cores.
- `references/animation.md` – ciclos, frames, tempos, easing.
- `references/quality-checklist.md` – lista de revisão aprovado/reprovado.
- `references/resources.md` – 12+ sites e 20+ skills/servidores da comunidade para estudar e integrar.
- `references/mcp-tools.md` – catálogo de ferramentas.
- Skills companheiras opcionais: `color` / `/color` (escolha e espelho de paleta), uma skill de design frontend se os sprites forem para uma UI web.

## Limites honestos
Desenhar pixel a pixel por chamadas de ferramenta é lento e o modelo não "enxerga" a tela sem exportar. Prefira formas + método da grade + ciclo de revisão; use `analyze_reference` / `downsample_image` quando o usuário enviar uma imagem de referência.
