# Explicação do projeto Hana Social — para uma IA externa

Este arquivo existe para que uma IA de fora (sem acesso à máquina do Ramón, sem
Claude Code, só com esta pasta ou o conteúdo dela) entenda o projeto o
suficiente para revisá-lo ou, se preciso, reconstruí-lo do zero. Nenhum valor
de segredo (chave, token, senha) está neste arquivo — só caminhos e nomes de
variável.

---

## Seção 1 — Ferramentas e ambiente disponíveis na máquina do Ramón

Esta máquina roda o Claude Code (Anthropic) como orquestrador principal. Além dele:

**Hub de aprendizado (somente leitura de fora)**: pasta `Crescimento IA` no Desktop
do OneDrive é a consultoria central — regras de trabalho, ranking de ferramentas de
IA visual, lições dos "diretores" (agentes especializados) e o diário de bordo de
todos os projetos. Caminho: `%USERPROFILE%\OneDrive\Desktop\Crescimento IA`.
Arquivos-chave lá dentro: `APRENDIZADO-IA.md` (ranking de foto/vídeo, evolui),
`METODO-DE-TRABALHO.md` (escada de custo e ciclo de trabalho), `06-SISTEMAS\
agentes\memoria\*.json` (memória de cada diretor), `06-SISTEMAS\ambiente.json`
(manifesto de programas/skills que a máquina precisa ter), `ESTADO-DOS-PROJETOS.md`
(diário de bordo de todos os projetos do Ramón).

**Time de "diretores" (subagentes especializados do Claude Code)**, em
`~\.claude\agents\`: diretor-financas, diretor-criativo, diretor-pesquisa,
diretor-atualidades, diretor-visual, diretor-processos, diretor-automacao,
diretor-carreira, diretor-criacao, diretor-redes, diretor-reels, diretor-vendas,
e um "conselheiro" que é consultado antes de decisões de peso. Cada um tem
memória própria (JSON no hub) e foca numa especialidade. Os diretores diretor-reels
e diretor-redes são especialmente relevantes para este projeto (Instagram/Reels).

**Ponte para outras IAs (IA-Hub)**: script `python "%USERPROFILE%\.claude\ia-hub\
ask-ai.py" <chatgpt|gemini|deepseek|grok> "pergunta"` (rodar via terminal bash, não
PowerShell). Opções: `--arquivo caminho.txt` (textos longos), `--sistema "..."`,
`--modelo "..."`. As chaves de API dessas IAs ficam em `IA-Hub\chaves-api.txt`,
dentro da pasta "Claude Code" do OneDrive — NÃO estão neste projeto; quem precisar
delas tem que pedir ao Ramón ou localizar esse arquivo (o valor das chaves nunca
deve ser copiado para dentro de pastas de projeto). Este projeto tem um `.env.example`
próprio — as variáveis reais ficam num `.env` local (não versionado no git) que NÃO
deve ter seu conteúdo copiado para este arquivo de explicação. Antes de gastar
crédito de qualquer IA, roda-se `python "%USERPROFILE%\.claude\ia-hub\
checar-credito.py" <ia>`. Roteamento: Gemini = documentos longos/volume (grátis,
primeira escolha); DeepSeek = volume repetitivo barato; ChatGPT = texto
criativo/revisão de redação; Grok = assunto do momento/redes sociais. Existe também
IA local grátis via Ollama: `python "%USERPROFILE%\.claude\ia-hub\ia-local.py"
"tarefa"`.

**Geração de imagem/vídeo**: padrão é sempre o melhor modelo disponível. Imagem via
`gemini-3.1-flash-image` pelo script `Crescimento IA\Documents\IA-Hub\ia-imagem.ps1`
(~R$0,37 por 1000 imagens); vídeo via Veo 3.1 qualidade cheia. O ranking completo e
atualizado de ferramentas de foto/vídeo está em `APRENDIZADO-IA.md` do hub — ler
ANTES de qualquer tarefa visual, pois evolui.

**Escada de custo** (do mais barato ao mais caro, descer antes de gastar): 1) tarefa
de regra fixa = robô/script (zero custo); 2) volume alto com pouca inteligência = IA
local (Ollama, zero custo); 3) volume com alguma qualidade = DeepSeek; 4) análise
e entrega final = Claude/diretores. Dentro do próprio Claude Code há uma escada de
motor: Sonnet 5 para tarefas rotineiras, Opus 5 para trabalho normal de projeto
(padrão), Fable 5 para análise pesada/decisão de dinheiro, "Ultracode" para programar
um app inteiro do zero.

**Conectores/MCP disponíveis no Claude Code desta máquina** (alguns exigem login
prévio do Ramón): Gmail, Google Calendar, Google Drive, Figma, Canva, Gamma
(apresentações), Shopify, Lovable (gerador de apps), Docusign, Fireflies (atas de
reunião), Superhuman Docs/Coda, Indeed, e um conector de finanças pessoais (Era
Context). Cada projeto pode ter seu próprio `.mcp.json` na raiz listando conectores
específicos daquele projeto — este projeto tem um `.mcp.json` próprio, documente o
que ele contém (nomes de conectores, sem valores de credencial).

**Git/GitHub**: cada projeto tem seu próprio repositório git local; a sincronização
entre os 3 aparelhos do Ramón (PC trabalho, PC casa, celular) depende de cada projeto
ter um remoto no GitHub configurado. Este projeto tem uma pasta `.github`, verifique
se há GitHub Actions configuradas e documente o que elas fazem.

### O que este projeto especificamente tem desses itens

- **`.mcp.json` deste projeto** (conteúdo integral, sem segredo — é só a URL do
  servidor):
  ```json
  {
    "mcpServers": {
      "kairogen-hana": {
        "type": "http",
        "url": "https://mcp.kairogen.ai/mcp"
      }
    }
  }
  ```
  Um único conector: **Kairogen** (`kairogen-hana`), servidor MCP remoto por HTTP.
  Não há evidência no restante do código de que ele seja efetivamente chamado por
  algum script Python — os scripts do projeto geram legenda com a API do Gemini
  direto (`lote_automatico.py`) e nunca chamam serviço de imagem/vídeo por API
  (ver regra 3j-i abaixo). O uso do Kairogen, se houver, é manual pelo Claude Code
  na conversa, não parte do pipeline automatizado.
- **`.github/workflows/publish.yml`**: um único workflow, "Publicar posts da Hana".
  Roda a cada 30 min (cron `*/30 * * * *`) mais um reforço nos horários de
  publicação (seg/qua/sex, 11:00Z = 8h de Itajaí). Também pode ser disparado manualmente
  (`workflow_dispatch`) com vários parâmetros opcionais (forçar reporte semanal,
  mandar recado avulso no Telegram, mostrar a fila inteira, mandar mídia avulsa,
  etc.). Etapas do job, em ordem: instalar dependências → rodar `publisher/run.py`
  (aprova/publica) → `publisher/metrics.py` (coleta métricas, 1x/dia) →
  `publisher/reporte_semanal.py` (pauta de segunda) → `publisher/mandar_recado.py`
  (canal Claude→Telegram) → `publisher/mostrar_fila.py` / `mandar_midia.py`
  (sob demanda) → `publisher/diagnostico.py` (grava aprendizado) →
  `publisher/leitura_d1.py` → `publisher/avisar_lote.py` (entrega recado do robô
  local) → `publisher/sentinel.py --token` (avisa token vencendo) → commit +
  push do estado da fila (com rebase e retry em caso de corrida) →
  `publisher/sentinel.py` (falha alto se algo ficou para trás, e-mail do GitHub
  avisa). Só este workflow existe — não há outros arquivos em `.github/workflows/`.

---

## Seção 2 — O que é o projeto Hana Social

**Objetivo do negócio** (fonte: `brand-brief.md`, README.md): crescer o Instagram
`@hanaduransanches`, perfil de uma cadela real do Ramón — uma Exotic Bully Micro,
cor **Tri Lilac Merle** (variação rara e valorizada nesse nicho de raça), nascida
em 10/02/2024. O Ramón é dono/gestor da conta e aparece como coadjuvante em
alguns conteúdos ("assistente de palco da patroa"), mas **a Hana é sempre a
estrela**.

**Posicionamento**: não é "perfil de cachorro fofo genérico" — é "cultura bully
premium": status, estética streetwear, comunidade que se reconhece e gasta. A
persona editorial vigente (aprovada em 31/07/2026) é **"a patroa mimada"**: ela
manda na casa, o Ramón obedece; tom infantil, leve, engraçado, nunca adulto ou
melancólico.

**Pilares de conteúdo vigentes** (viraram em 31/07/2026, substituindo os 3
antigos de fofura/dor-do-dono/lifestyle): **A PATROA MANDA** · **MICRO NO APÊ**
· **INIMIGOS DA PATROA** (com desfecho obrigatório: ela "late e expulsa" ou
"ignora e sai andando" — nunca foge).

**Não existe produto à venda hoje, de propósito** (decisão do Ramón,
31/07/2026): o objetivo atual é só crescer audiência; venda fica para depois.
Há uma parceria comercial de fornecimento de fotos com outro projeto do Ramón
(Canecas POD / Brushed & Brewed), documentada em `content/parceria-canecas-pod.md`,
com regra de fronteira rígida (fotos só da Hana sozinha, nunca com o Ramón; não
mexer nos arquivos do outro projeto).

**Como o sistema funciona, em uma frase** (README.md): duas caixas — o
**Estúdio** (Claude, sob demanda, edita fotos/vídeos, escreve legendas e
enfileira posts) e a **Impressora** (este repositório sozinho, sem IA, roda de
graça no GitHub Actions e publica no horário aprovado). A meta editorial atual
é 3 Reels por semana (segunda/quarta/sexta, 8h de Itajaí), com o vídeo real (não
foto parada) como formato obrigatório — decisão tomada depois de medir que fotos
publicadas geravam 0 salvamentos, 0 compartilhamentos e 0 seguidores ganhos em
4 posts seguidos.

---

## Seção 3 — Estrutura de pastas, arquivos e arquitetura do código

### Visão geral da árvore

```
Hana Social/
  README.md, SETUP.md, brand-brief.md, DECISOES.md, ORGANOGRAMA.md   -> docs
  .env.example, requirements.txt, .mcp.json, .gitignore
  yolov8n.pt                       -> pesos do YOLOv8n (ignorado no git; ver abaixo)
  .github/workflows/publish.yml    -> único workflow do GitHub Actions
  .claude/skills/hana-social/SKILL.md  -> "memória viva" do projeto p/ o Claude Code
  publisher/                       -> "Impressora": publica, roda no GitHub Actions
  studio/                          -> "Estúdio": produção/edição, roda LOCAL (PC do Ramón)
  content/                         -> fila de posts, publicados, métricas, planejamento
  estrategia/                      -> registro das decisões da reunião semanal (JSON)
  Fotos da Hana/                   -> mídia bruta e editada (fora do git, ~195 MB)
```

### `publisher/` — publicação automática (roda no GitHub Actions, sem IA)

Arquivos e responsabilidade:
- `ig_api.py` — cliente mínimo da Instagram Graph API: cria container de imagem
  (`create_image_container`) ou de Reel (`create_reel_container`, com
  `audio_configuration` opcional), espera o processamento assíncrono
  (`wait_until_ready`) e publica (`publish_container`). `GRAPH_BASE` é
  configurável (fluxo novo "Instagram Login" via `graph.instagram.com`, ou
  clássico via `graph.facebook.com`).
- `postqueue.py` — gerência da fila. Cada post é uma pasta
  `content/queue/<id>/` com `post.json` + mídia. Status possíveis: `pending`
  → `approved`/`rejected` → `posted`/`failed`. `criar_post()` é a **porta de
  entrada única** para gravar posts novos (valida o campo opcional `pilar`
  contra os 3 pilares vigentes). `media_url()` monta a URL pública da mídia e
  assina com um hash SHA-1 do conteúdo do arquivo (`?v=<hash>`) — necessário
  porque o Telegram cacheia por URL, então mídia trocada no mesmo nome de
  arquivo precisa de URL nova para não reenviar a versão antiga.
- `run.py` — orquestrador do cron. Ordem por ciclo: (1) revalida se a
  mídia/legenda mostrada no Telegram ainda bate com o que está no disco —
  senão o post volta a `pending`; (2) sincroniza aprovações do Telegram
  (`sync_approvals`); (3) notifica posts `pending` ainda não mostrados; (4)
  publica os `approved` cujo horário já venceu. Tem um freio de mão (comando
  "pausar"/"voltar" pelo Telegram, via `comandos.py`) e uma trava de
  auditoria: só publica um post novo se `post.json` tiver
  `"auditoria": {"veredito": "SEM OBJECAO"}` — uma lista fechada de 4 IDs
  antigos está isenta por ordem explícita do Ramón (registrada em código,
  não em data, para não virar um "backdoor" que aceita post forjado com data
  passada).
- `telegram_approve.py` — manda os posts pendentes com botões
  ✅ Aprovar/❌ Recusar, lê os cliques (`getUpdates`), e confere que quem
  clicou é o dono do bot (compara `chat_id` — sempre como texto, nunca
  comparando tipos diferentes).
- `metrics.py` — coleta diária de métricas via Graph API (alcance, curtidas,
  comentários, salvos, compartilhamentos, seguidores ganhos), grava série
  histórica em `content/metricas.json` e reescreve `content/placar.md`
  (versão legível, com médias por tipo de post e por pilar editorial).
- `comandos.py`, `diagnostico.py`, `etiqueta.py`, `leitura_d1.py`,
  `mandar_midia.py`, `mandar_recado.py`, `mostrar_fila.py`,
  `recepcionista.py`, `reporte_semanal.py`, `sentinel.py`,
  `veredito.py` — utilitários de apoio ao ciclo do GitHub Actions: comandos
  de pausa, registro de aprendizado, leitura do "dia 1" de métricas de um
  post, envio de mídia avulsa e recados manuais, exibição da fila inteira no
  Telegram, resposta automática a mensagens de texto (usa Gemini Flash, com
  `GEMINI_API_KEY` como secret), pauta semanal, julgamento por código das
  decisões da reunião anterior (`veredito.py`, três resultados possíveis:
  MEXEU / NÃO MEXEU / NÃO TESTADO), e o "sentinela" que falha o job (e
  dispara e-mail do GitHub) se algo passou do horário sem publicar.

Único requisito de terceiros do `publisher/`: **`requests`** (ver
`requirements.txt`). Roda em Python 3.11 no `ubuntu-latest` do GitHub
Actions.

### `studio/` — produção e edição (roda LOCAL, no PC do Ramón, fora do git actions)

Arquivos principais:
- `preparar_lote.py` — edição mecânica de fotos: corrige rotação EXIF, corta
  4:5, aplica tratamento "clean premium" (brilho/contraste/cor/warmth),
  exporta 1080x1350, gera `contact_sheet.jpg` numerado. `post()` cria o post
  na fila chamando `postqueue.criar_post`.
- `montar_reel.py` — o montador de Reel "de verdade" (multi-clipe), usado
  desde 02/08/2026 depois que a primeira versão (`reel_de_video.py`, um clipe
  + uma frase) foi reprovada pelo Ramón como "amador". Lê um roteiro em JSON
  (pasta `studio/roteiros/`) com lista de `cortes` (arquivo, trecho, tipo de
  movimento: `seco`/`punch`/`zoomout`/`acelerado`, parâmetros de recorte
  `aproximar`/`foco`/`foco_y`, correção de exposição `clarear`, filtro
  `cinema`) e `textos` com entrada/saída no tempo. Aceita **foto como corte**
  (foto vira clipe de N segundos com movimento, desde 04/08/2026). Suporta
  trilha (mixada com o áudio original da cena via `abafar_ate`). Usa
  `imageio_ffmpeg` (baixa um binário de ffmpeg automaticamente) e monta tudo
  via chamadas de linha de comando ao ffmpeg (crop/scale/concat/overlay de
  texto/mix de áudio). Tem uma trava (`_conferir_repetida`) que RECUSA montar
  se uma foto já usada em post anterior for reaproveitada sem
  `"permitir_repetir": true` no roteiro — comparação por dHash (impressão
  digital de imagem), não por nome de arquivo.
- `reel_de_video.py`, `reel_ritmado.py`, `gerar_reel.py` — versões mais
  simples/antigas de montagem de Reel (um clipe ou slideshow de fotos com uma
  frase). Mantidas no repositório mas superadas por `montar_reel.py` para
  peça "de verdade" (a skill explicitamente instrui a não voltar a usar
  `reel_de_video.py` para conteúdo final).
- `checar_repetida.py` — compara a fila contra o que já está publicado no
  perfil (via Graph API) e a fila contra si mesma, usando **dHash** (hash
  perceptual de imagem, tolerante a corte/brilho/recompressão; distância de
  Hamming ≤ 10 bits conta como repetida).
- `garimpo.py` — **é onde o `yolov8n.pt` é usado.** Varre o rolo de câmera do
  iCloud sincronizado localmente (`~\iCloudPhotos\Photos`, ~34 mil arquivos)
  em busca de fotos/vídeos com cachorro e sem gente. Funil de custo crescente:
  filtra por extensão conhecida → tamanho mínimo (15 KB) → descarta `.png`
  sem abrir (tratado como print de tela) → abre de verdade (PIL +
  `pillow_heif` para HEIC; `ffmpeg` extrai 5 frames de vídeo) e descarta
  resolução baixa → roda o **YOLOv8n** (via biblioteca `ultralytics`, CPU,
  100% local/offline) nos frames: reprova se aparecer a classe `person` em
  qualquer frame (confiança ≥ 0.30), aprova se aparecer `dog` (confiança ≥
  0.40) e não aparecer pessoa. Calcula um score ponderado (área do cão no
  quadro, nitidez via variância do Laplaciano com `cv2`, resolução, confiança
  do detector, bônus para vídeo) e copia o top-30 para uma subpasta separada.
  É explicitamente **um ranking, não um reconhecedor da Hana individualmente**
  — "isto é um cachorro" ≠ "isto é a Hana"; confirmação final é humana. É
  retomável (salva estado a cada poucos arquivos em
  `studio/.garimpo_estado.json`, ignorado no git) e limitado por
  `--minutos`/`--amostra`. Baixa o modelo `yolov8n.pt` (~6 MB de pesos, do
  repositório oficial da Ultralytics) uma única vez para
  `studio/.garimpo_modelo/yolov8n.pt`; o `yolov8n.pt` solto na raiz do
  projeto é uma cópia adicional que a própria biblioteca `ultralytics` larga
  ali ao rodar (também ignorado no `.gitignore`, mas existe fisicamente no
  disco do Ramón — não deveria ser versionado nem copiado para outro
  ambiente, só baixado de novo).
- `lote_automatico.py` — o robô semanal que monta o lote de posts sem gastar
  tokens do Claude. Desde 31/07/2026, foco em VÍDEO (não fabrica mais foto —
  ver regra 4c-i da skill): procura vídeos novos em
  `Fotos da Hana/01 - brutas (suba aqui)`, monta rascunhos de Reel (sem
  gancho, que fica para o julgamento humano/Claude na reunião de segunda). Se
  não houver vídeo novo, não inventa post — escreve um recado pedindo
  filmagem em `content/aviso_lote.md`, usando o pedido de cena escrito pelo
  comitê em `content/pedido-de-cena.md` (ou um texto de reserva, avisando que
  é reserva). Modo antigo (`--fotos`) ainda edita fotos e pede legenda ao
  **Gemini Flash multimodal** (vê a foto), usando uma chave lida de
  `chaves-api.txt` no OneDrive (fora do projeto). Roda dentro da tarefa
  agendada `Hana Sentinela` no PC do Ramón.
- `design_kit.py` — templates de arte compostos sobre foto real editada
  (capa de revista "BULLY", poster "A CHEFIA"), extraindo a paleta lilás
  diretamente da foto. Nunca gera imagem falsa.
- `gerar_trilha.py` — gera trilha instrumental própria via **Lyria 3** (API
  do Gemini, ~US$ 0,04 por clipe de 30s).
- `estado.py` — gera `ESTADO-ATUAL.md` (a "foto" automática do projeto: fila,
  publicados, saúde da automação, acervo, git log, pendências) a partir das
  fontes reais (arquivos + `git log` + `gh`), para nunca ficar desatualizado.
- `sentinela.py` / `sentinela.bat` — vigia local (Agendador de Tarefas do
  Windows, roda seg/qua/sex por volta das 18h): confere se o post do dia
  está atrasado e, se sim, dispara o workflow do GitHub manualmente
  (`gh workflow run`). O `.bat` encadeia, em ordem: renovar token → sentinela
  → lote automático (só executa efetivamente 1x/semana, controlado por um
  marcador local) → garimpo (40 min/dia, retomável).
- `renovar_token.py` — renova o token de longa duração do Instagram antes de
  vencer (~60 dias).
- `painel_aprovacao.py`, `para_aprovar.py` — geram um painel HTML local
  (`aprovar.html`, ignorado no git) para o Ramón revisar o lote da semana.
- `checar_repetida.py`, `design_kit.py` etc. dependem de um arquivo local
  `studio/.token` (token do Instagram, fora do git) e, quando aplicável,
  `studio/.telegram` (credencial local do bot, também fora do git).

**Dependências reais do `studio/`, não listadas em `requirements.txt`**
(inferidas dos `import` de cada script — `requirements.txt` só cobre o que
roda no GitHub Actions, ou seja, só `publisher/`): `Pillow` (`PIL`),
`pillow_heif` (leitura de `.HEIC` do iPhone), `imageio_ffmpeg` (baixa/expõe um
binário de ffmpeg), `ultralytics` (YOLOv8), `opencv-python` (`cv2`, nitidez
via Laplaciano — vem como dependência do `ultralytics`), `numpy`, `requests`.
Alguns scripts também dependem de fontes do Windows fixas em
`C:\Windows\Fonts\` (`arialbd.ttf`, `BOD_B.TTF`, `seguisb.ttf`, `segoeui.ttf`,
`OCRAEXT.TTF`, `FRAHV.TTF`, `FRADMCN.TTF`, `bahnschrift.ttf`) e de utilitários
do Windows (`ctypes`/`SHGetFolderPathW` para resolver a pasta pessoal do
usuário sem depender de variável de ambiente, que se mostrou instável rodando
o `python.exe` a partir do Git Bash com o nome de usuário acentuado "Ramón
França" — ver comentário em `garimpo.py`). Ou seja, o `studio/` é
**Windows-específico** por construção; `publisher/` é portátil (roda em
`ubuntu-latest`).

### `content/` — a fila e o estado editorial

- `queue/<id>/` — posts aguardando aprovação/publicação: `post.json` +
  mídia (`image.jpg` ou `video*.mp4`).
- `posted/<id>/` — posts já publicados, arquivados pelo `postqueue.archive()`.
- `previas/`, `previews/`, `trilhas/` — material de apoio (prévias de reel,
  trilhas de áudio geradas).
- Arquivos de estado/registro (não editar à mão, gerados por código):
  `metricas.json`/`placar.md` (métricas — ver `metrics.py`),
  `fotos-usadas.json`/`videos-usados.json` (registro anti-repetição),
  `fotos-livres.json`, vários arquivos ocultos de controle (`.aviso_lote_enviado`,
  `.lote_semana_executada`, `.semanas_sem_cena`, etc. — marcadores locais de
  idempotência, não segredo).
- Documentos de planejamento/registro editados por humano ou IA:
  `aprendizado.md`, `benchmark-instagram.md`, `benchmark-tecnico.md`,
  `calendario-editorial.md`, `hipoteses-produto.md`, `parceria-canecas-pod.md`,
  `pauta_extra.md`, `pedido-de-cena.md`, `plano-semana.md`,
  `playbook-reels.md`, `recados.md` (mensagens de texto do Ramón capturadas
  pelo bot do Telegram, para o Claude responder na próxima conversa).

### `estrategia/`

Um único arquivo por enquanto: `decisoes-2026-08-02.json` — registro
estruturado da reunião semanal do "comitê" (diretores + conselheiro), com
cada decisão trazendo o que se espera que mude, o número que mede isso, a
pré-condição checável por código, e a "regra de morte" (quando considerar que
não funcionou). `publisher/veredito.py` lê esses arquivos e julga por código
se a semana seguinte mexeu, não mexeu, ou não pôde ser testada.

### `Fotos da Hana/`

Fora do git (`.gitignore` exclui `/Fotos da Hana/` inteira, ~195 MB). Layout
numerado fixo (não renomear `03` e `04` — são a interface de leitura/escrita
com o projeto parceiro Canecas POD):
`01 - brutas (suba aqui)` → `02 - selecionadas` → `03 - editadas` →
`04 - artes recebidas` → `05 - APROVAR (semana)` → `06 - videos e trilhas` →
`07 - nao compartilhar (com o Ramon)`. Dentro de `01 - brutas`, a subpasta
`garimpo/` é a saída do `garimpo.py` (com `melhores-30/` para o ranking top
30 e `RELATORIO.md`).

### `.claude/skills/hana-social/SKILL.md`

Não é código do pipeline — é a "memória viva" que o Claude Code carrega ao
abrir uma conversa nesta pasta. Guarda o histórico de erros já cometidos e
corrigidos (com uma "Regra Zero" contra afirmar sem conferir a fonte real),
todas as decisões de posicionamento/tom/trilha/veto de artista do Ramón, o
protocolo de auditoria obrigatória antes de qualquer mídia chegar até ele, e
instruções de formato de resposta (respostas curtas, decisão em vez de
pergunta operacional). É extremamente detalhada e vale a leitura direta por
quem for dar continuidade ao projeto — resume praticamente todo o histórico
de decisões humanas que não está no código.

---

## Seção 4 — Como reconstruir do zero

Passo a passo técnico, assumindo Windows (o `studio/` depende de Windows) com
Python 3.11+ instalado:

1. **Clonar/criar a estrutura de pastas** exatamente como descrito na Seção 3:
   `publisher/`, `studio/`, `content/{queue,posted,previas,previews,trilhas}`,
   `estrategia/`, `Fotos da Hana/{01 - brutas (suba aqui),02 - selecionadas,
   03 - editadas,04 - artes recebidas,05 - APROVAR (semana),
   06 - videos e trilhas,07 - nao compartilhar (com o Ramon)}`,
   `.github/workflows/`.

2. **Instalar dependências.**
   - Para o publicador (o que roda no GitHub Actions): `pip install -r requirements.txt`
     (hoje só `requests>=2.31,<3`).
   - Para o estúdio (o que roda local, não coberto pelo `requirements.txt`):
     `pip install Pillow pillow_heif imageio_ffmpeg ultralytics opencv-python numpy requests`.
   - Precisa de `ffmpeg` disponível (o `imageio_ffmpeg` normalmente baixa um
     binário sozinho na primeira execução).
   - Precisa das fontes do Windows citadas na Seção 3 (`C:\Windows\Fonts\...`)
     para os scripts que desenham texto/arte sobre a imagem/vídeo.
   - Instalar o GitHub CLI (`gh`) autenticado, usado por `estado.py` e pelo
     vigia local (`sentinela.py`) para consultar/disparar workflows.

3. **Configurar as variáveis de ambiente**, com base no `.env.example` (nomes,
   nunca valores):
   - `IG_USER_ID` — id numérico da conta Instagram Business/Creator.
   - `IG_ACCESS_TOKEN` — token de longa duração da Graph API (renovar a cada
     ~60 dias; ver `SETUP.md` para o passo a passo completo de criação do app
     na Meta).
   - `GRAPH_BASE` — `https://graph.instagram.com/v21.0` (fluxo novo, padrão)
     ou `https://graph.facebook.com/v21.0` (fluxo clássico, via Página do
     Facebook — necessário só se for usar a Audio API para trilha de
     tendência em Reels).
   - `MEDIA_BASE_URL` — URL pública base de onde a Graph API baixa a mídia
     (ex.: raw do próprio repositório, se público).
   - `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` — só se for usar aprovação
     pelo Telegram (opcional; ver `REQUIRE_APPROVAL`).
   - `REQUIRE_APPROVAL` — `1` (exige aprovação no Telegram antes de publicar,
     padrão) ou `0` (publica direto no horário agendado).
   - Localmente, copiar para `.env` (nunca commitado); no GitHub Actions,
     cadastrar como Secrets/Variables do repositório (ver `SETUP.md` passo 5
     para a lista exata e quais vão em Secrets vs. Variables).
   - Também usadas pelo workflow, mas opcionais/degradam sem quebrar:
     `GEMINI_API_KEY` (recepcionista do Telegram), `IG_USER_ID_FB` /
     `FB_ACCESS_TOKEN` (fluxo Facebook Login, só para trilha de áudio de
     tendência em Reels), `IG_TOKEN_EXPIRA_EM` (aviso de vencimento).

4. **Credenciais locais do `studio/`** (fora do git, criadas manualmente):
   `studio/.token` (linha `IG_ACCESS_TOKEN=...`, usado por scripts que rodam
   fora do Actions, como `checar_repetida.py`), `studio/.telegram` (formato
   `TELEGRAM_BOT_TOKEN=...` / `TELEGRAM_CHAT_ID=...`, para o robô local avisar
   sem depender dos secrets do GitHub), e a chave do Gemini em
   `chaves-api.txt` fora do projeto (caminho: `~/OneDrive/Desktop/Claude code
   APIs/Documents/IA-Hub/chaves-api.txt`, linha `GEMINI_API_KEY=...`).

5. **Contas externas necessárias** (passo humano, ver `SETUP.md` na íntegra):
   conta Instagram Business/Creator; app na Meta (developers.facebook.com)
   com o produto "Instagram → API with Instagram Login", permissões
   `instagram_business_basic` + `instagram_business_content_publish`, App
   Review submetido (2-4 semanas); opcionalmente bot do Telegram via
   @BotFather; repositório GitHub público (ou bucket alternativo) para servir
   a mídia por URL pública.

6. **Ordem de execução dos scripts principais** (fluxo normal de uso, depois
   de tudo configurado):
   1. `python studio/preparar_lote.py editar` — edita fotos brutas em
      `01 - brutas (suba aqui)`, gera `contact_sheet.jpg` em `02 - selecionadas`.
   2. Escolher/criar Reel: montar um roteiro JSON em `studio/roteiros/` e
      rodar `python studio/montar_reel.py roteiro.json saida.mp4` (ou, para
      foto avulsa, `python studio/preparar_lote.py post <foto> <id> <data>
      "<legenda>" [pilar]`).
   3. `python studio/checar_repetida.py` — confere repetição contra o que já
      está no ar e dentro da própria fila, antes de aprovar.
   4. Publicação: automática via `.github/workflows/publish.yml` (cron a
      cada 30 min + reforço nos horários fixos), ou manual via
      `gh workflow run publish.yml -R <owner>/<repo>`.
   5. `python publisher/metrics.py` (ou automático, 1x/dia dentro do
      workflow) — atualiza `content/placar.md`.
   6. Rotina semanal sem gastar tokens do Claude:
      `python studio/lote_automatico.py --simular` (só mostra o plano) ou sem
      `--simular` (executa de verdade) — normalmente disparado pela tarefa
      agendada `Hana Sentinela` no PC do Ramón (`studio/sentinela.bat`), não
      manualmente.
   7. `python studio/estado.py --mostrar` (ou sem `--mostrar`, para
      regerar `ESTADO-ATUAL.md`) — é o primeiro comando que qualquer sessão
      nova do Claude Code deveria rodar nesta pasta, por instrução da própria
      skill do projeto.

7. **Agendamento local** (Windows Task Scheduler): uma única tarefa,
   "Hana Sentinela", chamando `studio/sentinela.bat`, configurada para rodar
   segunda/quarta/sexta por volta das 18h (horário local do Ramón). Não criar
   tarefas agendadas adicionais — a skill do projeto é explícita que só deve
   existir este robô local; qualquer coisa nova deve ser encaixada dentro
   dele ou do workflow do GitHub.

---

## Seção 5 — Estado atual e pendências

Fonte: `ESTADO-ATUAL.md` (gerado automaticamente em 04/08/2026 08:21),
`DECISOES.md` e `content/placar.md`. Como este arquivo é gerado por código a
partir das fontes reais, ele é a referência mais confiável sobre "onde o
projeto está agora" — o resumo abaixo pode ficar desatualizado; para o estado
mais recente, rodar `python studio/estado.py --mostrar`.

- **Fila**: 8 posts aguardando publicação entre 05/08 e 21/08/2026 — 2 fotos
  já aprovadas (05/08, 07/08), 2 Reels aprovados (10/08, 12/08), 4 Reels ainda
  `pending`. A grande maioria do conteúdo futuro é Reel (não foto), por
  decisão editorial de 31/07/2026.
- **Publicados**: 6 posts (5 fotos + o restante listado), até 03/08/2026.
  Nenhum Reel publicado ainda — o primeiro está agendado para 10/08.
- **Métricas** (`content/placar.md`, coleta de 04/08/2026): 330 seguidores,
  crescimento praticamente parado (329→330 em uma semana). Alcance médio por
  foto: 46. **Zero salvamentos, zero compartilhamentos e zero seguidores
  ganhos** em todos os 6 posts de foto medidos — é o número que motivou a
  virada editorial para Reel de vídeo real com rosto em quadro.
- **Automação**: publicador rodando com sucesso nas últimas execuções
  registradas; vigia local ativo; renovação automática de token configurada.
- **Esperando o OK do Ramón**: um lote de mídias numeradas em
  `Fotos da Hana\05 - APROVAR (semana)` (fotos, Reels e prévias de trilha),
  que ele revisa pelo celular via OneDrive.
- **Acervo**: 38 arquivos brutos a processar, 4 editados prontos, 1 arte
  recebida do parceiro, e **34.455 arquivos do rolo de câmera do iCloud**
  ainda sendo varridos pelo `garimpo.py` (roda ~40 min/dia, retomável —
  estimativa de ~89 horas de processamento total na velocidade medida).
- **Pendência ativa mais recente** (segundo `DECISOES.md`): o Reel de 12/08
  passou por sete versões e cinco reprovações de auditoria antes de ser
  aprovado (03/08/2026) — as lições viraram regras permanentes na skill
  (Reel precisa de história + trilha, mínimo 5 cortes, corrigir material
  ruim trocando o clipe em vez de insistir no ajuste, mídia refeita precisa
  de nome de arquivo novo). Havia também alterações não commitadas no
  momento da última geração do `ESTADO-ATUAL.md` (posts removidos/renomeados
  na fila, roteiros novos de Reel, trilhas novas) — conferir `git status` na
  hora de continuar o trabalho, pois pode ter mudado.
- **Regras que não devem ser reabertas sem ordem explícita do Ramón** (lista
  longa em `SKILL.md`, section 2): não misturar a Página do Facebook da Hana
  como canal ativo (ela existe só como infraestrutura da Graph API para
  áudio), não usar música de artista da lista negra (Anitta, Xuxa), não
  propor produto/venda, não gerar foto/vídeo de IA por API (só pelo app
  pago, como usuário comum, sempre em qualidade máxima), "ronda de
  engajamento" está morta (matada pelo conselheiro em 03/08/2026 por falta
  de teste que comprovasse retorno).

---

## Verificação final desta sessão

`git status` na pasta, no momento em que este arquivo foi escrito: **limpo**
(`nothing to commit, working tree clean`, branch `main` sincronizado com
`origin/main`). Não havia mudança não salva no momento da análise — mas note
que `ESTADO-ATUAL.md` (gerado antes, às 08:21 de 04/08) registrava várias
alterações não commitadas que já não estavam mais presentes nesta checagem,
ou seja, algo foi commitado entre a geração daquele arquivo e agora. Não foi
feito nenhum commit por esta análise.

## 🔗 Relacionados

> Ligações geradas automaticamente por `tecer-vault-obsidian.py` a
> partir das citações que já existiam no texto acima.

- [[DECISOES]]
- [[ESTADO-ATUAL]]
- [[ORGANOGRAMA]]
- [[aviso_lote]]
- [[benchmark-instagram]]
- [[benchmark-tecnico]]
- [[brand-brief]]
- [[calendario-editorial]]
- [[hipoteses-produto]]
- [[parceria-canecas-pod]]
- [[pauta_extra]]
- [[pedido-de-cena]]
