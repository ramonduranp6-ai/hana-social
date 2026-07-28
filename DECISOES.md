# Decisões e contexto — Hana Social

Parte humana do estado: o que o Ramón decidiu e o que código nenhum adivinha.
**Atualizar ao fim de cada sessão** (a parte automática vem de `studio/estado.py`).
Mais recente em cima.

## Onde paramos (28/07/2026 — fim do dia)

**FECHADO: a trilha do Reel de 10/08 fica como está** (a lo-fi própria já
aplicada). Palavras dele: *"por enquanto vamos manter como está, nos próximos eu
aprovo novamente"*. Ou seja: **não mexer mais na trilha do 10/08**; a conversa de
música volta na produção dos PRÓXIMOS Reels.

**FEITO em 28/07/2026 — separação do pessoal e do da Hana.** Ele perguntou se os
posts vão para o Facebook: **não vão**, o publicador é só Instagram. Propus ligar
o compartilhamento automático para alimentar a Página de graça e **estava errado**
— a tela só oferece mandar para o **perfil pessoal do Ramón**, não para a Página.
Não liguei. E encontrei o **story já ligado** (stories da Hana caindo no Facebook
pessoal dele): **desliguei as duas chaves** com o OK dele — *"não podemos
misturar o pessoal com o da hana"*. Regra na skill (3b-ii).
**ENCERRADO: a Página do Facebook fica vazia, de propósito.** Eu ia deixar ele
pôr foto de perfil e capa; ele cortou e está certo — *"como não vamos usar o
facebook, não tem porque a Hana estar com foto de capa e perfil"*. A Página é só
encanamento da Graph API (áudio de tendência). Não reabrir. Só não pode ser
apagada nem desligada do Instagram, senão a API de áudio cai.

**NOVO em 28/07/2026 — o projeto passou a MEDIR.** Ele escolheu a automação do
placar (*"faz a 1"*). `publisher/metrics.py` roda dentro do publicador que já
existia (regra do robô único), **uma coleta por dia**, e escreve
`content/metricas.json` + `content/placar.md`. Testado ponta a ponta com o token
real. **Primeiro número medido, e ele é duro:** 329 seguidores, alcance de
**30 a 50 por post** (~13% da base), **0 salvamento** e **0 seguidor ganho** nos
3 posts publicados. Tradução: o conteúdo circula só na rede pessoal do Ramón e
não converte quem vê em seguidor. Confirma por número o que estava escrito em
`content/metricas.md`: **o gargalo é alcance**. Próxima leitura fica mais rica
quando o Reel de 10/08 entrar (aí dá para comparar Reel x Foto de verdade).

**Próxima conversa começa por aqui:**
- **Ler `content/placar.md` antes de opinar sobre o que funciona.**
- **Ampliar a amostra do nicho antes de escolher trilha do próximo Reel** (ver
  achado abaixo). Faltou cobrir `ohanabulls_club`, `omundobully` e
  `canilelohimbull`.

**ACHADO em 28/07/2026 — o nicho não roda em música, roda em ÁUDIO ORIGINAL.**
Ideia dele: em vez de pegar a lista de tendências geral do Brasil (que vem cheia
de funk e pop adulto), olhar **o que está dando like em perfil de cachorro**.
Varredura feita (subagente, via navegador): dos Reels de maior alcance do nicho
bully BR — incluindo um de **1 milhão** de views (@guerreirobully) e um de 119
mil (@americanbullymicro) — **4 de 4 usam "Áudio original"**, nenhum usa faixa
licenciada. **Limite declarado: amostra de só 4 Reels em 2 perfis** — o Instagram
não renderizou a grade de 5 dos 7 perfis alvo. Não virou regra ainda, mas aponta
que eu vinha caçando a coisa errada: o gargalo do Reel pode ser o gancho e o som
da cena, não a trilha.

**Recusas de trilha nesta rodada (todas dele):** *Legado (feat. Chorão)* —
Marcelo Falcão; *Lua de Cristal* — Xuxa; *Animal* — KATSEYE. As duas primeiras
por artista (viraram veto permanente na skill, junto com Anitta); a terceira
depois de ouvir. **Regra nova que ele deu: sem ouvir, ele não decide trilha** —
proposta por descrição não serve. Caminho para ele ouvir música de gravadora:
abrir o `on_platform_audio_preview_link` no Chrome da Hana (a página do áudio tem
player). Está registrado na skill como regra 3g.

**Aguardando o Ramón:**
- **Decidir se monta a biblioteca de 12 trilhas** (US$ 0,48 no crédito do
  Gemini) ou fica só com as 3 atuais.
- **Decidir se publica o Reel de 10/08 como "Reel de teste"** (trial reel: só
  não-seguidores veem, não aparece no perfil) para conferir o resultado com a
  trilha antes de valer. É a única forma de ver o Reel montado com o áudio.

**DECIDIDO em 28/07/2026 — posicionamento do perfil: "A PATROA MIMADA".**
Ele escolheu entre duas opções que apresentei. A Hana manda na casa, o Ramón
obedece; humor com atitude, ele no papel de "funcionário". Descartada a opção
"fofa premium" (beleza/cor rara), com o argumento que ele aceitou: **fofura é o
piso do nicho, não diferencial** — todo Exotic Bully é fofo, e foto bonita
concorre com todo mundo. Personalidade é o que faz seguir. A bio já vinha
apontando para lá ("A patroa: aqui quem manda sou eu"). Isso agora manda em
legenda, escolha de cena, gancho de Reel e **escolha de trilha**.

**PROVADO em 28/07/2026 — áudio de tendência via API FUNCIONA.**
Era o gargalo de alcance do projeto e caiu. O que foi feito e testado na tela:
- **A Audio API é oficial** (`developers.facebook.com/docs/instagram-platform/
  content-publishing/audio-api/`) — eu vinha tratando como "indício de
  integradores"; é documentação da Meta.
- **App novo `Hana Audio` criado** (id `2297820570982525`), ligado ao portfólio
  `616358434290372`. Foi preciso porque o app antigo **"Hana Social" recusa** as
  permissões do fluxo Facebook Login ("Ocorreu um erro" em toda tentativa) — ele
  nasceu no fluxo Instagram Login e os dois não convivem no mesmo app.
  **O publicador não foi tocado**: `IG_ACCESS_TOKEN` e fluxo de sempre intactos.
- **Token gerado** pelo Facebook Login com `instagram_basic`,
  `instagram_content_publish` e `pages_show_list`. O ig-user-id por esse caminho
  é **`17841471483838197`** (diferente do `27631851599815469` do Instagram Login).
- **Busca de faixas em alta funcionou**: devolveu música brasileira licenciada
  (Marcelo Falcão, Anitta/Los Brasileiros, Anitta/Alceu Valença).
- **Anexar funcionou**: container do Reel de 10/08 criado com
  `audio_configuration` e chegou a `status_code: FINISHED` — "pronto para
  publicar". **Nada foi publicado** (não chamei `media_publish`).
- **Limites que ficaram claros:** `download_url` é **null** para música de
  gravadora, então **não dá para montar prévia local** do vídeo com a faixa; e a
  Meta não oferece pré-visualização do Reel com áudio — só publicando.
- **Consequência:** cai a pendência antiga de "publicar Reel pelo celular para
  ter áudio de tendência". A automação faz sozinha.

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
