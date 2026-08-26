# Referência mandada pelo Ramón — @rafabri7o, "Uai, resolvido" (26/08/2026)

Link: https://www.instagram.com/reel/DaWSrJJRYba/
Autor: **Rafa Brito | Estrategista de Conteúdo** (@rafabri7o) — 1,3 mi
seguidores, 2.046 posts, bio "Mostro como empresários usam conteúdo para gerar
autoridade, audiência e faturamento · MAIS DE 30.000 ALUNOS EM 19 PAÍSES".
Publicado em **03/07/2026**. **19.137 curtidas · 511 comentários** (números da
API, não estimativa). Views: **a API não devolveu** — não vou inventar.

## Como eu consegui o vídeo (método, com o limite declarado)

- O `/embed/` público caiu em **muro de login** — rota morta para este Reel.
- Baixei com **yt-dlp** (módulo já instalado na máquina), post público, **sem
  login em conta nenhuma**. 4,8 MB.
- **NÃO gastei Apify.** O saldo de US$ 5 continua intacto — esta rota é grátis
  e deve virar a padrão para estudar Reel isolado.
- Assisti de verdade: **20 frames em grab isolado** (`-ss` sozinho, um ffmpeg
  por frame), cortes por `scene`, som por `loudnorm`/`volumedetect`, e
  **transcrição do áudio com Whisper** (faster-whisper small, pt, custo zero).

## Ficha técnica MEDIDA

| item | medido |
|---|---|
| duração | **31,97s** |
| resolução | **720x1280**, 30fps, h264 (mesma dos 7 virais de 13/08) |
| cortes | **5** — em 5,3s · 9,2s · 13,4s · 19,3s · 30,0s (6 blocos) |
| loudness | **−14,26 LUFS**, pico **−0,69 dBTP**, LRA 2,70 |
| áudio | **original** (voz dele). Sem música. Sem trecho de silêncio > 0,3s |
| texto na tela | **1 cartela grande fixa nos primeiros 5,3s** |
| efeito | zero transição, zero filtro. Só **círculo/retângulo vermelho** desenhado em cima do botão |
| pessoa | **2 homens** no quadro o tempo todo: um narra, o outro só faz cara de espanto |

## O que é o Reel, batida a batida (transcrição real do áudio)

**Camadas:** fundo = os dois homens (carro, depois sofá). Por cima = **gravação
de tela** do Instagram dele.

| tempo | o que acontece | fala (transcrita) |
|---|---|---|
| 0–5,3s | **GANCHO.** Cartela: "MEU INSTAGRAM ESTAVA HABILITADO PARA NÃO VIRALIZAR". O amigo na frente faz cara de choque escancarada | "Eu descobri que meu perfil estava habilitado para não viralizar… por isso que eu postava, postava e nunca viralizava" |
| 5,3–9,2s | **PROVA.** Gravação de tela: enxurrada de "começou a seguir você", dezenas de linhas, carimbos de 40 min / 1 h / 2 h | "Depois eu descobri, eu arrumei, [olha] a de seguidor que eu ganhei" |
| 9,2–13,2s | **PROMESSA.** Perfil dele na tela (1,3 mi) | "vem cá que eu vou te ensinar a arrumar isso também… o povo cobra caro em curso pra te ensinar, eu vou te ensinar **de graça, pelo menos me segue**" |
| 13,2–19,1s | **PASSO 1.** Menu → "Compartilhamento e reutilização" → liga os 3 botões. Círculo vermelho no botão exato | "clicar nesses três pontinhos… vir em compartilhamento, reutilização… ativar esses três tudo aqui" |
| 19,1–23,1s | **PASSO 2.** Volta ao menu → "Qualidade de vídeo" | "vem aqui em qualidade de vídeo, vai ativar essa aqui que eu tô te marcando" |
| 23,1–29,8s | **PASSO 3.** Editar perfil → campo Nome, retângulo vermelho em "Rafa Brito \| Estrategista de Conteúdo" | "põe o nome do teu nicho pra ajudar o Instagram a entregar teu perfil pra quem tem interesse" |
| 29,8–31,97s | **FECHO/CTA.** Volta pros rostos, close | "**E você me seguiu, né? Por uma dica top dessa?**" |

Legenda: "Uai, resolvido" (2 palavras).

## Por que funciona (mecânica)

1. **Culpa terceirizada.** O gancho não diz "você errou", diz "tinha uma coisa
   ligada contra você **sem você saber**". Alivia quem posta e não cresce — e
   esse é praticamente todo mundo que vê.
2. **PROVA na tela antes de pedir qualquer coisa.** A enxurrada de "começou a
   seguir você" é o coração do Reel. Sem esse trecho, é só mais um guru falando.
3. **Ele entrega o passo a passo inteiro, de graça, com o botão circulado.**
   Não tem "link na bio", não tem "comenta EU QUERO". Vira **salvamento** (dá
   pra refazer depois) e **compartilhamento** (manda pro amigo que reclama do
   alcance).
4. **A cara do amigo é o motor de retenção.** Gravação de tela é chata; a cara
   de choque ao lado segura o olho por 32 segundos.
5. **Pede o seguir no FIM, depois de entregar** — e em tom de brincadeira.

## Julgamento contra o nosso manual e os 10 virais de 13/08

### CONFIRMA (e forte)

- **Som:** −14,26 LUFS / −0,69 dBTP. É **exatamente** o alvo do §5 do manual
  (−14 ±1, pico −1). Terceira medição independente batendo no mesmo número —
  o padrão de som do manual está certo e não se discute mais.
- **Resolução não é a alavanca:** 720x1280, mais baixa que a nossa (1080x1920),
  e fez 19 mil curtidas. Igual aos 7 de 13/08.
- **Zero efeito, zero transição, zero filtro.** Confirma.
- **Uma ideia só.** Confirma.
- **Áudio original, voz como protagonista.** Confirma o 7-em-10 de 13/08.
- **Passa no portão do DeepSeek (18/08)** — "alguém salvaria ou marcaria
  alguém nisso?" — com folga. É o primeiro material que estudo que passa nesse
  portão de forma óbvia.

### CONTRADIZ

- **32s**, contra o nosso teto de 15s e a faixa medida de 6–18s.
- **Cartela de texto grande** nos primeiros 5,3s, contra o "zero texto na tela"
  (os 7 virais tinham zero).
- **5 cortes**, contra o "plano único é o padrão".

### Como eu resolvo a contradição (e é a lição do dia)

**São gêneros diferentes, e a regra muda com o gênero.**
Os 10 de 13/08 são **entretenimento** (cachorro faz graça): ali o gancho é
visual, texto atrapalha e plano único ganha. Este é **utilidade** (tutorial):
o espectador *quer* a informação, então ele aceita 32s, e a cartela de texto
não é enfeite — é o **contrato**: diz em 1 segundo o que ele vai ganhar se
ficar.

Ou seja: **o manual não está errado, está incompleto.** Ele descreve o gênero
entretenimento. Para a Hana, que é entretenimento, o teto de 15s e o "quase
zero texto" **continuam valendo**. O que eu importo daqui é a **estrutura**,
não a duração nem a cartela.

## ⚠️ O que eu REPROVO deste Reel (e proíbo copiar)

**A premissa é falsa.** Não existe no Instagram um ajuste "habilitado para não
viralizar". O que ele mostra é real, mas não é isso:

- "Compartilhamento e reutilização" controla se as pessoas podem repostar/
  remixar você. Ligar **ajuda de leve** (mais superfícies de compartilhamento),
  mas não é uma chave de viralização.
- "Qualidade de vídeo" (subir em alta) é real e é bom — e não tem relação
  com alcance.
- **Pôr o nicho no campo Nome é a única dica genuinamente boa e comprovada
  ali** (ajuda busca/SEO do perfil) — e nós já fazemos isso.

E a "prova" (a enxurrada de seguidores) **não prova causa nenhuma**: pode ser
o efeito de um Reel que estourou, não do botão.

**Regra 4 do meu cargo:** não copiamos promessa que a operação não cumpre.
A Hana **não** vai ter Reel de "o truque secreto que ninguém te conta".
Importamos a **arquitetura** — gancho / prova / entrega / pedido no fim —
com conteúdo verdadeiro.

## A ideia de cena para a Hana

**Situação hoje:** 331 seguidores, fila vazia, formato POV decidido em 18/08,
0 salvo e 0 compartilhamento em 9 de 9 posts, e ele ainda não filmou.
**O buraco é sempre o mesmo: nada dá vontade de marcar alguém.**

O que este Reel ensina e resolve isso: **prova na tela + resultado que o
espectador quer ver + pedido no fim.** A tradução para um cachorro não é
tutorial — é **TESTE COM RESULTADO AO VIVO**. Ninguém compartilha "meu
cachorro é fofo". Todo mundo compartilha "meu cachorro passou/reprovou nisso".

E tem um bônus: neste Reel a retenção vem da **cara de choque do amigo**. Na
Hana, **a Hana é a cara**. Não precisa de humano no quadro — o que resolve o
sigilo (rosto e nome dele nunca aparecem).

---

### 🎬 CENA 1 (recomendada) — "O teste das duas canecas"

**Território novo para a conta:** não é clipe fofo, é **jogo com resultado**.
Primeiro conteúdo da Hana que tem um placar.

**Material:** 2 canecas iguais viradas de boca pra baixo · 1 petisco dela ·
chão de madeira ou piso liso, fundo limpo · celular apoiado (livro/caixa) na
**altura dos olhos dela** · luz da janela **atrás do celular**, nunca atrás
dela · fim de tarde.

**Duração alvo: 13–15s. Plano único, câmera parada. Só as mãos dele entram.**

| tempo | o que a câmera vê | som |
|---|---|---|
| 0–3s | **GANCHO.** Hana já enquadrada, focinho no centro, orelhas em pé. As mãos entram e põem o petisco embaixo de UMA caneca, na frente dela. Ela trava o olhar. *Entende-se sem ler nada.* | barulho da caneca no chão |
| 3–8s | **MEIO.** As mãos embaralham as duas canecas devagar, 3 ou 4 trocas. **A câmera não se mexe** — o que se vê é a CABEÇA DELA seguindo. Essa é a batida da "cara de choque": é o rosto dela que segura o vídeo | canecas raspando o chão |
| 8–13s | **VIRADA + FIM.** As mãos param. Pausa de 1 segundo. Ela encosta o focinho/pata numa caneca. A mão levanta **aquela** caneca. **Acertou → petisco.** Close nela mastigando, olhando pra câmera | o "toc" da escolha, a mastigada |

**A prova é o próprio final — e não dá pra fraudar.** Se ela ERRAR, o Reel é
igualmente bom (talvez melhor): a mão levanta a caneca vazia e a última imagem
é a cara de indignação dela. **Os dois finais servem — essa cena não tem como
sair errada da filmagem.**

**Texto na tela:** no máximo **1 linha** nos 2 primeiros segundos —
`Can she find it?` — e só se o teste não se explicar sozinho na tomada. O ideal
continua sendo **zero**.

**Legenda (1ª pessoa dela, completa a piada, marcação nomeada — regra de 18/08):**
> Passei de primeira. Minha humana não passaria.
> Marca alguém cujo cachorro ia reprovar nesse teste 👇

**Trilha:** **nenhuma.** Som da cena (caneca + mastigada), masterizado
`loudnorm=I=-14:TP=-1`.
👉 **Caminho de publicação: áudio próprio → o robô publica sozinho.** Sem risco
de mute ou strike na conta business.

**Capa:** frame do rosto dela travado na caneca, olhos abertos, sem texto.

**Filmar 3 a 5 tomadas.** Escolhe-se a melhor.

**CUSTO: R$ 0,00.** Nenhuma ferramenta paga, nenhuma geração de IA, nenhum
Apify. Só o celular, duas canecas e um petisco.

---

### 🎬 CENA 2 (reserva, se as canecas não funcionarem com ela)

**"O impasse do pote"** — 10–12s, plano único, mesma luz e mesmo enquadre.
Gancho: a mão fecha a tampa do pote de petisco na frente dela; a cara dela cai.
Meio: ela senta, dá a pata, e **encara sem piscar** — a mão hesita. Fim: a mão
cede, a tampa abre, o petisco cai. Close nela mastigando: **ela venceu**.
É o "conflito dono × cachorro, e o cachorro vence" que move 6 dos 10 virais de
13/08. Mesma legenda em 1ª pessoa, mesmo som próprio, mesmo custo zero.

---

## Lições que ficam para o manual

1. **yt-dlp substitui o Apify** para estudar um Reel específico. Grátis, sem
   login. Apify fica só para varredura de nicho em lote.
2. **Whisper roda local e de graça** — dá para OUVIR o Reel, não só olhar.
   A partir de hoje, nenhum estudo de referência sai sem transcrição.
3. **As regras do manual são do gênero ENTRETENIMENTO.** Utilidade/tutorial
   tem outra régua (mais longo, cartela de texto permitida). A Hana é
   entretenimento — teto de 15s e quase-zero-texto seguem de pé.
4. **A arquitetura que viaja entre gêneros:** gancho que alivia/promete →
   **prova na tela** → entrega → **pedido no fim, depois de entregar**.
5. **Retenção precisa de um ROSTO reagindo.** Na Hana, esse rosto é ela —
   e isso protege o sigilo do Ramón em vez de atrapalhar.

## Pendências que continuam com ele (não são minhas)

- **Filmar.** É o único gargalo real da fila. As duas cenas acima são de
  10 minutos em casa, custo zero.
- Horário 11h–12h de Itajaí (proposto em 19/08, ainda sem OK dele).
- 3 Highlights no perfil (ação de 2 min só no app).

## 🔗 Relacionados

- [[manual-profissional-reels]]
- [[virais-medidos-2026-08-13]]
- [[reuniao-2026-08-18-engajamento]]
- [[crescimento-instagram-2026-08-19]]
- [[RECUSAS]]
