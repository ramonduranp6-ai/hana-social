# Diário de crescimento — 28/08/2026

## Status da coleta

**Hoje (28/08) ainda não coletou.** Às 13:25 UTC (mais de 1h depois do cron
de 12:15) não há nenhum run novo do `maintenance.yml` — o último foi o de
27/08. Isso já passa o teto de atraso visto nos últimos dias (48-65 min) e
merece atenção: **o run de 27/08 rodou às 22:17 UTC, ~10h depois do horário
marcado** — bem acima do padrão normal de atraso do GitHub Actions. Ainda
não é "2 dias sem coleta" (o robô entregou dado ontem, ainda que tarde), mas
o atraso está piorando, não é mais só "scheduler lento". Vou seguir o plano
de ontem e analisar 26/08 → 27/08, que é o par novo que chegou.

## Números: 26/08 vs 27/08

- **Seguidores: 331 → 331.** Sem mudança, 4º dia seguido parado nesse
  número.
- **`2026-08-26_retrato-oficial`** (1º post no formato retrato editorial via
  Gemini): media parcial em 26/08 (poucas horas no ar) tinha alcance 23;
  medida completa em 27/08 fechou em **alcance 36**. Comparado à média das
  8 fotos no formato antigo (53 de alcance): **o retrato ficou abaixo da
  média**, não acima — a aposta no formato novo não rendeu mais alcance.
  Curtidas (12) e comentário (1) ficaram dentro do normal de foto. Resposta
  à pergunta de ontem: **o formato novo rendeu PIOR em alcance**, não
  melhor, pelo menos nesta 1ª tentativa.
- **`2026-08-K_chegada-eloen`** (Reel fora do calendário, anúncio especial,
  publicado 26/08 14h): **alcance 988, 1310 views** — 5x o Reel de melhor
  alcance até então (195). Mas **0 salvos, 0 compartilhamentos, e
  seguidores não se moveram** (331→331) apesar do pico de alcance. Achado
  real: alcance grande não está puxando conversão nenhuma — nem salvo, nem
  compartilhamento, nem seguidor novo.

## Regra de morte (formato POV "A PATROA MANDA")

Conferido: só **2 Reels** publicados nesse formato até agora —
`2026-08-12_cenoura-filhote` (publicado de fato em 22/08, teve **1
compartilhamento**) e `2026-08-14_regras-da-casa` (publicado 24/08, 0/0).
A regra de morte exige **3 Reels com 0 salvo E 0 compartilhamento nos 3**.
Não bateu ainda (só 2 Reels) — e já não pode bater nesse trio específico,
porque o `cenoura-filhote` já quebrou o 0/0 com aquele compartilhamento.
**Não declaro morte de formato.**

## Veredito

Dia sem seguidor novo e sem salvo/compartilhamento novo. O único fato novo
é negativo pro formato retrato-editorial (rendeu menos alcance que foto
antiga) e chama atenção pro Reel especial da Eloen: alcance recorde não
virou nem salvo nem seguidor — o gargalo do perfil é conversão, não
alcance, confirmando o que já tinha sido visto em 18/08.

## Ações para amanhã

1. **Claude da conversa**: assim que a coleta de 28/08 aparecer (ou de
   29/08, se seguir atrasada), comparar de novo. Se passar 2 dias corridos
   (28 e 29) sem nenhum run do `maintenance.yml`, aí sim declarar robô
   quebrado e avisar o Ramón — antes disso é atraso, não pane.
   Se sair um 2º post no formato retrato-editorial, comparar de novo com a
   média de foto (53) para ver se 26/08 foi só ruído de 1 amostra.
2. **Claude da conversa**: ao ver o próximo Reel do formato POV (o
   3º), essa peça decide se a regra de morte revive num trio novo — juntar
   `regras-da-casa` (0/0) + o novo, e checar se os dois batem 0/0.
3. **Robô**: nenhuma ação nova — só observar se o atraso do cron piora de
   novo amanhã.
