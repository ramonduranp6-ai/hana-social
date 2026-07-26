# Benchmark técnico de infraestrutura (25/07/2026)

Troca de arquitetura entre os dois projetos do Ramón, autorizada por ele.
Escopo: só infraestrutura de publicação. Marca e estratégia não se misturam
(ver `parceria-canecas-pod.md`).

## O que confirmamos que já está certo aqui
- Fluxo **Instagram API with Instagram Login** (sem Página do Facebook) é o
  caminho certo — os dois projetos chegaram nele de forma independente.
- Fila versionada em git + **GitHub Actions** como agendador é superior a
  Task Scheduler local, porque sobrevive à máquina desligada. O outro projeto
  vai migrar para esse modelo.
- Mídia servida pelo `raw.githubusercontent` continua sendo a melhor opção
  para nós (eles usam o CDN da Etsy, que não temos).

## O que ADOTAMOS deles

### 1. Renovação automática do token (resolve o maior risco do projeto)
`GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=...`
devolve token novo de 60 dias e **não exige app secret** no fluxo Instagram
Login. Implementado em `studio/renovar_token.py`: renova quando faltam 20 dias,
grava em `studio/.token` (fora do git) e atualiza o secret no GitHub via
`gh secret set`. Nunca imprime o valor do token.

### 2. Gerador de Reel sem IA
`studio/gerar_reel.py` usa o ffmpeg embutido do `imageio-ffmpeg` com filtros
`zoompan` + `xfade` direto, em vez de gerar frame a frame com PIL (que era como
fazíamos). Mais rápido e sem lixo em disco.

## Limites e pegadinhas da API (anotados para não descobrir na dor)
- **Convite de testador**: o popup de autorização só vincula depois que a conta
  é convidada em Funções do app **e** o convite é aceito em
  `instagram.com/accounts/manage_access` → aba "Convites do testador".
- **Limite de publicação**: 25 posts por 24h por conta. Consultável em
  `GET /{ig_user_id}/content_publishing_limit`.
- **Rate limit do app**: 10 QPS / 10.000 req/dia no padrão da Meta. Sem
  bloqueio publicando 10 posts com 2 min de intervalo.
- **Stories via API não existem** no fluxo Instagram Login. Só na Graph API
  clássica, com conta Business ligada a uma Página do Facebook. Se um dia
  quisermos story automatizado (ex.: cross-promo), é preciso montar o caminho
  clássico em paralelo — decisão do Ramón, não é trivial.
- **Carrossel** (children containers): nenhum dos dois implementou. Fica na
  lista de melhorias.
- Foto também processa de forma assíncrona: esperar `status_code=FINISHED`
  antes de publicar, senão vem "Media ID is not available".

## Achado nosso, fora do benchmark
O cron do GitHub Actions é **estrangulado**: pedimos `*/30` e ele roda a cada
~4h em repositório pouco movimentado. Por isso o vigia local
(`studio/sentinela.py`, Agendador do Windows, seg/qua/sex 18:10, tolerância de
5 min) é quem garante o horário do post.
