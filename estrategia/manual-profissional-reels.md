# Manual profissional de Reels — padrão de qualidade medido (13/08/2026)

Origem: bronca dele ("falta e muita qualidade técnica e profissional") + os 7
virais baixados e medidos com ffmpeg (30M a 670k views). Cada número abaixo é
medido, não opinião. **Toda peça nova segue este manual; quem aplica é o
diretor-reels; quem audita, o auditor; quem aprova, o Ramón.**

## 0. A régua técnica — virais × nossos (medido 13/08)

| métrica | virais (7) | nossos 3 da fila | alvo |
|---|---|---|---|
| brilho médio | 112-127 | 108-123 ✅ | 110-130 |
| variação de brilho no vídeo | 10-25 (luz ESTÁVEL) | **80-196 e 68-151** ❌ | < 30 |
| loudness | −13,8 a −15,9 LUFS | **−18,5** (fraco) ❌ | −14 LUFS |
| pico de áudio | ≤ +0,5 dBTP | −5,9 (sobra headroom) | −1 dBTP |
| resolução | 720x1280 (deles) | 1080x1920 ✅ (melhor) | 1080x1920 30fps |
| cortes | **5 de 7 = PLANO ÚNICO** | 4-7 cortes | ver §4 |
| texto na tela | **ZERO nos 7** | 3 frases | ver §4 |
| efeitos/transições | zero | zoom/punch-in | zero |

Tradução da bronca dele em números: **nosso defeito não é resolução — é luz
inconsistente entre cortes (parece amador) e som fraco.** O Instagram normaliza
para ~−14 LUFS: áudio em −18,5 chega "murcho" no feed.

## 1. PRÉ-PRODUÇÃO (é aqui que o viral nasce — não na edição)

- **A cena é ENCENADA, não achada.** O prank de 1,0M é: prop (balão) + cão
  dormindo + câmera parada + esperar. Planejar: qual é a piada, qual prop,
  onde a Hana está, onde a câmera fica, o que dispara a reação.
- **Cenário limpo:** fundo sem bagunça (parede, chão de madeira, mesa). Tirar
  objeto que não serve à piada do quadro.
- **Luz natural forte e UMA só:** golden hour (fim de tarde) foi a luz do
  viral de 945k. Nunca misturar cômodo escuro + claro na mesma peça.
- **Câmera na ALTURA DA HANA** (chão/mesa), não olhando de cima. Tripé ou
  apoio fixo para cena encenada; mão firme para POV/flagrante.
- **Filmar 3-5 tomadas** da mesma cena. Escolhe-se a melhor, não a única.

## 2. CAPTURA (o que pedir ao Ramón quando ele filmar)

1080x1920 (vertical, celular deitado NUNCA) · 30fps · foco travado no rosto
dela · rosto visível já no 1º segundo · luz atrás da CÂMERA, nunca atrás dela
(contraluz vira vulto) · deixar 2s "mortos" antes e depois da ação (margem de
corte) · som da cena limpo (sem TV/voz de fundo, a menos que seja a piada).

## 3. DIREÇÃO DA CENA

- UMA piada. Conflito dono × Hana. Ela vence.
- O gancho é VISUAL no 1º segundo: a situação se entende sem ler nada.
- Desfecho no ROSTO dela (o viral de 4,8M termina em close do focinho).
- Duração alvo: 6-18s.

## 4. EDIÇÃO (regra nova, medida)

- **Plano único é o padrão para cena encenada forte** (5 de 7 virais).
  Montagem multi-corte fica para peça de acervo (regra 3n-i dele) — conflito
  declarado, decisão final é dele.
- Se cortar: corte seco, **zero transição, zero filtro, zero zoom artificial**.
- **Luz consistente entre cortes: variação de brilho < 30** no vídeo final
  (medir com signalstats; foi nosso maior defeito medido: 80→196).
- **Texto na tela: zero é o ideal.** Máximo 1 frase curta, só se a cena não
  se explica sozinha. (Os 7 virais têm zero.)
- Grading leve e uniforme: mesmo tom em todos os cortes (eq/curves no ffmpeg),
  nada de filtro estiloso.

## 5. SOM (novo padrão obrigatório)

- **Masterizar para −14 LUFS, pico −1 dBTP** (`loudnorm=I=-14:TP=-1` no
  passo final do montar_reel.py). Nossos −18,5 LUFS acabaram hoje.
- Som da cena é o protagonista (7 de 10 virais). Música só quando é
  PERSONAGEM da piada (Godfather no cão-estátua; samba no malandro) — e aí
  entra alta, não de fundo. Trilha própria Lyria continua para peça montada.
- Regras 3e/3f/3k continuam: combina com a cena, sem Anitta/Xuxa, tom
  criança-cachorro.

## 6. ENTREGA (descrição, capa, metadado)

- Legenda: 1ª pessoa DELA, completa a piada (não descreve o vídeo), termina
  com pergunta que pede marcação. Máx. 4 hashtags (nicho + humor). Geotag.
- Capa: frame do ROSTO dela, olhos abertos, sem texto ou com 1 palavra.
- Horário: seg/qua/sex 11:00Z (8h Itajaí). Share é a métrica que importa.

## 7. O PROMPT COMPLETO (encomenda de peça ao diretor-reels)

> Produza um Reel da Hana no padrão do manual profissional
> (`estrategia/manual-profissional-reels.md`). PRÉ: defina a piada única
> (conflito dono × Hana, ela vence), o prop, o cenário limpo, a posição de
> câmera fixa na altura dela e a luz única — entregue isso como PEDIDO DE
> CENA de 5 linhas para o Ramón filmar em 3-5 tomadas (1080x1920, 30fps,
> rosto no 1º segundo, luz atrás da câmera, 2s de margem). PRODUÇÃO: monte
> preferindo PLANO ÚNICO; se cortar, corte seco sem transição/filtro/zoom,
> luz consistente (variação < 30 no signalstats). Zero texto na tela (máx. 1
> frase se imprescindível). SOM: cena em primeiro plano, master −14 LUFS
> pico −1 dBTP; música só se for personagem da piada (sem Anitta/Xuxa/funk/
> tristeza); senão, Lyria. ENTREGA: vídeo + legenda em 1ª pessoa dela que
> completa a piada e termina pedindo marcação (máx. 4 hashtags) + capa do
> rosto + 1 linha justificando trilha e corte. Depois: auditor (3i) com o
> checklist técnico abaixo; repetição (2c); aprovação dele no Telegram.

## 8. Checklist técnico do auditor (reprova com número, não com opinião)

- [ ] Variação de brilho > 30 → REPROVA (luz inconsistente).
- [ ] Loudness fora de −14 ±1 LUFS ou pico > −1 dBTP → REPROVA.
- [ ] Transição, filtro ou zoom artificial → REPROVA.
- [ ] Texto na tela com 2+ frases → REPROVA.
- [ ] Rosto ausente do 1º segundo ou do desfecho → REPROVA.
- [ ] Mais de uma piada / mais de 18s sem virada → REPROVA.
- [ ] + os itens de sempre: anatomia, cor tri lilac merle, 9:16, repetição.

## 9. Ferramentas para o nível profissional (escada de custo)

| ferramenta | para quê | custo | estado |
|---|---|---|---|
| ffmpeg `loudnorm` | som no padrão do feed (−14 LUFS) | zero | **usar já** |
| ffmpeg `signalstats` | medir luz antes de aprovar | zero | **usar já** |
| ffmpeg `vidstab` | estabilizar vídeo de mão tremida | zero | usar quando precisar |
| ffmpeg `eq/curves` | igualar cor/luz entre cortes | zero | **usar já** |
| Lyria 3 (`gerar_trilha.py`) | trilha própria | US$ 0,04 | ativo |
| Gemini/Flow (app, plano dele) | trecho gerado premium (regra 3j-i) | já pago | ativo |
| Apify | benchmark mensal de virais | ~US$ 0,15/rodada | ativo |
| Kairogen (Topaz upscale, Veo, Kling) | upscale/geração premium | créditos, requer login | ⏳ precisa ele autorizar no claude.ai |
| CapCut desktop | edição manual fina (se ele quiser mexer) | grátis | opcional, instala com 1 ok dele |

Sem gasto novo sem OK dele. O salto de qualidade imediato (luz + som) é
100% ffmpeg, custo zero, e já vale para o próximo Reel.
