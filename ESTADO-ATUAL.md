# ESTADO ATUAL — Hana Social

Gerado automaticamente por `studio/estado.py` em 27/07/2026 13:09. **Não editar à mão** — para registrar
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

## Esperando o OK do Ramón
Mídias numeradas em `C:\Users\Ramón França\OneDrive\Fotos da Hana\03 - APROVAR (semana)` (ele abre no OneDrive do celular):

- 00_LEGENDAS.txt
- 01_27-07.jpg
- 02_29-07.jpg
- 03_31-07.jpg
- 04_03-08.jpg
- 05_05-08.jpg
- 06_07-08.jpg
- 07_10-08_REEL.mp4
- 07_10-08_REEL_capa.jpg

Ele responde pelos números. Enquanto não responder, **não commitar**
mudança de status nem publicar.

## Acervo de fotos
- Brutas a processar: 26 arquivos
- Editadas prontas: 9
- Artes recebidas do outro projeto: 1
- Fotos do iPhone sincronizadas (iCloud): 34380

## Últimas mudanças no projeto
```
2ca48a3 feat: skill do projeto + estado que se regenera sozinho (retomar conversa sem perder o fio)
b56fd01 fix: aviso do Telegram manda a foto/video e para de reenviar a cada 30 min
d6079df docs: checagem de metricas 26/07 - sem post novo publicado desde a baseline
07c536e chore: previews do lote da semana para aprovacao [skip ci]
d80d524 docs: linha de base de metricas medida no perfil
fb04d0f feat: renovacao automatica de token e gerador de reel via ffmpeg (benchmark tecnico)
2772a40 fix: vigia local com tolerancia de 5 min (cron do GitHub e estrangulado) e regra de imagem do Ramon corrigida
a472e43 docs: filtro de privacidade no fornecimento de fotos (so Hana sozinha)
```
Alterações não commitadas:
```
M .claude/skills/hana-social/SKILL.md
 M DECISOES.md
 M ESTADO-ATUAL.md
 M studio/estado.py
?? studio/para_aprovar.py
```

## Decisões e contexto
# Decisões e contexto — Hana Social

Parte humana do estado: o que o Ramón decidiu e o que código nenhum adivinha.
**Atualizar ao fim de cada sessão** (a parte automática vem de `studio/estado.py`).
Mais recente em cima.

## Onde paramos (27/07/2026)

**Aguardando o Ramón — o mais urgente:**
- **Aprovar os 7 posts da fila pelos números.** Todos estão `pending`; nenhum
  publica sem ele. Estão na pasta do OneDrive `Fotos da Hana\03 - APROVAR
  (semana)` (numerados + `00_LEGENDAS.txt`) e chegam no Telegram como foto/vídeo.
  Ressalva aberta: o post 4 (03/08, praia na canga amarela) é do mesmo dia de
  praia do vídeo na areia que já está no ar — cena diferente, decisão dele.
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
3. **COMO mostrar post pra ele aprovar — testado em 26-27/07/2026.**
   O que **NÃO funciona** (ele não enxerga, já falhou três vezes seguidas):
   link markdown do `raw.githubusercontent.com`, arquivo anexado na conversa
   (SendUserFile) e link de página publicada (Artifact). Não insistir nesses.
   O que **funciona**: gravar as mídias numeradas na pasta do OneDrive dele
   `Fotos da Hana\03 - APROVAR (semana)`, junto de um `00_LEGENDAS.txt` com as
   legendas na mesma ordem — ele abre no app do OneDrive no celular. O segundo
   canal é o Telegram, que manda foto e vídeo de verdade com botões
   Aprovar/Recusar. Ele responde pelos números.
4. **Conferir repetição ANTES de propor qualquer foto.** Abrir
   `instagram.com/hanaduransanches` no Chrome, rolar os 38 posts do grid e
   comparar cena por cena — inclusive entre os posts do próprio lote (dois posts
   do mesmo passeio, com dias de diferença, também contam como repetido). Ele
   pegou uma repetida que passou batido; é obrigatório desde então.
5. **Fronteira com o projeto Canecas / Brushed & Brewed:** parceria comercial
   sim, interferência não. Não opinar sobre marca, estratégia ou execução deles;
   não mexer na pasta deles. Ao fornecer fotos, **só a Hana sozinha** — nunca
   com o Ramón (a imagem dele é livre aqui, vedada no projeto comercial dele).
6. **Um robô só.** Não criar agendamento novo; expandir o `hana-rotina`.
7. **Verificar a conta ativa no Instagram** antes de qualquer ação no navegador
   — o Chrome do Ramón alterna entre 3 contas.
8. **Fechar as abas** do navegador ao terminar qualquer trabalho.
9. **Economia:** trabalho mecânico em Python local; IA só onde agrega.

## Becos sem saída (não repetir a tentativa)

- **A pasta do iPhone (`iCloudPhotos\Photos`) é o rolo de câmera inteiro** —
  ~34 mil arquivos sem organização, a maioria sem nenhuma relação com a Hana.
  Não dá para garimpar por ali. As fotos boas vêm de `01 - brutas (suba aqui)`,
  onde o Ramón coloca o que quer usar.
- **Mostrar imagem dentro da conversa não funciona**: o widget inline bloqueia
  imagem de fora e embutir mídia em base64 estoura o limite da mensagem.

## Norte estratégico

Audiência → autoridade → produto. O produto ainda não existe; o pilar "roupa que
não serve em bully" é o candidato natural. O gargalo real, medido em
`content/metricas.md`: a base atual é a rede pessoal do Ramón, não o nicho —
crescer exige Reels, hashtag de nicho e presença nos perfis grandes da raça.
