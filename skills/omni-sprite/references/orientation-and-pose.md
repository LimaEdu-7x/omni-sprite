# Orientação, pose e direção (decida ANTES de desenhar)

A maioria dos personagens "estranhos" vem de misturar ângulos de câmera em um só sprite (torso de frente + cabeça de lado + espada de outro plano). Trave uma vista e derive todas as partes dela.

## 1. Escolha UMA vista e UM lado de olhar
| Vista | Use para | Notas |
|---|---|---|
| **Lateral (perfil), voltado para a direita** | plataforma, beat'em up, tudo com ciclos de andar/ataque | Padrão. Desenhe voltado para a direita; espelhe no motor para a esquerda. Nunca desenhe à mão voltado para a esquerda. |
| 3/4 top-down (RPG) | RPGs de 4/8 direções | Exige 4 ou 8 linhas separadas (S, SW/W, NW, N…); não falsifique uma direção ausente espelhando se o desenho for assimétrico. |
| Frontal / busto | retratos, UI | Simétrico; props posicionados à mão. |
| Isométrica | tática, construção de cidades | Linhas de pixel 2:1, 3 faces visíveis. |

Registre a escolha no briefing: `view=lateral, facing=direita, luz=superior-esquerda`.

## 2. Lado perto / lado longe (vista lateral)
- Os membros **próximos** (do lado da câmera) ficam na frente do torso; os **distantes**, atrás. Ordem das camadas: sombra → capa/itens das costas → membros e prop distantes → perna próxima → torso/armadura → cabeça → braço e prop próximos → FX → linhas → contorno.
- **Atribua props às mãos de propósito:** um prop por mão, segurado à frente do corpo. Exemplo: espada na mão próxima (na frente do torso, lâmina para a frente), escudo no braço distante, à frente do peito (visível além da borda do torso). Nunca ponha um prop atrás das costas, a menos que seja mochila/item de capa.
- **A cabeça olha para a direção do olhar**: viseira/placa facial, olho e queixo na frente; penacho, cabelo e capa caem para **trás**.
- **Capas se prendem nas costas dos ombros e caem para trás**; ficam na camada mais baixa, atrás do torso (use o teste de sobreposição: uma capa larga ainda pode parecer atravessar o corpo onde encontra o cinto e as pernas, então mantenha-a estreita e ancorada baixo nas costas). Balance com atraso de fase (veja animação).
- O torso é uma forma de perfil: elipse de peito + abdômen, não uma peitoral de frente.

## 3. Esqueleto primeiro, desenho depois
Defina juntas e comprimentos de segmento e derive as formas: quadril, ombro, cabeça, pé próximo/distante, mão próxima/distante, ângulo do prop. Pernas e braços usam IK de 2 ossos (coxa+canela, braço+antebraço; joelhos dobram para a frente, cotovelos para trás/baixo). Frame = pose(juntas) → formas → sombreamento. Isso mantém as proporções constantes entre os frames e torna os ciclos simples (veja `examples/knight/rig.py`).

## 4. Testes
- **Teste de silhueta:** preencha de preto; dá para distinguir frente de costas e para onde olha? Os props devem ler como formas separadas.
- Teste de espelho: espelhado na horizontal, a direção de olhar inverte de forma óbvia? (deve inverter)
- Teste de sobreposição: nada do lado distante é desenhado acima de partes do lado próximo; a capa não cobre o torso.
- Proporção: cabeça ≈ 1/7–1/6 da altura em estilo realista, 1/4–1/3 em chibi; joelhos na metade da perna; mãos chegam à metade da coxa em repouso.
- Luz: mesma direção em todas as partes; num sprite voltado para a direita com luz superior esquerda, a sombra cai sob o queixo/frente e no lado direito dos membros.

## 5. Conjuntos de direções (quando precisar de mais de um lado)
- Plataforma lateral: 1 lado (direita), espelhe para a esquerda.
- RPG 4 direções: baixo, cima, lado (espelhado para o outro) = 3 linhas desenhadas.
- 8 direções: desenhe S, SE, E, NE, N e espelhe para obter SW, W, NW só quando o desenho for simétrico (sem arma/emblema assimétrico).
Convenção de linhas usada pela skill da comunidade `character-sprite`: S, SW, W, NW, N, NE, E, SE.
