# Diário de crescimento — 28/09/2026

## Status da coleta — PROBLEMA

`placar.md` ainda mostra última coleta em **2026-09-27** — não atualizou hoje.
Conferido na fonte (`actions_list` do GitHub, não suposto): o
`maintenance.yml` (que roda `metrics.py` às 12:15 UTC) **não rodou hoje** —
o último run bem-sucedido dele foi 27/09 16:59 UTC. Os runs de hoje no
histórico são só do vigia de saúde, não da manutenção. Por isso não comparo
"hoje vs ontem": uso a coleta de 09-27 vs 09-26, que ainda não tinha sido
analisada (o diário de ontem comparou 09-26 vs 09-25).

## Números: coleta 09-27 vs 09-26

- **Seguidores: 330** (+1 desde 09-26). Dentro da faixa de ruído 329-331 de
  sempre, sem tendência.
- **Post a post: sem post novo.** Ainda os mesmos 13 posts — **33 dias sem
  publicar** desde `2026-08-26_retrato-oficial`.
- **Salvos/compartilhamentos: zero mudança.** 12 dos 13 posts em 0/0; só
  `cenoura-filhote` com 1 compartilhamento, de sempre.
- `2026-08-28_comida-servida` segue `status: pending`, auditoria
  `SEM OBJECAO` desde 28/08 — **31 dias parada** esperando aprovação do
  Ramón.

## Regra de morte (formato POV "A PATROA MANDA")

Sem mudança: só 2 Reels do formato foram ao ar. A 3ª peça (`comida-servida`)
segue travada na fila — regra de morte ainda não julgável.

## Veredito

Sem novidade real: o +1 de seguidor é ruído, não há post novo, e a
manutenção diária (que gera o placar) não rodou hoje.

## Ações para amanhã

1. **Ramon**: aprovar ou recusar `2026-08-28_comida-servida` — 31 dias
   parado, é a única coisa que destrava dado novo.
2. **Robô**: se `maintenance.yml` continuar sem rodar amanhã no horário,
   é bug de agendamento (GitHub Actions), não de dado — investigar o
   workflow, não só ler o placar.
3. **Claude da conversa**: quando `comida-servida` for ao ar, comparar
   alcance com a média dos outros Reels do pilar e checar
   salvo/compartilhamento; julgar a regra de morte do formato POV quando
   os 3 Reels estiverem publicados.
