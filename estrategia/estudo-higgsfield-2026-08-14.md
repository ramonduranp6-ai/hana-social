# Estudo Higgsfield — o que a ferramenta entrega e o que vale aprender dela (14/08/2026)

Origem: ordem dele — *"Peça para o diretor de reels aprender todas técnicas
usadas pelo higgsfield. Estudem o que o higgsfield retorna de resultado. No
futuro eu quero que vcs criem vídeos e fotos como o higgsfield, mesmo padrão!"*
Primeiro teste real do conector, conta pessoal dele, plano **plus**.

**Todo número aqui é medido** (ffprobe/signalstats no arquivo baixado, ou
preflight `get_cost` da própria API). Onde eu não medi, está escrito que não medi.

---

## 0. Prova de que os números conferem

Antes de escrever qualquer conclusão, reconferi o que foi relatado:

| conferência | resultado | como conferi |
|---|---|---|
| custo do teste | saldo caiu de **110 → 102,5** = exatamente **7,5 créditos** | `balance` agora |
| arquivo entregue | h264, 5,04s, 121 frames, 10,2 Mbps | `ffprobe` |
| identidade da Hana | mantida (cor tri lilac merle, rugas, roupinha, proporção) | li os 5 frames |

O relato estava certo no essencial. **Duas coisas o relato não pegou** — §2 e §3.

---

## 1. O que o Higgsfield RETORNA (o formato do resultado)

- **Job assíncrono**: você submete, recebe um `job_id`, consulta com
  `job_status`/`jobs_wait`. Não trava a conversa.
- **Entrega**: URL do vídeo + URL da thumbnail, ambas em CDN própria
  (`cdn.higgsfield.ai`). Baixar é responsabilidade nossa — **nada fica salvo no
  projeto sozinho**.
- **Cobrança**: em créditos, debitados na hora, com **preflight opcional e
  gratuito** (`get_cost: true` devolve o preço sem submeter nada).
- **Resolução: ele entrega o que o modelo decidir, não o que você pediu.** Ver §2.

### Preços reais medidos hoje (preflight, nada foi gasto)

| operação | créditos | comentário |
|---|---|---|
| `kling3_0` std, 5s, sem som | **7,5** | foi o teste feito |
| `kling3_0` pro, 5s | 8,75 | +17% por qualidade maior |
| `kling3_0` 4k, 5s | 30 | 4x o std |
| `veo3_1` basic, 4s | 11 | |
| **`reframe` 5s → 720p** | **28,5** | ⚠️ |
| **`reframe` 5s → 9:16 1080p** | **51** | ⚠️ **6,8x o custo de gerar o clipe** |
| `upscale_video` | **não dá para saber antes** | a API não aceita `get_cost` nessa ferramenta |

⚠️ **O achado econômico do estudo:** consertar o enquadramento de um clipe de 5s
custa **51 créditos — metade de todo o saldo restante (102,5)** — para um clipe
que custou 7,5 para nascer. **Consertar na pós é economicamente absurdo aqui.**
A correção tem de ser na ENTRADA (§3), e é de graça.

---

## 2. Achado técnico nº 1 — a resolução/fps saiu fora do padrão (confirmado, e a causa é outra)

| | pedido | entregue | padrão do manual |
|---|---|---|---|
| proporção | `aspect_ratio: "9:16"` | **856x1072 = 4:5** | 9:16 |
| fps | — | **24 fps** | 30 fps |
| áudio | `sound: "off"` | **nenhuma faixa de áudio** | master −14 LUFS |

**A causa, medida:** a foto de entrada (`post_oncinha.jpg`) é **1080x1350 = 4:5
exato**. A saída 856x1072 dá 0,798 — ou seja, **o modelo copiou a proporção da
foto e jogou fora o `9:16` que eu pedi**. E não é limitação declarada: `9:16`
está na lista oficial de proporções do `kling3_0`. **É o parâmetro sendo
silenciosamente ignorado quando existe imagem de partida.**

Consequência prática: **em imagem-para-vídeo, quem manda na proporção é a FOTO,
não o parâmetro.** Isso vira regra de operação.

---

## 3. Achado técnico nº 2 — esta foto NÃO tem conserto para 9:16 (e por quê)

Fiz a conta antes de propor qualquer solução:

- Manter a altura (1072) e cortar as laterais para 9:16 → largura **603 px**.
  São **30% da largura fora**. Olhando os frames, o corpo da Hana ocupa quase
  toda a largura: **esse corte decepa as patinhas dela**, que são a graça da foto.
- Manter a largura (856) e completar a altura → precisa **inventar 450 px** de
  cenário (outpaint, pago).
- Cortar a foto original 1080x1350 para 9:16 → sobra **759x1350**, mesmo problema.

**Conclusão honesta: não existe conserto bom, nem de graça nem pago, para este
clipe.** O defeito nasceu antes: a foto-fonte não era 9:16.

**A correção é uma regra nova de captura, custo zero:** *foto que vai ser
animada tem de ser escolhida/cortada em 1080x1920 ANTES de subir.* Isso entra ao
lado do §2 do manual (captura). Depois disso, o upscale 856→1080 e o 24→30 fps
são ffmpeg, de graça, no `montar_reel.py`, que já é o passo final de toda peça.

---

## 4. Achado técnico nº 3 — a luz saiu MELHOR que a dos virais

Esta é a boa notícia, e é a mais importante do estudo. Medi o clipe gerado com o
mesmo `signalstats` que reprova as nossas peças:

| métrica | virais (7) | nossos 3 da fila | **clipe do Higgsfield** | alvo |
|---|---|---|---|---|
| variação de brilho | 10-25 | **80-196 e 68-151** ❌ | **4,27** ✅ | < 30 |
| brilho médio | 112-127 | 108-123 | 133,7 ⚠️ | 110-130 |

**Variação de 4,27 contra um teto de 30.** O clipe gerado é **mais estável de luz
que os próprios virais de 30M de views**, e resolve estruturalmente o nosso maior
defeito medido (80→196). Faz sentido: é um plano único sintético, sem troca de
cômodo, sem mudança de exposição de celular.

O brilho médio 133,7 ficou 3 pontos acima da faixa alvo — defeito pequeno e
corrigível com `eq` no ffmpeg, custo zero.

---

## 5. Achado técnico nº 4 — a identidade se mantém, mas o DETALHE derrete (o relato não pegou isso)

Li os 5 frames. No grosso, o relato está certo: cor tri lilac merle, rugas,
roupinha de oncinha, proporção do corpo — tudo consistente, sem membro extra.
**Mas comparando o frame 1 com o frame 4, há degradação real:**

1. **As patas perdem os dedos.** No frame 1 e 3 as patinhas têm coxim e unha
   definidos. No frame 4 a pata erguida virou **um toco liso, sem dedo nenhum**.
2. **A estampa de oncinha se reorganiza.** As pintas pretas mudam de lugar e
   ficam borradas — não é a roupa se mexendo, é a textura escorregando.
3. **As rugas do focinho amaciam** — ela perde a cara de shar-pei justamente no
   fim, que é onde o manual manda terminar (§3: desfecho no rosto dela).

**Regra que sai daí:** clipe gerado tem prazo de validade curto. **O detalhe
aguenta ~2-3s; aos 5s já derreteu.** E o defeito cai exatamente onde o manual
mais exige qualidade — o rosto no desfecho.

**🔴 Correção pós-entrega — erro mais grave que o §5 original registrou.** O
Ramón viu o clipe e apontou na hora: *"Hana não tem rabo."* O prompt do teste
pedia "tail gives one lazy wag" — eu escrevi isso sem conferir a anatomia real
dela antes de gerar. Isto não é "detalhe que derrete com o tempo" (o defeito do
resto desta seção) — **é o motor inventando uma parte do corpo que ela não
tem**, do início ao fim do clipe. Nem eu nem o diretor-reels pegamos isso
olhando os frames, porque a checagem foi "tem membro a mais/estranho?", não
"esse traço existe nela de verdade?". **Checklist do §8 do manual precisa de
um item novo: conferir cada traço do prompt contra o animal real ANTES de
gerar, não só o resultado depois.** Fato de anatomia registrado em memória
permanente do projeto (Hana é uma Exotic Bully sem rabo — bobtail natural da
raça) para nunca mais entrar num prompt de geração dela.

---

## 6. As técnicas do Higgsfield — quais já temos e quais são NOVAS

O pedido dele foi "criar como o Higgsfield, mesmo padrão". Separei o que é
**método** (dá para copiar de graça) do que é **ferramenta** (custa crédito).

### 6.1 Já existe no projeto (não precisamos deles para isso)

| técnica deles | nosso equivalente | quem ganha |
|---|---|---|
| Workflows com roteiro embutido (10 no catálogo) | **roteiro em JSON do `montar_reel.py`** (`studio/roteiros/*.json`, com piada, origem e batidas) | **empate** — o nosso é mais específico do nicho |
| `virality_predictor` (nota de viralidade) | **auditor com checklist técnico** (§8 do manual) | **nós** — o nosso reprova com NÚMERO MEDIDO; o deles é uma previsão de caixa-preta, sem fonte |
| Pós-produção dedicada em vez de regerar (`reframe`, `upscale`, `deflicker`) | **ffmpeg** (`eq`, `curves`, `vidstab`, `loudnorm`, crop) | **nós** — mesmo princípio, custo zero contra 28-51 créditos |

Vale registrar: o `video_deflicker` deles existe para resolver exatamente o
problema que o nosso manual mede (luz instável). O princípio está certo — mas o
`signalstats` + `eq` do ffmpeg já faz isso por R$ 0.

### 6.2 NOVO — vale adotar como MÉTODO (custo zero, é jeito de trabalhar)

1. **Preflight de custo antes de gastar.** Eles têm `get_cost` em quase tudo.
   Nós hoje geramos e descobrimos o preço depois. **Adotar como regra da casa
   para qualquer geração paga** (Lyria, Gemini, Kairogen): dizer o preço antes,
   e ele autoriza. Casa perfeitamente com a regra 2 (nenhum gasto sem OK dele).
   Nota: nem eles cumprem isso 100% — o `upscale_video` não aceita preflight.
2. **Roteamento explícito por modelo.** Eles têm ~30 modelos de vídeo e uma
   ferramenta (`models_explore`) só para escolher. Nós escolhemos por hábito.
   **Adotar: toda encomenda declara qual motor e por quê, em 1 linha**, antes de
   gerar.
3. **Gerar em lote e escolher a melhor** (`count: 2-4`, `generate_video_batch`).
   Isto é literalmente o §1 do nosso manual — *"filmar 3-5 tomadas, escolhe-se a
   melhor, não a única"*. **Nós pregamos isso para a FILMAGEM e não fazemos para
   a GERAÇÃO.** Incoerência nossa, e o conserto é de graça no método.
4. **Biblioteca de encomendas versionada.** O valor dos presets deles não é o
   efeito — é serem *prompt + parâmetros empacotados, com nome, reutilizáveis*.
   **Nossa versão disso são os nossos roteiros JSON promovidos a modelo
   versionado** ("O TESTE DO MEU HUMANO v5" já tem até histórico de reprovação
   dentro). Copiar a ARQUITETURA deles, nunca o CONTEÚDO deles.

---

## 7. VEREDITO sobre os 62 presets prontos: **NÃO SERVEM. Reprovo.**

Contei o catálogo inteiro: **62 presets**. Motivos técnicos, na ordem:

1. **Todos são EFEITO.** Earth Zoom, Sticker Peel, Action Figure, Kung Fu Hit,
   Ice Statue, Clay Figurine, Red Carpet, Zombie Dance, CGI Breakdown…
   A régua medida dos 7 virais do nosso nicho diz: **efeitos = zero, transições
   = zero, filtro = zero, zoom artificial = zero.** Um preset chamativo não é
   "melhorar o Reel", é **quebrar o único padrão que a gente provou que funciona**.
   O §8 do manual já reprova isso automaticamente: *"Transição, filtro ou zoom
   artificial → REPROVA."* **Um preset entra reprovado de fábrica.**
2. **Foram feitos para SELFIE HUMANA.** As descrições dizem "you", "your
   outfit", "your identical twin", "your grey outfit". São para o rosto de uma
   pessoa. Dos 62, só 3 citam animal (*Animal chase*, *Animal ride*, *Me and pet
   transformation*) — e nesses o animal é acessório de um humano, nenhum tem o
   pet como sujeito. **Zero presets pensados para cachorro sozinho.**
3. **Colidem com a regra de sigilo.** Metade pressupõe um humano em quadro. A
   regra da casa é que o rosto dele nunca aparece.
4. **Colidem com a linha editorial "acervo real".** Transformar a Hana em
   estátua de gelo ou boneco de ação não é a Hana — é outra personagem.

**Sobre os 10 workflows: mesma reprovação, por motivos diferentes.** Os 7 de UGC
exigem criador falando na câmera (sigilo). O `faceless-channel-video` é narrado
com legenda queimada (o manual manda **zero texto na tela**, medido nos 7
virais). O `youtube-thumbnail-generator` seria o único adjacente — mas a nossa
capa é **frame do rosto real dela** (§6), não capa gerada.

> **O que presta no Higgsfield não é o catálogo. É o motor cru de
> imagem-para-vídeo, sem preset nenhum** — que foi exatamente o que o teste usou,
> e foi acerto de método.

---

## 8. Onde este motor TEM uso legítimo, e onde NÃO tem

### Pode (sem violar o manual)

- **Dar vida sutil a uma foto real da Hana, em trecho de 2-3s, dentro de peça de
  acervo.** A linha editorial "acervo real" se mantém porque a partida é uma foto
  real da cachorra real. E a estabilidade de luz medida (4,27) é melhor que a do
  material filmado no celular.
- **Capa/primeiro frame com micro-movimento** — respeitando o §6 (rosto dela,
  olhos abertos).
- **Salvar material antigo bom mas parado**: foto ótima que nunca virou Reel
  porque não tinha vídeo.

### Não pode

- **Encenar uma cena que nunca aconteceu.** O manual inteiro diz que o viral
  nasce na **encenação real** (§1) e na piada dono × Hana. Fabricar a Hana
  fazendo algo que ela não fez é a mesma família de proibição de inventar
  depoimento de cliente. **Reprovo por princípio, não por qualidade.**
- **Corpo principal da peça.** Pelo §5: o detalhe derrete depois de ~3s, e
  derrete no rosto — que é onde o desfecho tem de estar.
- **Peça que dependa do som da cena.** O clipe sai **mudo**. Em 7 dos 10 virais
  o som da cena é o protagonista. Clipe gerado não tem cena para soar.
- **Sem declarar que é IA.** Regra do cargo: alegação de trabalho manual sem
  declarar IA é motivo de reprovação.

---

## 9. Comparativo com Gemini/Flow (regra 3j-i, já pago)

**Limitação declarada, para não inventar:** eu **não** rodei a mesma foto no
Gemini/Flow nesta sessão. A coluna do Flow abaixo é capacidade declarada + o uso
que o projeto já faz; **só a coluna do Higgsfield é medida hoje.** Confiança:
alta no Higgsfield, média no Flow.

| critério | Higgsfield (medido) | Gemini/Flow (não medido hoje) |
|---|---|---|
| fidelidade da identidade | **boa no grosso, derrete no detalhe** a partir de ~3s (patas, estampa, rugas) | histórico do projeto: bom em foto, vídeo pouco testado com a Hana |
| controle de movimento | **alto** — prompt movimento a movimento funcionou (piscar, virar a cabeça) | menor controle fino pelo app |
| controle de proporção | **falhou** — ignorou o `9:16` pedido e copiou a foto | app entrega 9:16 do jeito que se pede |
| estabilidade de luz | **4,27 — melhor que os virais** | não medido |
| som | nenhum | Veo gera som nativo |
| custo | **7,5 créditos/clipe de 5s**, saldo finito de 102,5 | **já pago** no plano dele — custo marginal zero |
| facilidade | roda dentro da conversa, sem ele mexer em nada | exige ele abrir o app e operar |

**Leitura honesta:** o Higgsfield ganha em **controle** e em **não consumir o
tempo dele** (ele comanda, não executa). O Flow ganha em **custo marginal zero**
e em **proporção correta**. Com 102,5 créditos, o Higgsfield dá para **~13
clipes de 5s** e acabou — não é ferramenta de rotina, é de peça especial.

---

## 10. PROPOSTA (esperando OK dele — não é decisão)

**Não decidi adotar nada.** O que eu recomendo, em ordem:

1. **Adotar de graça, hoje, sem gastar 1 crédito — as 4 técnicas de MÉTODO do
   §6.2** (preflight de custo, roteamento por modelo declarado, gerar em lote e
   escolher a melhor, biblioteca de encomendas versionada). É aqui que mora o
   "mesmo padrão do Higgsfield" que ele pediu. **Não depende de assinatura
   nenhuma.** ← *é a parte que eu mais recomendo*
2. **Adotar a regra de captura nova:** foto que vai virar vídeo é escolhida em
   **1080x1920 antes de subir**. Custo zero, resolve o defeito do §2/§3 na raiz.
3. **Higgsfield NÃO vira ferramenta oficial de rotina.** Vira **motor de exceção**
   para trecho curto (2-3s) de peça de acervo, com os 62 presets **proibidos** e
   uso sempre declarado como IA. Motivo: saldo finito, sem som, e o detalhe
   derrete.
4. **Não gastar os 51 créditos em `reframe`.** É metade do saldo para consertar
   um clipe de 7,5. Se ele quiser um teste em 9:16 de verdade, o certo é
   **regerar a partir de uma foto 9:16 por 7,5 créditos** — 7x mais barato.
5. **Se ele quiser comparação de verdade com o Flow**, eu preciso do OK para
   gastar mais ~7,5 créditos rodando a MESMA foto (já cortada em 9:16) e comparar
   lado a lado com o que o Flow entrega. Sem esse teste, o §9 continua sendo meia
   medida.

**Nada foi publicado, a fila não foi tocada, `DECISOES.md` e `PROXIMA-CONVERSA.md`
não foram alterados. Gasto nesta sessão: zero** (todos os preços do §1 vieram de
preflight gratuito).
