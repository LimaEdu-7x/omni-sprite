# Animação

## Configuração
- Mesma tela em todos os frames; linha-base dos pés numa linha fixa; pivô constante.
- Frames em um único arquivo Aseprite, **uma tag por ciclo** (`create_tag`, direção forward/pingpong). Use camadas por parte do corpo só se for reposicionar; senão redesenhe em `base`.
- Partes estáticas (ex.: fundo, prop segurado): `link_cel`.

## Abordagem por esqueleto (recomendada)
Calcule cada frame a partir de juntas em vez de redesenhar: deslocamentos de quadril/ombro/cabeça, alvos dos pés (perto/longe: apoio = deslizar linear para trás no chão, passada = smoothstep para a frente com arco de elevação), alvos das mãos, ângulo do prop, fase da capa/penacho. IK de 2 ossos para pernas e braços (joelhos para a frente, cotovelos para trás). Andar: quadril mais baixo no contato, mais alto na passagem (2 quicadas por ciclo); braços opostos às pernas; capa e penacho atrasados em fase. Ataque: pronto → preparação → pico → golpe (rastro de corte, 50–60 ms) → impacto (segurar) → recuperação. Implementação completa: `rig.py` + `make_anims.py` em https://github.com/LimaEdu-7x/omni-sprite/tree/main/examples/knight (idle 6f, andar 8f, ataque 6f, tags, GIF + spritesheet + JSON).

## Processo
1. Poses-chave (extremos) → 2. poses de quebra/passagem → 3. intermediários → 4. acabamento (movimento secundário, rastros/FX) → 5. ajuste de tempo → 6. teste de loop (último→primeiro deve ser contínuo).
Use `duplicate_frame` e edite; nunca redesenhe do zero.

## Receitas de ciclo (vista lateral, personagem nível L)
| Ciclo | Frames | ms por frame | Notas |
|---|---|---|---|
| idle | 4–8 | 150–200 | balanço de 1–2 px no peito/cabeça, tecido/cabelo 1 frame atrasado |
| andar | 6–8 | 100–125 | contato, baixo, passagem, alto ×2 lados; cabeça mais baixa no "baixo" |
| correr | 6–8 | 70–90 | inclinação maior, frame no ar, braços a 90° |
| pular | 4–6 | variável | antecipação (agachar) 1f, subida, ápice (segurar), queda, aterrissagem (agachar) |
| ataque corpo a corpo | 5–8 | antecipação 120, golpe 40–60, recuperação 100 | rastro/arco no frame do golpe; segure o frame de impacto por 2 ticks extras |
| dano | 2–3 | 80–100 | flash de troca de paleta (branco) no frame 1, recuo |
| morte | 6–10 | 100–150 | o último frame se mantém |
| conjurar/atirar | 6–8 | 100 | antecipação clara; FX na camada `fx` |

## Princípios
Antecipação → ação → continuação; ease in/out por **espaçamento de frames** (mais frames perto dos extremos); *squash & stretch* de 1–2 px no nível L; arcos nos membros; ação sobreposta em cabelo/capa/rabo (1–2 frames de atraso). 8–12 fps é o padrão em pixel art; segure poses importantes com `set_frame_duration` mais longo em vez de duplicar frames.

## Cor e sombra em movimento
A direção da luz nunca muda. Paleta fixa; sem cores novas entre frames (confira `get_palette`). Movimento em subpixel: desloque os aglomerados de sombra em 1 px, não refaça o dither a cada frame (cintilação), exceto em efeitos deliberados.

## Exportar
- `export_sprite` GIF (prévia) e PNG por tag, se necessário.
- `export_spritesheet` com layout `rows`/`horizontal` e JSON de metadados (tags, durações) para motores de jogo.
