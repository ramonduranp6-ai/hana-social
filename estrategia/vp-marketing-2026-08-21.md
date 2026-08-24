# Ciclo do VP de Marketing — 21/08/2026 (12:20 UTC)

Rodada automática. **Nada foi publicado, aprovado ou teve status alterado neste ciclo** —
o VP só analisa, prepara, atribui e cobra. Publicação continua exigindo o Ramón.

## Veredito da rodada: **NÃO TESTADO — e isso conta como NÃO ENTREGA do time**

331 seguidores, **+0 em 12 dias**. 9/9 posts com **0 salvo e 0 compartilhamento**
(fonte: `content/placar.md`, coleta 21/08 pela API do IG). Nada foi testado porque
**nada foi ao ar desde 10/08** — 11 dias de silêncio por um portão de auditoria que
nenhum código alimentava. A culpa não é do algoritmo nem do Ramón: faltou dono da
pergunta *"publicou de verdade?"*. Terceira semana seguida sem teste válido.

### Achado novo deste ciclo (conferido no arquivo, não relatado)

A legenda nova com CTA de salvar (`content/legendas-pov-2026-08-21.md`, escrita hoje
de madrugada) **não foi colada em post.json nenhum**. `regras-da-casa` (14:00Z hoje) e
`cenoura-filhote` (14:00Z amanhã) ainda carregam o CTA-pergunta que o próprio time
declarou morto em 18/08:

| Peça | Legenda que vai ao ar hoje/amanhã | Deveria ser |
|---|---|---|
| regras-da-casa | "Quem assina as regras aí na sua casa: você ou o pet?" | "Regra 1: o sofá é meu. (…) **Salva** pra ele reler depois." + marcação nomeada |
| cenoura-filhote | "Quando foi que essa troca aconteceu aí na sua casa?" | versão 3 do pacote POV, com CTA de salvar embutido |

Consequência: a única janela de teste de 48h seria gasta com a munição velha.

**Dois achados secundários:** (1) essas duas peças **não são o formato POV** — são peças
de 12 e 14/08 do mesmo pilar; a regra de morte de 18/08 (3 Reels POV) segue com **0 de 3
no ar**, parada há 3 dias. (2) Depois de 22/08 a fila fica **vazia** — 6 rejeitadas (todas
do pilar único) e `chegada-eloen` sem data. O buraco recomeça em 23/08.

## Veredito por diretor

| Diretor | Veredito | Entregou | Ficou devendo |
|---|---|---|---|
| diretor-redes | **ENTREGA** | Consertou o portão da auditoria e o cron de reforço (ainda apontava 11:00Z), remarcou os 2 Reels para o pico real, escreveu a linha de corte (commit `0e6b5f9`) | Não conferiu se a legenda nova entrou na peça. Sem falha acumulada. |
| diretor-reels | **ENTREGA parcial / NÃO TESTADO** | Roteiro POV #1 "A PATROA MANDOU" (13s, plano único, zero texto, R$ 0) | Arquivo untracked; não resolveu o buraco de 23/08. 1ª cobrança — a filmagem é do Ramón e não conta contra ele. |
| diretor-criativo | **ENTREGA de peça / falha de execução** | 3 legendas POV com CTA de salvar + marcação nomeada, painel de 3 IAs e revisão cruzada | Escreveu e não colou. **1ª falha registrada** — copy que não chega no post.json é copy que não existe. |
| diretor-atualidades | **NÃO ENTREGA — 2ª SEGUIDA** | Nada | Nada em `estrategia/` nesta rodada; na anterior, quem levantou fontes foi o diretor-pesquisa. Grok está com crédito — não há desculpa técnica. |

## Ordens desta rodada

| nº | Dono | Tarefa | Entregável | Prazo (UTC) |
|---|---|---|---|---|
| 1 | diretor-redes | Preparar a troca de legenda das 2 peças pelas versões 2 e 3 do pacote POV e **pedir ao Ramón um sim/não de uma linha** (ele aprovou a legenda velha em 17/08 — trocar sozinho seria aprovar no lugar dele) | Recado no Telegram + patch pronto para aplicar em 1 comando | hoje **13:30Z** |
| 2 | diretor-redes | Provar por execução (não por relato) que `regras-da-casa` foi ao ar: log do run + ID do post | Linha datada em `ESTADO-ATUAL.md` | hoje **15:00Z** |
| 3 | diretor-redes | Coletar 48h e julgar contra a linha de corte (share ≥3 / salvo ≥3 / alcance ≥250) | `placar.md` atualizado + veredito em `ESTADO-ATUAL.md` | **23/08 15:00Z** |
| 4 | diretor-reels | Tapar o buraco de 23/08: 1 peça publicável **sem filmagem nova**, ou declaração formal de impossibilidade com o motivo | `estrategia/fila-23-08.md` + post.json em `content/queue/` com status `draft` (sem aprovar) | **22/08 12:00Z** |
| 5 | reels + criativo | Commitar os 2 arquivos untracked. Arquivo não commitado = trabalho que não aconteceu | Commit único | hoje **16:00Z** — *cumprido neste ciclo* |
| 6 | diretor-criativo | O pilar é único e nunca teve alternativa testada: 3 conceitos de um **pilar B** executável sem filmagem nova | `content/pilar-b-2026-08-21.md` | **22/08 18:00Z** |
| 7 | diretor-atualidades | Última régua: 5 contas do nicho que ganharam salvo/share nos últimos 14 dias, **com link e data verificáveis** | `estrategia/atualidades-2026-08-22.md` | **22/08 12:00Z** |
| 8 | diretor-redes | Um recado único ao Ramón com as 4 coisas que só ele faz: filmar POV #1 (10 min), 3 Highlights (2 min), data do Eloen, recarga do Gemini | Recado enviado + resposta registrada | hoje **18:00Z** |

## Risco e decisão dura (sem suavizar)

- **Recomendação de troca:** aposentar o **diretor-atualidades** deste projeto (ou trocar
  o motor dele) se a ordem 7 não vier com link e data até 22/08 12:00Z. Duas rodadas
  seguidas sem entregável verificável, com o Grok funcionando. **Quem decide é o Ramón.**
- **Regra de morte mais perto de vencer: 23/08 15:00Z.** Se as 2 peças derem alcance ≥182
  e 0 salvo / 0 share, é o **10º zero seguido** e o pilar "A PATROA MANDA" morre — não
  reagenda. **Ressalva do VP:** se saírem com a legenda velha (ordem 1 não cumprida), o
  teste está contaminado e **não se mata o pilar com esse dado** — teria queimado 48h
  medindo a hipótese errada. É por isso que a ordem 1 é a mais urgente das oito.
- **O pilar é único.** Se ele morrer sem o pilar B pronto (ordem 6), o projeto fica sem
  nada para publicar. Por isso a ordem 6 não espera o resultado do teste.
- **Aposta disfarçada de estratégia:** o formato POV depende de 10 minutos de filmagem do
  Ramón, pedidos desde 07/08 — duas semanas parado. Enquanto a cena não existir, POV não
  é estratégia, é intenção.

## O que só o Ramón faz

1. Sim/não para trocar a legenda das 2 peças (o mais urgente — antes das 14:00Z).
2. Filmar a cena do POV #1 (3-5 tomadas, ~10 min, celular + tripé). Roteiro pronto.
3. Criar os 3 Highlights no perfil (2 min, só pelo app) — pendente desde 19/08.
4. Data do `chegada-eloen` (decisão de família) e recarga do Gemini (sem crédito desde 18/08).

## Recado ao Ramón — NÃO ENVIADO (sem credencial neste ambiente)

`python publisher/mandar_recado.py` respondeu `[erro] faltam TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID`
— esta rodada automática não tem as variáveis do Telegram (só existe `.env.example` no repo).
Ciclo não travou por isso. Texto que deveria ter ido, para reenvio manual:

> **VP de Marketing — 21/08**
>
> 331 seguidores, zero a mais em 12 dias, e nenhum dos 9 posts teve um único salvo ou
> compartilhamento. Hoje às 11h sai o primeiro post em 11 dias.
> Achei um erro que dá pra consertar antes disso: o time escreveu uma legenda nova (com
> "salva essa", que é o que faz o post render) e esqueceu de colocar no post. Do jeito que
> está, ele sai com o texto velho. Preciso de um "pode trocar" seu até 10h30 — sem isso o
> teste de 48h vira desperdício.
> Depois de amanhã a fila fica vazia de novo; já cobrei peça nova pra amanhã de manhã.
> Duas coisas continuam só com você: os 10 minutos de filmagem da Hana (roteiro pronto) e
> os 3 Destaques no perfil (2 min no celular).
> O diretor de Atualidades falhou 2 rodadas seguidas sem motivo técnico — se não entregar
> até amanhã, minha recomendação é tirá-lo do projeto.

## 🔗 Relacionados

> Ligações geradas automaticamente por `tecer-vault-obsidian.py` a
> partir das citações que já existiam no texto acima.

- [[ESTADO-ATUAL]]
- [[legendas-pov-2026-08-21]]
