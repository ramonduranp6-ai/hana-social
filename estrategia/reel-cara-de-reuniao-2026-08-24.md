# Reel "cara de reunião" — 24/08/2026

**Peça:** `content/queue/2026-08-26_cara-de-reuniao/` · **status `pending`** (só
ele aprova) · agendada para **qua 26/08, 14:00Z** · **custo R$ 0,00**.

---

## 1. Por que esta peça existe

A fila estava em **0 posts futuros desde 23/08**. A cena encenada pedida a ele
(`content/pedido-de-cena.md`) não foi filmada, e a varredura de 21/08 já tinha
concluído que o acervo bruto **não serve para um POV encenado** — falta
conflito e desfecho, e o único clipe tecnicamente aprovável até então
(`garimpo/84E10F1E`) tem luz estourada.

A saída veio da mudança de abordagem do **Kimi K3** (liderança de estratégia
deste projeto desde 21/08), relendo o benchmark medido em 13/08:

> A piada não precisa estar **encenada no vídeo**. Ela pode morar na **legenda**.
> O vídeo só precisa ser **prova**: a Hana visível, contínua, 6-18s, com uma
> expressão que sustente qualquer legenda-julgamento.

Isso o acervo tem. Esta é a **primeira peça montada nesse formato**.

## 2. Como escolhi o clipe

O garimpo do rolo de câmera terminou uma rodada em 24/08 18:50 e reordenou o
top-30. Dos 30, **7 são vídeo**. Medi os 7 com ffprobe e olhei frame a frame:

| # | arquivo | dur | resolução | veredito |
|---|---|---|---|---|
| **1** | **E5DBFA8E** | **17,3s** | **1080x1920 nativo** | **ESCOLHIDO** — ela sob a cadeira encarando a lente o tempo todo, sem pessoa, sem outro cão, luz estável |
| 2 | B9E89AD8 | 26,2s | 1080x1920 | perna humana entra no quadro em 3 trechos; ela anda **de costas** na maior parte |
| 5 | A5077980 | 30,7s | 1080x1920 | mão humana com relógio no desfecho; pelagem não bate com a da Hana nos frames medidos |
| 8 | 1907544a | 10,0s | **474x850** | resolução baixa demais |
| 9 | 7DDBC71C | 18,8s | 1080x1920 | câmera solta, borrão de movimento, pé no quadro, ela quase sempre de barriga pra cima |
| 20 | F1167E60 | 4,7s | 1080x1920 | **curto demais** (piso é 6s) |
| 26 | 84E10F1E | 7,5s | 1080x1920 | o já reprovado em 21/08 — nitidez 102, a pior das 7 |

**Ganho técnico inédito:** o E5DBFA8E é **1080x1920 nativo a 9,85 Mbps**. Todas
as peças anteriores partiam de bruto de 576 px reais e saíam macias por
ampliação — foi exatamente a reclamação dele em 14/08 ("a qualidade do vídeo
parece estar bem ruim"), registrada como teto do material na auditoria da
chegada-eloen. **Este clipe não tem esse teto.**

**Confirmação de identidade:** o detector do garimpo sabe dizer "é um cachorro",
não "é a Hana". Conferi à mão contra duas fotos já publicadas
(`2026-07-23_olhar-no-tapete` e `2026-07-29_lilac-ao-sol`): mesma mancha branca
descendo o focinho, mesmos olhos claros, mesmo nariz lilás. É ela.

## 3. A montagem

**Plano único, 7,71s, um corte só, zero texto, zero transição, zero zoom de pós.**

- **Janela 1,70 → 9,40 do bruto.** O clipe abre num plano geral da sala (ela
  minúscula do outro lado) e o celular faz um *push-in* in-camera que só pousa
  em close por volta de 1,5s. Começar em 1,70 garante o **rosto legível no
  primeiro frame** — item de reprovação do checklist. Fim em 9,40 porque em 9,6
  a câmera trombou (borrão) e em 10,2 a moldura inclina e entra teto no quadro.
- **O movimento é do material, não meu.** Dentro da janela o push-in continua e
  ela cresce sozinha até o fim — o mesmo recurso do viral de 4,8M ("fecha no
  rosto no fim"). Não acrescentei nenhum movimento em pós.
- **Desfecho:** o único movimento dela na peça inteira é o **ladeio de cabeça**
  que começa aos 6,7s e segura até o último frame, olhando na lente.

## 4. Som — e por que está mudo

O áudio original tem **voz humana em rajadas do começo ao fim**. Confirmado por
espectrograma: pilhas harmônicas de 200-2000 Hz, mais densas entre 10,5 e 14s.

Não consigo ouvir aqui o que é dito nem de quem é a voz. Publicar às cegas fere
o sigilo do projeto e a regra de "sem pessoa terceira". Somado a isso, o bruto
já estava em **-19,2 LUFS**, fora do padrão de qualquer jeito.

**Decisão: mudo, com trilha própria.** Se ele ouvir o arquivo original e
liberar, a peça se refaz com som real em minutos (é uma linha no roteiro).

**Trilha escolhida por medição, não de ouvido.** RMS a cada 0,1s da
`03-comico-pizzicato` (Lyria 3, já paga, custo R$ 0,00): a faixa sobe até um
**pico em 17,00-17,10s (-10,2 dB)** e despenca logo depois (-17,5 / -22,5 /
-26,0), com quase-silêncio em 17,9-18,2s. Entrando em **10,20s** (um vale de
-20,4 dB, para não cortar frase no meio), o pico cai em **6,85s da peça — em
cima do ladeio de cabeça** — e a queda deixa o final quase sem música, com ela
parada olhando. Sting cômico + silêncio, no lugar de cama de fundo genérica.

## 5. Conserto de ferramenta feito nesta sessão

`studio/montar_reel.py` ganhou a opção **`gamma`** por corte.

O script só tinha `clarear` (que **só** levanta sombra — valor negativo era
ignorado em silêncio pelo guarda `> 0.001`) e `cinema` (que escurece, mas junto
com vinheta, proibida pela §4 do manual). Faltava o meio-termo que a §4
**autoriza**: grading leve e uniforme, sem nada estiloso junto.

É gamma puro, sem mexer em saturação, de propósito — para não adulterar a cor
tri lilac merle, que é item de reprovação do checklist. Vale para toda peça
futura. Aqui `gamma: 0.94` levou o brilho médio de **135,6 (fora da faixa) para
130,6 (dentro)**.

## 6. Auditoria — checklist §8 do manual, item a item

| item | medido | veredito |
|---|---|---|
| variação de brilho (teto 30) | amplitude **16,52** · desvio **3,57** | PASSA — melhor número já medido no projeto |
| loudness (-14 ±1 LUFS) | **-14,01** | PASSA |
| pico (reprova se > -1 dBTP) | **-2,60 dBTP** | PASSA |
| transição / filtro / zoom artificial | nenhum; só gamma 0,94 (§4 autoriza) | PASSA |
| texto na tela (máx. 1 frase) | **zero** | PASSA |
| rosto no 1º segundo e no desfecho | presente nos dois, na lente | PASSA |
| 1 piada só, < 18s, com virada | 7,71s, virada aos 6,7s | PASSA |
| anatomia, tri lilac merle, 9:16, repetição | real sem IA, 1080x1920, saturação intocada, bruto inédito | PASSA |

### **VEREDITO: SEM OBJEÇÃO.**

**Três observações declaradas — nenhuma é reprovação:**

1. **Brilho médio 130,63** fica dentro da faixa 110-130 mas **no teto dela**, e
   acima dos 7 virais medidos (112-127). A origem é o cômodo (piso e parede
   brancos, luz de dia), não erro de edição. YMAX 227 e YMIN 12 confirmam que
   não há estouro nem esmagamento.
2. **Pico -2,60 dBTP** deixa 1,6 dB de folga sem usar. O loudness integrado
   bateu o alvo exato, então não há o que corrigir sem arriscar o pico
   verdadeiro do AAC — tentativa manual disso já falhou em 14/08 e está
   registrada.
3. **Trilha de biblioteca em vez de som de cena**, quando o benchmark diz que 7
   dos 10 virais rodam em áudio original. Aqui foi **imposição do material**
   (voz humana não identificável), não escolha estética.

**Risco estratégico que eu declaro, e não escondo:** esta peça **não tem cena
encenada com conflito**. O vídeo é prova, a piada é a legenda. Se a legenda não
pegar, não sobra peça. Isso é a mudança de abordagem, não defeito escondido — e
**continua valendo o pedido de cena encenada**, que rende mais.

## 7. A legenda

```
Ele fala. Eu olho.
Ele repete mais alto, achando que o problema é o volume.
Aí eu inclino a cabeça — não porque entendi, mas pra ele achar que entendi.

Salva essa cara pra próxima reunião.
Marca quem já fingiu entender só pra conversa acabar logo.

#exoticbully #microbully #vidadecachorro #patroamimada
```

**Por que assim:**

- **Escrita nova, para esta cena.** Não reaproveitei nenhuma das 3 de
  `content/legendas-pov-2026-08-21.md` — aquelas foram escritas para outro vídeo
  ("ele levantou do sofá", "o sofá é meu", "dono-garçom") e nenhuma se sustenta
  em cima de um encarar seguido de ladeio de cabeça.
- **A legenda completa a piada, não descreve o vídeo** (§6 do manual). O vídeo
  mostra o ladeio de cabeça; a legenda diz o que ele *significa* — e isso o vídeo
  nunca poderia mostrar.
- **Território novo.** Os últimos assuntos foram "ela manda na casa", "ela é
  móvel", "as regras da casa". Aqui o assunto muda de *ela domina o espaço* para
  **ela manipula o humano** — e o gancho de marcação sai do nicho pet e entra na
  vida de trabalho ("cara de reunião"), que é gente marcando gente fora da
  bolha de dono de cachorro.
- **CTA de salvar embutido**, porque o placar mostra **0 salvos e 0
  compartilhamentos em 10 de 10 posts** — é a métrica travada, não o alcance.
- **4 hashtags**, teto do manual (§6). Pilar "A PATROA MANDA", que é o de maior
  alcance medido no placar (188 contra 66 dos sem pilar).

**Alternativa de teste A/B para o fecho** (se ele quiser trocar):
`Marca quem tem essa mesma cara na terceira reunião do dia.`

## 8. O que falta — decisão dele

1. **Aprovar ou recusar** a peça (vai chegar no Telegram como `pending`).
2. **Opcional, se quiser som real:** ouvir o bruto
   `garimpo/melhores-30/01_E5DBFA8E-...mp4` e dizer se a voz pode ir ao ar.
   Se puder, refaço com som de cena — que é o que os virais usam.
3. **Opcional, capa:** o publisher não manda capa, então o Instagram usa o
   primeiro frame (rosto dela, olhos na lente — dentro da regra). A capa do
   **ladeio de cabeça** é mais forte, mas exige escolher à mão no app.
4. **Continua de pé o pedido de cena encenada.** Esta peça tira a fila do zero;
   ela não substitui uma cena com conflito e desfecho, que rende mais.

**Nada foi gasto e nada precisa ser autorizado para esta peça ir ao ar.**
Bruto já existia, trilha já existia, edição 100% ffmpeg. Custo R$ 0,00.

## 🔗 Relacionados

- [[manual-profissional-reels]]
- [[virais-medidos-2026-08-13]]
- [[legendas-pov-2026-08-21]]
- [[auditoria-chegada-eloen-2026-08-14]]
- [[placar]]
