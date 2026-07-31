# Time da Hana — operacional e estratégico

Montado em 31/07/2026 a pedido do Ramón. Passou pelo conselheiro antes de ser
apresentado, e **mudou por causa dele** — o registro dessa mudança está no fim.

---

## O que o time existe para resolver (número, não opinião)

Fonte: `content/placar.md`, coleta da API do Instagram em 31/07/2026.

| Fato medido | Número |
|---|---|
| Seguidores | 329 — parado (329 → 329 → 328 → 329 em 4 dias) |
| Alcance por post | 40 a 54 (média 47, ~14% da base) |
| Salvos | **0** em todos os 4 posts |
| Compartilhamentos | **0** em todos os 4 posts |
| Seguidores ganhos | **0** em todos os 4 posts |
| Reels publicados | **nenhum** (o primeiro está na fila para 10/08) |

**Diagnóstico corrigido pelo conselheiro:** eu ia dizer que o gargalo é *alcance*.
O número mais duro diz outra coisa: das ~47 pessoas que veem cada post, **zero**
salva, compartilha ou segue. Quem já é visto e não move ninguém tem problema de
**conteúdo**, não de entrega. E, com 0 Reels publicados, não existe dado nenhum
sobre o único formato que o nicho indica que cresce.

Ou seja: o time não é montado para "distribuir mais". É montado para **descobrir
qual conteúdo faz alguém salvar, compartilhar ou seguir** — e a primeira medição
disso ainda não existe.

---

## Andar ESTRATÉGICO — gasta Claude, e por isso é pequeno

| Cargo | De quem é a decisão | Quando é acionado |
|---|---|---|
| **Presidente** (Claude Opus, na conversa) | Coordena, confere na fonte e é o único que fala com o Ramón | Sempre |
| **Diretor de Conteúdo** (fusão de redes + criativo + visual numa sessão só) | Formato, gancho dos 3 primeiros segundos, escolha da cena, legenda | 1x por semana |
| **Conselheiro** (Fable) | Não decide nada — contesta antes de decisão de peso | Toda decisão de peso |

**Por que fundir redes + criativo + visual:** "gancho" estava com dois donos
(redes e criativo). Cargo sobreposto é teatro, e três invocações separadas para
3 posts por semana queima token contra a ordem do Ramón de 31/07. Voltam a ser
cargos separados quando o volume justificar.

**Banco de reserva — só sob demanda, não entra na rotina:**
`diretor-atualidades` (áudio/trend do momento) · `diretor-pesquisa` (varredura de
nicho em lote) · `diretor-automacao` (quando houver robô novo para construir) ·
`diretor-financas` (quando houver dinheiro no jogo).

**`diretor-vendas` fica FORA.** Não há produto. Cargo sem trabalho é custo.
Entra no dia em que existir o que vender.

**Tirado do mandato do time (por enquanto):** otimizar horário, hashtag e
frequência. Com 4 posts medidos isso é adivinhação. Volta ao mandato quando
houver 15 a 20 posts no placar.

---

## Andar OPERACIONAL — robô, custo zero de token

Ordem do Ramón, 31/07/2026: *"não use a claude, crie robôs operacionais fora
para claude para fazer isso, vamos economizar tokens"*.

| # | Robô | Onde roda | Quando | Estado |
|---|---|---|---|---|
| 1 | `publish.yml` — publica o que venceu, coleta métricas 1x/dia, sentinela | GitHub (nuvem) | a cada 30 min | saudável |
| 2 | `Hana Sentinela` — renova token, avisa atrasado, dispara o lote | notebook do Ramón | dom/seg/qua/sex 18:10 | consertado em 31/07 (recupera horário perdido) |
| 3 | `lote_automatico.py` — monta o lote da semana com o Gemini vendo a foto | dentro do #2 | domingo | **precisa mudar — ver abaixo** |
| 4 | **NOVO — robô do placar semanal** | GitHub, junto do #1 | segunda de manhã | a construir |
| 5 | Ronda de engajamento semi-automática | — | — | **em espera até medir** |

**#3 precisa mudar, e é urgente.** No domingo 02/08 o robô vai fabricar mais
**3 fotos** — exatamente o formato que mediu zero — oito dias antes do primeiro
Reel ir ao ar. A esteira está trabalhando contra o teste. Ou ele passa a montar
Reel primeiro, ou o lote de domingo produz mais zeros.

**#4, por que existe:** o placar já é coletado, mas ninguém lê. O robô compara a
semana com a anterior e manda no Telegram: alcance, salvos, compartilhamentos,
seguidores ganhos. Custo zero de token, e é o que impede o time de decidir por
intuição.

**#5, por que está em espera:** decisão já registrada — fazer **uma** ronda de 10
comentários e ler o placar antes de automatizar qualquer coisa.

---

## Cadência

- **Semanal:** uma sessão de conteúdo + leitura do placar. Uma só.
- **Mensal:** julgamento dos robôs (cada um prova que serve, ou sai) e corte do
  que não rende.

## Critério de corte — o que prova que este time funcionou

**3 Reels com ganchos diferentes até ~20/08.** Se, depois deles, "seguidores
ganhos" continuar em 0, o que muda é a **abordagem de conteúdo** — não o
organograma. Sem esse critério, a estrutura vira burocracia que se justifica
sozinha.

---

## Registro da revisão (o que o conselheiro derrubou)

Proposta original: organograma completo com 5 diretores no andar estratégico,
apoiado no diagnóstico de que "o gargalo é alcance".

Objeções aceitas:
1. **O diagnóstico não estava provado.** 0 salvo / 0 compartilhado / 0 seguidor
   entre quem já vê aponta conteúdo, não distribuição.
2. **O robô automatiza a produção de zeros** — o lote de domingo faz mais fotos
   antes do primeiro Reel ser testado.
3. **Cargo sobreposto é teatro** — dois donos do "gancho".
4. **Horário e hashtag com n=4 é astrologia.**
5. **Faltava critério de corte** — que número, em que data, prova que funciona.

Objeção não aceita: nenhuma. As cinco entraram no desenho acima.
