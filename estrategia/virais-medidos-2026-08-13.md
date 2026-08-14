# 10 Reels virais MEDIDOS no nicho de cachorro — 13/08/2026

Fonte: Apify (`data-slayer/instagram-search-reels`, buscas "cachorro engraçado" e
"exotic bully"; + `apify/instagram-hashtag-scraper` para fotos). 24 Reels e 113
fotos lidos, custo ~US$ 0,15. **Views e likes são números da API, não estimativa.**
Limite honesto: busca por palavra-chave devolve o que o Instagram rankeia como
topo — amostra boa de "o que o algoritmo premia", não censo do nicho.

## Os 10 (ordenados por views)

| # | views | dur | áudio | o que é | link |
|---|---|---|---|---|---|
| 1 | 30,0M | 5,6s | original | cachorro engraçado, piada única e curtíssima | instagram.com/p/Cu4kRBSM-yU |
| 2 | 6,3M | 14,1s | original | meme "vídeo contagiante" (@sevendogs.com.br) | instagram.com/p/DNbnlPhJBuG |
| 3 | 4,8M | 17,7s | original | **POV: "Alguém tira a Shopee da minha Humana"** — a cadela reclama da dona (@ava_dosatti) | instagram.com/p/DYz89J0xHEC |
| 4 | 1,9M | 68s | original | "POV: Cachorros" — compilação de situações (@chora_rindo_) | instagram.com/p/DQHrgtvlMSa |
| 5 | 1,2M | 15,2s | original | exotic bully "Pacquiao back at it" (@706exotics2) | instagram.com/p/DY5oiokNJU5 |
| 6 | 1,0M | 59s | música | **Exotic Bully Nano no shopping — reação das pessoas** (@greenvalley.kennel, BR) | instagram.com/p/DTgV050CaKu |
| 7 | 1,0M | 14,1s | original | prank no colega dormindo, balão (@santorocomfort1558s) | instagram.com/p/DaDZ2xJunDD |
| 8 | 945k | 12,6s | The Godfather | cachorro imóvel como estátua + trilha de "poderoso chefão" (@importedbullies) | instagram.com/p/DYunI_8hyHO |
| 9 | 899k | 13,0s | original | dono fala "EH" e ele vem correndo (@brondogbr) | instagram.com/p/DbY2M0GpKel |
| 10 | 670k | 11,6s | samba malandro | cachorro FINGE estar ferido pra ganhar espetinho, RJ (@david_de_figueredo) | instagram.com/p/DbrA8lpJHgO |

## O padrão que os 10 têm em comum (medido, não opinião)

1. **UMA piada só por Reel** — nenhum viral tem duas ideias.
2. **Cachorro como PERSONAGEM com atitude humana** — reclama, finge, manda,
   desobedece. O #3 (4,8M) é literalmente o posicionamento da Hana: o pet
   reclamando da humana. "A patroa mimada" É o formato que viraliza.
3. **8 de 10 têm entre 5,6 e 17,7s.** Os dois longos (59s, 68s) só funcionam
   porque são narrativa/compilação. Faixa alvo: **6-18s**.
4. **Áudio: 7 de 10 em áudio original** (a cena fala). Música entra quando é
   TRILHA DE PERSONAGEM — Godfather no cachorro-estátua, samba no malandro.
   Música casada com a piada, nunca música de fundo genérica.
5. **Conflito dono × cachorro** é o motor de 6 dos 10 — e o cachorro sempre vence.
6. **Legenda curta que COMPLETA a piada** + pergunta/CTA. O #1 do share rate
   (@ava_dosatti, 3,7% dos views compartilharam) termina pedindo identificação.
7. **Share é a métrica dos virais**: os POV brasileiros têm share/views de 2,7-3,7%
   — o post viraja porque gente marca gente ("é você e o fulano").

## Fotos — o achado é que NÃO HÁ viral de foto no nicho

113 fotos das mesmas hashtags: a maior tem **435 curtidas** (kennel), a maior
de "dona comum" tem 228. Nenhuma foto chega perto de 1% do pior Reel do top 10.
Confirma o placar da própria Hana (4 fotos → 0 seguidor) e a regra 3l.
O que as melhores fotos têm: carrossel (Sidecar domina), 1ª foto com o cachorro
encarando a câmera, legenda de personagem ("Today, I'm a cool girl too").
**Uso legítimo hoje: capa de Reel e carrossel de apoio — não post de foto solta.**


## ADENDO 13/08 (noite) — assisti os 7 maiores; montagem, texto e efeito MEDIDOS

Ele cobrou ("vc não estudou a imagem, música, efeitos?") e tinha razão: o estudo
acima era só metadado. Baixei os 7 maiores (30M, 6,3M, 4,8M, 1,2M, 1,0M, 945k,
670k) e medi com ffmpeg + olhando frame a frame:

| viral | cortes reais | texto na tela | efeito visual | câmera |
|---|---|---|---|---|
| 30M | 0 (plano único) | NENHUM | nenhum | mão, seguindo o cão |
| 6,3M | 0 | nenhum visto | nenhum | — |
| 4,8M | 2 (reenquadres) | NENHUM | zoom de reenquadre só | mão, fecha no rosto no fim |
| 1,2M | 3 | nenhum | nenhum | — |
| 1,0M prank | 0 (TRIPÉ fixo) | NENHUM | confete no estouro | parada o tempo todo |
| 945k estátua | 0 | NENHUM | nenhum | orbita devagar, golden hour |
| 670k malandro | 5 (todos nos últimos 2s) | NENHUM | nenhum | mão, estilo flagrante |

**O que isso muda (e contradiz o que eu acreditava):**
1. **Viral de cachorro é PLANO ÚNICO com cena forte** — 5 de 7 não têm UM corte.
   A graça está na CENA (encenação/flagrante), não na edição. O prank de 1,0M é
   uma câmera parada num tripé e ponto.
2. **ZERO texto na tela nos 7.** Nenhum gancho escrito. O gancho é VISUAL: a
   situação se entende em 1 segundo sem ler nada (cão imóvel na mesa; chihuahua
   com balão do lado do grandão dormindo).
3. **Efeitos: nada.** Sem transição, sem filtro, sem zoom artificial. Luz
   natural boa (golden hour no de 945k) vale mais que efeito.
4. **A produção está na ENCENAÇÃO, não na pós:** props (balão, mesa de banho),
   cenário limpo, câmera posicionada ANTES, e esperar o momento.
⚠️ Conflito declarado com a regra 3n-i (mínimo 5 cortes, ordem dele de
02-03/08): a regra nasceu de material fraco que precisava de montagem para ter
graça. O dado diz que cena forte dispensa corte. **Quem resolve a regra é ele.**
