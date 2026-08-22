# Decisões e contexto — Hana Social

Parte humana do estado: o que o Ramón decidiu e o que código nenhum adivinha.
**Atualizar ao fim de cada sessão** (a parte automática vem de `studio/estado.py`).

## 🔓 21/08/2026 (noite) — 3 BUGS OPERACIONAIS CONSERTADOS; REPO VOLTOU A SER PÚBLICO

Bronca dele: *"estou recebendo emails de erro... isso não é problema de
aprovação minha é problema operacional... você precisa trabalhar melhor meu VP"*.
Ele tinha razão: eu tinha tratado a falha como se dependesse da decisão dele.

**1. CAUSA RAIZ do e-mail em loop (a que importava):** o repositório estava
**PRIVADO**. O Instagram baixa a mídia por `raw.githubusercontent.com` — com o
repo privado essa URL devolve **404**, e TODO post falhava. Não era defeito da
mídia (ffprobe conferiu: 1080x1920 30fps, h264+aac, 11,8s, íntegro).
**Ele autorizou tornar público** (perguntei porque expõe também o material da
Eloen/chá revelação, que era sigilo de família). Conferido depois de trocar:
`HTTP 200, 10.038.432 bytes`, idêntico ao arquivo local. Varredura de segredo
nos arquivos rastreados **e no histórico inteiro do git** antes de publicar:
nada encontrado.
Post `regras-da-casa` destravado (`failed` → `approved`) e remarcado 21/08 →
**24/08 14:00Z** (o slot de 21/08 já tinha passado; 24/08 é segunda, dia normal
da grade).

**2. E-mail em loop (o sintoma):** post com `status=failed` fazia o sentinela
derrubar o job a cada 30 min PARA SEMPRE, repetindo a MESMA falha já
diagnosticada. Agora só a 1ª vez é alarme; da 2ª em diante vira aviso no log
(`content/.falhas_avisadas.json`). Mesmo padrão do conserto do post-sem-data
de 19/08.

**3. "Telegram não saiu" do ciclo do VP:** conferido — as credenciais do
Telegram **nunca existiram nesta máquina** (nem variável de ambiente, nem
registro do Windows, nem `studio/.telegram`), só como secret do repositório.
Por isso o resumo do VP morria no log. `mandar_recado.py` agora procura em 4
lugares e, não achando nenhum, **dispara o próprio workflow** (que tem os
secrets) em vez de desistir. Testado ponta a ponta: run `32542427926`,
**SUCCESS**, recado entregue.

⚠️ **Sobre a rotina do VP a cada 2 dias:** ela roda em ponte com o PC dele. O
erro *"Não é possível conectar ao seu computador"* na tela dele é isso — PC
suspenso/desligado na hora do disparo, não bug do robô. Se ele quiser que rode
independente da máquina, tem que virar rotina de nuvem (perde o acesso aos
diretores locais e ao IA-Hub).
## 🧾 21/08/2026 12:20Z — CICLO DO VP DE MARKETING (automático, nada publicado)

Veredito: **NÃO TESTADO — e isso conta como não entrega do time.** 331 seguidores, +0 em 12
dias, 9/9 posts com 0 salvo e 0 compartilhamento; nada foi ao ar desde 10/08. O VP achou um
furo ainda consertável: as legendas novas com CTA de salvar (`content/legendas-pov-2026-08-21.md`)
**não foram coladas em post.json nenhum** — `regras-da-casa` (hoje 14:00Z) e `cenoura-filhote`
(amanhã) sairiam com o CTA-pergunta declarado morto em 18/08, contaminando o teste de 48h.
Trocar a legenda **precisa do sim dele** (ele aprovou a versão velha em 17/08), então nada foi
alterado. Diretores: redes ENTREGOU, reels e criativo entregaram peça mas deixaram o arquivo
fora do repositório, **atualidades falhou pela 2ª rodada seguida** — recomendação do VP é tirá-lo
do projeto se não entregar até 22/08 12:00Z (decisão do Ramón). Fila fica vazia a partir de
23/08. Ordens numeradas, donos e prazos: `estrategia/vp-marketing-2026-08-21.md`.

## 🔴 21/08/2026 — BUG REAL: "regras da casa" ficou 34h travado, achado ao checar "como estamos"

Causa: `publisher/run.py` exige `post.json["auditoria"]["veredito"]=="SEM OBJECAO"`
desde 31/07, mas nenhum código escreve esse campo — só é populado manualmente.
Os 3 posts aprovados por ele na conversa em 17/08 (regras-da-casa, cenoura-filhote,
chegada-eloen) nunca tiveram esse campo escrito. O "regras da casa", ao vencer
em 19/08, ficou TRAVADO — sentinela falhando a cada 30 min desde então, sem eu
notar (o e-mail de falha real virou igual ao ruído do bug já consertado de
19/08, e eu não tinha voltado a checar o log).

**Conserto:** escrevi o campo `auditoria` nos 3 posts.json com o veredito REAL
já documentado nas notas de cada um (histórico de auditoria + aprovação
pessoal dele em 17/08 — não inventei nenhum veredito novo). Testado:
`passou_auditoria()` libera os 3 agora. Nota nova na skill (3i) pra isso não
se repetir: todo post aprovado precisa do campo escrito NA HORA.

Mais recente em cima.

## 📅 21/08/2026 — CALENDÁRIO DE RETOMADA (decisão do diretor-redes, alçada dele)

11 dias sem publicar (último post 10/08). Datas remarcadas — só `scheduled_for`,
nada de status, nada publicado na mão:

| Peça | Itajaí | UTC |
|---|---|---|
| regras-da-casa | 21/08 11:00 | `2026-08-21T14:00:00Z` |
| cenoura-filhote | 22/08 11:00 | `2026-08-22T14:00:00Z` |
| chegada-eloen | SEM DATA — decisão da família, não se mexe | — |

`regras-da-casa` vai primeiro: perdeu o slot de 19/08 pelo bug da auditoria e o
conceito nasceu do estudo de virais (lista quebrada + veredito + pergunta de
identificação). Um por dia, nunca dois no mesmo slot — datas iguais publicariam
juntos na mesma rodada. Não publiquei agora (23h de Itajaí, horário morto):
esperar 12h pelo pico medido vale mais que 12h a menos de silêncio.

**Métrica-alvo em 48h** (baseline: 9/9 posts com 0 salvo e 0 share; melhor Reel
= 182 de alcance). `regras-da-casa` → **COMPARTILHAMENTO ≥ 3** (CTA é pergunta de
identificação; e `sends per reach` é o sinal nº1 do Mosseri). `cenoura-filhote`
→ **SALVAMENTO ≥ 3** (arco de nostalgia é isca de salvar, não de mandar). Os dois
→ alcance ≥ 250. Curtida não conta.
**Linha de corte:** se alcance ficar ≥182 e share/salvo derem 0 de novo, é o 10º
zero seguido — o problema é o CONCEITO, não o horário nem a fila, e o pilar
"A PATROA MANDA" precisa morrer em vez de ser reagendado.

**Segundo conserto na mesma checagem:** a salva de reforço do cron
(`.github/workflows/publish.yml`) ainda disparava 11:00Z seg/qua/sex — o reforço
das 8h antigas. Desde 19/08 o horário é 11h de Itajaí = 14:00Z, e a linha não foi
movida junto: o reforço protegia um horário que não existe mais, e sábado não
tinha reforço nenhum. Movida para `14 * * *` (14:00Z, todo dia).

## 🎓 19/08/2026 — PESQUISA DE CRESCIMENTO (~20 fontes) + 4 IAs reagiram

Ele: *"Estude como aumentar seguidores, assista 20 vídeos, traga pras IAs hub
e aprenda."* Ata completa: `estrategia/crescimento-instagram-2026-08-19.md`.
Legenda longa descartada (unanimidade das 4 IAs). Achado real na API: pico dos
NOSSOS seguidores é 10h-14h Itajaí, não 8h (horário atual) — proposto mudar,
esperando OK dele. Highlights por pilar: só ele faz (app). Collab e CTA
seguem como já estava.

## 📣 18/08/2026 — REUNIÃO DE EMERGÊNCIA: 7 IAs opinaram sobre o engajamento travado

Ele: *"não estou vendo estratégia... fale com todas as ias, quero a opinião sem
falta de todas."* Ata completa em `estrategia/reuniao-2026-08-18-engajamento.md`.

Resumo: 4 diretores + ChatGPT + DeepSeek + Grok deram opinião às cegas (Gemini
sem crédito, Kimi instável). Conselheiro vetou o pacote por empilhar 7 mudanças
de uma vez e mandou checar a premissa do diretor-redes antes de apostar nela.
**Checagem real (Graph API):** 72% do alcance dos últimos 9 dias já vem de
conta NÃO-seguidora — a tese de "só a base vê" caiu. O problema é conversão
(zero salvo, zero compartilhamento em 9/9 posts), não distribuição.
**Decisão:** próximo Reel muda o sujeito (a Hana "denuncia" o dono, não só faz
graça), roteiro só passa se alguém salvaria/marcaria de verdade, fecho de
legenda com marcação nomeada. Regra de morte: 3 Reels no formato novo com 0
salvo E 0 compartilhamento nos 3 → volta a discutir distribuição/TikTok.

## 🖥️ 18/08/2026 — SEGUNDA AUDITORIA DA MÁQUINA NOVA: achado e consertado o bug que ia furar o domingo

Ordem dele: *"audite de ponta a ponta e veja se precisa arrumar algo para esse
computador conseguir rodar"*. Tudo abaixo é conferido por comando nesta sessão
(regra zero) — a auditoria de 17/08 (ambiente geral) já tinha passado; esta foi
mais funda, script por script.

**🔴 Bug real, achado e já consertado:** `studio/lote_automatico.py` procurava a
chave do Gemini em `~\OneDrive\Desktop\Claude code APIs\...` — pasta que **nunca
existiu nesta máquina**. No próximo domingo o robô ia quebrar tentando gerar a
legenda, exatamente o mesmo tipo de bug que `gerar_trilha.py` já tinha levado em
02/08/2026. Corrigido com a mesma lista de lugares que `gerar_trilha.py` e
`recepcionista.py` já usam (prioridade: `OneDrive\IA-Hub\` pessoal primeiro).
**De quebra:** o `.garimpo_estado.json.tmp` (escrita atômica do garimpo) tinha o
mesmo furo de privacidade do arquivo real — nomes do rolo de câmera pessoal sem
entrar no `.gitignore`. Fechado junto.

**Conferido e OK, sem mexer:** os 43 itens do `ambiente.json` do hub · token do
Instagram (válido até 24/09) · variáveis TELEGRAM/IG_ACCESS_TOKEN definidas no
usuário local · os 3 perfis do Chrome (pessoal, Hana, Canecas) sincronizados
nesta máquina · Ollama rodando com 2 modelos · `git config windows.appendAtomically`
persistiu do conserto de 17/08. O "erro" do publicador no GitHub Actions
continua sendo o alarme de propósito (Reel da Eloen aprovado sem data), não bug.

**Falso alarme que quase virei achado:** os textos de `motivos_reprovacao` no
estado do garimpo pareciam corrompidos ("reconhec�vel") ao imprimir no terminal
— conferi os bytes crus do arquivo e do `.py` fonte: os dois estão em UTF-8
correto. Era só o display do meu terminal, não o dado real. Registrado para não
repetir a checagem incompleta da próxima vez.

## ✅ 17/08/2026 — ELE APROVOU 3 REELS NA CONVERSA; BALÕES RECUSADO

Ele viu os 4 Reels na conversa (mandados por arquivo, não pelo Telegram) e
respondeu: *"Aprovado 1 2 4 / 3 não aprovado"*.

- **AS REGRAS DA CASA** → aprovado, remarcado para **19/08 11:00Z** (qua).
- **CENOURA FILHOTE** → aprovado, remarcado para **21/08 11:00Z** (sex).
- **CHEGADA DA ELOEN** → aprovado, **de propósito sem data**: o dia do anúncio
  é decisão da família dele, não do calendário de conteúdo (mantém a decisão
  de 14/08). Só publica quando ele disser o dia.
- **BALÕES DELA** → `rejected`. Era a peça que a auditoria já tinha marcado com
  teto de qualidade (bruto deitado 1024x576, 1º segundo sem o rosto dela).
  Ele confirmou o veredito. **Não retrabalhar esta peça** — regra 3n-ii: o
  defeito é do material de origem, não do ajuste.

**As duas datas eu decidi** (regra 8b — data de fila é operacional, não é
decisão dele): os slots de 14/08 e 17/08 já tinham vencido, então as duas peças
foram para os próximos slots livres seg/qua/sex, na ordem cronológica original.

**🔴 Segundo bug da mesma família, achado ANTES de aprovar a Eloen:**
`postqueue.is_due()` fazia `post["scheduled_for"].replace(...)` sem guarda.
Marcar a Eloen como `approved` sem data teria quebrado o **publicador** — não
só o vigia. Consertado: post sem data devolve `False` (nunca está na hora),
então peça aprovada sem dia espera em vez de derrubar o robô.
**Lição:** o mesmo padrão (`scheduled_for` tratado como sempre existente)
estava em dois arquivos. Ao consertar um bug de campo que pode ser nulo,
procurar TODOS os usos do campo antes de dar por fechado — foi o que evitou o
segundo apagão.
Conferido depois de aplicar: os 3 aprovados passam pela trava de fingerprint
sem voltar pra `pending`, e a Eloen dá `is_due=False`.

## 🖥️ 17/08/2026 — AUDITORIA DA MÁQUINA NOVA: ambiente aprovado, 1 bug real achado e consertado

Ordem dele: *"Começamos em um computador novo... Audite todo esse projeto, veja
se já estamos prontos para continuar."* Tudo abaixo foi conferido por comando
nesta sessão, nada veio de memória nem de arquivo do projeto (regra zero).

**O ambiente está pronto — conferido, não suposto:**
- Python 3.13.15 + PIL, requests, imageio_ffmpeg, numpy, dotenv (todos importam).
  ⚠️ O Python foi instalado hoje 12:34 e o PATH do usuário já está correto; só a
  sessão do Claude tinha herdado o PATH velho. Não é problema da máquina.
- ffmpeg 9.0, ImageMagick, Node, jq, Ollama, gh e git no PATH.
- `gh` logado como `ramonduranp6-ai`. Os 6 secrets do repo existem;
  `IG_TOKEN_EXPIRA_EM = 2026-09-24` (37 dias de folga).
- Tarefa **`Hana Sentinela`** recriada nesta máquina: dom/seg/qua/sex às 18:10 de
  Itajaí, apontando para o `sentinela.bat` no caminho novo. Ainda não rodou
  porque o horário de hoje não chegou — não é falha.
- `estado.py` e `lote_automatico.py --simular` rodaram limpos.
- Git: puxada 1 novidade do outro aparelho e subido o conserto abaixo.
  ⚠️ **Pegadinha desta máquina:** o git quebrava com `unable to append to
  .git/logs/HEAD` (conflito do OneDrive com escrita atômica). Resolvido com
  `git config windows.appendAtomically false` neste repo. Se aparecer em outro
  projeto dentro do OneDrive, é a mesma receita.

**🔴 O bug que a auditoria achou (estava quebrado desde 14/08):** o publicador
do GitHub falhava em TODAS as execuções — 6 seguidas conferidas. Causa: o Reel
da chegada da Eloen ficou de propósito **sem data** (decisão dele em 14/08), e o
`publisher/sentinel.py` assumia que todo post `pending` tinha `scheduled_for`.
Quebrava com `AttributeError` na primeira linha do laço.
**O que isso custou:** o passo é o ÚLTIMO do workflow, então publicar, coletar
métricas e salvar estado continuaram funcionando — mas **o vigia ficou mudo por
3 dias**, justamente o robô que existe para avisar que a fila travou. Consertado
(post sem data agora vira aviso próprio) e rodado local: volta a listar os 4
problemas reais.
⚠️ **O workflow vai continuar VERMELHO enquanto a fila estiver travada** — o
sentinela sai com erro de propósito quando acha problema, é o alarme funcionando.
Ele fica verde quando os Reels forem aprovados.

**O que a auditoria mostrou que só depende dele:** os 4 Reels da fila foram
enviados no Telegram (`notified: True`) e **nenhum foi aprovado** — 14/08 e 17/08
já passaram da hora. Último post no ar: 10/08. E o robô do lote registrou a
**1ª semana sem filmagem nova**.

## 🎬 14/08/2026 (manhã) — REFEITO O REEL DOS BALÕES: achado o bug real, corrigido o que dá, e um teto de qualidade que não dá

Ele: *"toda vez que peço para vc alterar vc apenas trocar a descrição... não vejo
edição de imagens, não vejo vc colocar músicas legais... muito ruim."* Ordem:
*"Faça e audite. Veja se está no padrão de vídeo viral para o nosso nicho."*

**O bug real, achado antes de mexer em qualquer coisa:** existia um roteiro
(`studio/roteiros/2026-08_J_ela-achou-que-era-dela-FINAL.json`) com edição
cuidadosa auditada quadro a quadro em 10/08 (corte, zoom, crop, tudo verificado
contra rosto de terceiro) — mas o vídeo que foi pra fila **nunca tinha rodado
esse roteiro pelo `montar_reel.py`**. Era o corte cru, com só o áudio tratado.
Por isso parecia amador: era mesmo, o trabalho de edição nunca foi construído,
só planejado no papel.

**O que fiz:** rodei o roteiro de verdade (`V2-real.json`, mesmos cortes/crops
já auditados, zero cartelas de texto — o manual mede texto=zero em 7/7 virais
reais, contra as 4 cartelas que existiam). Gerei `baloes-dela-v4-editado.mp4`.

**Auditoria independente (diretor-reels, `estrategia/auditoria-baloes-v4-2026-08-14.md`),
reconferindo rosto de terceiro por 3 métodos próprios, não aceitando o que eu
tinha medido:**
- **Privacidade: PASSA.** Nenhum rosto de terceiro, nenhuma fumaça de chá
  revelação, zero texto — conferido nos 216 quadros.
- **Achei um erro meu no áudio**, que o auditor pegou: eu tinha lido os campos
  de ESTIMATIVA do `loudnorm` como se fossem a medida real. O valor real era
  −12,03 LUFS/pico −0,17 dBTP (fora do alvo). **Corrigi de verdade** com ganho
  medido + conferência por duas ferramentas independentes: agora −14,6/−15,2
  LUFS, pico −1,5 dBTP — dentro do padrão.
- **Achado que ninguém tinha medido: o material bruto é 1024x576 deitado.**
  Depois do crop 9:16 + zoom só sobram 135 a 216 pixels reais de largura (os
  virais medidos têm 720). A nitidez caiu 85% (149,5 → 23,1) por causa do zoom.
  **Mais zoom PIORA — não existe zoom a mais pra dar.** É limite do material
  filmado (celular, deitado, ela longe), não falta de trabalho.
- **1º segundo sem rosto dela** (abre de costas) — reprova o checklist, sem
  conserto possível nesta peça.
- **Veredito: NÃO está no padrão viral medido.** Passa privacidade e luz;
  reprova em áudio (já corrigido), gancho sem rosto e detalhe real da imagem.

**Decisão que só é dele:** (A) subir mesmo assim como peça de acervo, sabendo
do teto de qualidade medido; ou (B) engavetar e usar o esforço numa cena
filmada de propósito pelo manual (câmera fixa, luz única, rosto no 1º segundo —
é de lá que sai viral, 5 dos 7 medidos são plano único). Aviso à parte, também
dele decidir: mesmo sem fumaça/texto, balão rosa + piquenique + ursinho + casal
pode ler como chá revelação pro público americano — é sigilo de família.

**Lição de processo:** o `post.json` chegou a ter escrito "diretor-reels
auditou este V4" ANTES da auditoria existir — o auditor pegou isso também.
Corrigido. Mesma classe de erro que ele já cobrou antes: afirmar antes de
verificar.

## 🎬 14/08/2026 (tarde) — REEL DA CHEGADA DA ELOEN: 2 travas levantadas por ele, peça nova, auditada e corrigida

Ele: *"Quero que vc faça um reels decente para a publicação da chegada da Eloen,
irmã da hana"*. Eloen é a bebê humana do chá revelação (mesmo material do Reel
dos balões auditado hoje de manhã). Ele levantou explicitamente as duas travas
que valiam desde 09/08: **(1) pode anunciar a gravidez** e **(2) rosto de
família pode aparecer** ("podemos aparecer sim").

**O que foi feito:** montado `content/queue/2026-08-K_chegada-eloen/chegada-eloen-v3.mp4`
(5,98s) a partir do mesmo bruto, agora com 4 cortes reais do evento: ela
chegando com os balões, a explosão de fumaça (antes proibida), a reação da
família com ela no meio, e o fecho com ela em pé junto dos dois — sempre
terminando nela, nunca só no casal (regra 1 do projeto).

**2 rodadas de auditoria independente (diretor-reels), 1 achado grave de
processo no meio:**
- 1ª rodada (v2): reprovado em 3 pontos — rosto da Hana ausente no 1º segundo
  e no fecho, zoom artificial proibido no gancho, som fora do padrão (pico
  estourava o teto). Todos corrigidos: troquei os cortes por janelas onde o
  rosto dela aparece (reconferido com grab isolado antes de trocar), tirei o
  zoom artificial, e **corrigi o `studio/montar_reel.py` para sempre
  masterizar o áudio em 2 passadas** — ele nunca tinha esse passo, então TODA
  peça já montada por ele nasceu fora do padrão de som do manual. Vale pra
  peças futuras, não só esta.
- Achado de processo: uma varredura rápida por "-ss + -to" deu frames com
  timestamp ERRADO (confirmado contra grab isolado) — foi por isso que a
  primeira versão (v1) tinha o gancho e o fecho no lugar errado. Lição:
  para escolher corte, usar sempre grab isolado (`-ss` sozinho), nunca a
  varredura por intervalo.
- Medido na peça final: brilho variação 21,13 (teto 30) · som −15,0 LUFS pico
  −1,0 dBTP (medido em loop de 24x pra tirar viés de clipe curto, método que a
  auditoria validou) · 1080x1920 30fps · zero texto · som real da cena (sem
  risco de direito autoral, pode publicar pelo robô).
- Achado sem conserto: o bruto é só 576x1024 de detalhe real — a imagem final
  é ampliada, por isso fica mais macia que 1080p nativo. Não é defeito da
  montagem, é o material que existe.

**Decisão dele, não tomada sozinha:** sem data de publicação (anúncio de bebê
combina com a família, não é calendário de conteúdo) e sem decidir se estica
a duração (6s vs 9-12s, sugestão do auditor). Esperando ele ver e aprovar.

## 🏁 BASTÃO (atualizado em 21/08 23:26 Itajaí)
· **Onde paramos:** VP de Marketing e Performance contratado (ordem dele,
  21/08) — `~/.claude/agents/vp-marketing.md`, revisão a cada 2 dias já
  agendada (rotina no PC dele, 9h Itajaí). Achou e o time consertou um bug
  real: a fila ficou 34h travada (post.json sem campo de auditoria que nada
  no código escrevia) — os 3 posts aprovados em 17/08 já estão destravados.
  Formato POV+CTA nomeado (18/08) e horário novo 11h/14:00Z (19/08) **ainda
  não têm nenhuma peça publicada** — 0 salvo/0 compartilhamento continua
  valendo pros 9 posts antigos, nada novo foi medido ainda.
· **Esperando ele:**
  1. **Filmar "a patroa mandou"** (10 min, celular, roteiro pronto em
     `studio/roteiros/2026-08_POV1_a-patroa-mandou.md`) — é o único gargalo
     real hoje, aberto desde 07/08.
  2. Responder se troca a legenda velha dos 2 posts que publicam 21/08 e
     22/08 pelas novas com CTA de salvar (`content/legendas-pov-2026-08-21.md`)
     — perguntado, resposta pendente.
  3. Decidir o futuro do diretor-atualidades: 2ª falha seguida (sem fonte
     verificável), o VP recomendou última régua (até 22/08 12:00Z) ou
     aposentar o cargo neste projeto.
· **Próximo passo:** assim que a filmagem chegar, diretor-reels já monta na
  hora (roteiro pronto). Sem filmagem, a fila fica vazia depois de 22/08 (só
  sobra o pilar antigo, todo rejeitado, e a Eloen sem data).

## 🎬 14/08/2026 — TESTE REAL DO HIGGSFIELD: motor bom, catálogo de efeitos reprovado

Ordem dele: *"testei o higgsfield... traga o resultado para aprovar... peça
para o diretor de reels aprender todas as técnicas... no futuro quero que vcs
criem vídeos e fotos como o higgsfield, mesmo padrão."*

**O que foi feito:** subi a foto real `post_oncinha.jpg` (Hana de barriga pra
cima, roupinha de oncinha) como referência e gerei 1 vídeo com `kling3_0`
(motor cru, sem preset), 5s, 9:16 pedido, custo real 7,5 créditos (saldo caiu
110→102,5, conferido). Resultado em
`Fotos da Hana/06 - videos e trilhas/testes-higgsfield/2026-08-14_teste-higgsfield-kling3.mp4`
— **não está na pasta de aprovar**, porque não é candidato a publicar (ver
motivo abaixo). diretor-reels auditou com o mesmo `signalstats`/`ffprobe` do
manual e escreveu o estudo completo.

**Achados medidos, não opinião:**
- Identidade da Hana mantida (cor, rugas, roupinha) até ~3s; depois disso o
  detalhe derrete — patas perdem os dedos, estampa embaralha, rugas somem —
  bem na hora do desfecho, que é onde o manual exige mais qualidade.
- Luz do clipe gerado: variação de brilho **4,27**, melhor que os 7 virais reais
  (10-25) e muito melhor que nossas 3 peças da fila (80-196). Prova que plano
  único sintético resolve o maior defeito medido do projeto.
- Proporção pedida (9:16) foi IGNORADA — o modelo copia a proporção da foto de
  entrada. A foto usada era 4:5 e não tem conserto bom pra 9:16 (cortar decepa
  as patas dela); consertar na ferramenta (`reframe`) custaria 51 créditos.
- Vídeo sai mudo — sem uso em peça onde o som da cena é o protagonista (7 dos
  10 virais).
- Catálogo de 62 presets prontos do Higgsfield: **reprovados em bloco** — são
  efeito de selfie humana (Sticker Peel, Action Figure, Kung Fu Hit...), e a
  régua do manual (medida nos virais reais) diz efeito/transição/filtro = zero.

**Proposta do diretor-reels (não é decisão, esperando ele):** ver BASTÃO acima,
itens 1-5. Nada foi publicado nem adotado como padrão oficial sozinho.

**🔴 CORREÇÃO (mesma sessão): o prompt do teste inventou um rabo que a Hana não
tem.** Ele viu o vídeo e cortou na hora: *"Não gostei! Hana não tem rabo."* Eu
escrevi no prompt "tail gives one lazy wag" sem checar antes — não é traço
sutil de raça, é um erro de anatomia que ele pegou na hora, eu não. **Não é só
"o detalhe derrete" (§5 do estudo) — é fabricação de uma parte do corpo que não
existe**, o tipo de erro que um seguidor identifica na hora e vira vergonha
pública, não só defeito técnico. Reforça ainda mais o veredito do §8: este
motor não pode encenar nada que não seja checado parte por parte contra o
animal real antes do prompt, não só depois no resultado. Fato registrado em
memória para nunca mais entrar num prompt de geração da Hana.

## 🎬 13/08/2026 — HIGGSFIELD ASSINADO (conta pessoal dele); conector ainda não carrega

Ele: "Assinei o higgsfield na minha conta pessoal, pode usar esse conector."
Autorização de USO dada por ele. Conferido via ToolSearch nesta conversa:
**nenhuma ferramenta higgsfield disponível ainda** — conector adicionado no
meio de uma conversa só carrega na SEGUINTE (mesmo caso do Apify em 09/08).
Primeiro uso planejado: efeitos/vídeo de qualidade profissional para os Reels
(entra na escada junto com Gemini/Flow; comparar qualidade antes de adotar).

## 🧰 13/08/2026 — KAIROGEN: ele liberou o GRÁTIS; conta conectada é a PESSOAL com 0 crédito

Ele: "Pode usar o grátis!" — sem assinatura, só o plano free. Conferido pela
API na hora (regra zero): o conector ativo é a conta PESSOAL dele
(ramon.d.franca@gmail.com), plano free, **0 crédito disponível** (os "10/dia"
do site não constam na API). Existe um segundo conector "kairogen-hana" que
exige autorização dele no claude.ai e nunca foi autenticado.
Combinado implícito: usar só crédito grátis; upscale Topaz de teste fica
pendente até ter crédito. Preço conferido no site: free 10/dia · R$ 49 a
R$ 1.199/mês. Decisão de assinar é dele, e só depois de teste medido.

## 🎯 13/08/2026 — 10 VIRAIS MEDIDOS + SKILLS reel-viral E foto-viral (pedido dele)

Ele pediu: "Encontre 10 reel virais do nosso nicho... crie uma skill de reel
virais... faça isso tb para fotos." Feito por dado (Apify, ~US$ 0,15, 24 Reels
+ 113 fotos com números reais da API):
- **Relatório:** `estrategia/virais-medidos-2026-08-13.md` — top 10 de 670 mil
  a 30 milhões de views. Padrão: UMA piada, cachorro-personagem com atitude,
  6-18s, conflito dono×cão em que o cão vence, áudio original (7/10), legenda
  que pede marcação (share é a métrica).
- **Skills novas:** `.claude/skills/reel-viral/` (prompt de produção +
  checklist de reprovação) e `.claude/skills/foto-viral/` (capa/carrossel;
  respeita a regra 3l — foto solta continua fora do ar).
- **Achado das fotos:** maior foto do nicho = 435 curtidas vs 30M do maior
  Reel. Foto não viraliza no nicho; confirma o placar da Hana e a regra 3l.
- O 3º maior viral (4,8M) é um pet reclamando da dona — o posicionamento
  "patroa mimada" É o formato que viraliza. Manter.

## 🔁 11/08/2026 — ELE TINHA RAZÃO: REPETIÇÃO REAL ACHADA NOS 2 POSTS APROVADOS

Ele pediu: *"Veja se esses posts que está me sugerindo já não tem fotos iguais no
Instagram da hana."* Abri o perfil de verdade (regra 2c) e achei DUAS repetições:

1. **O Reel de 12/08 (v7, já aprovado) tinha um corte de praia (`IMG_1725.MOV`)
   do MESMO passeio do post "dia-de-praia" publicado em 03/08** — confirmado
   comparando frame a frame: mesmo colar de conchas branco, mesma praia, mesma
   bandeira. Removido o corte.
2. **O mesmo Reel de 12/08 também repetia com o Reel de 14/08**: os dois usavam
   quase o mesmo segundo (0,2-2,6 vs 0,5-2,3) do clipe da cama à noite
   (`11984692...mp4`). Troquei o corte do de 12/08 para 6,0-8,4s do mesmo
   clipe — mesma cena, sem sobreposição.

**Virou VERSÃO 8** (`content/queue/2026-08-12_cenoura-filhote/video-v8.mp4`),
6 cortes em 12s, reauditada (sem objeção). Como o `media_file` mudou depois de
"approved"+"notified", **a trava de fingerprint do próprio robô** (regra 3n-iii,
`telegram_approve.revalidar_conteudo()`) vai devolver o post pra 'pending'
sozinha no próximo ciclo e reenviar pra ele aprovar de novo — não precisei
mexer no status manualmente.
**Lição:** ele suspeitou por conta própria, sem eu ter avisado — a checagem de
repetição da regra 2c precisa rodar SEMPRE antes de aprovar, não só quando ele
perguntar. Os outros posts da fila (17/08 em diante) estão `rejected`, não
publicam, não precisam da mesma checagem agora.

## 🎬 10/08/2026 — REEL DO CHÁ REVELAÇÃO: 3 rodadas até ficar seguro, mostrado a ele antes de enviar

O vídeo "nova irmã" (ver entrada abaixo) é chá revelação de gravidez, não cachorra
nova — corrigido depois de extrair frame. Regra aplicada: **não é notícia da Hana
pra dar** (sem palavra/som que confirme gravidez) e **a estrela continua sendo a
Hana**, nunca o casal.

Processo (diretor-reels roteiriza, auditor independente audita — nunca quem
constrói aprova, regra 3n):
1. Roteiro A: tinha corte com a fumaça rosa da revelação — **vazamento real**,
   auditoria reprovou.
2. Corrigi um zoom pra tirar o rosto do parceiro dela de um corte — não resolveu,
   o rosto reconhecível estava no corte SEGUINTE (que eu não tinha tocado).
3. Diretor-reels trocou o desfecho inteiro (regra 3n-ii: corte reprovado 2x pelo
   mesmo motivo, troca-se o material, não o parâmetro) — e achou um TERCEIRO
   rosto (o dela) escondido num corte que os dois auditores tinham deixado passar.
4. Versão final: 7,2s, 4 cortes, reauditada quadro a quadro (36 frames) —
   **SEM OBJEÇÃO** em rosto de terceiro e em vazamento de notícia. Ressalva de
   qualidade (não de segurança): ela fica pequena em ~60% dos frames de
   caminhada — mandado a ele mesmo assim, avisado do porém, esperando o aval.
Arquivo: `Fotos da Hana/06 - videos e trilhas/rascunhos/2026-08-J_balloes-dela-FINAL.mp4`.
Roteiro: `studio/roteiros/2026-08_J_ela-achou-que-era-dela-FINAL.json`.
**Custo R$ 0,00** — trilha já existia (Lyria). Como a trilha é nossa, pode
publicar pelo robô normal, não precisa subir na mão.
**Lição que fica:** revisão dupla pegou 3 vazamentos de privacidade que a
produção sozinha não veria — vale o custo de token nesta faixa (3n).

## ✅ 09/08/2026 (3ª sessão) — 14/08 aprovado, DMs mandadas, vídeo novo: NOVA IRMÃ

Ele respondeu os 3 pedidos: (1) **14/08 "regras da casa" aprovado** (já estava
`approved` no post.json — conferido, nada a mudar). (2) DM de collab prontas e
entregues no Telegram pra ele mandar do celular: **@troy.abully** e
**@zaya.lifestylee** (não fiz a @dudinhabully de novo, já tinha ido em 09/08).
(3) **Vídeo novo salvo:** `hana_noticia_nova_irma.mov` (6,4 MB) em
`01 - brutas (suba aqui)` — ele descreveu como "a Hana descobrindo, dando a
notícia da nova irmã dela". **CORRIGIDO em 10/08 depois de extrair frame: não
é cachorra nova — é chá revelação (fumaça rosa, ursinho, casal), a "nova irmã"
é um BEBÊ HUMANO.** Eu tinha suposto "nova cachorra" sem olhar o vídeo — errado,
corrigido antes de virar decisão (regra zero).

**Instrução dele em 10/08:** "esse lote que abriu aqui na nossa conversa já
foi postado, cuidado com isso, para não repetir" — leitura: o chá revelação em
si já foi postado em outro canal (pessoal), não é pra repetir esse anúncio na
Hana. "Vídeo novo pode montar, me traga antes de enviar" — autoriza um corte
NOVO, focado na Hana (não repetição do anúncio), mostrado a ele antes de ir
pro Telegram. Decisão editorial minha, a confirmar com ele: manter a estrela
sendo a Hana (regra 1), sem texto que anuncie a gravidez — isso não é notícia
da Hana pra dar.

## 📊 09/08/2026 (2ª sessão) — GARIMPO DE COLLAB E BENCHMARK POR DADO (APIFY)

Tarefa deixada pronta em `PROXIMA-CONVERSA.md` (apagado ao terminar). Resultado
completo em `estrategia/garimpo-apify-2026-08-09.md`. Custo: ~US$ 0,19.

- **Os 5 collabs escolhidos à mão bateram com o dado** (seguidores conferidos
  por API). Mas 2 reservas (@ravenna_bully_, @dom_exotic_bully) estão **parados
  há 63 dias** — saem da lista ativa.
- **3 alvos novos achados por hashtag** (não no olho): @troy.abully,
  @zaya.lifestylee, @caioguedesmbc. Lista final por engajamento:
  @troy.abully → @zaya.lifestylee → @dudinhabully (já contatado) →
  @pituco_bully → @momoamora1.
- **Corrige a regra 3h da skill:** a amostra de 4 Reels que dizia "nicho roda
  100% em áudio original" virou **80 Reels medidos = 49% original / 51%
  música** — quase empate. A régua que decide a trilha continua sendo a 3e-ii
  (combinar com a cena), não mais "o nicho manda".
- Nenhuma ação além de leitura (sem seguir/curtir/DM por robô).

## 🧰 09/08/2026 — APIFY ENTROU; REUNIÃO DAS 4 IAs DEU 3 DECISÕES

**Reunião** (formato fixo: proposta às cegas → debate com ataque/retirada/voto →
conselheiro): ata em `estrategia/decisoes-2026-08-09.json`, revisão automática 16/08.
Mortas no debate: "embaixador orgânico" e "remix de virais". As 3 vivas: gancho
sonoro + pedido de compartilhamento nos Reels · SEO de descoberta · 1 collab/semana.
**Ele autorizou tocar as três** ("Se não houver custo, vc pode tocar!!!"), mantendo
o portão: *"antes de postar vc me mostra pra eu aprovar"*.

**Correções que a conferência na tela impôs às decisões da reunião:**
- O **SEO do perfil JÁ EXISTIA** — nome "Hana 🐾 Exotic Bully Micro" e bio com
  "Tri Lilac Merle", "a patroa" e "Itajaí SC". As 4 IAs propuseram algo já feito.
  Nada foi alterado. Restou da decisão só geotag + hashtags nos posts.
- O conselheiro consertou 3 pontos antes de liberar: regra de morte com **OU** (o
  **E** tornava o formato imortal), contagem por **Reel publicado** e não por semana
  de calendário, e custo honesto da collab (**15-30 min**, não os "5 min" propostos).

**APIFY** — conferido pela API em 09/08 (regra zero): MCP HTTP `mcp.apify.com`,
plano **grátis US$ 5/mês**, US$ 0,07 usados, token válido, sem autorização pendente.
Eu disse a ele duas vezes que "não estava instalado" — **estava**, no `.claude.json`
global; a lista desta conversa não o mostrava porque MCP instalado no meio de uma
conversa só carrega na seguinte. **O que teria pego o erro:** procurar no
`.claude.json` antes de afirmar, em vez de confiar na lista de ferramentas da sessão.
Tarefa preparada em **`PROXIMA-CONVERSA.md`** (apagar quando terminar).

**Incidente de conta:** durante o garimpo de collab, a aba do Chrome caiu e a
varredura terminou logada no Instagram **pessoal do Ramón**, não no da Hana. Só
leitura de perfis públicos, nenhuma ação (sem seguir/curtir/comentar). Avisado a ele.


## 🔴 06-07/08/2026 — ELE RECUSOU O LOTE INTEIRO DE 5 REELS; REFEITO COM ESTUDO DE VIRAIS

Recado dele no Telegram (04/08, respondido 06/08): "Não aprovado nenhuma". Depois, na conversa:
*"Muito fraco os vídeos, quem é o diretor de criação que não consegue fazer um vídeo viral?...
Pegar referência dos principais virais do mês, aprender a editar imagens, fazer cortes, crie
vídeos no Gemini que são divertidos e geram interação e caem no algoritmo."*

**O que foi feito:**
- Os 5 posts (14 a 24/08) marcados `rejected`; mídias deles removidas da pasta 05 - APROVAR.
- `diretor-reels` produziu `estrategia/estudo-virais-2026-08.md` (6 mecânicas + 3 conceitos;
  atenção: as mecânicas são de fonte secundária/WebSearch, nenhum Reel real foi medido).
- Catálogo frame a frame dos 25 clipes do garimpo: `estrategia/catalogo-garimpo.md`.
  ⚠️ 4 arquivos não eram conteúdo da Hana (peru, meme de pintinho, border collie, tour vazio)
  — movidos para `06 - videos e trilhas/referencias (nao publicar)`.
  ⚠️ O catálogo ERROU no clipe 3e9f6791 ("em cima do balcão"): ela está no CHÃO da cozinha.
  Pego conferindo o frame grande antes de usar (regra zero).
- **Reel novo "AS REGRAS DA CASA" (conceito 1 do estudo, 100% acervo real)** montado,
  auditado (2 reprovações → aprovado na v4; pico de áudio -1,1 dBTP na v5) e **enviado no
  Telegram com botões em 07/08 — ESPERANDO O APROVAR DELE** para o slot de 14/08 11:00Z.
  Roteiro: `studio/roteiros/2026-08_I_regras-da-casa.json`; trilha nova `07-marcha-travessa`
  (+ edit2 emendada por medição).
- Conceitos 2 e 3 do estudo são HÍBRIDOS (cena real + trecho gerado no app Gemini, regra
  3j-i: pelo app, premium, nunca API). Prompts prontos no estudo. **Ainda não produzidos** —
  próxima peça se ele aprovar a linha.

**Pendências dele:** aprovar/recusar o Reel de 14/08 no Telegram. Slots de 17/08 em diante
estão VAZIOS (fila útil: 07/08 foto aprovada, 10/08 e 12/08 reels aprovados, 14/08 pendente).


## 🎬 O REEL DE 12/08 — SETE VERSÕES ATÉ ELE APROVAR (02-03/08/2026)

**Aprovado por ele no Telegram em 03/08/2026** (`approved`, confirmado no
post.json). Reação antes disso: *"Melhorou"*.

**As três broncas dele, na ordem, porque cada uma corrigiu coisa diferente:**
1. *"Tá horrível o conjunto do vídeo, coisa de amador, vc só colocou um texto,
   tem um puta time e entrega um resultado desse? Vcs basicamente me proporiam o
   vídeo que mandei… sejam criativos de vdd, ou mande todo mundo embora e faço eu
   mesmo."* → faltava MONTAGEM. Virou 7 cortes com movimento.
2. *"Vc me mandou o mesmo vídeo! Qual a sua dificuldade?"* → não era o vídeo,
   era o CANAL: regravei por cima do mesmo `video.mp4` e o Telegram, que guarda
   mídia pela URL, reenviou o antigo.
3. *"Cadê a música, não era pra ser algo divertido? Cadê a criatividade, não tem
   um storytelling."* → faltava TRILHA e ARCO. Virou uma história com música.

**A peça aprovada** (`studio/roteiros/2026-08-12_cabia-na-minha-mao.json`):
14s, 7 cortes. Ela cabia na mão dele → filhote de suéter → filhote correndo atrás
da bolinha **rosa** → **a virada:** adulta com a bola **vermelha** → praia → a
cama com as luzes da cidade → dormindo em cima da perna dele. Só 3 frases na
tela. Trilha própria (Lyria 3, US$ 0,04) que cresce **no corte da virada** —
encaixe achado com `astats`, não de ouvido.

**As lições, que já estão na skill (3n-i, 3n-ii, 3n-iii):**
- Reel é história com trilha; lista com texto carimbado ele reprova.
- **Quando o defeito é do material, troca-se o material.** A auditoria reprovou o
  mesmo corte 3x pelo mesmo motivo e eu insisti duas vezes em ajustar o
  enquadramento. Luz se corrige (`clarear` por gamma salvou o corte da virada);
  enquadramento de origem, não.
- Mídia refeita precisa de URL nova. Consertado no código
  (`postqueue.media_url()` assina com sha1), mas trocar o nome do arquivo também.
- Custo: 5 reprovações da auditoria antes do OK. Cada uma pegou defeito real que
  teria chegado nele.

**Ferramenta nova: `studio/montar_reel.py`** — o projeto não sabia cortar vídeo.
Corte seco, punch-in, zoom-out, acelerado, `aproximar`, `clarear`, texto com
entrada/saída e trilha com abafamento. Roteiro em JSON, não no código.
⚠️ Bug pago: `zoompan` ESTICA o clipe (1,8s viraram 36s, a peça saiu com 83s em
vez de 11,6). Zoom é feito com `crop` animado.

## 🔴 O ACERVO NUNCA ESTEVE ZERADO — e ele viu antes de mim (02/08/2026)

Palavras dele: *"Segue vídeos da hana… Até acho estranho vc não ter visto."*
Ele está certo. **Conduzi a reunião inteira sobre a premissa "o acervo de vídeo
está ZERADO", e era falso.** O garimpo já tinha aprovado 16 vídeos e 7 estavam
em disco em `Fotos da Hana\01 - brutas (suba aqui)\garimpo`. Eu repeti o aviso
do robô do lote sem abrir a pasta. **O que teria pego: um `ls`.** É o mesmo erro
da Regra Zero pela sexta vez, e desta vez contaminou a decisão de cinco diretores.

**Os 3 vídeos que ele mandou** (salvos em `01 - brutas (suba aqui)`):
- `hana_filhote_cenoura.mp4` — 22s, **já vertical 9:16**, ela filhote com o rosto
  ocupando a tela inteira comendo cenoura da mão dele. **O melhor material que o
  projeto já teve.** Virou o Reel de 12/08.
- `hana_filhote_bolinha.mov` — 24s, mas **deitado (16:9)**, precisa corte.
- `hana_creche_cachorros.mp4` — 19s, outros cachorros roubam o quadro.

**A varredura dos 7 do garimpo** (subagente olhou frame a frame):
| | o que é | nota |
|---|---|---|
| V03 | filhote de suéter rosa encarando a câmera | **8 — o melhor** |
| V07 | ela andando com bolinha vermelha na boca | 7 |
| V01 | deitada na cama, olhando a câmera, parada | 5 |
| V04 | brincando com outros dois cães | 5 |
| V06 | dormindo no colo, olhos fechados | 4 |
| V02 | **outro cachorro**, e some do quadro | 1 |
| V05 | **meme de pintinho fazendo ioga** | 0 |
⚠️ **Limite do garimpo confirmado na prática:** ele reconhece "isto é um cachorro",
não "isto é a Hana" — e nem isso: aprovou um meme de pintinho. **Toda saída do
garimpo precisa de olho humano antes de virar post.**

**O Reel de 12/08** (`content/queue/2026-08-12_cenoura-filhote`, `pending`):
15s do vídeo da cenoura, gancho "EU SÓ SEGURO A CENOURA", **áudio original da
cena** (sem música — o nicho roda em áudio original). Auditado: a 1ª versão foi
**reprovada** por faltar o acento em "SÓ" e o texto ficar na faixa da interface
do Instagram; corrigido e reauditado.
**O slideshow de 12/08 não foi apagado** — era teste medido autorizado por ele em
01/08. Foi **remarcado para 14/08** e continua esperando o OK dele.

## 🆕 REUNIÃO REFEITA COM DEBATE + A REVISÃO SEMANAL (02/08/2026)

Ordem dele: *"refaça a reunião com todas as ias, eles devem participar e precisa
que vcs debatam a ideia de cada um deles"* e *"na próxima reunião, revisar como
foi o andamento da estratégia dessa semana que passou. Assim conseguimos decidir,
e ir melhorando semana a semana."*

**Como foi feita** (formato novo, virou o padrão): rodada 1, cinco diretores
propõem sem ver a proposta dos outros (redes, criativo, atualidades, processos,
visual). Rodada 2, cada um recebe as outras quatro e é obrigado a atacar — com as
contradições apontadas na cara. Rodada 3, o conselheiro veta. Resultado: quatro
dos cinco retiraram ou rebaixaram a própria proposta. Debate de verdade muda voto;
rodada única de opinião não muda.

**O QUE O CONSELHEIRO VETOU**
1. Mexer nos 3 posts de foto já aprovados (hashtag, legenda ou corte). Formato
   já condenado e post já aprovado por ele — mudar exigiria novo OK.
2. A ronda de engajamento, **sem nem fazer o teste de 10 comentários**: 10
   comentários rendem de 0 a 2 seguidores, indistinguível de ruído, por 60 a 120
   mil tokens. "Teste que não pode responder não é teste." ⚠️ Como a ronda foi
   combinada COM o Ramón em 28/07, só ele encerra — **pendente de uma linha dele.**
3. Laudo de auditoria como argumento, quando o laudo é checável por código.

**O QUE FICOU APROVADO PARA A SEMANA (03 a 09/08)**
1. UM pedido a ele: a cena A PATROA MANDOU, prazo quinta 07/08, com roteiro e
   enquadramento já prontos no mesmo recado — uma tarefa, não três decisões.
2. Plano B engavetado: Reel com os ~4s de rosto achados no vídeo da praia. Só vai
   ao ar se a cena não chegar até quinta.
3. Radar de concorrente antes de fechar o Reel de 12/08.
Frase do conselheiro que resume: *"nada nesta mesa move 330 para 400. A mesa
inteira serve para uma coisa — o Reel de 12/08 existir com rosto."*

**🔴 ERRO DESCOBERTO NA REUNIÃO — a auditoria de 31/07 estava errada.**
O laudo dizia "o rosto não aparece em NENHUM frame dos 12 vídeos". Conferido em
02/08 com ffprobe e grade de frames (dois comandos):
- **Nunca existiram 12 vídeos.** Nove dos doze são clipes companheiros de Live
  Photo do iPhone, de 1,5 a 3 segundos, cada um com um .HEIC de mesmo nome ao
  lado. O acervo real sempre foi de **3 vídeos**.
- **IMG_1725.MOV (praia, 18,6s) TEM ROSTO** — cerca de 4 segundos, dela deitada
  na areia com a cabeça virada, focinho e língua à mostra. Os outros dois
  (TV e navio) o laudo acertou: de costas do começo ao fim.
O que teria pego: extrair os frames antes de escrever o laudo. O laudo errado
fez três diretores mudarem de voto na reunião. **Regra nova: laudo que dá para
conferir com dois comandos não é fato até ser conferido.**

**O MECANISMO DE REVISÃO SEMANAL (o pedido principal dele) — construído hoje**
- `estrategia/decisoes-<data>.json`: o Claude grava as decisões ao fim de cada
  reunião. Cada uma nasce com quatro campos obrigatórios — o que se espera que
  mexa, qual número, a **pré-condição checável por código** e a **regra de morte,
  escrita ANTES de saber o resultado** (regra de morte escrita depois é desculpa).
- `publisher/veredito.py`: lê o arquivo, confere no mundo real e devolve um
  veredito por decisão. Custo de token: zero — quem julga é código.
- `publisher/reporte_semanal.py`: passou a imprimir esse bloco **no topo** da
  pauta do domingo, antes até do diagnóstico, porque ele lê no celular e para de
  ler cedo.
- Três vereditos: **MEXEU · NÃO MEXEU · NÃO TESTADO**. O terceiro é o que faz o
  mecanismo sobreviver a semana em que nada foi feito: pré-condição que não
  aconteceu **nunca vira "falhou"** — vira "não testado", o contador de semanas
  sem execução sobe e a decisão continua na pauta.

## 🆕 COMANDOS PELO TELEGRAM + REUNIÃO NO DOMINGO (02/08/2026)

Duas ordens dele: *"Transfira a reunião estratégia de segunda para domingo às
9 da noite"* e *"Gostaria de poder te dar comandos dos Telegram."*

**Reunião:** era segunda 8h de Itajaí, agora é **domingo 21h**. A conta passou a
ser feita no fuso dele, não em UTC — domingo 21h em Itajaí é segunda 00h UTC, e
escrever "segunda, hora 0" seria a armadilha que faz a reunião cair no dia
errado. Testado nos 5 casos de borda (20h59 não dispara, 21h00 dispara).

**Comandos (`publisher/comandos.py`):** ele digita a palavra sozinha no Telegram
e o robô executa na rodada seguinte. São 6: `ajuda` · `estado` · `ver fila` ·
`placar` · `pausar` · `voltar`.
- Entram ANTES da recepcionista, senão "pausar" viraria papo do Gemini.
- Só casam com a **frase inteira** (até 4 palavras): "pausar" é comando, mas
  "acho que a gente devia pausar os posts de foto" é conversa. Testado.
- **Nenhum comando publica.** Quem publica continua sendo o botão Aprovar.
- `pausar` grava `content/.pausado` e o `run.py` para antes do laço de
  publicação — mas DEPOIS da recepção de mensagens, de propósito: senão ele
  pausaria e não teria como mandar `voltar` pelo celular.

⚠️ **Limite honesto, e ele foi avisado:** o robô acorda a cada 30 min. Não é
chat ao vivo — o comando entra na próxima rodada.

## 💸 O QUE CUSTA TOKEN NESTE PROJETO — medido em 02/08/2026

Ele perguntou se o que construímos está gastando muito. Resposta medida, com
os números que os próprios subagentes reportaram nesta conversa:

| Quem | Para quê | Tokens |
|---|---|---|
| Auditor de mídia | Prévia do Reel de 10/08 | 149.337 |
| Auditor de mídia | Slideshow, 1ª versão | 142.870 |
| Diretor de Criação | Montar o slideshow | 138.384 |
| Diretor de Criação | Escolher a trilha de 10/08 | 131.875 |
| Auditor de mídia | Slideshow, corte novo | 96.504 |
| Auditor de código | `mostrar_fila.py` | 95.356 |
| **Total** | | **754.326** |

**Auditoria de mídia = 388.711, ou 52% de tudo** — é o item mais caro do
projeto, porque cada auditor extrai frames e olha imagem por imagem.
**Custo zero de token:** publicador, placar, garimpo, comandos do Telegram,
lote de domingo, sentinela. A recepcionista roda em Gemini (centavos).
Nada disso fica ligado gastando: subagente só existe enquanto é chamado.

**Regra prática que sai daí:** cada Reel novo custa de **250 a 390 mil** entre
criação e auditoria, por causa da regra 3i (nenhuma mídia chega nele sem
auditor). Isso é o preço de não mandar vídeo com defeito — não é desperdício.

⏳ **PROPOSTA ESPERANDO O OK DELE (não é decisão):** separar a auditoria em
duas. A parte MECÂNICA — proporção 9:16, brilho, frame congelado, pico de
áudio, texto vazando — é medição e roda num motor barato. A parte de
JULGAMENTO — "isso ficou bom ou ficou estranho?" — continua no motor caro.
Cortaria a maior fatia sem perder a trava de segurança. **Ele não respondeu
ainda; não executar sozinho.**

## Onde paramos (02/08/2026, fim do dia)

**Fila com 5 posts aprovados, até 12/08.** 03/08, 05/08 e 07/08 são foto
(aprovadas antes da regra nova, exceção declarada por ele); 10/08 é o Reel
recortado em 9,8s com o pizzicato; 12/08 é o Reel-slideshow "a patroa mimada"
com ukulele — **o teste medido**. Ler o placar no dia 1 e no dia 3 do 12/08:
é ele que decide se slideshow volta ao cardápio ou sai de vez.

**Telegram virou canal de verdade.** Comandos (`ajuda`, `estado`, `ver fila`,
`placar`, `pausar`, `voltar`) e a recepcionista agora responde em vez de só
anotar — escalar deixou de descartar o que ela já sabia. Reunião estratégica
passou para **domingo 21h** no fuso de Itajaí.

**Garimpo parado por ora, na rodada 4** (~3.800 de 34.442 varridos, 36 fotos
dela em `02 - selecionadas`). Retomar é `python studio/garimpo.py --minutos 55`
+ eu triar os aprovados e apagar as cópias que não são ela.

**O que só depende dele:** filmar. Depois de 12/08 a fila acaba, e a regra
pede Reel de vídeo real com o rosto dela — o acervo antigo não tem isso
(conferido vídeo a vídeo, inclusive o único 1080x1920, que não serve).

## ✅ EU ESTAVA ERRADO: O DISCO NÃO É PROBLEMA — o garimpo voltou (02/08/2026)

**Correção de uma afirmação minha.** Eu disse a ele que o garimpo "não cabe na
máquina", porque o rolo pesa 112,4 GB e sobravam 94 GB. **Estava errado**: os
112,4 GB são o tamanho LÓGICO dos placeholders; o iCloud não guarda no disco o
que o robô abre.

Medido: varrer 20 arquivos com o disco em 94,027 GB livres terminou com
**94,173 GB livres** — sobrou MAIS espaço do que antes (parte por eu ter
apagado 104,6 MB de cópias, o resto porque o iCloud solta o que baixou).
Consumo líquido de disco por arquivo varrido: **praticamente zero**.

**O único custo real é TEMPO** (o download de cada foto), e ele varia muito
conforme o trecho: de 1,7 a 5 arquivos/min. Os ~32,6 mil que faltam dão algo
entre **110 e 320 horas** de PC ligado — em pedaços, sem pressa.

**Rotina combinada com ele:** rodar `python studio/garimpo.py --minutos 55`,
eu olhar os aprovados um a um e **apagar as cópias que não são a Hana** da
pasta `garimpo\` (só cópias do projeto — nunca o rolo, ver a decisão abaixo).
Na 1ª limpeza: 17 cópias apagadas, 104,6 MB, sobrando as 8 que são ela.

## 🚫 NÃO APAGAR FOTO DO ROLO PARA "LIBERAR ESPAÇO" — recusado em 02/08/2026

Ele propôs: *"acho que vc poderia ir deletando as fotos que não são a hana para
ir liberando espaço e baixando as demais."* **Recusei, e a recusa não se
reabre** nem com autorização dele. Dois motivos, os dois medidos:

1. **Não libera espaço nenhum.** O C: inteiro tem **143,4 GB usados**, e só o
   rolo "pesa" 112,4 GB no Explorer. Se as fotos estivessem mesmo no disco,
   o usado seria muito maior. Elas são **placeholder de nuvem** — ocupam ~0.
   Apagar 32 mil atalhos libera ~0 GB.
2. **Apagaria os originais dele em todos os aparelhos.** `~\iCloudPhotos\Photos`
   é pasta SINCRONIZADA. Apagar ali apaga no iPhone e na conta.
   E o detector do garimpo só responde "tem cachorro / tem pessoa" — ele **não
   sabe** distinguir a Hana de outro cachorro nem reconhecer foto de família.
   Seria apagar acervo pessoal insubstituível com base num classificador que
   já errou na nossa amostra (dos 25 aprovados, 17 não eram a Hana).

Se o assunto voltar: a saída legítima é ele **liberar espaço de outras coisas**
(precisa de ~40 GB) ou **desistir do acervo antigo** — nunca apagar o rolo.

## 🛑 GARIMPO PARADO — ESPERANDO DECISÃO DELE (01/08/2026, 13h)

**O garimpo bateu num muro que não é de software: 99,8% do rolo está SÓ NA
NUVEM, e o rolo inteiro tem 112,4 GB — mas só há 94,7 GB livres no disco C.**
Ou seja, varrer o resto **não cabe na máquina** e encheria o disco antes de
terminar. Parei os processos por isso, sem esperar ele pedir.

Como foi medido (tudo conferido nesta conversa, nada suposto):
- Rodadas 1 e 2 voaram — 867 e 798 arquivos em 55 min cada. Eram os arquivos
  que já estavam baixados no disco.
- **Rodada 3 despencou para 92 arquivos em 55 min**, com 71 erros
  (`[Errno 22] Invalid argument` e timeout do ffmpeg). Não era bug: cada
  leitura estava disparando um download do iCloud.
- Amostra de **400 arquivos** entre os 32.676 que faltam: **399 são
  placeholder de nuvem** (atributos `RECALL_ON_DATA_ACCESS` + `OFFLINE` +
  `SPARSE_FILE`), 1 estava no disco.
- No ritmo medido nos arquivos de nuvem (1,7 arquivo/min), o que falta levaria
  **~320 horas (13 dias) ligado** — não as 35 h que eu tinha estimado com o
  ritmo dos arquivos locais. **A estimativa de 35 h que dei hoje de manhã
  estava errada**, porque extrapolei do trecho fácil.

**Placar do que já rendeu:** 1.757 arquivos varridos, **25 aprovados**
(18 fotos + **7 vídeos**), em `Fotos da Hana\01 - brutas (suba aqui)\garimpo\melhores-30\`.
Ninguém olhou ainda — o detector só sabe "é um cachorro", não "é a Hana".

**As saídas (quem escolhe é ele):**
1. **Parar por aqui** e trabalhar com os 25 já garimpados + o que ele filmar.
   Custo zero. É o que eu recomendo: a linha editorial nova pede **vídeo com o
   rosto dela**, e disso o acervo velho é pobre por natureza.
2. **Deixar rodando dias**, aceitando internet ocupada — e ainda assim
   **esbarra no disco**: 112,4 GB não cabem em 94,7 GB livres.
3. **Ele mesmo baixar tudo do iCloud** antes (liberar espaço + "manter
   originais neste PC"). Só ele pode fazer, e resolve de vez.

Retomar é um comando só, quando ele mandar:
`python studio/garimpo.py --minutos 55` (o estado é salvo, nada se perde).

## FECHADOS, 01/08/2026 — os 7 itens do sinal amarelo da auditoria geral

Ordem dele: *"Sinal amarelo não é bom, precisa arrumar né… segunda quero o
resultado do fluxo 100%."* Os 7:
1. **Alarme de token cego** — `IG_TOKEN_EXPIRA_EM` não existia no GitHub porque
   `renovar_token.py` nasceu depois da última execução do notebook. Rodado
   manualmente (`python studio/renovar_token.py`), variável confirmada por
   `gh variable list` (2026-09-24). Sincroniza sozinha a cada boot do notebook.
2. **Fingerprint retroativo nos 4 posts aprovados** (03/08, 05/08, 07/08,
   10/08) — gravado `notified_fingerprint` usando a MESMA função de
   `telegram_approve._fingerprint()`, sem tocar caption/media/scheduled_for/status
   (provado por diff campo a campo antes/depois de cada gravação).
3. **Trava de auditoria** — o painel (Gemini/DeepSeek/Grok, sem objeção) e eu
   concordamos: blindagem criptográfica (GPG/branch protegida) é
   over-engineering para um projeto pessoal de 329 seguidores, porque a
   aprovação do Ramón no Telegram já é o gate humano externo ao repo antes de
   qualquer publicação real. Corrigido um bug real e independente: a isenção
   por DATA FIXA (`<= 2026-08-10`) nunca expirava sozinha — um `scheduled_for`
   forjado no passado escaparia da auditoria para sempre. Trocada por lista
   fechada dos 4 IDs isentos (`POSTS_ISENTOS_DE_AUDITORIA` em `run.py`).
4. **Fila até 10/08** — depende só dele filmar (fora do meu escopo). O alarme
   de fila com menos de 2 posts futuros (`sentinel.py::checar_fila`) foi
   testado com dado de mentira (fila vazia, 1 post, 2 posts) e dispara certo.
5. **`HANDOFF.md`** — apagado (`git rm`), mentia conta Business e post na fila
   já publicado; nada mais no projeto referenciava o arquivo.
6. **Comentário da tarefa "Hana Sentinela"** — dizia "seg/qua/sex 18:40",
   corrigido para "dom/seg/qua/sex 18:10" via `Set-ScheduledTask`. Gatilho
   (`StartBoundary`/`DaysOfWeek`) e ação conferidos iguais antes/depois — só o
   texto mudou.
7. **3 pastas vazias em `content/queue/`** — conferidas vazias (`find
   -mindepth 1`), não rastreadas no git, apagadas com `rmdir`.

**Bônus fora da lista:** `publisher/sentinel.py` era o único arquivo do
`publisher/` sem `sys.stdout.reconfigure()` — corrigido (achado testando o
item 1, não crashava no GitHub Actions porque o runner já é UTF-8, mas
quebraria em qualquer outro ambiente).

**Também provados com dado de mentira** (nunca tinham cruzado com post real):
`publisher/leitura_d1.py::montar()` (3 cenários: post de 24h aparece, post já
lido não repete, sem métrica sai calado) e a trava de auditoria com um ataque
explícito (forjar `scheduled_for` no passado — bloqueado).

## Onde paramos (01/08/2026)

**FEITO, 01/08/2026 — o "beco sem saída" do rolo de câmera (`iCloudPhotos\Photos`)
deixou de ser beco sem saída.** O Ramón autorizou o garimpo ("Pode começar o
garimpo"). Construído `studio/garimpo.py`: detector de objetos LOCAL (YOLOv8n,
ultralytics, CPU, offline — **nenhuma foto sai da máquina**, só o modelo de
~6 MB foi baixado do GitHub oficial) que reconhece `dog` e `person` e aprova só
quem tem cachorro e NÃO tem gente no quadro — a mesma régua da fronteira com o
Canecas. Testado com dado real do próprio projeto antes de rodar no acervo:
achou a Hana com 87% de confiança numa foto já aprovada, e rejeitou
corretamente uma foto com o Ramón (pasta `07 - nao compartilhar`) por "tem
pessoa no quadro". Suite de teste isolado (scratchpad, nunca toca produção)
confirmou aprovação, cópia, ranking, relatório e retomabilidade.
**ACHADO QUE MUDA O PLANO — medido, não suposto:** a pasta é sincronizada pelo
iCloud em modo "otimizar armazenamento" — a maioria dos arquivos é um
placeholder que precisa ser BAIXADO DA NUVEM pra abrir. Amostra real de 10
arquivos: média de **9,3 segundos por arquivo** (a maior parte é o
download/decodificação; o detector em si fica em 0,3-2,7s). Para os 34.431
arquivos inteiros isso dá **~89 horas seguidas** — inviável numa sessão só.
Por isso o robô é **retomável de verdade** (grava progresso a cada 10
arquivos em `studio/.garimpo_estado.json`, fora do git) e roda em pedaços com
`--minutos N`. Uma rodada de 75 min foi deixada rodando ao fim desta sessão;
o progresso e os achados ficam em
`Fotos da Hana\01 - brutas (suba aqui)\garimpo\RELATORIO.md` (top 30 em
`garimpo\melhores-30\`). **Para continuar:** `python studio/garimpo.py
--minutos 60` (ou mais) quantas vezes quiser — nunca reprocessa o que já viu.
**LIMITE HONESTO que precisa acompanhar qualquer achado deste robô:** o
detector reconhece "é um cachorro", não "é A Hana" — não existe reconhecimento
individual. Se o rolo tiver foto de cachorro de outra pessoa (amigo, canil,
rua), ela passa no filtro do mesmo jeito; quem confirma que é ela é o Ramón,
olhando o ranking. Vídeo é julgado por 5 frames amostrados (~primeiros 5s),
não pelo clipe inteiro.

## Onde paramos (31/07/2026)

## 👉 COMEÇAR A PRÓXIMA CONVERSA POR AQUI (respostas dele, 01/08/2026)

Ele fechou a conversa anterior com três respostas e pediu que a próxima já
continue daqui. **Não perguntar de novo — executar.**

1. **A CENA: ele não achou nada aproveitável nas fotos dele e vai FILMAR.**
   Palavras dele: *"Como vc quer a cena, me traga aqui, não achou nada que possa
   ser usado nas minhas fotos."* O roteiro completo está em
   `content/pedido-de-cena.md` e foi entregue a ele no chat. **Ao abrir, perguntar
   se ele já filmou** e, se sim, rodar o lote/Diretor de Criação em cima do
   material novo. A regra que não pode faltar: **rosto da Hana de frente nos 2
   primeiros segundos** — foi o defeito que reprovou os 12 vídeos do acervo e o
   próprio Reel de 10/08.
2. **REEL DE 10/08: ELE PEDIU A PRÉVIA DO RECORTE.** *"Me da uma prévia."*
   Ou seja: **recortar**, não subir como está. Tirar os 2,7s finais (43% mais
   escuros, ela vira vulto) e fechar no movimento — fica ~11s. A trilha
   `03-comico-pizzicato` já está aprovada tecnicamente pela auditoria e deve ser
   mantida. **A prévia PRECISA passar pelo auditor antes de chegar nele**
   (regra 3i) e ele precisa **ouvir** para decidir (regra 3g).
   ⚠️ Prazo real: o post sobe **10/08 às 21:00Z**. Se o recorte não estiver
   aprovado até lá, sobe a versão atual, que já está aprovada por ele.
3. **GARIMPO: autorizado a rodar.** *"Pode rodar."* Começou em 01/08 em segundo
   plano (`studio/garimpo.py --minutos 55`). É retomável e leva ~89h no total —
   rodar em pedaços, sem pressa: `python studio/garimpo.py --minutos 60`.
   Resultado em `Fotos da Hana\01 - brutas (suba aqui)\garimpo\`.

## Onde paramos (01/08/2026 — leia isto primeiro)

**O PROJETO SAIU DO AMARELO — os 7 itens da auditoria estão fechados e provados.**
Ele cobrou: *"Sinal amarelo não é bom, precisa arrumar né… segunda quero o
resultado do fluxo 100%."*
1. **Alarme de token deixou de estar cego.** Ele ligou o notebook, rodei
   `renovar_token.py` e a variável passou a existir: `IG_TOKEN_EXPIRA_EM =
   2026-09-24` (`gh variable list`). **Token válido até 24/09.**
2. **Os 4 posts da fila ganharam impressão digital** (`notified_fingerprint`) —
   agora, se alguém mexer na legenda ou na mídia depois de ele aprovar, o post
   volta para aprovação. Conferido no `git diff`: **só o campo novo entrou**,
   legenda/mídia/horário/status intactos.
3. **A isenção da trava de auditoria deixou de ser por DATA e virou lista dos 4
   IDs.** A data fixa (`<= 2026-08-10`) nunca expirava — um post forjado com data
   no passado escaparia da auditoria para sempre. Testado o ataque exato.
   **Decisão registrada:** blindagem criptográfica (GPG, branch protegida) foi
   avaliada e **descartada** — o gate humano de verdade é a aprovação dele no
   Telegram (`REQUIRE_APPROVAL=1`), que acontece antes de qualquer publicação.
   Painel de 3 IAs consultado; as 3 responderam SEM OBJEÇÃO à decisão.
4. `HANDOFF.md` **apagado** — estava parado em 27/07 e mentia (dizia conta
   "Business", que é **Criador**, e citava post publicado como se estivesse na fila).
5. Comentário da tarefa `Hana Sentinela` corrigido (dom/seg/qua/sex 18:10);
   gatilho e ação conferidos iguais antes e depois.
6. Três pastas vazias em `content/queue/` apagadas.
7. `leitura_d1.py` e a trava de auditoria foram provados com dado de mentira em
   ambiente isolado — nunca em `content/` real.
**O único item que continua aberto não é bug: a fila acaba em 10/08 e depende de
ele filmar.** O alarme de fila vazia está confirmado funcionando.

**NOVO ROBÔ, 01/08/2026 — `studio/garimpo.py` (autorizado por ele).**
Varre o rolo de câmera do iPhone (`C:\Users\Ramón França\iCloudPhotos\Photos`,
**34.431 arquivos**) atrás de foto e vídeo com cachorro **e sem pessoa** — o
filtro da parceria por construção. Detector **YOLOv8n local, offline**: nenhuma
imagem sai da máquina, porque a pasta é o rolo pessoal dele.
**Medição que muda o plano:** a pasta é iCloud "sob demanda", então cada arquivo
é baixado na hora — **9,3 segundos por arquivo**, ou seja, **~89 horas** para
varrer tudo. Por isso o robô é **retomável**: grava progresso a cada 10 arquivos
e nunca reprocessa. Rodar aos poucos: `python studio/garimpo.py --minutos 60`.
Saída em `Fotos da Hana\01 - brutas (suba aqui)\garimpo\` (+ `melhores-30`).
**Limite honesto e declarado:** o detector reconhece "é um cachorro", **não** "é
a Hana" — não há reconhecimento individual. Cachorro de terceiro passa no filtro.
Quem confirma é o Ramón, olhando o ranking.

**AUDITORIA DE MÍDIA — O REEL DE 10/08 FOI REPROVADO, e não é pela trilha.**
Ele pediu *"Coloque uma trilha"*; o Diretor de Criação produziu
`Fotos da Hana\05 - APROVAR (semana)\05_PREVIA-TRILHA.mp4`.
**A trilha passou em tudo:** é música de verdade (120 BPM, sol maior, alegre,
instrumental), entrou a −12 dB, o som da cena ficou intacto (correlação 0,973,
cena 11,8 dB acima da trilha) e não há estouro (−0,35 dBFS).
**O que reprovou foi o CORTE-BASE, que já vinha do Reel original:** os **2,7s
finais são 43% mais escuros** (brilho 88,9 → 51) e a Hana vira um vulto; há 2s de
close de pelo ilegível no meio; e termina parado, sem desfecho. **Remixar não
resolve — tem que recortar.**
⚠️ **PENDENTE DELE:** recortar o Reel (ficaria ~11s, terminando no movimento) ou
subir como está em 10/08, que ele já aprovou.
**CORREÇÃO DE UM ERRO MEU:** eu acusei o produtor de mentir sobre "stream copy".
Ele estava certo — o bitstream da prévia é **prefixo byte a byte** do original;
só os 3 frames finais (cena parada) foram aparados pelo `-shortest` do
`reel_de_video.py`. Eu afirmei sem medir direito.

**🔴 BUG ACHADO — `studio/gerar_trilha.py` CARIMBA "ok" EM QUALQUER COISA.**
A trilha `content/trilhas/02-lofi-sofa.mp3` **não é música**: correlação **+0,98**
com o áudio do próprio vídeo da Hana, andamento 53,3 BPM (o da cena, não os 80 do
prompt). O `extrair_audio()` aceita qualquer string grande que a API devolver,
pega a primeira e grava como `.mp3` **sem conferir se é áudio, se é música ou se
difere das outras faixas**. Não deu para concluir de onde veio a contaminação —
o script só manda texto para a API e nunca abre o vídeo.
**Não gerar trilha nova antes de consertar isso.** As faixas `01` e `03` foram
medidas e são música de verdade.

**DECIDIDO POR ELE, 01/08/2026 — A RONDA DE ENGAJAMENTO ESTÁ SUSPENSA.**
Palavras dele: *"Pode suspender então a ronda."* Fecha a pendência aberta desde
28/07. Motivo medido: a única ronda real (4 comentários, 27/07) **não trouxe
seguidor**, e ela custava 60 a 120 mil tokens por rodada, 3x por semana.
**Revisita em 13/08**, depois da leitura do Reel de 10/08 — não antes, e não por
intuição. Não propor ronda nesse meio-tempo.

**EM ANDAMENTO, 01/08/2026 — trilha do Reel de 10/08 (ele pediu: "Coloque uma
trilha").** O Diretor de Criação produziu `Fotos da Hana\05 - APROVAR (semana)\
05_PREVIA-TRILHA.mp4` — trilha `03-comico-pizzicato` misturada a -12 dB por
baixo do som da cena. Escolha justificada por assistir o vídeo: ela passa **10
dos 14 segundos parada**, e a faixa densa (194 ataques/min) segura o miolo.
**A PRÉVIA NÃO FOI MOSTRADA A ELE**: a auditoria obrigatória (regra 3i) foi
cortada por limite de sessão e ficou **incompleta**. O que ela alcançou a apontar
antes de morrer: o produtor afirmou "stream copy, imagem não reprocessada" e
**isso é falso** — conferido por mim, o vídeo foi re-encodado (417 frames contra
420, bitrate 6116→6138, duração 14,00s→13,98s). Resolução e proporção seguem
certas (1080x1920, 9:16), então o defeito é a **afirmação falsa**, não a imagem.
**Falta auditar:** anatomia, cor tri lilac merle, e o item mais importante — se a
faixa usada é música mesmo. Motivo: o Criador descobriu que
`content/trilhas/02-lofi-sofa.mp3` **não é música**, tem correlação +0,98 com o
áudio do próprio vídeo (ou o `gerar_trilha.py` gravou o som da cena com nome de
trilha, ou o arquivo foi trocado). **Conferir o `gerar_trilha.py` antes de gerar
qualquer trilha nova.**

**FECHADO, 31/07/2026 — a chave do Gemini NÃO será trocada.** Decisão dele:
*"não troca... para de encher o saco com isso"*, depois de eu conferir e provar
que a chave **não está no repositório público nem no histórico do git** — ela só
apareceu na saída de terminal desta conversa. Risco baixo, e a palavra dele
**encerra o veto do conselheiro** (ele está acima do conselheiro, que está acima
de mim). **Não reabrir o assunto.**

**REGRA DO MOTOR, aprovada por ele em 31/07/2026.** Eu **não consigo** trocar o
motor da conversa — só ele, com `/model`. O que eu faço é **rotear o trabalho**:
conselheiro em Fable, volume em Gemini/DeepSeek, código no diretor de automação,
enquanto a conversa fica onde ele deixou. Combinado: conversa no **Opus** por
padrão, eu roteio sozinho, e **só peço a troca quando o raciocínio final for a
entrega**. Ele avisou: *"Fable gasta muito"* — então Fable é para decisão de
dinheiro e leitura de resultado, não para escrever arquivo.

**FEITO, 31/07/2026 — o CRIADOR existe.** `~\.claude\agents\diretor-criacao.md`.
Dono único do trecho, do gancho, da legenda e da trilha, trabalhando **a partir
do plano do comitê**, nunca de improviso. Entrega pacote fechado em
`content/pacote-da-semana.md` — condição do conselheiro: sem gravar arquivo, ele
veta o cargo. A pauta de segunda passou a **cobrar o pacote** (item 7), porque o
cargo não pode depender de alguém lembrar. Ele não aprova nada: o pacote passa
pelo auditor antes de chegar ao Ramón.
E `content/pedido-de-cena.md` foi escrito — o robô já lê o arquivo de verdade,
não a reserva (conferido). A regra nova que faltava e é a mais importante:
**rosto da Hana de frente nos 2 primeiros segundos**.

**(RESOLVIDO — ver acima) A GEMINI_API_KEY apareceu em texto puro numa saída de terminal.** Um diretor
errou um comando e a chave saiu em texto puro numa saída de terminal. **Ele
precisa regenerar** em `aistudio.google.com/app/apikey` e me avisar — o secret
`GEMINI_API_KEY` do repo tem que ser atualizado junto (foi gravado hoje, 21:19Z).
Telegram e Instagram **não** vazaram. **O conselheiro VETOU** qualquer construção
de governança nova enquanto a chave não for trocada, e o veto dele está acima do
meu por ordem do Ramón (ver abaixo). Enquanto isso, só robô e correção de bug.

**CONSERTADO, 31/07/2026 — três coisas que dependiam dele deixaram de depender.**
Ele mandou *"arrume meu amigo"* em vez de sair criando credencial. Estava certo.
1. **O robô de domingo não precisa mais de senha na máquina dele.** Ia ser um
   `studio/.telegram` com o token do bot — senha em dois lugares é senha para
   vazar em dois lugares. Agora o robô local empurra `content/aviso_lote.md`
   para o repositório e o novo `publisher/avisar_lote.py` entrega no Telegram
   com o secret que já existe no GitHub. **Token continua num lugar só.**
2. **O cron do GitHub pula rodadas — medido, não suposto.** Em 31/07 ficou
   **2h44 sem nenhuma rodada agendada** (última às 20:43Z, nada até 23:27Z), e
   o post das 21:00Z só foi ao ar porque houve disparo manual. O cron de repo
   público é best-effort. Defesa: além do `*/30`, entrou uma salva de 6
   tentativas coladas em 21:00Z de seg/qua/sex. O `run.py` é idempotente, então
   repetir não duplica post. **Vigiar se volta a acontecer.**
3. **A rodada das 20:43 tinha FALHADO** e ninguém tinha visto: o passo "Salvar
   estado da fila" deu push simples enquanto eu empurrava da minha máquina e
   foi rejeitado. Agora rebaseia e tenta 3 vezes — provado, "estado salvo
   (tentativa 1)".
Mais: a recepcionista ganhou **modelo reserva** (`gemini-flash-lite-latest`),
porque o Flash devolveu "high demand" no primeiro teste, e o `maxOutputTokens`
subiu de 2000 para 8000 — ela morria antes de escrever a primeira letra.
Rodada de verificação 23:3xZ: **todos os passos verdes.**

**REGRA NOVA DE GOVERNANÇA, 31/07/2026** (ordem dele): *"todos o trabalho quando
for apresentado para mim precisa ser revisado para não ter erros… Coloque as ia
para questionar o trabalho um do outro… O conselheiro fable tem voz ativa acima
da do presidente."*
- **O conselheiro pode vetar o presidente (eu).** Vetado = não executo. O veto
  dele nunca passa por cima do Ramón, só por cima de mim.
- **Quem constrói não aprova.** O auditor nunca é o autor.
- **Faixa da revisão dupla** (proposta do conselheiro, ainda sem o OK dele):
  o que chega ao Ramón · o que sai em público · o que mexe em dinheiro · porta
  sem volta · o que toca segredo ou credencial. O resto passa com uma leitura.
  Motivo: revisão dupla em legenda que 47 pessoas leem é burocracia; em segredo
  e conta, é o que faltou hoje.
- **Nenhum diretor novo.** As 11 cadeiras cobrem tudo — cargo sem trabalho é
  custo. Isso responde o "crie diretores": eles já existem.
**Isto ainda não está escrito na skill** por causa do veto acima.

**FUNCIONOU NA PRIMEIRA APLICAÇÃO — a revisão adversarial pegou 6 defeitos.**
Dois graves, nos robôs que os diretores acabaram de construir:
(1) `publisher/.telegram_offset` estava no `.gitignore`, então o `git add` do
workflow falhava calado e **todo runner começava do zero** — as mensagens do
Telegram voltavam a cada 30 min. A prova estava no `content/recados.md`: a mesma
mensagem de 19:03 gravada duas vezes. Com a recepcionista isso viraria até 48
chamadas ao Gemini por dia, por mensagem.
(2) a recepcionista prometia no docstring que "nunca deixa exceção escapar" e
**não era verdade** — três chamadas de rede ficavam fora do try, e um timeout do
Telegram derrubaria o `run.py` inteiro, ou seja, **os posts do dia não subiriam**.
Corrigidos os dois, mais o marcador `[ESCALAR]` frágil (o Flash põe negrito
sozinho e o `startswith` cru falhava) e o `run.py`, que agora blinda a leitura do
Telegram. **Se ninguém tivesse revisado, isso ia para produção.**

**DECIDIDO POR ELE, 31/07/2026 — NÃO EXISTE PRODUTO, E ISSO É DE PROPÓSITO.**
Palavras dele: *"por enquanto não tem produto, é apenas a hana crescendo por ser
foda e bonitinha…. Acho que ainda não chegamos no ponto de anunciar esse tipo de
produto, não temos pessoas suficientes e ainda não tivemos melhora nas nossas
ações."* Isso **encerra** a cobrança do conselheiro (item D abaixo) e responde as
3 hipóteses que o diretor-vendas montou (peitoral de bully / camiseta do dono /
guia de medidas em PDF): **nenhuma foi escolhida, e não é para escolher agora.**
- **Não propor produto, loja, preço, teste de oferta, link na bio nem parceria
  comercial nova** enquanto ele não reabrir. O `diretor-vendas` continua fora do
  organograma, e agora por decisão dele, não por falta de assunto.
- **O objetivo hoje é um só: fazer a Hana crescer.** Conteúdo por conteúdo, sem
  segunda intenção comercial.
- As 3 hipóteses ficam guardadas em `content/hipoteses-produto.md` — se ele
  reabrir, não se refaz o trabalho. **Guardado ≠ aprovado.**
- Os dois motivos que ele deu são medíveis, e é assim que o assunto volta:
  (1) "não temos pessoas suficientes" → seguidores; (2) "não tivemos melhora nas
  nossas ações" → salvos, compartilhamentos e seguidores ganhos, hoje zerados.
  **Falta ele definir o número que reabre a conversa** (proposto, sem resposta).

**APROVADO POR ELE, 31/07/2026 — a virada editorial. Palavras dele: *"Aprova
todos. mas mantenha esses post já aprovados, a partir dos proximos voce executa
da maneira que sugeriu"*.** Reuni o comitê (diretor-redes + diretor-criativo +
conselheiro) em cima do placar medido e ele aprovou os 5 pontos em que os três
concordaram:
1. **Foto parada sai de cena** (testada 4x: 0 salvo, 0 compartilhamento, 0
   seguidor nas quatro). Sai junto o **carrossel** (é foto com outro nome) e o
   **Reel-slideshow** (foto parada disfarçada de vídeo).
2. **Reel de vídeo real é o formato**, com o **rosto da Hana obrigatório** no
   quadro.
3. **1 Reel por semana, não 2** — sobe para 2 só na semana em que houver sessão
   de filmagem. O plano de 2/semana não se sustenta com ele trabalhando em
   tempo integral.
4. **O acervo manda no calendário, não o contrário.** Data fixa com acervo
   vazio foi o que fabricou as 4 fotos paradas.
5. **O pilar "a cor tri lilac merle" cai** — bonito e sem conflito, morre na
   régua nova.
**A EXCEÇÃO QUE ELE DEU, e que não pode ser esquecida:** os posts **já
aprovados ficam** — 03/08, 05/08, 07/08 (fotos) e o **Reel-slideshow de 10/08**
vão ao ar como estão. A regra nova vale **a partir do primeiro post depois de
10/08**. Nada foi cancelado da fila. Se uma conversa futura for "limpar" a fila
em nome da régua nova, está errada: ele decidiu o contrário, com estas palavras.
**Ajuste técnico que veio junto:** o pilar INIMIGOS DA PATROA fica, mas com
desfecho novo — ela **late e expulsa** ou **ignora e sai andando**, nunca foge
(cão com medo contradiz "ela manda"). Ganchos prontos para as cenas de 01/08:
"Mandei. Já vai." · "Sai, o trono é meu." · "Ninguém acorda a patroa."

**AINDA ESPERANDO DECISÃO DELE — as 3 divergências do comitê + 1 cobrança.**
Estão escritas em `content/pauta_extra.md` e entram na pauta de segunda 03/08:
(A) **qual é o gargalo** — redes diz CANAL (foto de feed não tem porta de
entrada; 47 ÷ 329 = 14% é a base dele, não gente nova), criativo diz FALTA DE
ARCO (nenhuma peça tem desfecho, identificação ou pedido de salvar);
(B) **TikTok como laboratório de gancho** — mesmo master 9:16, custo marginal
zero, lá conta nova é entregue a estranho por padrão;
(C) **métrica que decide** — redes quer trocar "seguidores ganhos" por "% de
alcance vindo de não-seguidor" (com 47 de alcance, 1 seguidor é ruído);
conselheiro quer **parada dura em 30/09/2026: 500 seguidores ou 1.000 contas
alcançadas**, senão para ou muda de rota;
(D) **a cobrança dura:** o produto a ser vendido **não existe nem no papel**. O
conselheiro exige uma hipótese de produto escrita, senão isto é hobby
consumindo o fim de semana dele. **Não é decisão minha — é dele.**

**FEITO, 31/07/2026 — canal Claude → Telegram** (`publisher/mandar_recado.py`).
O bot só sabia falar sozinho (post para aprovar, pauta de segunda) e o token
mora nos secrets do GitHub, então eu não tinha como mandar recado. Agora
`publish.yml` aceita a entrada `recado`:
`gh workflow run publish.yml -R ramonduranp6-ai/hana-social --json < arquivo.json`
com `{"recado": "texto"}`. Testado ponta a ponta em 31/07 20:18Z — log do job:
`[ok] recado entregue (1219 caracteres)`. **Custo zero.**
Usado para pedir a ele as 3 cenas de 01/08.

**RESPONDIDO, 31/07/2026 — não existe "recepcionista" no Telegram.** Ele
perguntou se o bot responde as mensagens dele. Conferido em
`publisher/telegram_approve.py`: o bot é API do Telegram lida pelo GitHub
Actions a cada 30 min; quando ele escreve texto, o robô **anota** em
`content/recados.md` e devolve uma frase fixa. **Não há resposta inteligente** —
quem lê e responde sou eu, na conversa seguinte. Não prometer o contrário.

**DÍVIDA QUITADA, 31/07/2026 — o robô do lote parou de fabricar foto.** Eu tinha
decidido isso de manhã e não tinha implementado; ele mandou resolver (*"Pode
resolver e atualizar tudo"*). Agora, no domingo, `lote_automatico.py` procura
**vídeo novo**: se achar, monta rascunho de Reel em `06 - videos e trilhas/
rascunhos` (sem gancho, sem entrar na fila — trecho e gancho são julgamento);
se não achar, **não inventa post** e escreve em `content/aviso_lote.md` o pedido
das duas cenas que faltam. Os 12 vídeos velhos já entraram em
`content/.videos_usados`, então o robô só volta a trabalhar quando ele filmar.
Consequência: **domingo 02/08 não nasce lote nenhum** — e isso é o certo, porque
a alternativa era mais três fotos do formato que mediu zero quatro vezes.

**PENDÊNCIA ABERTA — o teste do bot de recados nunca foi feito.** Ele disse que
ia mandar mensagem no Telegram e a conversa acabou antes; `content/recados.md`
não existe ainda. Na próxima conversa, confirmar se o recado chega.

**TESTE DO TIME, 31/07/2026 — o auditor funciona e o acervo não presta.**
Montei o primeiro Reel de vídeo real (a Hana assistindo um cachorro na TV,
`IMG_2972.MOV`) e mandei ao auditor antes de mostrar ao Ramón, como manda a
regra 3i. **Reprovado duas vezes, com medição** — não com opinião: (1ª) pescoço
lendo como quebrado em 2 frames, pelo virando sépia no fim (R/B saltando de 1,5
para 4,68), texto do gancho por cima da cabeça dela e dentro da faixa da
interface do Reels; (2ª) cor corrigida e texto descido — confirmado —, mas o
pescoço continua e **a TV sai de quadro no meio** (pixel vivo no terço superior
caindo de 47,8% para 2,9%), porque a câmera se move.
**Conclusão que vale mais que o Reel:** o problema é o BRUTO, não a montagem —
a Hana está de costas o tempo todo e o rosto dela não aparece em nenhum frame.
Sem cena nova, este material não vira Reel. Isso confirma, com evidência, a
objeção que o conselheiro tinha levantado no desenho da linha editorial.
**O que o auditor evitou:** eu teria mandado ao Ramón, pela segunda vez, um
vídeo em que a cadela parece ter quebrado o pescoço.

**FEITO: `studio/reel_de_video.py`** — o projeto só sabia montar slideshow de
foto. Agora monta Reel de vídeo real (normaliza a rotação do iPhone, corta 9:16,
grava o gancho em PNG sobreposto, mantém o som da cena). Padrão do gancho ficou
em 16% do topo, medido pelo auditor: a 10% ele cai dentro da interface do Reels.

**PENDENTE DELE — filmagem.** Sem isso a linha editorial morre em 3 semanas.
Ele já se ofereceu para gravar ("posso fazer vídeos e tudo mais que precisar").


**COBRANÇA EM ABERTO — a decisão da NUVEM é dele, em outro projeto.** Palavras
dele, 31/07/2026: *"Sobre a nuvem ainda estou estudando, e não vai ser com você
aqui, vou decidir isso em outro projeto, em breve você receberá a notícia... mas
mantenha no seu radar para me cobrar isso."* Ou seja: **não propor arquitetura de
nuvem para a Hana** — só perguntar, a cada sessão, se a decisão já saiu. O que
está em jogo: hoje as rotinas locais dependem do notebook dele ligado.

**REGRA NOVA — o operacional é ROBÔ, não é Claude** (ordem dele, 31/07/2026:
*"não use a claude, crie robôs operacionais fora para claude para fazer isso,
vamos economizar tokens"*). Toda tarefa repetitiva do projeto nasce como script
que roda sozinho; o Claude só entra no que exige julgamento. Vale como régua
para a estrutura de times que ele pediu no mesmo dia (operacional × estratégico).

**FEITO em 31/07/2026 — conserto do robô local `Hana Sentinela`.** Ele tinha
desligado o notebook e a tarefa não roda desde 27/07 (log `studio/sentinela.log`
parado). Causa conferida no Agendador: `StartWhenAvailable=False` (horário
perdido não é recuperado) e `DisallowStartIfOnBatteries=True` (não roda fora da
tomada). Corrigido para `StartWhenAvailable=True` e rodar na bateria: agora,
sempre que o PC ligar depois de um horário perdido, ele se recupera sozinho —
custo zero de token. Rodado à mão uma vez (31/07 14:10): "tudo em dia", token do
Instagram válido, nada vencido. **Nenhum post ficou parado** — quem publica é o
`publish.yml` no GitHub, que roda a cada 30 min e não depende da máquina dele.
**Ponto ainda frágil, não resolvido:** a renovação do token do Instagram só
existe no robô local; se o notebook ficar semanas desligado, o token expira.

## Onde paramos (28/07/2026 — fim do dia)

**FEITO em 28/07/2026 — o campo "Nome" do perfil virou palavra-chave de busca.**
Ele perguntou o que dava para configurar no Instagram para ganhar seguidor.
Auditoria completa do perfil feita na tela (subagente, só leitura): conta
**pública**, "Mostrar sugestões de contas em perfis" **ligada**, indexação em
buscadores **ligada**, "Quem pode criar com seu conteúdo" = **Todos**, status da
conta sem nenhuma restrição. Ou seja, **configuração não era o problema** — só
uma alavanca estava sobrando: o campo **Nome**, que o Instagram indexa na busca,
estava "Hana Duran Sanches" (ninguém procura por isso). Ele autorizou e o nome
passou a ser **"Hana 🐾 Exotic Bully Micro"** — confirmado na tela do perfil.
**Falha honesta desta sessão:** eu não consegui digitar — o classificador de
segurança do Claude bloqueou `type` e `form_input` na tela da Meta. Achei a tela
certa (Central de Contas → perfil → Nome, editável na web, limite de 2 trocas em
14 dias) e **ele digitou**. Se precisar mexer de novo em campo de conta pela
Central de Contas, já contar com isso: o caminho é eu abrir a tela e ele digitar.
**Limite declarado:** isso é ganho pequeno, de descoberta por busca. O placar
continua dizendo que o gargalo é alcance de conteúdo, não configuração.
Achados que sobraram sem decisão (não propostos ainda): **zero destaques** no
perfil e **link/site vazio**; o rótulo de categoria está **oculto** de propósito.

**FECHADO: a trilha do Reel de 10/08 fica como está** (a lo-fi própria já
aplicada). Palavras dele: *"por enquanto vamos manter como está, nos próximos eu
aprovo novamente"*. Ou seja: **não mexer mais na trilha do 10/08**; a conversa de
música volta na produção dos PRÓXIMOS Reels.

**FEITO em 28/07/2026 — separação do pessoal e do da Hana.** Ele perguntou se os
posts vão para o Facebook: **não vão**, o publicador é só Instagram. Propus ligar
o compartilhamento automático para alimentar a Página de graça e **estava errado**
— a tela só oferece mandar para o **perfil pessoal do Ramón**, não para a Página.
Não liguei. E encontrei o **story já ligado** (stories da Hana caindo no Facebook
pessoal dele): **desliguei as duas chaves** com o OK dele — *"não podemos
misturar o pessoal com o da hana"*. Regra na skill (3b-ii).
**ENCERRADO: a Página do Facebook fica vazia, de propósito.** Eu ia deixar ele
pôr foto de perfil e capa; ele cortou e está certo — *"como não vamos usar o
facebook, não tem porque a Hana estar com foto de capa e perfil"*. A Página é só
encanamento da Graph API (áudio de tendência). Não reabrir. Só não pode ser
apagada nem desligada do Instagram, senão a API de áudio cai.

**NOVO em 28/07/2026 — o projeto passou a MEDIR.** Ele escolheu a automação do
placar (*"faz a 1"*). `publisher/metrics.py` roda dentro do publicador que já
existia (regra do robô único), **uma coleta por dia**, e escreve
`content/metricas.json` + `content/placar.md`. Testado ponta a ponta com o token
real. **Primeiro número medido, e ele é duro:** 329 seguidores, alcance de
**30 a 50 por post** (~13% da base), **0 salvamento** e **0 seguidor ganho** nos
3 posts publicados. Tradução: o conteúdo circula só na rede pessoal do Ramón e
não converte quem vê em seguidor. Confirma por número o que estava escrito em
`content/metricas.md`: **o gargalo é alcance**. Próxima leitura fica mais rica
quando o Reel de 10/08 entrar (aí dá para comparar Reel x Foto de verdade).

**NOVO em 28/07/2026 — o lote de domingo virou robô de verdade** (*"faz o 1"*).
`studio/lote_automatico.py`: edita as brutas, separa as inéditas, pede a legenda
ao **Gemini Flash mostrando a foto** e cria 3 posts `pending`. Entrou dentro da
tarefa `Hana Sentinela`, que passou a rodar **também aos domingos** — nenhum
agendamento novo. **Custo: zero token Claude**, fração de centavo do crédito
Gemini por foto. Testado com foto real; as duas legendas saíram no tom da patroa
mimada, com pergunta e 4 hashtags. Detectou 7 fotos inéditas das 14 editadas e
agendaria a partir de 12/08 (respeitando a fila que já existe).
**O que continua comigo:** Reel (montagem e gancho), trilha, e a ronda de
engajamento.

**CORRIGIDO em 28/07/2026 — o robô `hana-rotina` NUNCA EXISTIU.** Ele perguntou o
que ainda gasta token; fui conferir o Agendador do Windows e a única tarefa é
**`Hana Sentinela`** (`studio\sentinela.bat`). O "robô que produz o lote no
domingo" era **texto na documentação** — mesmo erro já pego em 27/07 com a "ronda
de terça e quinta". Removido da skill. **Nada produz conteúdo sozinho:** escolher
foto, escrever legenda e montar Reel é sempre o Claude, na conversa.

**Próxima conversa começa por aqui:**
- **Ler `content/placar.md` antes de opinar sobre o que funciona.**
- **Ampliar a amostra do nicho antes de escolher trilha do próximo Reel** (ver
  achado abaixo). Faltou cobrir `ohanabulls_club`, `omundobully` e
  `canilelohimbull`.

**ACHADO em 28/07/2026 — o nicho não roda em música, roda em ÁUDIO ORIGINAL.**
Ideia dele: em vez de pegar a lista de tendências geral do Brasil (que vem cheia
de funk e pop adulto), olhar **o que está dando like em perfil de cachorro**.
Varredura feita (subagente, via navegador): dos Reels de maior alcance do nicho
bully BR — incluindo um de **1 milhão** de views (@guerreirobully) e um de 119
mil (@americanbullymicro) — **4 de 4 usam "Áudio original"**, nenhum usa faixa
licenciada. **Limite declarado: amostra de só 4 Reels em 2 perfis** — o Instagram
não renderizou a grade de 5 dos 7 perfis alvo. Não virou regra ainda, mas aponta
que eu vinha caçando a coisa errada: o gargalo do Reel pode ser o gancho e o som
da cena, não a trilha.

**Recusas de trilha nesta rodada (todas dele):** *Legado (feat. Chorão)* —
Marcelo Falcão; *Lua de Cristal* — Xuxa; *Animal* — KATSEYE. As duas primeiras
por artista (viraram veto permanente na skill, junto com Anitta); a terceira
depois de ouvir. **Regra nova que ele deu: sem ouvir, ele não decide trilha** —
proposta por descrição não serve. Caminho para ele ouvir música de gravadora:
abrir o `on_platform_audio_preview_link` no Chrome da Hana (a página do áudio tem
player). Está registrado na skill como regra 3g.

**Aguardando o Ramón:**
- **PENDÊNCIA (28/07/2026): a ronda de engajamento vale a pena?** É o item mais
  caro que sobrou — estimativa de **60 a 120 mil tokens por ronda**, 3x/semana,
  algo entre 200 e 350 mil por semana. E **não se sabe se funciona**: a única
  ronda real (4 comentários, 27/07) não trouxe seguidor medido. Combinado: fazer
  **uma ronda de 10 comentários** e ler o `content/placar.md` depois. Se os
  seguidores mexerem, monta-se o semi-robô (Gemini escreve os comentários, ele
  cola no celular, custo zero de token); se não mexerem, a ronda sai de cena.
  **Ele ainda não marcou quando fazer essa ronda de medição.**
- **Decidir se monta a biblioteca de 12 trilhas** (US$ 0,48 no crédito do
  Gemini) ou fica só com as 3 atuais.
- **Decidir se publica o Reel de 10/08 como "Reel de teste"** (trial reel: só
  não-seguidores veem, não aparece no perfil) para conferir o resultado com a
  trilha antes de valer. É a única forma de ver o Reel montado com o áudio.

**DECIDIDO em 28/07/2026 — posicionamento do perfil: "A PATROA MIMADA".**
Ele escolheu entre duas opções que apresentei. A Hana manda na casa, o Ramón
obedece; humor com atitude, ele no papel de "funcionário". Descartada a opção
"fofa premium" (beleza/cor rara), com o argumento que ele aceitou: **fofura é o
piso do nicho, não diferencial** — todo Exotic Bully é fofo, e foto bonita
concorre com todo mundo. Personalidade é o que faz seguir. A bio já vinha
apontando para lá ("A patroa: aqui quem manda sou eu"). Isso agora manda em
legenda, escolha de cena, gancho de Reel e **escolha de trilha**.

**PROVADO em 28/07/2026 — áudio de tendência via API FUNCIONA.**
Era o gargalo de alcance do projeto e caiu. O que foi feito e testado na tela:
- **A Audio API é oficial** (`developers.facebook.com/docs/instagram-platform/
  content-publishing/audio-api/`) — eu vinha tratando como "indício de
  integradores"; é documentação da Meta.
- **App novo `Hana Audio` criado** (id `2297820570982525`), ligado ao portfólio
  `616358434290372`. Foi preciso porque o app antigo **"Hana Social" recusa** as
  permissões do fluxo Facebook Login ("Ocorreu um erro" em toda tentativa) — ele
  nasceu no fluxo Instagram Login e os dois não convivem no mesmo app.
  **O publicador não foi tocado**: `IG_ACCESS_TOKEN` e fluxo de sempre intactos.
- **Token gerado** pelo Facebook Login com `instagram_basic`,
  `instagram_content_publish` e `pages_show_list`. O ig-user-id por esse caminho
  é **`17841471483838197`** (diferente do `27631851599815469` do Instagram Login).
- **Busca de faixas em alta funcionou**: devolveu música brasileira licenciada
  (Marcelo Falcão, Anitta/Los Brasileiros, Anitta/Alceu Valença).
- **Anexar funcionou**: container do Reel de 10/08 criado com
  `audio_configuration` e chegou a `status_code: FINISHED` — "pronto para
  publicar". **Nada foi publicado** (não chamei `media_publish`).
- **Limites que ficaram claros:** `download_url` é **null** para música de
  gravadora, então **não dá para montar prévia local** do vídeo com a faixa; e a
  Meta não oferece pré-visualização do Reel com áudio — só publicando.
- **Consequência:** cai a pendência antiga de "publicar Reel pelo celular para
  ter áudio de tendência". A automação faz sozinha.

**Estrutura nova em 28/07/2026 — Página do Facebook criada e ligada:**
- **Página `Hana Duran Sanches`** criada (id `1235806802950209`), categoria
  "Criador(a) de conteúdo digital", bio puxada do Instagram. Portfólio
  empresarial gerado junto: `616358434290372`.
- **Instagram ligado à Página** — o Ramón fez o login (senha eu não digito,
  nunca). Confirmado na tela: o Business Suite mostra os 329 seguidores do
  Instagram e "hanaduransanches" ao lado da Página.
- **A conta CONTINUA Criador de conteúdo** depois de ligar — conferido na tela.
  O risco que eu tinha levantado (virar Business e perder o áudio em alta do
  app) **não aconteceu**.
- **O publicador não foi tocado.** `IG_ACCESS_TOKEN` segue o mesmo, fluxo
  Instagram Login intacto, post de 29/07 às 18h sem risco.
- **Próximo passo:** gerar um token pelo **Facebook Login** (app "Hana Social",
  id 1776084913751376) e testar a API de áudio de verdade — buscar faixas em
  alta e tentar anexar por `musicSoundInfo.musicSoundId`. Só então se sabe se o
  áudio de tendência entra na automação. **Enquanto não testar, não prometer.**
  Vale lembrar o que já está documentado: o catálogo da API pode diferir do que
  aparece no app, e não dá para pré-visualizar o Reel com o áudio antes de subir.

**Decidido em 28/07/2026:**
- **A conta JÁ ERA Criador de conteúdo** — conferido na tela, não havia nada a
  trocar. Ele decidiu manter assim e deixar Business para quando houver base
  grande. Motivo: só Criador enxerga a biblioteca de áudios em tendência —
  Business fica presa à Meta Sound Collection, porque os acordos da Meta com as
  gravadoras não cobrem uso comercial. Quando a Hana tiver audiência e o produto
  existir, Business passa a valer pelas ferramentas de loja — e ele mencionou
  que nessa hora compraria algum app de apoio.
  **Consequência que muda o jogo:** o áudio de tendência **já está disponível
  pra ele hoje**. O que separava a Hana dele nunca foi permissão — é só o fato
  de a API não anexar áudio de tendência, então o Reel tem que subir pelo
  celular. Custo: ~3 minutos por Reel.
- **Como achar o Chrome da Hana sem perguntar** (ele reclamou que a mesma
  pergunta veio 3x na mesma noite): `list_connected_browsers` →
  `select_browser` → `instagram.com/accounts/edit/` → `screenshot`, conferindo
  o @ na tela. Nome e id do navegador não são confiáveis. Receita na skill.
- **Trilha do Reel de 10/08: a lo-fi** (escolha delegada a mim). Já aplicada na
  fila e na pasta de aprovação.
- **Trilha própria virou capacidade do projeto:** `studio/gerar_trilha.py` gera
  clipes de 30s pelo Lyria 3 (Gemini, US$ 0,04 cada). Fica claro o limite: isso
  resolve QUALIDADE de áudio, não ALCANCE — quem move alcance é o áudio de
  tendência, que não existe via API.
- **Descoberta:** os Reels nunca tiveram música. O de 10/08 subia com o áudio
  cru do MOV (som da casa). Eu havia afirmado que não existia trilha nenhuma no
  projeto e estava errado: havia um `musica_hana.wav` de 25/07 largado na pasta
  de editadas, que nunca entrou em Reel.

**Resolvido em 27/07:**
- **Ronda de engajamento começou (27/07/2026).** Descoberto que a "ronda de
  terça e quinta" descrita aqui **nunca existiu em código** — era só texto.
  Agora é processo manual meu, aprovado por ele: **3x por semana, ~10
  comentários**, sempre com aprovação em bloco antes de publicar. Primeira ronda:
  4 comentários no ar como "a patroa" em @americanbully.insta.do.bruce,
  @ohanabulls_club (canil de Blumenau/SC), @guerreirobully e @canilelohimbull.
  Diagnóstico confirmado: nos comentários dos posts da Hana só aparecem amigos e
  família — o nicho ainda não chegou. Por isso a ronda existe.
- **Música nos Reels:** ele topa música embutida no arquivo (isso a automação
  faz). Áudio de tendência do Instagram continua fora — não existe via API.
- **Telegram no ar (27/07/2026, noite).** Bot `@Hanasocial_aproval_bot` criado
  por ele no BotFather; token e chat id gravados como secrets no GitHub
  (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) — antes eles **nunca existiram** e
  os botões nunca funcionaram. Testado ponta a ponta: mensagem com botões
  chegou no celular dele e o clique voltou pra API. Agora é o canal principal de
  aprovação; a pasta do OneDrive vira reserva.
- **Token do Instagram**: gerado no painel da Meta (app "Hana Social",
  id 1776084913751376), gravado em `studio/.token`, renovado até 24/09/2026 e
  secret do GitHub atualizado pelo script. A renovação passou a rodar toda
  semana dentro do `sentinela.bat` (não criei robô novo).
- **Trava de aprovação religada**: a variável `REQUIRE_APPROVAL` estava em **0**
  no GitHub — ou seja, a fila subia sozinha, contra a regra 2. Voltou para 1.
- **Os 7 posts da fila foram aprovados por ele**, condicionados a não haver
  repetida — checagem rodada, zero repetições. O primeiro sobe hoje 18h.
- Acentos corrigidos nos posts de 05/08, 07/08 e 10/08 (estavam sem).

**Feito e no ar:**
- Bio nova publicada (escolha delegada a mim): "A patroa: aqui quem manda sou eu".
- ~~Robô único `hana-rotina`~~ — **ERRADO, nunca existiu** (pego em 28/07 no
  Agendador). Quem roda de verdade: `Hana Sentinela` na máquina dele e o
  `publish.yml` no GitHub. Nada é publicado sem o "aprovado" dele.
- Primeiro Reel montado com a fórmula campeã do nicho (gancho "descreva essa
  cena com UMA palavra") sobre o vídeo dela assistindo TV.

## Regras permanentes (não reabrir sem ele mandar)

1. **A estrela é a Hana.** O Ramón pode aparecer, mas nunca é o assunto. Régua:
   se a Hana puder ser cortada do quadro sem mudar a piada, o post está errado.
2. **Nada é publicado sem aprovação explícita dele.** A automação prepara e
   pergunta; ele responde pelos números.
3. **COMO mostrar post pra ele aprovar — testado em 26-27/07/2026.**
   O que **NÃO funciona** (ele não enxerga, já falhou três vezes seguidas):
   link markdown do `raw.githubusercontent.com`, arquivo anexado na conversa
   (SendUserFile) e link de página publicada (Artifact). Não insistir nesses.
   O que **funciona no PC** (melhor canal, criado em 27/07/2026):
   `python studio/painel_aprovacao.py` — gera uma página local com foto grande +
   legenda + data, numerada, e abre **no Chrome do perfil da Hana**
   (`--profile-directory="Profile 2"`, `hanaduransanches@gmail.com`).
   **Nunca usar `webbrowser.open` nem `start`**: o navegador padrão do Windows
   é o perfil da marca Canecas, e abrir ali é erro que já custou três avisos
   dele na mesma conversa.
   No celular: `Hana Social\Fotos da Hana\05 - APROVAR (semana)`, numerada com
   `00_LEGENDAS.txt`. **Sempre escrever o caminho COMPLETO na mensagem** e nunca
   criar subpasta nova — ele não acha (pedido dele em 27/07/2026).
4. **Conferir repetição ANTES de propor qualquer foto** — rodar
   `python studio/checar_repetida.py`, que compara por impressão digital de
   imagem contra tudo publicado no perfil e a fila contra ela mesma.
   O proibido é **a mesma foto** ir ao ar duas vezes; **o mesmo passeio pode
   render vários posts**, desde que as fotos sejam diferentes (ele corrigiu isso
   em 27/07/2026 — eu tinha endurecido a regra sozinho e tirei um post bom da
   fila). Limite a declarar sempre: a checagem só pega FOTO. Vídeo antigo do
   perfil é dele e não preciso auditar; dos Reels que eu montar, o controle fica
   em `content/videos-usados.json`.
5. **Fronteira com o projeto Canecas / Brushed & Brewed:** parceria comercial
   sim, interferência não. Não opinar sobre marca, estratégia ou execução deles;
   não mexer na pasta deles. Ao fornecer fotos, **só a Hana sozinha** — nunca
   com o Ramón (a imagem dele é livre aqui, vedada no projeto comercial dele).
6. **Um robô só.** Não criar agendamento novo. A única tarefa agendada na
   máquina é **`Hana Sentinela`** (`studio\sentinela.bat`) — expandir ela ou o
   workflow `publish.yml`. (O `hana-rotina` que esta lista citava **nunca
   existiu**; corrigido em 31/07/2026.)
7. **Verificar a conta ativa no Instagram** antes de qualquer ação no navegador
   — o Chrome do Ramón alterna entre 3 contas.
8. **Fechar as abas** do navegador ao terminar qualquer trabalho.
9. **Economia:** trabalho mecânico em Python local; IA só onde agrega.

## Becos sem saída (não repetir a tentativa)

- **Mostrar imagem dentro da conversa não funciona**: o widget inline bloqueia
  imagem de fora e embutir mídia em base64 estoura o limite da mensagem.

## Norte estratégico

Audiência → autoridade → produto. **O produto não existe e isso é decisão dele,
de 31/07/2026** — *"é apenas a hana crescendo por ser foda e bonitinha"*. Só a
primeira etapa está em jogo hoje: AUDIÊNCIA. O pilar "roupa que não serve em
bully" segue como candidato natural **quando** o assunto reabrir, e as hipóteses
já trabalhadas estão em `content/hipoteses-produto.md`. O gargalo real, medido em
`content/metricas.md`: a base atual é a rede pessoal do Ramón, não o nicho —
crescer exige Reels, hashtag de nicho e presença nos perfis grandes da raça.
