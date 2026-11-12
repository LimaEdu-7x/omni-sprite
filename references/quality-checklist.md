# Checklist de qualidade (rode após cada render; corrija primeiro o pior defeito)

**Silhueta e leitura**
- [ ] Reconhecível em 1× e preenchida de preto
- [ ] Ponto focal (rosto/arma) com o maior contraste
- [ ] Hierarquia de formas clara: grande / média / pequena

**Ofício do pixel**
- [ ] Sem pixels órfãos (pixels soltos fora de um aglomerado), salvo intenção
- [ ] Sem "dobrados" (degraus de 2 px onde caberia uma linha limpa de 1 px); linhas com degraus de tamanho consistente
- [ ] Curvas com progressão suave de degraus (ex.: 1-2-3-3-2-1)
- [ ] Sem *banding* (linhas de contorno paralelas de degraus diferentes coladas no contorno)
- [ ] Sem *pillow shading* (luz irradiando do centro), exceto no estilo `cute-chibi`

**Cor**
- [ ] Dentro da paleta (`get_palette` = orçamento); sem preto/branco puros (exceto 1-bit)
- [ ] Rampas com mudança de matiz; ordem de valor monotônica; lê em escala de cinza
- [ ] Um único acento; fundo menos saturado que o sujeito

**Luz**
- [ ] Uma única direção de luz em todos os materiais
- [ ] Luz de contorno/rebatida só no lado da sombra; sombra projetada assentada no chão

**Fidelidade ao estilo**
- [ ] Segue o estilo escolhido (contorno, cores, dithering em `styles.md`)
- [ ] Só escala inteira; tamanho de pixel consistente em todo o conjunto

**Direção**
- [ ] Uma vista e um lado de olhar em todas as partes; cabeça, props e capa coerentes (veja `orientation-and-pose.md`)
- [ ] Capa/cabelo não atravessam o torso; membros distantes atrás, próximos na frente

**Animação**
- [ ] Loop contínuo; pés/pivô travados; tempo com ease; sem deriva de paleta

Relatório: liste os itens reprovados + o que foi alterado.
