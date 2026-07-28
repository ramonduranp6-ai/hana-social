# ESTADO ATUAL — Hana Social

Gerado automaticamente por `studio/estado.py` em 27/07/2026 22:58. **Não editar à mão** — para registrar
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
2026-07-27T22:19:13Z schedule success
2026-07-27T18:15:01Z schedule success
2026-07-27T17:42:23Z workflow_dispatch success
```
- Vigia local (Agendador do Windows): próxima execução quarta-feira, 29 de julho de 2026 18:10:00
- Token renovável automático: CONFIGURADO

## Esperando o OK do Ramón
Mídias numeradas em `C:\Users\Ramón França\OneDrive\Desktop\Hana Social\Fotos da Hana\05 - APROVAR (semana)` (ele abre no OneDrive do celular):

- 00_LEGENDAS.txt
- 01_27-07.jpg
- 02_29-07.jpg
- 03_31-07.jpg
- 04_03-08.jpg
- 05_05-08.jpg
- 06_07-08.jpg
- 07_10-08_REEL.mp4
- 07_10-08_REEL_capa.jpg
- 08_MUSICA-1-fofo.mp4
- 09_MUSICA-2-lofi.mp4
- 10_MUSICA-3-comica.mp4

Ele responde pelos números. Enquanto não responder, **não commitar**
mudança de status nem publicar.

## Acervo de fotos
- Brutas a processar: 26 arquivos
- Editadas prontas: 4
- Artes recebidas do outro projeto: 1
- Fotos do iPhone sincronizadas (iCloud): 34381

## Últimas mudanças no projeto
```
ecef4fc feat: Pagina do Facebook da Hana criada e ligada ao Instagram
45afd5b docs: a conta ja era Criador de conteudo + achar o Chrome da Hana sem perguntar
49e6502 docs: conta da Hana fica como Criador de conteudo (decisao do Ramon)
d92b249 feat: Reel de 10/08 ganha trilha (lo-fi) - liberado pelo Ramon
ba805b4 chore: arruma a pasta Fotos da Hana (pedido do Ramon)
5d90897 refactor: fotos da Hana passam a morar dentro do projeto (pedido do Ramon)
d78246b ï»¿docs: sempre passar o caminho completo e nao criar pasta nova (pedido do Ramon)
7d7295d feat: trilha propria para os Reels (Lyria 3 via Gemini) + 3 opcoes para o Ramon ouvir
```
Alterações não commitadas:
```
M DECISOES.md
```

## Decisões e contexto
# Decisões e contexto — Hana Social

Parte humana do estado: o que o Ramón decidiu e o que código nenhum adivinha.
**Atualizar ao fim de cada sessão** (a parte automática vem de `studio/estado.py`).
Mais recente em cima.

## Onde paramos (28/07/2026 — madrugada)

**Próxima conversa começa por aqui:**
- **Testar a API de áudio** (o assunto que ficou pela metade). Gerar token pelo
  **Facebook Login** no app "Hana Social" (id 1776084913751376), buscar faixas
  em alta e tentar anexar por `musicSoundInfo.musicSoundId`. **Não prometer
  nada antes de rodar** — o que existe hoje é indício de integradores, não
  documentação da Meta. Não trocar o `IG_ACCESS_TOKEN` que está funcionando.
- **Revisar as configurações da Página do Facebook.** Em 28/07/2026 o Ramón
  terminou o assistente de configuração "dando enter em tudo" para destravar a
  tela, e pediu revisão depois. Conferir o que entrou (contato, localização,
  botão de ação, foto de perfil e capa) e corrigir o que não faz sentido para a
  Hana. A Página ainda está sem foto de perfil e sem capa.

**Aguardando o Ramón:**
- **Decidir se monta a biblioteca de 12 trilhas** (US$ 0,48 no crédito do
  Gemini) ou fica só com as 3 atuais.
- **Decidir se quer publicar Reel pelo celular com áudio de tendência.** Agora
  que se sabe que a conta é Criador, isso está liberado — o único custo são
  ~3 minutos dele por Reel, porque a API não anexa áudio de tendência.

**Estrutura nova em 28/07/2026 — Página do Facebook criada e ligada:**
- **Página `Hana Duran Sanches`** criada (id `1235806802950209`), categoria
  "Criador(a) de conteúdo digital", bio puxada do Instagram. Portfólio
  empresarial gerado junto: `616358434290372`.
- **Instagram ligado à Página** — o Ramón fez o login (senha eu não digito,
  nunca). Confirmado na tela: o Business Suite mostra os 329 seguidores do
  Instagram e "hanaduransanches" ao lado da Página.
- **A conta CONTINUA Criador de conteúdo** depois de ligar — conferido na tela.
  O risco que eu tinha levantado (virar Business e perder o áudio em alta do
  app) **não aconteceu**.
- **O publicador não foi tocado.** `IG_ACCESS_TOKEN` segue o mesmo, fluxo
  Instagram Login intacto, post de 29/07 às 18h sem risco.
- **Próximo passo:** gerar um token pelo **Facebook Login** (app "Hana Social",
  id 1776084913751376) e testar a API de áudio de verdade — buscar faixas em
  alta e tentar anexar por `musicSoundInfo.musicSoundId`. Só então se sabe se o
  áudio de tendência entra na automação. **Enquanto não testar, não prometer.**
  Vale lembrar o que já está documentado: o catálogo da API pode diferir do que
  aparece no app, e não dá para pré-visualizar o Reel com o áudio antes de subir.

**Decidido em 28/07/2026:**
- **A conta JÁ ERA Criador de conteúdo** — conferido na tela, não havia nada a
  trocar. Ele decidiu manter assim e deixar Business para quando houver base
  grande. Motivo: só Criador enxerga a biblioteca de áudios em tendência —
  Business fica presa à Meta Sound Collection, porque os acordos da Meta com as
  gravadoras não cobrem uso comercial. Quando a Hana tiver audiência e o produto
  existir, Business passa a valer pelas ferramentas de loja — e ele mencionou
  que nessa hora compraria algum app de apoio.
  **Consequência que muda o jogo:** o áudio de tendência **já está disponível
  pra ele hoje**. O que separava a Hana dele nunca foi permissão — é só o fato
  de a API não anexar áudio de tendência, então o Reel tem que subir pelo
  celular. Custo: ~3 minutos por Reel.
- **Como achar o Chrome da Hana sem perguntar** (ele reclamou que a mesma
  pergunta veio 3x na mesma noite): `list_connected_browsers` →
  `select_browser` → `instagram.com/accounts/edit/` → `screenshot`, conferindo
  o @ na tela. Nome e id do navegador não são confiáveis. Receita na skill.
- **Trilha do Reel de 10/08: a lo-fi** (escolha delegada a mim). Já aplicada na
  fila e na pasta de aprovação.
- **Trilha própria virou capacidade do projeto:** `studio/gerar_trilha.py` gera
  clipes de 30s pelo Lyria 3 (Gemini, US$ 0,04 cada). Fica claro o limite: isso
  resolve QUALIDADE de áudio, não ALCANCE — quem move alcance é o áudio de
  tendência, que não existe via API.
- **Descoberta:** os Reels nunca tiveram música. O de 10/08 subia com o áudio
  cru do MOV (som da casa). Eu havia afirmado que não existia trilha nenhuma no
  projeto e estava errado: havia um `musica_hana.wav` de 25/07 largado na pasta
  de editadas, que nunca entrou em Reel.

**Resolvido em 27/07:**
- **Ronda de engajamento começou (27/07/2026).** Descoberto que a "ronda de
  terça e quinta" descrita aqui **nunca existiu em código** — era só texto.
  Agora é processo manual meu, aprovado por ele: **3x por semana, ~10
  comentários**, sempre com aprovação em bloco antes de publicar. Primeira ronda:
  4 comentários no ar como "a patroa" em @americanbully.insta.do.bruce,
  @ohanabulls_club (canil de Blumenau/SC), @guerreirobully e @canilelohimbull.
  Diagnóstico confirmado: nos comentários dos posts da Hana só aparecem amigos e
  família — o nicho ainda não chegou. Por isso a ronda existe.
- **Música nos Reels:** ele topa música embutida no arquivo (isso a automação
  faz). Áudio de tendência do Instagram continua fora — não existe via API.
- **Telegram no ar (27/07/2026, noite).** Bot `@Hanasocial_aproval_bot` criado
  por ele no BotFather; token e chat id gravados como secrets no GitHub
  (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) — antes eles **nunca existiram** e
  os botões nunca funcionaram. Testado ponta a ponta: mensagem com botões
  chegou no celular dele e o clique voltou pra API. Agora é o canal principal de
  aprovação; a pasta do OneDrive vira reserva.
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
   No celular: `Hana Social\Fotos da Hana\05 - APROVAR (semana)`, numerada com
   `00_LEGENDAS.txt`. **Sempre escrever o caminho COMPLETO na mensagem** e nunca
   criar subpasta nova — ele não acha (pedido dele em 27/07/2026).
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
