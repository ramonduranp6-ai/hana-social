# Decisões e contexto — Hana Social

Parte humana do estado: o que o Ramón decidiu e o que código nenhum adivinha.
**Atualizar ao fim de cada sessão** (a parte automática vem de `studio/estado.py`).
Mais recente em cima.

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
