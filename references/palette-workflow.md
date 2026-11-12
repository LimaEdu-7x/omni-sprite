# Fluxo de paleta

## Escolher
1. **Dada pelo usuário** → use como está; só acrescente degraus de rampa que faltem e avise.
2. **Do Lospec** → navegue em `https://lospec.com/palette-list` (filtre por número de cores/tag). Baixe o hex: `https://lospec.com/palette-list/<slug>.hex` (um hex por linha, sem `#`).
3. **De imagem de referência** → `analyze_reference` (k-means) → reduza ao orçamento abaixo → reagrupe em rampas.
4. **Gerada** → monte as rampas à mão (abaixo) ou use a skill `/color`, que também exporta a paleta para `.hex` do Aseprite.

## Orçamento de cores
S 8–16 · M 16–24 · L 24–40 · XL/Cena 32–64. Mais cores ≠ mais detalhe; cada cor extra precisa ter função (degrau de rampa, acento, tom de pele).

## Montar uma rampa (4–5 degraus)
Parta da cor média em HSL/OKLCH. A cada degrau a partir do meio:
- Luminosidade: ±12–18 (sombras) / ±10–14 (luzes).
- Matiz: sombras giram 10–25° para azul/roxo; luzes giram 10–20° para amarelo/laranja.
- Saturação: sombras um pouco mais saturadas ou iguais; brilhos menos saturados.
Nomeie papéis, não cores: `skin_1..5`, `metal_1..4`, `cloth_main_1..4`, `accent_1..3`, `outline`, `shadow_cast`.

## Papéis que todo sprite precisa
1 cor de contorno (a mais escura, com tinta) · 1 cor de sombra no chão (meio escura, matiz do ambiente) · rampas por material · 1 acento (chama o olhar) · 1 emissiva (opcional).

## Validação
`analyze_palette_harmonies` → confira equilíbrio de temperatura e se o acento não compete com o ponto focal. Veja a faixa de amostras ampliada em ×8. Teste em escala de cinza: a ordem de valor das rampas deve ser monotônica e o sprite deve ler bem em cinza.

## Carregar no Aseprite
`set_palette` (1–256 hex). Mantenha o índice 0 transparente. Depois de pintar, `get_palette` para confirmar que nenhuma cor extra entrou (`get_pixels` em áreas suspeitas).
