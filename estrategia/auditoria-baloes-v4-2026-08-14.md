# Auditoria independente — `baloes-dela-v4-editado.mp4` (14/08/2026)

Auditor: diretor-reels. **Quem construiu não auditou** — refiz todas as medições
no arquivo final, sem aceitar os números de quem montou.
Arquivo: `content/queue/2026-08-19_baloes-dela/baloes-dela-v4-editado.mp4`

> **VEREDITO: NÃO está no padrão de viral medido do nosso nicho.**
> Passa na trava de privacidade (o mais importante) e passa em luz e em texto.
> Reprova em 2 itens do checklist §8 e num terceiro que o checklist ainda não
> media. Detalhe abaixo, com número.
> **Isto não é reprovação definitiva da peça — é o laudo. Quem aprova é o Ramón.**

---

## 1. TRAVA DE PRIVACIDADE — PASSA (checado por mim, quadro a quadro)

Não aceitei a auditoria do `-FINAL.json`. Refiz no `.mp4` final, por três
métodos independentes:

1. Folhas de contato de 1 em cada 3 quadros (72 quadros).
2. Varredura da faixa superior do quadro em **resolução nativa** nos dois cortes
   de risco (onde uma cabeça poderia entrar).
3. Detector de rosto por rede neural (**YuNet/OpenCV**) rodado nos **216
   quadros**, com conferência visual de cada detecção forte.

### 1a. Rosto de terceiro — NÃO APARECE
| corte | tempo | o que aparece de pessoa | veredito |
|---|---|---|---|
| 1 gancho | 0,00–0,93s | pernas, pés, tênis | seguro |
| 2 setup | 0,93–3,30s | pernas, calça, mão, **nuca** do casal sentado | seguro |
| 3 close | 3,30–5,20s | tronco cortado no ombro, braços, mãos, mecha de cabelo | seguro |
| 4 desfecho | 5,20–7,20s | perna e mão segurando a guia | seguro |

- **Momento mais crítico (quadros 22–26, t≈0,73–0,87s):** o casal aparece
  sentado **de costas** — nuca e cabelo. Nenhum olho, nariz, boca, óculos ou
  perfil. Enquadra na definição de seguro da regra.
- **Corte 3 é o mais perto das pessoas.** Confirmei os **57 quadros**: a linha
  de corte do quadro fica no ombro/peito em todos. Nenhuma cabeça entra.
- O detector acusou 79 candidatos com confiança ≥0,70. Conferi os mais fortes
  um a um: **todos são a Hana** (quadros 187–212, 54, 95) **ou falso positivo**
  — o do quadro 150 (t=5,00s, confiança 0,81) é uma **mão com relógio**
  segurando os balões, não um rosto. Zero rosto humano.

### 1b. Notícia da gravidez — NÃO É CONFIRMADA
- **Nenhuma nuvem/explosão de fumaça rosa** em nenhum dos 216 quadros.
- **Zero texto na tela** — nenhuma menção a bebê, gravidez ou família.
- Regra cumprida na letra. **PASSA.**

> ⚠️ **Risco residual que é decisão dele, não minha.** A regra proíbe a fumaça e
> as palavras — e isso está cumprido. Mas o quadro tem **balões rosa + piquenique
> branco + ursinho de pelúcia** (visível nos quadros 14–26) **+ um casal**. Para
> o público dos EUA essa combinação lê como chá revelação, mesmo sem fumaça e
> sem texto. Não reprovo por isso: a regra escrita não proíbe. **Registro para o
> Ramón decidir**, porque é sigilo da família e a decisão é dele.

---

## 2. NÚMEROS QUE EU RECONFERI

| item | alegado | **eu medi** | §8 |
|---|---|---|---|
| resolução / fps | 1080x1920, 30fps | 1080x1920, 30fps, 216 quadros | ok (mas ver §3) |
| duração | 7,2s | 7,20s de vídeo (7,293s de container) | ok (6–18s) |
| variação de brilho | 18,41 | **18,41** (mín 112,64 / máx 131,05 / média 125,42) | **PASSA** |
| loudness | −13,12 LUFS | **−12,03 LUFS** | **REPROVA** |
| pico | −1,64 dBTP | **−0,17 dBTP** | **REPROVA** |
| texto na tela | zero | zero (conferido nos 216 quadros) | **PASSA** |

### 2a. Brilho — confirmado, e é o ponto forte da peça
18,41 de variação, contra teto de 30 do manual e faixa de 10–25 dos virais
reais. Média 125,42, dentro da faixa 110–130. Maior salto entre quadros
vizinhos: 13,5 (t=0,90s, na troca de corte) — imperceptível. **A luz está boa.**

### 2b. Loudness — o número alegado está ERRADO, e o certo reprova
Quem montou leu os campos **errados** da saída do `loudnorm`. No JSON:
- `input_i` / `input_tp` = **o que o arquivo É** → **−12,03 LUFS / −0,17 dBTP**
- `output_i` / `output_tp` = **o que ficaria SE a normalização fosse aplicada**
  → −13,12 / −1,64 (foi isso que foi reportado como se fosse a medição)

Conferi com uma segunda ferramenta independente (`ebur128`), que não tem esse
campo duplo: **I = −12,2 LUFS, true peak = −0,2 dBFS**. Os dois batem.

Contra o §8: alvo −14 ±1 (ou seja, −13 a −15) → **−12,1 está fora por ~0,9 LU**.
Pico tem de ser ≤ −1 dBTP → **−0,2 estoura por 0,8 dB**. **Reprova.**
Bom: é o defeito mais barato de corrigir — **só áudio, custo zero, não mexe em
um único quadro, não exige reconferir rosto.**

> Achado extra: o áudio está a **96 kHz**. Instagram trabalha com 44,1/48 kHz.
> Não é reprova, mas é gratuito e se resolve no mesmo passo.

---

## 3. O QUE NINGUÉM TINHA MEDIDO — e é o mais grave

### 3a. A resolução de 1080x1920 é da embalagem, não da imagem
O bruto `hana_noticia_nova_irma.mov` é **1024x576 — deitado e pequeno**.
O `montar_reel.py` recorta 9:16 (`crop=min(iw,ih*9/16)`), o que sobra
**324x576 pixels reais**. Aí o `aproximar` divide de novo, e só então sobe para
1080x1920:

| corte | aproximar | pixels REAIS usados | ampliação |
|---|---|---|---|
| 1 gancho | 1,5 | 216 x 384 | **5,0x** |
| 2 setup | 2,0 | 162 x 288 | **6,7x** |
| 3 close | 2,4 | **135 x 240** | **8,0x** |
| 4 desfecho | 2,2 | 147 x 262 | **7,3x** |

Os 7 virais medidos são **720x1280 de pixel real**. O nosso tem **135 a 216 de
largura real**, esticado para 1080. A linha do manual §0 que diz
"resolução 1080x1920 ✅ (melhor que a deles)" é **falso positivo** — mede o
arquivo, não a imagem. Sugiro corrigir essa linha do manual.

### 3b. Prova medida: a edição custou 85% da nitidez
Nitidez (variância do Laplaciano) — mesmo bruto, mesmos 4 cortes, mesmos 216
quadros, único fator diferente é o zoom:

| versão | nitidez |
|---|---|
| **v3** (corte cru, sem `aproximar`) | **149,5** |
| **v4** (com o zoom aplicado) | **23,1** |

Por corte na v4: gancho 23,3 · setup 29,1 · **close 16,2** (o pior, é o de 8x) ·
desfecho 22,3.

**Consequência direta para a pergunta do Ramón:** aumentar mais o zoom **não
resolve** o enquadramento — piora. O corte 3 já está em 8x. O trade-off como foi
colocado ("mais zoom resolveria mas exigiria reconferir rosto") é uma escolha
falsa: **não existe zoom a mais para dar.** O problema não é de checagem de
rosto, é de material bruto (filmado deitado, em 1024x576, com a cachorra longe).

### 3c. Quadro vazio — medido
Fração do quadro que é só grama:

| corte | mín | média | máx |
|---|---|---|---|
| 1 gancho | 47,2% | 58,1% | 68,5% |
| 2 setup | 71,4% | **74,0%** | 77,1% |
| 3 close | 31,8% | 40,5% | 43,9% |
| 4 desfecho | 80,5% | **82,3%** | 84,1% |

**O desfecho tem 4/5 da tela de gramado vazio** nos 2 segundos inteiros. No
celular, a Hana é um detalhe no canto.

### 3d. §8 — rosto ausente do 1º segundo → REPROVA
O checklist exige rosto no 1º segundo **e** no desfecho.
- **Desfecho: PASSA.** Dos quadros ~187 a 215 a Hana vem andando de frente,
  boca aberta, rosto visível (detector confirma, confiança 0,88).
- **1º segundo: REPROVA.** Nos quadros 0–29 a Hana está filmada **de costas** —
  vê-se o lombo, a guia e a bunda; a cabeça está virada para baixo/para o lado.
  Conferi nos quadros 5 e 20 em resolução ampliada. **O gancho da peça é a
  traseira da cachorra.** Os 7 virais abrem com a situação legível em 1 segundo;
  este abre com uma imagem que não se lê.

---

## 4. CHECKLIST §8 — placar final

| item do §8 | resultado |
|---|---|
| Variação de brilho > 30 | ✅ passa (18,41) |
| Loudness fora de −14±1 **ou** pico > −1 dBTP | ❌ **REPROVA** (−12,1 / −0,2) |
| Transição, filtro ou zoom artificial | ⚠️ conflito declarado (ver abaixo) |
| Texto na tela com 2+ frases | ✅ passa (zero) |
| Rosto ausente do 1º segundo **ou** do desfecho | ❌ **REPROVA** (falta no 1º seg.) |
| Mais de uma piada / +18s sem virada | ✅ passa (uma piada, 7,2s) |
| 9:16 | ✅ passa |
| **(novo) detalhe real vs. os virais** | ❌ 135–216px reais contra 720px deles |

### Sobre a exceção de acervo (regra 3n-i) — não salva esta peça
Perguntaram se o enquadramento cai na exceção. **Não cai.** A 3n-i autoriza
**multi-corte** em peça de acervo — é sobre montagem. Ela não fala de
enquadramento, de nitidez nem de rosto no 1º segundo. Os itens que reprovam
aqui (som, gancho sem rosto, detalhe real) **não são cobertos por ela**.
O zoom/punch-in fica como conflito declarado sob a 3n-i, e isso eu aceito —
mas não é isso que reprova a peça.

---

## 5. O QUE DÁ PARA FAZER (proposta — não é aprovação)

**Custo de tudo abaixo: R$ 0,00.** Nenhuma ferramenta nova, nenhum gasto.
Regra da casa: **nada é feito sem OK dele.**

**A. Conserta agora, só áudio, não reabre checagem de rosto** ✅ recomendo
Remasterizar para −14 LUFS / −1 dBTP e reamostrar para 48 kHz. Um passo de
ffmpeg, não toca em nenhum quadro, a trava de privacidade continua valendo como
está auditada. Isso apaga 1 dos 2 itens de reprova.

**B. Não aumentar o zoom.** Está medido: já são 5 a 8 vezes de ampliação e a
nitidez caiu 85%. Mais zoom piora e ainda obrigaria a reconferir rosto de novo.

**C. O 1º segundo e o enquadramento não têm conserto nesta peça.** Para abrir com
o rosto dela seria preciso um trecho do bruto onde ela apareça de frente e
perto — e o bruto é 1024x576, deitado, com ela longe. Não existe esse trecho com
qualidade. É limite do material, não de edição.

**D. As duas saídas honestas — escolha dele:**
1. **Subir mesmo assim**, com o áudio corrigido (A), sabendo que é peça de
   acervo abaixo da régua medida — vale como presença, não como aposta de
   alcance; ou
2. **Engavetar** e usar o esforço numa cena feita de propósito pelo manual
   §1–§3 (câmera fixa na altura dela, luz única, 3–5 tomadas, plano único,
   rosto no 1º segundo, filmada em pé 1080x1920). É de lá que sai viral —
   5 dos 7 medidos são plano único de cena forte, sem edição nenhuma.

---

## 6. Nota de processo (para não repetir a bronca dele)
O `post.json` da fila já trazia escrito *"diretor-reels auditou este V4
independente"* **antes de a auditoria existir**. É exatamente a classe de
problema que ele reclamou: afirmação escrita à frente do fato. Sugiro só
escrever "auditado" depois que o laudo estiver no lugar.

---

## Como reproduzir cada número
```
ffprobe -v error -show_entries stream=width,height,r_frame_rate,nb_frames <arq>
ffprobe -f lavfi -i "movie=<arq>,signalstats" -show_entries frame_tags=lavfi.signalstats.YAVG -of csv=p=0
ffmpeg -i <arq> -af "loudnorm=I=-14:TP=-1:print_format=json" -f null -   # ler input_i / input_tp
ffmpeg -i <arq> -af ebur128=peak=true -f null -                          # conferência independente
```
Rosto: OpenCV `FaceDetectorYN` (modelo YuNet, gratuito) nos 216 quadros +
conferência visual das detecções fortes. Nitidez: variância do Laplaciano.
Quadro vazio: máscara HSV de verde (25–75 de matiz).
