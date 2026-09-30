# Diário de crescimento — 30/09/2026

## Status da coleta — PROBLEMA (3º dia seguido)

`placar.md` ainda mostra **"Última coleta: 2026-09-29"** — não é de hoje.
O cron da manutenção roda 12:15 UTC; agora são ~13:15 UTC, 1h depois, e
ainda não apareceu commit de coleta novo hoje. Isso já é padrão dos
últimos dias (28/09 e 29/09 também atrasaram, chegando à noite). Por isso
não comparo "hoje vs ontem" com dado de hoje — uso a coleta de 09-29 vs
09-28, que ainda não tinha entrado em diário (o de ontem foi escrito antes
dela chegar).

## Números: coleta 09-29 vs 09-28

- **Seguidores: 331** (+0 desde 28/09). Mesma faixa de ruído 329-331 de
  sempre, sem tendência de subida ou queda.
- **Post a post: sem post novo.** Ainda os mesmos 13 posts — **35 dias sem
  publicar** desde `2026-08-26_retrato-oficial`.
- **Salvos/compartilhamentos: zero mudança.** 12 dos 13 posts continuam em
  0/0; só `cenoura-filhote` com 1 compartilhamento, de sempre. Meta de
  tirar salvo/compartilhamento do zero segue sem nenhum sinal novo.
- `2026-08-28_comida-servida` segue `status: pending` no `post.json`,
  auditoria `SEM OBJECAO` desde 28/08 — **33 dias parada** esperando só a
  aprovação do Ramón (conferido no arquivo, não suposto).

## Regra de morte (formato POV "A PATROA MANDA")

Sem mudança: só 2 Reels do formato foram ao ar. A 3ª peça
(`comida-servida`) segue travada na fila — regra de morte ainda não
julgável até ela publicar.

## Veredito

Sem novidade real de crescimento (+0 seguidor, nenhum post novo, salvos e
compartilhamentos travados em zero), e a manutenção que gera o placar está
atrasando 3 dias seguidos — vale acompanhar se vira bug de agendamento.

## Ações para o dia seguinte

1. **Robô**: se `maintenance.yml` atrasar um 4º dia seguido do horário
   (12:15 UTC), passa de "atraso" para "bug de agendamento" — investigar
   o workflow, não só esperar.
2. **Ramon**: aprovar ou recusar `2026-08-28_comida-servida` — 33 dias
   parado, é a única coisa capaz de gerar dado novo (post novo, chance de
   sair do zero em salvo/compartilhamento).
3. **Claude da conversa**: quando `comida-servida` for ao ar, comparar
   alcance com a média dos outros Reels do pilar, checar
   salvo/compartilhamento, e só então julgar a regra de morte do formato
   POV (3 Reels publicados).
