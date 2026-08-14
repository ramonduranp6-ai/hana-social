---
name: reel-viral
description: Receita medida (13/08/2026, 24 Reels com views reais via Apify) para criar Reel da Hana com padrão viral. Use SEMPRE ao criar, roteirizar ou julgar um Reel — junto com o diretor-reels, antes de montar_reel.py. Contém o prompt de produção e o checklist de reprovação.
---

# Reel viral — a receita medida do nicho

Base: `estrategia/virais-medidos-2026-08-13.md` (10 virais de 670 mil a 30
milhões de views, números da API — reler quando for atualizar esta skill).
**Esta skill NÃO substitui as regras da `hana-social`** (3i auditor, 3n-i
mínimo 5 cortes/trilha/história, 3e música combina com a cena, 3f vetos,
2c repetição): ela diz O QUE fazer; a hana-social diz o que é PROIBIDO.

## ⚡ O que os 7 maiores mostraram QUANDO ASSISTIDOS (13/08, ffmpeg + frames)

- **Plano único vence:** 5 de 7 virais não têm UM corte. A graça está na CENA
  encenada (props, câmera no tripé posicionada antes, esperar o momento) —
  não na edição. ⚠️ Conflita com a regra 3n-i (mín. 5 cortes); enquanto ele
  não decidir, a 3n-i vale para montagem de acervo e o plano único vale para
  CENA NOVA encenada forte.
- **ZERO texto na tela nos 7.** O gancho é visual: a situação se entende em
  1 segundo sem ler. Texto só quando a cena sozinha não conta a história.
- **Efeitos: nenhum.** Sem transição, filtro ou zoom artificial. Luz natural
  boa (golden hour) vale mais que qualquer efeito.
- **Câmera:** tripé fixo (prank, estátua) ou mão acompanhando (POV). Fecha no
  ROSTO no desfecho (o de 4,8M termina em close do focinho sorrindo).

## O padrão dos virais (medido, não opinião)

1. **UMA piada só.** Nenhum viral tem duas ideias. Se o roteiro precisa de
   "e depois…", corta em dois Reels.
2. **A Hana é PERSONAGEM, não bicho fofo.** Os virais têm o cachorro com
   atitude humana: reclama, finge, manda, desobedece. O 3º maior (4,8M) é
   um pet reclamando da dona — exatamente "a patroa mimada". Confiar no
   posicionamento: ele É o formato que viraliza.
3. **6 a 18 segundos.** 8 dos 10 virais estão em 5,6-17,7s. Acima de 20s só
   com narrativa que muda de estado no meio (ex.: shopping/reação, 1,0M).
4. **Conflito dono × cachorro, e a Hana SEMPRE vence** (bate com o pilar
   A PATROA MANDA e com a regra dos INIMIGOS: expulsa ou ignora, nunca foge).
5. **Áudio: a cena fala primeiro.** 7 de 10 virais rodam em áudio original.
   Música entra quando é TRILHA DE PERSONAGEM — casada com a piada (Godfather
   no cachorro-estátua; samba no malandro) — nunca fundo genérico.
6. **Legenda completa a piada e pede identificação/marcação.** O maior share
   rate (3,7%) termina com CTA de marcar alguém. Share é a métrica que
   viraliza — otimizar para "vou mandar pro fulano", não para curtida.

## O PROMPT DE PRODUÇÃO (usar ao encomendar o roteiro ao diretor-reels)

> Crie UM Reel da Hana (Exotic Bully Micro, "a patroa mimada") com UMA piada
> só, 6-18s, mínimo 5 cortes, a partir DESTE material: [listar clipes reais
> disponíveis e o que acontece em cada um]. A Hana é personagem com atitude:
> o conflito é dono × cadela e ELA vence (expulsa, ignora ou é servida —
> nunca medo). Estrutura: gancho visual/sonoro nos 2 primeiros segundos
> (rosto dela no quadro) → escalada → virada em que ela vence → corte seco
> final (sem sobra parada). Áudio: original da cena se a cena tem som que
> conta a história; senão trilha DE PERSONAGEM que faça piada com a cena
> (instrumental, tom criança/cachorro, sem Anitta/Xuxa, sem funk, sem
> tristeza). Máx. 3 frases de texto na tela. Legenda: 1-2 linhas que
> completam a piada + pergunta que pede identificação/marcação, PT-BR,
> máx. 4 hashtags. Entregar: roteiro batida a batida em JSON do
> montar_reel.py + justificativa de trilha em 1 linha.

## Checklist de reprovação (o Reel NÃO sai se falhar em qualquer um)

- [ ] Tem mais de uma ideia/piada → REPROVA (dividir).
- [ ] Rosto da Hana ausente dos 2 primeiros segundos → REPROVA.
- [ ] Mais de 18s sem mudança de estado no meio → REPROVA (encurtar).
- [ ] A Hana perde/foge/apanha do conflito → REPROVA (contradiz o posicionamento).
- [ ] Música de fundo genérica sem relação com a piada → trocar por áudio
      original ou trilha de personagem.
- [ ] Legenda não pede marcação/identificação → reescrever (share é a métrica).
- [ ] E os portões de sempre: auditor (3i), repetição (2c), aprovação dele.

## Manutenção

Repetir a medição a cada ~4-6 semanas (custa ~US$ 0,15):
`data-slayer/instagram-search-reels` com "cachorro engraçado" e "exotic bully",
2 páginas cada, rankear por `play_count`, atualizar o arquivo de estratégia e
esta skill se o padrão mudar.
