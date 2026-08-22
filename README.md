# Hana Social — sistema de publicação automática

Publica os posts da Hana (@hanaduransanches) no Instagram de forma automática,
com aprovação por um toque no Telegram. Roda de graça no GitHub Actions.

## Como funciona (as duas caixas)

**Estúdio (o Claude, sob demanda):** o Ramón manda um lote de fotos/vídeos,
o Claude edita, escreve as legendas e coloca os posts prontos na fila
(`content/queue/`). Só essa parte usa IA.

**Impressora (este repositório, sozinho):** um cron no GitHub Actions roda a
cada 30 min, avisa o Ramón no Telegram, e quando ele aprova, publica no horário
agendado via Instagram Graph API. Não usa IA. Uma rotina diária separada coleta
métricas, checa a cobertura da fila e envia alertas, sem pesar no publicador.

## Fluxo de um post

1. Claude cria uma pasta em `content/queue/<id>/` com a mídia + `post.json`
   (status `pending`).
2. O cron manda o post pro Telegram com botões ✅ Aprovar / ❌ Recusar.
3. Ramón toca ✅. O próximo ciclo marca o post como `approved`.
4. Chegando o horário (`scheduled_for`), o cron publica no Instagram.
5. O post é arquivado em `content/posted/`.

## Estrutura

```
publisher/
  ig_api.py           # cliente da Instagram Graph API
  postqueue.py        # leitura/escrita da fila
  telegram_approve.py # notificação e aprovação por Telegram
  run.py              # orquestrador (roda no cron)
  prontidao.py         # confere peça completa antes de ir ao Telegram
  cobertura_fila.py    # avisa se faltarem posts aprovados e agendados
content/
  queue/              # posts a publicar
  posted/             # arquivo dos já publicados
.github/workflows/
  publish.yml         # agendador (cron a cada 30 min)
  maintenance.yml     # métricas e alertas uma vez ao dia
```

## Formato do `post.json`

```json
{
  "type": "image",
  "media_file": "image.jpg",
  "caption": "texto + hashtags",
  "scheduled_for": "2026-07-22T21:00:00Z",
  "status": "pending"
}
```

`type` aceita `image` ou `reel`. `scheduled_for` é sempre em UTC.

## O que falta pra ligar

Ver [`SETUP.md`](SETUP.md). São as coisas que só o Ramón pode fazer:
criar o app na Meta, o bot do Telegram e cadastrar os segredos.
Enquanto isso não estiver pronto, o código está completo mas não publica.
