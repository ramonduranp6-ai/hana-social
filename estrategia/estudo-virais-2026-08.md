# Estudo de virais — reels de pet, jul/ago 2026

Motivo: os 5 reels de 14-24/08 foram reprovados por ele ("Muito fraco... pegar
referência dos principais virais do mês"). Ver `content/queue/2026-08-14_a-patroa-mimada`,
`.../2026-08-17_golden-hour`, `.../2026-08-19_a-noite-dela`,
`.../2026-08-21_dona-da-casa`, `.../2026-08-24_travesseiro` (todos `status: rejected`,
commit `d30bbe1`).

**Declaração de limite (regra 0 do cargo):** não existe ranking oficial de reels
por API, e Apify tem mensalidade (fere a regra de custo fixo zero da casa). Este
estudo foi montado com WebSearch (blogs de marketing/agência sobre práticas 2026)
e uma consulta ao Grok (IA-Hub, sem dados ao vivo de ago/2026 — ele mesmo avisou).
Nenhuma mecânica aqui vem de eu ter visto o reel específico rodando; são padrões
reportados por terceiros. Marcado item a item.

## PARTE 1 — Mecânicas (máx. 6, as que cabem em conta pequena e sem orçamento)

**M1 — Gancho de interrupção de padrão, 0-1,5s.** Close extremo (olho, pata, um
objeto fora do lugar) + texto grande que quebra a expectativa do que é "vídeo de
cachorro". Não é intro, é corte seco na cena mais forte. **[não verificado —
fonte secundária, sem link de post real]**
https://www.opus.pro/research/best-video-hooks-instagram ·
https://www.marketingblocks.ai/50-viral-hook-templates-for-ads-reels-tiktok-or-captions-2026-frameworks-examples-ai-prompts-included/

**M2 — Estrutura setup → virada em 7-15s.** Duas ou três batidas, não lista:
mostra uma coisa, uma coisa muda. Vídeos de pura viralidade ficam curtos
(7-15s); vídeo de valor/tutorial é que vai a 30-45s — não é o nosso caso.
**[não verificado — agregador de blogs]**
https://miraflow.ai/blog/how-to-go-viral-2026-what-actually-works-across-platforms ·
https://www.dinneroz.net/2026/05/how-to-go-viral-instagram-reels-2026.html

**M3 — Trava de direito autoral (regra do cargo, não achismo).** O acordo Meta
+ gravadoras cobre uso pessoal; conta business só pode Meta Sound Collection ou
áudio próprio. Isso significa: se a peça depender de áudio de tendência, ela sai
do robô e vai pelo app, na mão. **[fonte: documentação oficial da Meta, já
registrada em `content/benchmark-tecnico.md` do projeto — verificado]**

**M4 — Desfecho que puxa comentário, não CTA de seguir.** Pergunta direta
("does yours do this?"), "marca alguém" ou uma virada com efeito surpresa no
último segundo rendem mais comentário/compartilhamento do que pedir para seguir
— o algoritmo já despreza bait óbvio. **[não verificado — blog de marketing]**
https://www.socialmon.ai/blog/60-viral-reels-hooks-with-examples-that-stop-the-scroll ·
https://gradezilla.org/viral-reels-how-to-make-a-reel-go-viral-in-2026/

**M5 — A onda de vídeo de pet gerado por IA (Veo/Gemini).** Está bombando humor
absurdo/hiper-realista: bicho "falando" com boca sincronizada, cenário
impossível (escritório, tribunal, "se meu cão fosse humano"), vilão bobo tomando
vida. O que prende é humor seco + zero cara de plástico. **[não verificado —
matérias de imprensa de tecnologia, sem visualização própria dos vídeos]**
https://www.tomsguide.com/ai/ai-image-video/ai-cat-videos-are-suddenly-everywhere-heres-why-the-internet-cant-stop-watching ·
https://tech.yahoo.com/ai/articles/feed-suddenly-full-ai-cat-142209489.html

**M6 — Final em loop, sem CTA.** Terminar num frame que reconecta com o início
(mesma pose, mesmo objeto) prende replay e sobe watch-time sem gastar segundo
extra de roteiro. **[opinião — citado pelo Grok, ele mesmo avisou que não tem
dado ao vivo de agosto/2026, tratar como hipótese razoável, não fato]**

**Descartado por não caber em conta pequena:** publicar 4-7 vídeos por dia
(volume citado para operação com equipe de IA em escala) — incompatível com a
régua de 3 reels/semana e com custo zero.

## PARTE 2 — 3 conceitos (roteiro batida a batida)

Nenhum repete pilar+desfecho de post já publicado ou já reprovado. Legenda
sempre PT-BR terminando em pergunta (regra da casa); **texto na tela em inglês,
público EUA — pedido explícito desta tarefa; se ele preferir PT-BR na tela, é
só avisar.** 5 hashtags — acima do teto interno de 4 do projeto; fica marcado
para o diretor-redes bater o martelo, não é decisão minha.

---

### CONCEITO 1 — "A PLACA DA CASA" · pilar A PATROA MANDA · 100% real, sem IA

**Gancho (0-1,2s):** close no cartaz de papel escrito à mão "HOUSE RULES" preso
na parede, ela cheirando o cartaz por baixo. Texto: **"THE RULES"**.

| corte | tempo | o que mostra |
|---|---|---|
| 1 | 0,0-1,2s | close no cartaz "HOUSE RULES" + texto entra |
| 2 | 1,2-3,2s | punch-in: cartaz desce, revela ela sentada, cara de paisagem |
| 3 | 3,2-5,8s | clipe real: ela no sofá — regra "no sofa" riscada, zoom no rabisco |
| 4 | 5,8-8,2s | clipe real: ela na cama dele — regra "no bed" riscada |
| 5 | 8,2-10,8s | **virada**: ela comendo do prato dele — regra riscada, trilha sobe, corte acelerado |
| 6 | 10,8-13,2s | plano largo: ela no meio do sofá, dona da casa. Texto: **"MY RULES NOW"** |
| 7 | 13,2-15s | desfecho/loop: ela derruba o cartaz com a pata → volta pro frame do corte 1 |

**Acervo:** já existe (sofá, cama, comida — dos 25 clipes garimpados). **Precisa
filmar:** o cartaz "HOUSE RULES" escrito à mão, close nele, e ela derrubando/
mordendo no fim — cena nova, pedir ao Ramón.
**Trilha:** própria (Lyria 3, instrumental, tema cachorro-traquina), cresce no
corte 5. **Publica sozinho pelo robô** (trilha própria, sem áudio de terceiro).
**Legenda:** "Fiz uma placa de regras. Ela leu, entendeu e decidiu que as regras
são dela agora. Sua casa também tem dono disfarçado de cachorro?"
**Hashtags:** #exoticbully #bullymicro #trililacmerle #dogsofinstagram #dogmomlife
**Capa:** frame do cartaz com ela ao fundo. **Mecânica:** M1 + M2 + M6.
**Custo:** ~R$0,04 (Lyria) — precisa do seu OK para gastar.

---

### CONCEITO 2 — "O QUE ELA FAZ QUANDO A PORTA FECHA" · pilar MICRO NO APÊ ·
**híbrido: real + trecho gerado no Gemini**

**Gancho (0-1s):** close na maçaneta girando + som da porta fechando. Texto:
**"DOOR CLOSES..."**.

| corte | tempo | o que mostra |
|---|---|---|
| 1 | 0-1,0s | close na maçaneta/porta fechando + texto entra |
| 2 | 1,0-3,0s | real: ela olhando fixo pela fresta, orelhas em pé |
| 3 | 3,0-4,3s | **virada visual**: zoom no olho dela → transição pro trecho de IA |
| 4-5 | 4,3-9,0s | **IA (Gemini/Flow)**: ela "rainha da casa", óculos escuros, petisco deslizando até ela, luz de festa suave. Texto entra: **"5 MINUTES LATER"** |
| 6 | 9,0-11,0s | som de chave → corte seco de volta ao real, ela já "resetada", pose inocente |
| 7 | 11,0-13,3s | real: porta abre, ele entra, ela corre rosto na câmera, rabo abanando |
| 8 | 13,3-15s | desfecho: still do olhar de canto de olho pra câmera. Texto: **"HE'LL NEVER KNOW"** |

**Acervo:** nenhuma cena exata confirmada no acervo atual — **precisa pedir 2
cenas novas**: (a) porta fechando + ela olhando pela fresta, (b) porta abrindo +
ela recebendo, rosto na câmera.
**Prompt de vídeo (Gemini/Flow, app pago dele, NUNCA API, qualidade premium),
em inglês:**
> Cinematic vertical video (9:16), soft golden interior lighting. A small
> Exotic Bully puppy with a tri-color lilac merle coat (blue-grey mottled fur,
> white chest, tan points) — same face and markings as the reference photo —
> reclines regally on a cream sofa like royalty, wearing tiny black sunglasses.
> A small plate of treats slides gently toward her across a coffee table. Soft
> disco light flickers in the background, confetti drifts lazily. Smug,
> satisfied expression. Slow dolly-in, shallow depth of field, warm color
> grade, family-friendly comedic tone, no dialogue, no scary elements, keep
> her exact facial features and coat pattern consistent with the reference
> image. ~5 seconds, loopable feel.

**Trilha:** própria (Lyria, tema brincalhão/glamour), cresce na transição pra
IA. **Publica sozinho pelo robô.**
**Legenda:** "Ele acha que ela fica esperando na porta. Ela tem outros planos.
Sua casa também vira outra coisa quando ninguém tá olhando?"
**Hashtags:** as mesmas 5 do conceito 1.
**Capa:** frame dela olhando séria pela fresta da porta.
**Mecânica:** M5 + M1 + M4.
**Custo:** ~R$0,04 (Lyria) + geração no plano Gemini que ele já paga (sem custo
extra) — precisa do seu OK pra gastar o da trilha e pra rodar a geração.

---

### CONCEITO 3 — "O ASPIRADOR GANHOU VIDA" · pilar INIMIGOS DA PATROA ·
**híbrido: real + trecho gerado no Gemini**

**Gancho (0-1,2s):** close no aspirador ligando sozinho. Texto: **"ENEMY
SPOTTED"**.

| corte | tempo | o que mostra |
|---|---|---|
| 1 | 0-1,2s | close no aspirador ligando + texto entra |
| 2 | 1,2-3,0s | real: rosto dela, orelhas em pé, olhando fixo (rosto obrigatório) |
| 3 | 3,0-4,5s | **virada visual**: zoom no aspirador → transição pra IA |
| 4-5 | 4,5-8,0s | **IA (Gemini/Flow)**: aspirador ganha "olhos" de desenho, avança bamboleando, tom de vilão bobo de filme infantil, nunca assustador de verdade |
| 6 | 8,0-9,5s | corte seco de volta ao real, no instante exato do "ataque" |
| 7 | 9,5-12,0s | real: ela late e avança, aspirador tomba/desliga |
| 8 | 12,0-14,0s | desfecho: ela senta de costas pro aspirador, peito estufado. Texto: **"CASE CLOSED"** |

**Acervo:** **precisa pedir cena nova** — ela encarando o aspirador ligado, e
depois ela latindo/empurrando o aspirador desligado (com segurança: sem ela
perto da mangueira ligada).
**Prompt de vídeo (Gemini/Flow), em inglês:**
> Cinematic vertical video (9:16), playful children's-movie tone, bright and
> colorful lighting, NOT scary. A household vacuum cleaner comes comically to
> life: two big cartoonish googly eyes appear on its body, it wobbles forward
> in an exaggeratedly clumsy, non-threatening way, like a silly villain from a
> kids' cartoon. Warm color palette, comic orchestral sting feel. In frame, a
> small Exotic Bully puppy with tri-color lilac merle coat (blue-grey mottled
> fur, white chest, tan points, same face as reference image) watches alert,
> ears up. Low angle, slight camera shake for comic tension, family-friendly,
> whimsical, no gore, no real fear, cartoon-villain aesthetic. ~4 seconds.

**Trilha:** própria (Lyria, tema tenso-cômico), cresce na transição IA→real.
**Publica sozinho pelo robô.**
**Legenda:** "Ela tem um inimigo declarado dentro de casa: o aspirador de pó.
E ele já sabe quem manda. O seu também tem um vilão particular?"
**Hashtags:** as mesmas 5.
**Capa:** frame dela latindo pro aspirador, boca aberta, ação.
**Mecânica:** M5 + M4 + M2.
**Custo:** ~R$0,04 (Lyria) + geração no plano Gemini (sem custo extra) —
precisa do seu OK.

## O que não é meu nesta entrega
Horário, hashtag final e formato → diretor-redes. Geração de imagem/vídeo em si
(execução da câmera, ranking de ferramenta) → diretor-visual. Preço/margem →
fora de escopo (não há produto).

## 🔗 Relacionados

> Ligações geradas automaticamente por `tecer-vault-obsidian.py` a
> partir das citações que já existiam no texto acima.

- [[benchmark-tecnico]]
