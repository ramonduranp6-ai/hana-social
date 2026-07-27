# ESTADO ATUAL — Hana Social

Gerado automaticamente por `studio/estado.py` em 27/07/2026 11:56. **Não editar à mão** — para registrar
decisões, use `DECISOES.md`.

## Fila (o que ainda vai ao ar)

| Quando (UTC) | Post | Tipo | Status |
|---|---|---|---|
| 2026-07-27T21:00:00Z | 2026-07-27_pijama-oncinha | image | pending |
| 2026-07-29T21:00:00Z | 2026-07-29_lilac-ao-sol | image | pending |
| 2026-07-31T21:00:00Z | 2026-07-31_roda-gigante | image | pending |
| 2026-08-03T21:00:00Z | 2026-08-03_dia-de-praia | image | pending |
| 2026-08-05T21:00:00Z | 2026-08-05_navio-importacao | image | pending |
| 2026-08-07T21:00:00Z | 2026-08-07_banho-de-sol | image | pending |
| 2026-08-10T21:00:00Z | 2026-08-10_escolheu-o-canal | reel | pending |

## Publicados: 2
- 2026-07-22_bar-hana — IG `18118796690302997`
- 2026-07-23_olhar-no-tapete — IG `18140672137562244`

## Automação
Últimas execuções do publicador no GitHub:
```
2026-07-27T12:39:28Z schedule success
2026-07-26T23:45:55Z schedule success
2026-07-26T20:15:45Z schedule success
```
- Vigia local (Agendador do Windows): próxima execução segunda-feira, 27 de julho de 2026 18:10:00
- Token renovável automático: FALTA criar studio/.token

## Acervo de fotos
- Brutas a processar: 26 arquivos
- Editadas prontas: 9
- Artes recebidas do outro projeto: 1
- Fotos do iPhone sincronizadas (iCloud): 34380

## Últimas mudanças no projeto
```
b56fd01 fix: aviso do Telegram manda a foto/video e para de reenviar a cada 30 min
d6079df docs: checagem de metricas 26/07 - sem post novo publicado desde a baseline
07c536e chore: previews do lote da semana para aprovacao [skip ci]
d80d524 docs: linha de base de metricas medida no perfil
fb04d0f feat: renovacao automatica de token e gerador de reel via ffmpeg (benchmark tecnico)
2772a40 fix: vigia local com tolerancia de 5 min (cron do GitHub e estrangulado) e regra de imagem do Ramon corrigida
a472e43 docs: filtro de privacidade no fornecimento de fotos (so Hana sozinha)
8322685 docs: fronteira entre projetos - parceria comercial, sem interferencia mutua
```
Alterações não commitadas:
```
?? .claude/
?? DECISOES.md
?? ESTADO-ATUAL.md
?? content/queue/2026-08-05_navio-importacao/
?? content/queue/2026-08-07_banho-de-sol/
?? content/queue/2026-08-10_escolheu-o-canal/
?? studio/estado.py
```

## Decisões e contexto
# Decisões e contexto — Hana Social

Parte humana do estado: o que o Ramón decidiu e o que código nenhum adivinha.
**Atualizar ao fim de cada sessão** (a parte automática vem de `studio/estado.py`).
Mais recente em cima.

## Onde paramos (27/07/2026)

**Aguardando o Ramón:**
- Gerar token novo do Instagram no painel da Meta (2 min, com ele junto) para
  criar `studio/.token` e ligar a renovação automática. Sem isso, o token vence
  por volta de 21/09/2026 e **os posts param calados**.
- Decidir se o primeiro Reel vai pela automação (com a trilha original que
  compus) ou se ele publica pelo celular com áudio em alta — áudio de tendência
  rende mais alcance e é licenciado, mas não existe via API.

**Feito e no ar:**
- Bio nova publicada (escolha delegada a mim): "A patroa: aqui quem manda sou eu".
- Robô único `hana-rotina`: domingo produz o lote, terça e quinta faz ronda de
  engajamento. Nada é publicado sem o "aprovado" dele.
- Primeiro Reel montado com a fórmula campeã do nicho (gancho "descreva essa
  cena com UMA palavra") sobre o vídeo dela assistindo TV.

## Regras permanentes (não reabrir sem ele mandar)

1. **A estrela é a Hana.** O Ramón pode aparecer, mas nunca é o assunto. Régua:
   se a Hana puder ser cortada do quadro sem mudar a piada, o post está errado.
2. **Nada é publicado sem aprovação explícita dele.** A automação prepara e
   pergunta; ele responde pelos números.
3. **Fronteira com o projeto Canecas / Brushed & Brewed:** parceria comercial
   sim, interferência não. Não opinar sobre marca, estratégia ou execução deles;
   não mexer na pasta deles. Ao fornecer fotos, **só a Hana sozinha** — nunca
   com o Ramón (a imagem dele é livre aqui, vedada no projeto comercial dele).
4. **Um robô só.** Não criar agendamento novo; expandir o `hana-rotina`.
5. **Verificar a conta ativa no Instagram** antes de qualquer ação no navegador
   — o Chrome do Ramón alterna entre 3 contas.
6. **Fechar as abas** do navegador ao terminar qualquer trabalho.
7. **Economia:** trabalho mecânico em Python local; IA só onde agrega.

## Norte estratégico

Audiência → autoridade → produto. O produto ainda não existe; o pilar "roupa que
não serve em bully" é o candidato natural. O gargalo real, medido em
`content/metricas.md`: a base atual é a rede pessoal do Ramón, não o nicho —
crescer exige Reels, hashtag de nicho e presença nos perfis grandes da raça.
