# Diário de crescimento — 06/10/2026

## Status da coleta — PROBLEMA

`content/placar.md` mostra **"Última coleta: 2026-10-04"** — hoje é dia 06,
então a coleta está **2 dias atrasada**, não 1 como nos dias anteriores
(`metricas.json` confirma: o último bloco de coleta registrado também é de
10-04, nada de 10-05 nem de 10-06). O padrão normal já visto era 1 dia de
atraso (API do Instagram demora a liberar); agora dobrou. Pelas regras
desta rotina, dado de 2 dias atrás não deve ser analisado como se fosse de
hoje — por isso não vou julgar número novo neste diário.

Não investigo a causa (sem acesso à máquina local nem a outros agentes),
só registro: alguém precisa checar se `publisher/metrics.py` rodou e
falhou silenciosamente (o workflow de manutenção roda com
`continue-on-error: true`, então uma falha não quebra o job nem avisa
ninguém sozinha).

## O que dava para comparar (10-04 vs 10-03, já visto no diário de ontem)

Sem novidade além do que já foi registrado: 331→330 seguidores, zero post
novo, salvos/compartilhamentos travados em 0/0 (exceto o 1 compartilhamento
de sempre em `cenoura-filhote`), `2026-08-28_comida-servida` ainda
`pending`.

## Veredito

Não é dia de julgar crescimento — é dia de desconfiar da própria coleta.
O atraso dobrou (1 dia → 2 dias) e isso é, em si, um sinal pior que
"seguidor parado".

## Ações para o dia seguinte

1. **Robô**: investigar por que `publisher/metrics.py` não gravou coleta
   em 10-05 nem 10-06 (ver logs do workflow `maintenance.yml`, já que o
   `continue-on-error: true` esconde falha).
2. **Claude da conversa**: na próxima rodada, se o placar ainda estiver
   parado em 10-04, não repetir só o aviso — abrir o log do workflow para
   achar a causa, já que 2 dias seguidos sem gravar é padrão novo, não API
   lenta pontual.
3. **Ramon**: nada novo que só ele possa fazer hoje (segue valendo o pedido
   já registrado antes: aprovar/recusar `comida-servida`).

## 🔗 Relacionados

> Vizinhos por assunto (calculados automaticamente)

- [[diario-crescimento-2026-10-04]]
- [[diario-crescimento-2026-10-02]]
- [[diario-crescimento-2026-09-30]]
