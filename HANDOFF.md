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

## PRÓXIMO PASSO IMEDIATO (onde paramos)
No painel do app (developers.facebook.com/apps/1776084913751376), o Ramón ia
clicar em **"Personalizar o caso de uso 'Gerenciar mensagens e conteúdo no
Instagram'"** para:
1. Conectar a conta @hanaduransanches (Business Login for Instagram).
2. Pedir os escopos `instagram_business_basic` e `instagram_business_content_publish`.
3. **Gerar o token de longa duração** → `IG_ACCESS_TOKEN`.
4. Pegar o **id numérico da conta** → `IG_USER_ID`.

> Essa etapa é no navegador da Meta. Claude Code não clica em site — é guiada por
> print (Ramón manda screenshot, Claude diz o próximo clique) ou pela extensão
> do Claude no Chrome.

## O que ainda falta depois do token
1. Deixar o repositório **público** (ou usar bucket) para hospedar a mídia →
   definir `MEDIA_BASE_URL`.
2. Cadastrar os Secrets no GitHub Actions (ver `SETUP.md`): `IG_USER_ID`,
   `IG_ACCESS_TOKEN`, `MEDIA_BASE_URL`; Variables `REQUIRE_APPROVAL` e `GRAPH_BASE`.
3. Testar o disparo manual do workflow.
4. **App Review da Meta** (2-4 semanas) para publicação em produção. Até lá,
   testar em modo desenvolvimento na própria conta.
5. Enquanto o review não sai, postar pelo Meta Business Suite (grátis) o conteúdo
   que o Claude edita.

## Decisões de estilo/marca já firmadas
- Ver `brand-brief.md`. Resumo: marca premium "cultura bully", preservar a cor
  lilac/merle (não estourar saturação), fundo limpo, legenda termina com pergunta,
  máx. 4 hashtags. Nunca gerar imagem falsa da Hana, só editar material real.
- Cadência: 3 posts/semana, trabalho em lote (6-10 arquivos por vez).
- Pilar que faz crescer: "dor do dono de bully" (roupa/coleira não serve). Ainda
  falta gravar clipes desse pilar.

## Branch
Trabalho na branch `claude/ola-513skx`.
