# Garimpo de collab e benchmark de Reels — por dado (Apify, 09/08/2026)

Ferramenta nova: Apify (MCP `mcp.apify.com`, plano grátis US$ 5/mês). Custo desta
tarefa: **~US$ 0,19** (2 chamadas de hashtag scraper + 2 de profile scraper, 84
Reels + 32 perfis lidos). Só leitura — nenhuma ação de seguir/curtir/DM.

## 1. Collab — os 5 escolhidos na mão bateram com o dado

Rodei `apify/instagram-profile-scraper` nos 7 perfis do garimpo manual
(`PROXIMA-CONVERSA.md`). **Os números batem** — o garimpo à mão estava certo:

| perfil | seguidores (medido) | último post | ativo (<30d)? | engaj. (curtidas/seguidores, último Reel) |
|---|---|---|---|---|
| @dudinhabully | 561 | 07/08 | ✅ | 0,33x — **DM já mandada 09/08** |
| @pituco_bully | 981 | 22/07 | ✅ | 0,055x |
| @fionaabully_ | 1.370 | 20/07 | ✅ | 0,019x |
| @rolly_bully | 1.461 | 18/07 | ✅ | 0,006x |
| @ravenna_bully_ | 2.602 | 07/06 | ❌ (63 dias) | 1,15x (mas parado) |
| @dom_exotic_bully | 2.708 | 07/06 | ❌ (63 dias) | 0,02x (parado) |
| @momoamora1 | 2.289 | 07/08 | ✅ | 0,035x |

**Achado:** 2 dos 5 reservas escolhidos à mão (@ravenna_bully_ e @dom_exotic_bully)
estão **parados há mais de 2 meses** — não valem mais como alvo agora, mesmo
tendo o número de seguidor certo. Trocar por @momoamora1 (ativo, mesmo range).

## 2. Três novos alvos achados pelo dado (garimpo por hashtag, não olho)

Busquei Reels em `#exoticbullybrasil`, `#americanbullybrasil`, `#microbully`
(84 Reels, 60+ contas), filtrei quem tem 500-3.000 seguidores, postou nos
últimos 30 dias e **não é canil/pet shop** (bio de dono comum):

| perfil | seguidores | último post | engaj. (curtidas/seguidores) | obs |
|---|---|---|---|---|
| @troy.abully | 524 | 02/08 | **12,8x** | 1 Reel bombou muito acima do normal — checar se é fluke antes de apostar tudo nele |
| @zaya.lifestylee | 779 | 06/08 | 1,34x | boa e consistente |
| @caioguedesmbc | 1.418 | 17/08 (23 dias) | 0,037x | fraco, fica como reserva |

## 3. Lista final de collab por ordem de engajamento (ativos, dono comum)

1. @troy.abully (12,8x — outlier, vale espiar o Reel antes)
2. @zaya.lifestylee (1,34x)
3. @dudinhabully (0,33x — **já contatado**)
4. @pituco_bully (0,055x)
5. @momoamora1 (0,035x)

Reservas: @fionaabully_, @rolly_bully, @caioguedesmbc.
**Fora da lista** (inativos >30 dias, medido, não trocar sem novo check):
@ravenna_bully_, @dom_exotic_bully.

## 4. Benchmark de Reels — corrige a regra 3h da skill (amostra era de 4)

A regra 3h dizia "o nicho não roda em música, roda em áudio original" com base
em **4 Reels de 2 perfis**. Com o Apify, medi **80 Reels de ~60 contas de bully
BR/internacional** (hashtags `exoticbullybrasil`, `americanbullybrasil`,
`microbully`):

- **Áudio original: 39/80 (49%) · Música/trilha: 41/80 (51%)** — é meio a meio,
  não um domínio de áudio original como a amostra pequena sugeria.
- Duração: a maioria fica entre 7-30s; poucos passam de 40s.
- **Conclusão prática:** a regra 3h vira "quase empate" — não é mais motivo
  para descartar trilha de terceiro. A régua que decide continua sendo a 3e-ii
  (o que combina com a cena), não a estatística do nicho.

⚠️ Amostra ainda mistura contas BR e internacionais (a hashtag `microbully`
não é exclusiva do Brasil) — não é 100% BR puro, mas é 20x maior que a anterior.

## 5. Linha de base do nicho (repetir semanalmente)

Medido em 09/08/2026, hashtags `exoticbullybrasil` + `americanbullybrasil` +
`microbully`, 84 Reels: contas de 100 a 100.000+ seguidores, mediana de
curtidas na faixa de contas pequenas (500-3.000 seguidores) fica entre
**500 e 3.000 curtidas por Reel** quando o conteúdo acerta — ou seja, o nicho
pequeno consegue engajamento proporcionalmente alto. Comparar com o placar da
Hana (`content/placar.md`) nas próximas reuniões para saber se 331 seguidores
é problema nosso ou o nicho inteiro está devagar.
