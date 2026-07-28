# HANDOFF — estado atual do projeto Hana Social

Documento de passagem de bastão. Se você (Claude) está lendo isto numa sessão
nova, leia também `brand-brief.md`, `README.md` e `SETUP.md` para ter todo o
contexto. Este arquivo diz onde paramos.

## O que é o projeto
Sistema para crescer e automatizar o Instagram da cadela Hana
(@hanaduransanches, Exotic Bully Micro, Tri Lilac Merle). Duas frentes:
1. **Conteúdo**: editar fotos/vídeos que o Ramón manda e montar posts (o "estúdio").
2. **Automação**: publicar via Instagram Graph API, agendado no GitHub Actions,
   com aprovação por Telegram (a "impressora"). Código já pronto em `publisher/`.

## Quem é o Ramón (dono)
- Diretor de Controladoria, mora em Itajaí/SC. Estilo direto, sem rodeio, quer
  honestidade e não bajulação. Responder em português.
- Não é técnico em dev/API. Precisa de passo a passo mastigado.
- Existe um skill `ramon-cfo-context` com o contexto de carreira dele (busca
  confidencial de CFO). Não misturar os dois assuntos.

## Status ATUAL (o que já foi feito)
- Repositório estruturado com o pipeline completo (`publisher/`, workflow do
  GitHub Actions, docs). Código compila e a fila lê o primeiro post.
- 1 post pronto na fila: `content/queue/2026-07-22_bar-hana/` (foto do bar editada).
- Conta da Hana confirmada: **Profissional (Business)** e **pública**. OK.
- App criado no Meta for Developers:
  - Nome: **Hana Social**
  - **App ID: 1776084913751376**
  - Caso de uso escolhido: **"Gerenciar mensagens e conteúdo no Instagram"**
    (fluxo novo, Instagram API with Instagram Login, sem Página do Facebook).
  - App ainda **não publicado** (modo desenvolvimento).

## FEITO em 23/07/2026 (token + secrets) ✅
- Conta @hanaduransanches conectada ao app (Business Login) e token gerado
  pelo painel da Meta (via extensão do Claude no Chrome + aprovação do Ramón).
- `IG_USER_ID = 17841471483838197`.
- Secrets gravados no GitHub (repo ramonduranp6-ai/hana-social):
  `IG_ACCESS_TOKEN` e `IG_USER_ID`. Variables: `REQUIRE_APPROVAL=0` (modo
  simples, sem Telegram) e `GRAPH_BASE=https://graph.instagram.com/v21.0`.
- Token testado com sucesso (`GET /me` retornou username e user_id corretos).
- ⚠️ Token vence em ~60 dias (por volta de **21/09/2026**). Renovar antes,
  senão os posts param calados.

## FEITO em 23/07/2026 (primeiro post publicado) ✅
- Repositório tornado **público** e secret `MEDIA_BASE_URL` configurado.
- Workflow testado via disparo manual — 3 execuções com sucesso.
- **Primeiro post publicado no Instagram**: `2026-07-22_bar-hana` (foto do bar),
  movido para `content/posted/`, `instagram_id = 18118796690302997`.
- Pipeline completo funcionando ponta a ponta em modo desenvolvimento.

## PRÓXIMO PASSO IMEDIATO (onde paramos)
1. **Produzir o próximo lote de conteúdo** (6-10 arquivos): Ramón manda as
   fotos/vídeos, Claude edita e monta os posts na fila. A fila está vazia.
2. Gravar clipes do pilar "dor do dono de bully" (roupa/coleira não serve).

## O que ainda falta depois disso
1. **App Review da Meta** (2-4 semanas) para publicação em produção. Até lá,
   testar em modo desenvolvimento na própria conta (a conta conectada é
   testadora, então já dá pra publicar nela).
2. Enquanto o review não sai, postar pelo Meta Business Suite (grátis) o conteúdo
   que o Claude edita.

## Decisões de estilo/marca já firmadas
- Ver `brand-brief.md`. Resumo: marca premium "cultura bully", preservar a cor
  lilac/merle (não estourar saturação), fundo limpo, legenda termina com pergunta,
  máx. 4 hashtags. Nunca gerar imagem falsa da Hana, só editar material real.
- Cadência: 3 posts/semana, trabalho em lote (6-10 arquivos por vez).
- Pilar que faz crescer: "dor do dono de bully" (roupa/coleira não serve). Ainda
  falta gravar clipes desse pilar.

## Branch
Trabalho direto na `main`. O repositório agora vive na máquina local do Ramón
(`Desktop\Hana Social`), que funciona como servidor — sessões são comandadas
pelo celular via claude.ai/code. Fotos brutas vão em
`Hana Social\Fotos da Hana\01 - brutas (suba aqui)` — dentro do projeto desde
28/07/2026 (antes ficavam soltas na raiz do OneDrive), e fora do git.
