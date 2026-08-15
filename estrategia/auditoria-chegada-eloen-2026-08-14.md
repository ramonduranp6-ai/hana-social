# Auditoria — "A chegada da Eloen" (peça 2026-08-K)

**Arquivo auditado:** `content/queue/2026-08-K_chegada-eloen/chegada-eloen-v2-editado.mp4`
**Roteiro:** `studio/roteiros/2026-08-K_chegada-eloen.json`
**Bruto:** `Fotos da Hana/01 - brutas (suba aqui)/hana_noticia_nova_irma.mov`
**Data:** 14/08/2026 · **Auditor:** diretor-reels (quem constrói não audita)
**Custo desta auditoria:** R$ 0,00 — só ffmpeg/ffprobe, nenhuma ferramenta paga, nenhuma IA externa.

> **Esta auditoria NÃO aprova nada.** Quem aprova é o Ramón. O que está aqui é
> se a peça está ou não dentro do padrão técnico da casa, com número em cima.

---

## 0. As duas travas antigas foram levantadas — o que isso muda aqui

O Ramón levantou nesta conversa as duas restrições que valiam desde 09/08:
(1) pode anunciar a gravidez publicamente; (2) rosto de família pode aparecer.

**Consequência para esta auditoria:** a checagem de rosto/fumaça da
`auditoria-baloes-v4-2026-08-14.md` **não se aplica a este material** e não foi
refeita. Rosto de família no quadro e a explosão de fumaça rosa **não são
defeito** nesta peça — são o conteúdo autorizado. Tudo abaixo é medição nova.

---

## 1. O que eu medi por conta própria (não aceitei número de ninguém)

| item | medido por mim | alvo do manual | veredito |
|---|---|---|---|
| resolução | 1080x1920 | 1080x1920 | ✅ |
| proporção | 9:16 | 9:16 | ✅ |
| fps | 30 (constante, 183 frames) | 30 | ✅ |
| duração | 6,176 s (vídeo 6,100 / áudio 6,176) | 6-18 s | ✅ no piso |
| brilho médio | 124,81 | 110-130 | ✅ |
| **variação de brilho** | **22,03** (mín 112,40 / máx 134,43; desvio-padrão 6,77) | < 30 | ✅ |
| texto na tela | zero | zero | ✅ |
| **loudness real** | **≈ −15,1 LUFS** (ver §2) | −14 ±1 | ❌ fora por um fio |
| **pico verdadeiro** | **−0,45 / −0,5 dBTP** | ≤ −1 dBTP | ❌ **estoura o teto** |
| zoom artificial | **existe** (corte 1: `punch`, força 0,08) | zero | ❌ |
| transição / filtro | zero (corte seco nos 4) | zero | ✅ |
| rosto da Hana no 1º segundo | **ausente** (ver §4) | obrigatório | ❌ |
| rosto da Hana no desfecho | **ausente** (ela aparece, o rosto não) | obrigatório | ❌ |

**Confirmei o número de brilho do construtor:** 22,03. Está certo, passa com
folga. Esse era o pior defeito histórico da casa (80→196) e está resolvido.

---

## 2. O caso do loudness — os dois números dele estavam errados, e eu descobri por quê

O construtor entregou dois valores que discordavam (−15,95 do `loudnorm` e
−14,6 do `ebur128`) e pediu desempate. Refiz as duas medições e fiz um teste
para desempatar.

**Reprodução (arquivo final, e depois no áudio extraído em WAV 24 bits — mesmo
resultado nos dois, então não é problema de container):**

- `ebur128`: I = **−14,6 LUFS**, LRA 14,9 LU, true peak **−0,5 dBFS**
- `loudnorm` (análise): input_i = **−15,95**, input_tp = **−0,45**, input_lra = 14,30

**O desempate.** O loudness integrado da norma EBU R128 não muda quando você
repete o mesmo áudio — é média com portão, não soma. Então repeti o áudio 8x
(49 s) e 24 s (148 s) para tirar o viés de arquivo curto e medi de novo:

| medição | `ebur128` | `loudnorm` |
|---|---|---|
| arquivo original (6,18 s) | −14,6 | −15,95 |
| mesmo áudio repetido 8x | −15,0 | −15,17 |
| mesmo áudio repetido 24x | **−15,0** | **−15,12** |

Com o clipe longo os dois métodos **convergem em ≈ −15,1 LUFS**. Ou seja:

- **A verdade é ≈ −15,1 LUFS.** Nenhum dos dois números dele estava certo.
- O −15,95 do `loudnorm` estava baixo demais; o −14,6 do `ebur128` estava alto
  demais. Os dois erram no mesmo motivo: **6 segundos é curto demais** para o
  portão do R128 se estabilizar (a explosão de fumaça é muito mais alta que o
  resto — LRA de 14,3-14,9 LU num clipe de 6 s).
- **Regra para o futuro, que é o achado de processo desta sessão:** em peça de
  menos de ~10 s, medir loudness no arquivo repetido em laço, não no arquivo
  cru. Os dois métodos batem e aí o número é confiável.

**Contra o checklist do manual (§8):**
- Loudness: alvo −14 ±1 = janela **[−15,0 ; −13,0]**. Medido **−15,1** →
  **fora por 0,1 LU**. Reprova pela letra, mas é um fio de cabelo.
- Pico: teto **−1 dBTP**. Medido **−0,45 / −0,5 dBTP** → **reprova sem margem
  de discussão**, está 0,5 dB acima do teto.

### A causa-raiz (isto é mais importante que o número)

**O `studio/montar_reel.py` nunca aplica `loudnorm` no passo final.** Ele só
faz `dynaudnorm=f=250:g=15` corte a corte (nivelar entre cortes) — o que é
outra coisa. O `studio/reel_ritmado.py` tem o `loudnorm=I=-14:TP=-1:LRA=11`
(linha 181), o `montar_reel.py` não tem. Toda peça montada por esse script vai
sair fora do padrão de som do manual, não só esta.

Comprovação: o rascunho `chegada-eloen-v2-RASCUNHO.mp4` mede −14,8 / pico −0,4
e o "editado" mede −14,6 / pico −0,5 — ou seja, **nenhum passo de masterização
aconteceu** entre um e outro; o "editado" só reencodou vídeo.

### O conserto — eu testei antes de recomendar

Rodei a correção num arquivo temporário e medi o resultado (depois apaguei):

```
ffmpeg -y -i chegada-eloen-v2-editado.mp4 -c:v copy \
  -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=-15.95:measured_TP=-0.45:measured_LRA=14.30:measured_thresh=-28.92:offset=0.66" \
  -c:a aac -b:a 192k -ar 48000 chegada-eloen-v3.mp4
```

Resultado medido no arquivo corrigido (leitura no laço, sem viés):
**I = −14,6 / −14,7 LUFS · true peak = −1,0 dBTP exato.** Os dois critérios
passam.

**Detalhe técnico que importa:** na segunda passada é preciso alimentar o
`loudnorm` com os números que **o próprio `loudnorm`** mediu (−15,95 etc.), não
com os do `ebur128`. Misturar os dois é exatamente o erro que gerou a confusão.

Custo: **R$ 0,00**, ~2 segundos, vídeo intocado (`-c:v copy`, sem perda de
qualidade de imagem).

---

## 3. Quais critérios do manual NÃO se aplicam a esta peça — e por quê

O `manual-profissional-reels.md` e o `virais-medidos-2026-08-13.md` foram
escritos medindo **um gênero só: reel cômico dono × cão, onde o cão vence.**
Esta peça é outro gênero: **anúncio de marco de família, registro único de um
evento real e irrepetível.** Reprovar por critério de comédia aqui seria erro
meu, não defeito da peça. Declaro item a item:

**NÃO se aplicam:**

1. **"UMA piada. Conflito dono × Hana. Ela vence." (§3)** — não existe piada
   aqui e não deveria existir. O motor emocional é surpresa + afeto, não humor.
   *"Não tem piada" não é defeito desta peça.*
2. **"A cena é ENCENADA, não achada" / "filmar 3-5 tomadas" (§1)** — impossível
   por definição. O chá revelação aconteceu uma vez, foi filmado por terceiro,
   sem direção nossa. Não há segunda tomada e nunca haverá.
3. **Pedido de cena, câmera na altura dela, tripé, luz única atrás da câmera,
   cenário limpo, 2 s de margem (§1 e §2)** — são instruções de **captura
   futura**. Não julgam material de arquivo. Ignorados.
4. **"Plano único é o padrão" (§4)** — o próprio manual abre exceção para "peça
   de acervo". Um marco de família é exatamente isso. **4 cortes está correto**
   e não conta como defeito.
5. **"Música só quando é personagem da piada" (§5)** — não há piada. Aqui o som
   real da cena é a escolha certa e a mais forte que existia (ver §6).
6. **"Mais de uma piada" (§8)** — sem objeto. (A outra metade do mesmo item,
   "mais de 18 s sem virada", **se aplica** e passa: 6,18 s.)

**SE APLICAM integralmente e foram julgados acima:** luz estável, som no
padrão do feed, 9:16 / 1080x1920 / 30fps, texto na tela zero, zero transição /
filtro / zoom, ausência de erro técnico, anatomia e cor da Hana, e — o mais
importante — **a Hana ser o centro, com rosto no início e no desfecho.**

---

## 4. A Hana: presença, protagonismo, anatomia e cor

### Presença — ela está, e nos dois extremos ✅ (com ressalva séria)

Mapa dos cortes (0,90 + 1,70 + 2,40 + 1,10 = 6,10 s):

| trecho | o que é | Hana está? |
|---|---|---|
| 0,00-0,90 | gancho, ela com os balões | ✅ ela é o único assunto |
| 0,90-2,60 | a revelação, plano aberto | ⚠️ presente, mas é uma manchinha |
| 2,60-5,00 | reação da família | ✅ no meio dos dois, sendo acariciada |
| 5,00-6,10 | fecho no cobertor | ✅ terço inferior do quadro |

**Confirmo a decisão de parar em 18,90 s do bruto.** Conferi o bruto de 17 s a
29,5 s: **de 19,4 s em diante a Hana some do quadro e sobra só o casal se
beijando até o fim dos 30 s.** Cortar antes disso estava certo e é a aplicação
correta da regra permanente 1. Ponto bem executado.

### O problema: **o rosto dela não aparece nem na abertura nem no fecho** ❌

Extraí a peça quadro a quadro nos dois extremos.

**Primeiro segundo (0,03 · 0,18 · 0,33 · 0,48 · 0,63 · 0,78 s):** a Hana está
**de costas ou de traseiro para a câmera, indo embora**, nos seis quadros. Em
0,33 s é traseiro puro. **O rosto dela não é legível em nenhum quadro do
primeiro segundo.** Além disso, os 45% de cima do quadro são grama vazia e ela
fica pequena, no canto de baixo.

**Último segundo (5,10 · 5,35 · 5,60 · 5,85 · 6,00 · 6,05 s):** em 5,10 ela
está quase fora do quadro, na beirada direita. Ela volta e no fim ocupa o terço
inferior — mas vista **de cima e de trás**, com a cabeça baixa. Só no
derradeiro quadro (6,05) aparece um perfil parcial, com a boca aberta e borrado
de movimento.

Isso viola o item mais direto do checklist (§8):
> **"Rosto ausente do 1º segundo ou do desfecho → REPROVA."**

E este critério **se aplica sim a este gênero**. O conceito da peça é "a Hana é
a mensageira" — a legenda é em 1ª pessoa dela. Se nos 3 primeiros segundos o
espectador vê um traseiro de cachorro andando para longe, o conceito não chega.
É o gancho, é onde 3 segundos decidem se o vídeo é entregue ou não.

**Consequência prática que fecha o caso:** o manual §6 exige capa com **frame
do rosto dela, olhos abertos**. Varri a peça inteira: **não existe um único
frame no arquivo entregue que sirva de capa segundo essa regra.** Isso sozinho
já mostra que o problema não é chatice de auditor.

### Onde está o material melhor — eu procurei no bruto e achei

Varri os 30 s do bruto com grab isolado (`-ss` sozinho, o método confiável que
o próprio construtor identificou):

- **GANCHO — trocar `6,05-6,95` por ≈ `5,00-5,90`.** Entre 4,8 s e 6,0 s a Hana
  vem **andando reto na direção da câmera, cabeça erguida, rosto inteiro
  visível**, com os balões nas costas e a mãe de branco atrás dela. Ela
  **cresce no quadro sozinha** conforme se aproxima. A janela escolhida
  (6,05-6,95) começa no finzinho desse trecho e cai quase toda em 6,6-6,9,
  onde ela já virou e está correndo de costas — que é exatamente o que se vê
  no arquivo final.
  **Bônus:** como ela cresce no quadro por conta própria, **dá para apagar o
  `punch` artificial** — a aproximação vira movimento real de câmera, e some
  também a terceira reprova (§5 abaixo).
  *Ressalva honesta:* entre 5,4 s e 5,9 s passam desconhecidos no fundo (um
  casal de idosos, uma mulher de azul com bebê). Em 4,8-5,3 o fundo é limpo.
  Vale testar as duas janelas.
- **FECHO — testar ≈ `16,2-17,2` no lugar de `17,80-18,90`.** Em 16,0-16,8 s
  ela está **bem maior no quadro, em pé sobre o cobertor, de cabeça erguida**,
  entre o casal e a câmera. Muito mais legível que a janela usada, onde ela já
  se acomodou de cabeça baixa. Continua terminando nela, continua respeitando
  a regra 1.

### Anatomia e cor ✅

- **Rabo: não tem, e não aparece nenhum.** Conferi nos quadros de traseiro puro
  (0,33 e 0,48 s), que é onde um erro apareceria. Bobtail natural preservado.
  Registro que a bronca original (`DECISOES.md`: *"Não gostei! Hana não tem
  rabo."*) foi sobre vídeo **gerado por IA**.
- **Este material é filmagem real, não gerado.** Não há prompt, não há modelo,
  não há como inventar anatomia. A classe inteira de risco "erro anatômico de
  IA" **não existe nesta peça** — e, pela mesma razão, **não há nada a declarar
  sobre uso de IA** na publicação.
- **Cor tri lilac merle:** o padrão mesclado lilás/acinzentado no dorso lê
  corretamente sob o sol forte, com o fulvo claro nas patas e no focinho.
  Nenhuma saturação estourada (o `brand-brief.md` proíbe). Sem correção de cor
  aplicada pelo montador. ✅
- **Proporção do corpo:** normal para Exotic Bully Micro, sem distorção de
  esticamento. Confirmei que o recorte não é anamórfico: 9:16 puro em todos os
  cortes.

---

## 5. Os outros achados

### 5.1 Zoom artificial no corte 1 ❌ (reprova pela letra do manual)

O roteiro pede `"movimento": "punch", "forca": 0.08` no corte de abertura, e o
`montar_reel.py` (linhas 118-129) transforma isso numa expressão `zoompan`
animada ao longo dos 0,9 s. O manual §4 e §8 são literais:
> "corte seco, **zero transição, zero filtro, zero zoom artificial**"
> "Transição, filtro ou zoom artificial → **REPROVA**"

É sutil (8%), mas é a regra escrita. **Conserto grátis:** trocar `"punch"` por
`"seco"`. E se o gancho for trocado para 5,00-5,90 (§4), o punch fica
desnecessário de qualquer jeito, porque ela se aproxima de verdade.

### 5.2 A resolução real é 576x1024, não 1080x1920 ⚠️ (não é reprova, mas ele precisa saber)

O bruto é **1024x576 com rotação −90 nos metadados**, ou seja, **576x1024 de
detalhe real**. O arquivo entregue diz 1080x1920, mas é ampliação:

- corte 2 (`aproximar: 1.0`): ampliação de **1,88x**
- cortes 1 e 3 (`aproximar: 1.3`): ampliação de **2,44x**

Por isso a imagem é macia, especialmente na grama. **Isso não tem conserto por
software e não é culpa da montagem** — é o material que existe. Registro só
para ele não esperar nitidez de 1080p nativo, e para reforçar o pedido do
manual §2 de gravar em 1080x1920 daqui para frente. Os virais medidos são
720x1280, então isso não impede a peça de funcionar.

### 5.3 Uma terceira pessoa filmando entra no quadro em ~1,3 s ⚠️

No corte da revelação, uma mulher com celular na mão aparece na beirada direita
do quadro. É documental e some rápido, mas é um borrão que não serve à
história. Se o corte for remontado, vale começar 2-3 frames depois ou apertar
um pouco o enquadramento. Não é motivo de reprova sozinho.

### 5.4 A revelação (28% da peça) é o único trecho onde a régua permanente aperta ⚠️

Regra permanente 1 do projeto (`DECISOES.md` e `brand-brief.md`):
> "se a Hana puder ser cortada do quadro sem mudar a piada, o post está errado"

No corte 2 (0,90-2,60 s), o casal está pequeno no meio de um plano aberto e a
Hana é uma manchinha de poucos pixels ao lado dos balões. Dá para cortá-la fora
do quadro sem mudar nada. **A peça como um todo passa na régua** — a história é
dela (ela leva os balões, a legenda é a voz dela, abre e fecha nela) — mas o
clímax não é dela. Registro como observação de conceito, não como reprova.
*[opinião, não medição]*

### 5.5 Duração: 6,18 s está no piso ⚠️ *[opinião]*

Fica dentro do alvo (6-18 s) e bem abaixo do meu teto de 15 s. Mas quatro
batidas em 6,18 s dá **1,7 s para a revelação**, que é o miolo emocional. Em
anúncio de família o gênero pede que o clímax respire. **Sugiro testar 9-12 s**
— continua dentro da faixa de retenção boa (a assistida só desaba depois de
15 s) e o momento tem tempo de aterrissar. Não é defeito, é margem de melhora.

### 5.6 Legenda e hashtags ✅ (com um reparo pequeno)

- Primeira linha é gancho de 1ª pessoa dela e cabe antes do "ver mais" ✅
- Termina com pergunta que puxa comentário ✅
- 4 hashtags, dentro do teto do `brand-brief.md` ✅
- ⚠️ `#chegoueloen` é hashtag inventada, com volume zero. São só 4 vagas; essa
  gasta uma sem trazer alcance nenhum. Trocar por uma das fixas fortes
  (`#bullymicro` ou `#bullylife`) rende mais. *[opinião — a palavra final sobre
  hashtag é do diretor-redes, não minha.]*
- Nada inventado: sem depoimento falso, sem número inventado, sem promessa que
  a operação não cumpre, sem alegação de trabalho manual. ✅

### 5.7 Direito autoral e caminho de publicação ✅ — **este ponto é bom**

A peça usa **só o som real da cena**, nenhuma faixa licenciada. Conta business
não pode usar hit de gravadora; aqui não usa. Portanto:

> **Esta peça pode ser publicada pelo robô, automaticamente. Não precisa
> subida manual pelo app, não corre risco de mute nem de strike.**

O som real também é a escolha artística certa: numa revelação, o grito e o
estouro são a prova de que aconteceu de verdade. Aplaudo a decisão.

---

## 6. A história tem os três atos? ✅

Sim, e essa é a maior virtude da peça — é a primeira do projeto com arco de
verdade, não clipe bonito com música em cima:

- **Começo:** a Hana leva os balões até a família (ela é a mensageira).
- **Meio:** a fumaca rosa estoura — a virada.
- **Fim:** a família comemora e ela se acomoda no meio deles.

A legenda fecha o arco com a reviravolta ("sem saber que a festa também era
minha"), que é o que transforma registro em história. **Conceito aprovado.** O
problema desta peça não é o conceito nem o roteiro — é a **execução do gancho e
do fecho**, que não mostram o rosto da protagonista.

---

## 7. Veredito

### ❌ **NÃO está no padrão técnico ainda.** Três reprovas confirmadas.

| # | defeito | critério | conserto | custo |
|---|---|---|---|---|
| 1 | pico −0,45 dBTP (teto −1) e loudness −15,1 (janela −15,0 a −13,0) | manual §8 | **barato** — 1 comando, vídeo intocado, já testei e funciona | R$ 0,00 |
| 2 | rosto da Hana ausente no 1º segundo **e** no desfecho | manual §8 e §3 | **remontar — mas remontagem barata** | R$ 0,00 |
| 3 | zoom artificial (`punch`) no corte 1 | manual §4 e §8 | trocar 1 palavra no JSON | R$ 0,00 |

**Sobre o defeito 2 — é remontagem, não é conserto de cor ou som, mas é a
remontagem mais barata possível:** não precisa filmar nada, não precisa
ferramenta paga, não precisa IA. São **quatro números no
`studio/roteiros/2026-08-K_chegada-eloen.json`** e rodar o montador de novo:

```
corte 1 (gancho):  de 6.05 → ~5.00   ate 6.95 → ~5.90   movimento "punch" → "seco"
corte 4 (fecho):   de 17.80 → ~16.2  ate 18.90 → ~17.2
```

Depois: rodar o `loudnorm` do §2 no arquivo final, e **remedir** — brilho com
`signalstats` (a janela nova é outra luz, o 22,03 não vale mais) e loudness com
o teste em laço.

**Correção obrigatória de processo, além desta peça:** o `montar_reel.py`
precisa ganhar o passo `loudnorm=I=-14:TP=-1:LRA=11` que o `reel_ritmado.py` já
tem. Sem isso, **toda** peça montada por ele nasce fora do padrão de som.

### O que passa e não precisa mexer

Luz (22,03, o melhor número da história do projeto) · 9:16 1080x1920 30fps ·
zero texto na tela · zero transição e zero filtro · som real sem risco de
direito autoral (o robô pode publicar sozinho) · história com três atos ·
anatomia e cor da Hana corretas · nada inventado · fecho parando antes do trecho
sem ela (decisão certa, conferida por mim) · custo R$ 0,00 do começo ao fim.

### O que precisa de decisão do Ramón (não minha, não do construtor)

1. **A data.** Anúncio de bebê tem hora combinada com a família — não entra em
   calendário de conteúdo. Está corretamente sem data no `post.json`.
2. **A duração.** Fica em 6 s ou testa 9-12 s para a revelação respirar?
3. **Publicar assim mesmo?** Os defeitos 1 e 3 são objetivos e grátis — não vejo
   argumento para não consertar. O defeito 2 é o que muda a peça: se ele quiser
   publicar hoje do jeito que está, é escolha dele, e o custo é entregar o
   momento mais importante do ano da família com um gancho que mostra a Hana de
   costas indo embora.

**Nenhum gasto proposto nesta auditoria. Nada foi publicado. Nada foi alterado
na peça.**
