# ESTADO ATUAL — Hana Social

Gerado automaticamente por `studio/estado.py` em 27/07/2026 15:05. **Não editar à mão** — para registrar
decisões, use `DECISOES.md`.

## Fila (o que ainda vai ao ar)

| Quando (UTC) | Post | Tipo | Status |
|---|---|---|---|
| 2026-07-29T21:00:00Z | 2026-07-29_lilac-ao-sol | image | approved |
| 2026-07-31T21:00:00Z | 2026-07-31_roda-gigante | image | approved |
| 2026-08-03T21:00:00Z | 2026-08-03_dia-de-praia | image | approved |
| 2026-08-05T21:00:00Z | 2026-08-05_navio-importacao | image | approved |
| 2026-08-07T21:00:00Z | 2026-08-07_banho-de-sol | image | approved |
| 2026-08-10T21:00:00Z | 2026-08-10_escolheu-o-canal | reel | approved |

## Publicados: 3
- 2026-07-22_bar-hana — IG `18118796690302997`
- 2026-07-23_olhar-no-tapete — IG `18140672137562244`
- 2026-07-27_pijama-oncinha — IG `18073337600408952`

## Automação
Últimas execuções do publicador no GitHub:
```
2026-07-27T17:42:23Z workflow_dispatch success
2026-07-27T12:39:28Z schedule success
2026-07-26T23:45:55Z schedule success
```
- Vigia local (Agendador do Windows): próxima execução segunda-feira, 27 de julho de 2026 18:10:00
- Token renovável automático: CONFIGURADO

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
c822544 docs: estado apos publicar pijama-oncinha antecipado
0335b27 chore: atualiza estado da fila [skip ci]
f32c80d chore: antecipa o post pijama-oncinha para agora (pedido do Ramon)
2ddbab8 feat: token renovando sozinho, trava de aprovacao religada e checagem de foto repetida
cb45731 docs: skill aprende os canais que funcionam com o Ramon e a checagem de repeticao
2ca48a3 feat: skill do projeto + estado que se regenera sozinho (retomar conversa sem perder o fio)
b56fd01 fix: aviso do Telegram manda a foto/video e para de reenviar a cada 30 min
d6079df docs: checagem de metricas 26/07 - sem post novo publicado desde a baseline
```
Alterações não commitadas:
```
M ESTADO-ATUAL.md
```

## Decisões e contexto
# Decisões e contexto — Hana Social

Parte humana do estado: o que o Ramón decidiu e o que código nenhum adivinha.
**Atualizar ao fim de cada sessão** (a parte automática vem de `studio/estado.py`).
Mais recente em cima.

## Onde paramos (27/07/2026 — tarde)

**Aguardando o Ramón:**
- **Criar o bot do Telegram** (@BotFather → `/newbot`) para ligar a aprovação
  pelo celular. Descoberto hoje: os secrets `TELEGRAM_BOT_TOKEN` e
  `TELEGRAM_CHAT_ID` **nunca existiram no GitHub** — os botões Aprovar/Recusar
  nunca funcionaram de verdade. Enquanto isso, aprovação é na conversa.
- Decidir se o Reel de 10/08 vai pela automação (trilha original) ou se ele
  publica pelo celular com áudio de tendência — áudio em alta rende mais
  alcance e é licenciado, mas **não existe via API** (limite da Meta, não falta
  de ferramenta).

**Resolvido hoje:**
- **Token do Instagram**: gerado no painel da Meta (app "Hana Social",
  id 1776084913751376), gravado em `studio/.token`, renovado até 24/09/2026 e
  secret do GitHub atualizado pelo script. A renovação passou a rodar toda
  semana dentro do `sentinela.bat` (não criei robô novo).
- **Trava de aprovação religada**: a variável `REQUIRE_APPROVAL` estava em **0**
  no GitHub — ou seja, a fila subia sozinha, contra a regra 2. Voltou para 1.
- **Os 7 posts da fila foram aprovados por ele**, condicionados a não haver
  repetida — checagem rodada, zero repetições. O primeiro sobe hoje 18h.
- Acentos corrigidos nos posts de 05/08, 07/08 e 10/08 (estavam sem).

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
   O que **funciona no PC** (melhor canal, criado em 27/07/2026):
   `python studio/painel_aprovacao.py` — gera uma página local com foto grande +
   legenda + data, numerada, e abre **no Chrome do perfil da Hana**
   (`--profile-directory="Profile 2"`, `hanaduransanches@gmail.com`).
   **Nunca usar `webbrowser.open` nem `start`**: o navegador padrão do Windows
   é o perfil da marca Canecas, e abrir ali é erro que já custou três avisos
   dele na mesma conversa.
   No celular: pasta do OneDrive `Fotos da Hana\03 - APROVAR (semana)` numerada
   com `00_LEGENDAS.txt`. O Telegram é o canal que ele quer ligar — os secrets
   nunca foram criados, então hoje ele não funciona.
4. **Conferir repetição ANTES de propor qualquer foto** — rodar
   `python studio/checar_repetida.py`, que compara por impressão digital de
   imagem contra tudo publicado no perfil e a fila contra ela mesma.
   O proibido é **a mesma foto** ir ao ar duas vezes; **o mesmo passeio pode
   render vários posts**, desde que as fotos sejam diferentes (ele corrigiu isso
   em 27/07/2026 — eu tinha endurecido a regra sozinho e tirei um post bom da
   fila). Limite a declarar sempre: a checagem só pega FOTO. Vídeo antigo do
   perfil é dele e não preciso auditar; dos Reels que eu montar, o controle fica
   em `content/videos-usados.json`.
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
