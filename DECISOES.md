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
