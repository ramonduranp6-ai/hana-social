# Pacote da semana — Reel-slideshow de teste

Criado pelo **Diretor de Criação** em 01/08/2026, a pedido do Ramón
(*"vamos medir um slide show, mas que seja legal né, voce tinha feito um muito
ruim, por isso barrei, use seu diretor de criatividade"*).

⚠️ **NÃO APROVADO.** Quem cria não aprova (regra 3i / 3n). Este pacote vai para o
**auditor de mídia** antes de chegar ao Ramón.

---

## Peça 1 — `era-pra-ser-meu-cachorro`

### Conceito
A história de como o dono perdeu a casa: a Hana chegou cabendo na mesa do
restaurante, foi tomando a cama, depois o sofá inteiro, e hoje o Ramón é
funcionário dela. **Pilar: A PATROA MANDA.**

### Hipótese em teste
Slideshow **com virada narrativa e desfecho** gera salvamento/compartilhamento —
coisa que as 4 fotos paradas não geraram (0 salvo, 0 compart., 0 seguidor, alcance
médio 47). O que se mede em D+1: **salvos e compartilhamentos**, não curtida.

### Roteiro foto a foto

| # | Arquivo (em `02 - selecionadas`) | Frames @30fps | Duração | Papel na história |
|---|---|---|---|---|
| 1 | `garimpo_23_08211450-26dd-468e-a477-7b093d72ccf6.jpg` | 61 | 2,034s | Filhote minúscula na mesa — o "antes" |
| 2 | `garimpo_09_0440D040-DD38-40D4-965A-C0D0B1DF00F6.jpg` | 46 | 1,525s | Cresceu e encara a câmera — o aviso |
| 3 | `garimpo_03_09B1EFB1-20A5-4300-B4B5-EAE4400C3FBF.jpg` | 30 | 1,017s | Adulta instalada na cama — 1ª conquista |
| 4 | `garimpo_14_06bae585-c1d3-4b7c-bcdb-ebd79a657435.jpg` | 30 | 1,017s | Esparramada no sofá inteiro — escalada |
| 5 | `13_IMG_3306.jpg` | 92 | 3,051s | Ela de cara amarrada, o dono sorrindo — desfecho |

**Total: 259 frames = 8,63s.** A ordem é escalada, não álbum: cada slide entrega
mais território para ela e menos para ele. Os cortes **aceleram** (2,0 → 1,5 →
1,0 → 1,0) e param no desfecho (3,0s), que é onde a piada precisa respirar.

### Gancho (1ª tela, sobre a foto 1)
```
ERA PRA SER
MEU CACHORRO
```
24 caracteres, 2 linhas. Arial Bold **96px** (hoje o script usa 62).
Medido: 655px e 804px de largura em 1080 — não vaza.
Posição: **16% do topo** (y≈307). Na foto 1 o topo é o mural, então não cobre o
rosto dela.

### Textos de apoio (terço inferior, y≈1450, Arial Bold 66px)
- Foto 2: `aí ela cresceu`
- Foto 3: `e tomou a cama`
- Foto 4: `e o sofá inteiro`
- Foto 5: `eu virei o mordomo`

Conferido foto a foto: em 2, 3, 4 e 5 o terço inferior é corpo/almofada/ombro —
**nenhum texto cai em cima do rosto dela**.

### Legenda
> Ela chegou em casa cabendo na palma da mão.
> Hoje ela tem a cama, o sofá e um funcionário de tempo integral — eu.
> Não lembro de ter assinado esse contrato.
> Em que momento você acha que eu perdi o controle?
>
> #exoticbully #microexoticbully #bullybrasil #trililacmerle

A pergunta final **não exige ter cachorro** para responder (correção pedida no
plano da semana: 6 de 9 legendas faziam isso) e **não repete a piada de dinheiro**.

### Trilha
**`content/trilhas/03-comico-pizzicato.mp3`**, do segundo 0 ao 8,63.

Por que combina com a cena: pizzicato cômico é o som universal de "pequeno
trambiqueiro armando um plano" — é literalmente a trilha de alguém tomando a
casa aos poucos, que é a história do Reel.

Medido (não deduzido do nome): 118 batidas/min, 4,7 ataques/s — a mais
percussiva das quatro faixas disponíveis, a única com pontuação suficiente para
cortar em cima da batida. O segundo 0 é o pico de energia da faixa (rms 0,267),
então o Reel abre no ponto mais forte dela.

Descartadas: `musica_hana.wav` (15,5s, 1,4 ataque/s, rms 0,098 — é ambiente,
é exatamente o "arrastado" que estragou o anterior); `02-lofi-sofa` (lo-fi =
vibe adulta, barrada pela 3e-i); `01-fofo-ukulele` (fofo, mas liso demais para
piada com desfecho).

⚠️ Regra 3g: ele **precisa ouvir**. O Reel vai ao Telegram já com a trilha
montada — não mandar o nome da faixa e pedir decisão.

---

## Receita técnica — mudanças pedidas em `studio/gerar_reel.py`

1. **Duração por foto vira lista, não constante.** Trocar `DUR = 4` por
   `frames=[61,46,30,30,92]`. É o que mata o "4s parado por foto".
2. **Acabar com o `xfade`.** Todos os cortes são secos (concat), batendo no BPM
   118 medido. Fade de 0,8s repetido 4x é o que deixou o anterior mole.
3. **Movimento de câmera alternado, um por slide** (hoje é o mesmo zoom-in em
   todos):
   - 1: push-in lento `1.00→1.06`
   - 2: **pull-back** `1.10→1.00` (soco, revela a cabeça inclinada)
   - 3: push-in rápido `1.00→1.08`
   - 4: **zoom-out** `1.12→1.00` — *este é o que conta a piada*: abrindo, revela
     que ela ocupa o sofá inteiro
   - 5: push-in lento `1.00→1.05` (assenta no desfecho)
4. **Texto em TODAS as fotos**, não só na 1ª. Assinatura vira
   `preparar(caminho, destino, texto, posicao)`, com `posicao='topo'` (y=0,16·H)
   para o gancho e `posicao='baixo'` (y≈1450) para os apoios. Manter o texto
   assado no PIL (drawtext do ffmpeg com acento + caminho do Windows é dor de
   cabeça conhecida).
5. **Tarja escura translúcida atrás do texto** (retângulo preto ~55% alpha com
   16px de folga). O mural da foto 1 e o sofá da 4 são fundos ruidosos.
6. **Áudio.** Entrada nova `-i 03-comico-pizzicato.mp3`, `-t 8.633`,
   `afade=out:st=8.13:d=0.5`, `-c:a aac -b:a 128k -shortest`. Hoje sai mudo.
7. **Sem fade-in na abertura**: o gancho tem que estar legível no frame 0.
8. `exif_transpose` **já está certo** — conferido: `garimpo_01/03/09` têm
   `orient=6` e giram sozinhas. Não mexer.

---

## Fotos que olhei e recusei (com o motivo)

- **`garimpo_02` e `garimpo_19`** (as duas "Hana filhote" que o briefing sugeriu
  como forte apelo): **não entram.** Olhei — é a Hana **internada**, de cone,
  com acesso venoso e a pata enfaixada. Apelo emocional existe, mas é de
  cachorro doente: quebra o tom "criança e cachorro, leve e engraçado" (3e-i) e
  transforma um susto de saúde em isca de engajamento. Se o Ramón quiser contar
  essa história um dia, é decisão dele e é outro post, com outro tom.
- **`garimpo_20`**: a Hana **de costas**, rosto nenhum no quadro — é o defeito
  exato que reprovou os 12 vídeos do acervo.
- **`12_IMG_3199`** (elevador): a cabeça dela fica escondida atrás do celular.
  A composição do dono agachado é ótima, o rosto dela não aparece.
- **`garimpo_01`** (praia): boa, mas a mão do dono aperta o focinho dela —
  contradiz "ela manda".
- **`contact_sheet nº 9 e 10`**: mesmo passeio, uma é quase a outra (risco de
  repetida dentro do próprio lote).

## Pendências honestas (não conferi)

- **Não abri o perfil no Chrome** para comparar cena a cena com os 38 posts
  (regra 2c). Trabalhei com a lista de "já usadas" que veio no briefing.
- **Não ouvi as faixas** — não consigo. A escolha é por medição (BPM, densidade
  de ataques, energia), não por audição. Por isso a regra 3g vale dobrado aqui.
- Este Reel tem o Ramón no slide 5: **não entregar à parceria Canecas** (regra 5).
