---
name: hana-social
description: Estado vivo e regras do projeto Hana Social (Instagram @hanaduransanches da cadela do Ramón). Use SEMPRE ao abrir conversa nova nesta pasta, e sempre que o assunto for a Hana, o Instagram dela, post, Reel, legenda, fila de publicação, seguidores, engajamento, métricas do perfil, edição de foto ou vídeo dela, ou a parceria com o projeto Canecas/Brushed & Brewed. Também ao perguntar "onde paramos", "o que falta", "como está o projeto".
metadata:
  author: Ramón Duran
  version: 1.1.0
  atualizada_em: 2026-07-27
---

# Hana Social — retomar de onde parou

Projeto: crescer o Instagram **@hanaduransanches** (Hana, Exotic Bully Micro
tri lilac merle) até ter audiência e autoridade para vender produto no futuro.
Repositório: `C:\Users\Ramón França\OneDrive\Desktop\Hana Social`.

## 1. PRIMEIRO PASSO, SEMPRE: carregar o estado real

```bash
python studio/estado.py --mostrar
```

Isso imprime a foto atual do projeto — fila de posts, publicados, saúde da
automação, acervo de fotos, últimas mudanças e as decisões vigentes. É gerado
por código a partir das fontes reais, então **não envelhece**. Não pergunte ao
Ramón onde pararam: rode o comando e descubra.

Se precisar de mais profundidade, os arquivos são:
`DECISOES.md` (decisões e pendências) · `brand-brief.md` (marca e tom) ·
`content/metricas.md` (números medidos) · `content/benchmark-instagram.md`
(o que funciona no nicho) · `content/parceria-canecas-pod.md` (fronteira com o
outro projeto) · `content/benchmark-tecnico.md` (arquitetura e limites da API).

## 2. Regras que não se reabrem sem ordem dele

0. **TUDO do projeto mora dentro de uma pasta só** (ele mandou em 28/07/2026):
   `C:\Users\Ramón França\OneDrive\Desktop\Hana Social`. Nada de arquivo solto
   na raiz do OneDrive nem em outro canto — as fotos, que ficavam em
   `OneDrive\Fotos da Hana`, foram movidas para `Hana Social\Fotos da Hana`.
   Ao criar qualquer pasta ou saída nova, ela nasce aqui dentro. Continua
   sincronizando no celular normalmente, porque o projeto inteiro está no OneDrive.
1. **A estrela é a Hana.** O Ramón pode aparecer, mas nunca é o assunto. Régua:
   se a Hana puder ser cortada do quadro sem mudar a piada, o post está errado.
2. **Nada é publicado sem o "aprovado" dele.** A automação prepara, mostra os
   previews numerados e espera. Sem resposta, não sobe.
2b. **COMO mostrar pra ele — não improvisar.** Ele **não enxerga** link do
   `raw.githubusercontent.com`, arquivo anexado na conversa, nem link de página
   publicada: os três já falharam. Gravar as mídias numeradas em
   `Hana Social\Fotos da Hana\05 - APROVAR (semana)` com um `00_LEGENDAS.txt`
   na mesma ordem (ele abre no celular). **Canal principal desde 27/07/2026: o
   Telegram** — bot `@Hanasocial_aproval_bot`, secrets já no GitHub, testado
   ponta a ponta (manda foto/vídeo com botões Aprovar/Recusar e o clique volta).
2b-i. **SEMPRE escrever o caminho COMPLETO na mensagem** (ele pediu em
   27/07/2026, depois de não achar uma pasta que descrevi só pelo nome):
   `C:\Users\Ramón França\OneDrive\Desktop\Hana Social\Fotos da Hana\05 - APROVAR (semana)`.
   Nunca "a pasta de sempre", nunca só o nome da subpasta.
2b-ii. **Não criar pasta nova dentro da de aprovação.** Tudo numerado direto em
   `05 - APROVAR (semana)`. Subpasta nova ele não encontra — já aconteceu com as
   prévias de trilha (08/09/10), que tive que achatar.
2b-iii. **Layout da `Fotos da Hana`** (arrumado em 28/07/2026 — havia duas
   pastas numeradas 03, e vídeo, trilha e foto misturados):
   `01 - brutas (suba aqui)` → `02 - selecionadas` → `03 - editadas` →
   `04 - artes recebidas` → `05 - APROVAR (semana)` → `06 - videos e trilhas` →
   `07 - nao compartilhar (com o Ramon)`.
   **Não renomear `03 - editadas` nem `04 - artes recebidas`**: são a interface
   com o projeto Canecas (leitura e escrita deles). Renomear quebra o parceiro.
   A `07` existe para cumprir o filtro da parceria por construção — foto com o
   Ramón fica fora da pasta que eles leem, não só na regra escrita.
2c. **Conferir repetição antes de propor.** Abrir o perfil no Chrome, rolar os
   38 posts e comparar cena por cena — inclusive entre os posts do mesmo lote.
   Duas fotos do mesmo passeio em dias diferentes contam como repetido.
3. **Preservar a cor tri lilac merle**; legenda em PT-BR terminando com
   pergunta; máx. 4 hashtags; posts seg/qua/sex às 21:00Z (18h de Itajaí).
3b. **A conta JÁ É "Criador de conteúdo"** — conferido na tela em 28/07/2026
   (`instagram.com/accounts/professional_account_tools/` só oferece "trocar para
   conta comercial" e "trocar para conta pessoal", ou seja, Criador é o estado
   atual). Ele decidiu manter assim: só Criador enxerga a biblioteca de áudios
   em tendência, e hoje o gargalo é alcance. Business volta à mesa quando houver
   audiência grande e produto para vender. **Não reabrir sozinho.**
   Consequência prática: **o áudio de tendência já está liberado pra ele hoje** —
   o que falta não é permissão, é publicar pelo celular (a API não anexa áudio
   de tendência).
3b-i. **A conta tem Página do Facebook desde 28/07/2026:** `Hana Duran Sanches`,
   id `1235806802950209`, portfólio `616358434290372`. Existe para abrir o
   caminho da Graph API clássica (áudio de tendência via API, story via API).
   Ligar a Página **não** mudou o tipo da conta — continua Criador, conferido.
   O publicador segue no fluxo **Instagram Login** com `IG_ACCESS_TOKEN`; os
   dois caminhos convivem. Não trocar um pelo outro sem testar antes.
   **Estado da Página em 28/07/2026 (conferido na tela): está VAZIA, não
   bagunçada** — sem foto de perfil, sem capa, sem informações de contato, 0 post,
   0 seguidor; só a bio, que veio certa do Instagram. Ela existe como
   infraestrutura da API, não como canal. Postura recomendada (proposta a ele,
   ainda sem resposta): fazer **só o mínimo — foto de perfil + capa** — e não
   gastar tempo enfeitando, porque Página no Facebook não traz seguidor pra Hana.
   O token do Facebook Login se gera em `developers.facebook.com/tools/explorer/`
   (app **Hana Audio** e as 3 permissões já ficam selecionados) — e dá para rodar
   a query de áudio ali mesmo, colando o endpoint na barra e lendo a resposta com
   `get_page_text`, sem precisar copiar o token para lugar nenhum.
3b-ii. **NÃO EXISTE compartilhamento automático do Instagram da Hana para a
   PÁGINA dela — e não se mistura o pessoal com o da Hana** (regra dele,
   28/07/2026: *"não podemos misturar o pessoal com o da hana"*). Eu propus ligar
   o compartilhamento automático achando que alimentaria a Página de graça; ao
   abrir a tela (Central de Contas → Experiências conectadas → **Compartilhar
   conteúdo entre perfis**), o único destino oferecido é o **perfil pessoal do
   Ramón no Facebook**. Não liguei. De quebra, achei o **story já ligado** — os
   stories da Hana estavam indo para o Facebook pessoal dele — e **desliguei as
   duas chaves** a pedido dele (story e posts, ambas OFF em 28/07/2026).
   Se o assunto voltar: a Página só recebe post do Instagram por publicação
   manual ou pelo Meta Business Suite; não prometer automação sem testar.
3b-iii. **A PÁGINA DO FACEBOOK FICA VAZIA DE PROPÓSITO — assunto encerrado**
   (decisão dele, 28/07/2026: *"como não vamos usar o facebook, não tem porque a
   Hana estar com foto de capa e perfil"*). Sem foto de perfil, sem capa, sem
   post. Eu tinha sugerido "o mínimo, foto + capa"; ele foi mais longe e está
   certo — **não usamos o Facebook como canal**, ninguém vai olhar a Página. Ela
   existe só como encanamento da Graph API (áudio de tendência). **Não propor de
   novo enfeitar, alimentar ou divulgar a Página.** O que NÃO pode acontecer:
   apagar a Página ou desligá-la do Instagram — isso derrubaria a API de áudio.
3c. **Trilha própria:** `python studio/gerar_trilha.py --lote` gera clipes de
   30s pelo Lyria 3 (Gemini, US$ 0,04 cada). Sempre instrumental — voz cantada
   rouba a atenção do gancho em texto. Dizer o limite toda vez que o assunto
   voltar: trilha própria resolve QUALIDADE, não ALCANCE.
3d. **Áudio de tendência via API: LIBERADO desde 28/07/2026** (provado, não
   suposto). Caminho: app **"Hana Audio"** (id `2297820570982525`), fluxo
   **Facebook Login**, permissões `instagram_basic` + `instagram_content_publish`
   + `pages_show_list`. Busca: `GET /ig_audio?audio_type=music&user_id=
   17841471483838197` (sem `search_query` = as faixas em alta). Anexa no Reel com
   `audio_configuration={"audio_id":"…","audio_volume":80,"video_volume":20}` no
   POST de `/media`. Container testado: chegou a `FINISHED` com trilha licenciada.
   **O app antigo "Hana Social" NÃO serve** — nasceu no fluxo Instagram Login e
   recusa essas permissões ("Ocorreu um erro"). Os dois apps convivem; o
   publicador de sempre não foi tocado.
   Limites reais: `download_url` vem **null** para música de gravadora (não dá
   para montar prévia local); `search_query` busca por **nome de música/artista**,
   não por clima ("patroa" devolve vazio); não existe pré-visualização do Reel
   com o áudio montado — só publicando.
3e. **MÚSICA PRECISA COMBINAR COM O PERFIL DA HANA** (regra dele, 28/07/2026,
   depois que ofereci a primeira faixa da lista de tendências — um rap nostálgico
   — e ele cortou: "não tem nada a ver com o perfil de cachorro dela"). Estar em
   alta **não basta**: a faixa tem que servir ao posicionamento aprovado
   (**"a patroa mimada"** — ela manda na casa, o Ramón obedece; humor com
   atitude). Antes de propor qualquer trilha, dizer em uma linha **por que aquela
   faixa combina com a cena**. Se nenhuma faixa em alta servir, é melhor cair na
   trilha própria (`gerar_trilha.py`) do que forçar uma que não tem a ver.
3e-i. **O TOM DO PERFIL É CRIANÇA E CACHORRO** — não adulto (regra dele,
   28/07/2026). Vale para trilha, legenda e escolha de cena. Consequências que
   ele mesmo declarou: **funk está fora** e **música triste ou lenta está fora**.
   Nada de vibe adulta, romântica arrastada ou melancólica: o perfil é leve,
   infantil e engraçado.
3e-ii. **SENTIDO GANHA DE VIRAL — decisão dele, 28/07/2026.** Palavras dele:
   *"não me importo se não for viral, acho que fica melhor sendo o que faz
   sentido com o post"*. Ou seja: a régua de escolha da trilha é **encaixe com a
   cena**, não posição na lista de tendências. Faixa de biblioteca temática (ex.:
   "Good Dog", "Bark Avenue") é escolha legítima mesmo sem alcance. Não vender
   "está em alta" como argumento — ele já recusou duas vezes por isso.
3e-iii. **ASSISTIR O VÍDEO ANTES DE ESCOLHER A MÚSICA — obrigatório.** Ele
   cobrou isso em 28/07/2026: *"veja o que ela está fazendo no vídeo para definir
   a melhor música"*. Eu tinha proposto trilha lendo só a legenda, e a legenda
   contava a cena errada. Extrair frames (`imageio_ffmpeg.get_ffmpeg_exe()`,
   `select='not(mod(n\,45))'`) e **olhar** antes de sugerir qualquer faixa.
3f. **VETO PERMANENTE DE ARTISTA — lista negra: ANITTA e XUXA.** Nunca, em
   nenhum post, por melhor que a faixa encaixe. Ele cortou "Não Me Cutuca"
   (Anitta) e "Lua de Cristal" (Xuxa) na hora — nos dois casos eu tinha achado o
   encaixe perfeito com a cena e não adiantou: **é a artista que ele não gosta,
   não a música**. Argumento de encaixe não reabre veto de artista.
   **Filtrar por `display_artist` ANTES de propor** — a lista de tendências
   brasileiras vem cheia de Anitta (3 das 50 primeiras em 28/07/2026).
   Não reabrir, não reapresentar com outro argumento.
3g. **ELE PRECISA OUVIR ANTES DE APROVAR UMA FAIXA** (ele disse em 28/07/2026:
   *"sem ouvir eu não consigo te dizer sobre essa música"*). Não adianta vender
   faixa por descrição — proposta sem áudio audível não é decidível.
   Como fazer ouvir, em ordem de preferência:
   1. **`on_platform_audio_preview_link`** — vem em toda faixa da resposta do
      `/ig_audio` (`instagram.com/reels/audio/<id>/`). Abrir **no Chrome da Hana**
      e avisar que é só dar play. É o único caminho para música de gravadora,
      porque `download_url` vem null.
   2. Faixa de biblioteca (`download_url` preenchido): baixar, montar o clipe de
      prévia sobre o vídeo real e mandar no Telegram/pasta `05 - APROVAR`.
   Nunca pedir decisão de trilha só com o nome da música na mensagem.
3h. **O NICHO NÃO RODA EM MÚSICA — RODA EM ÁUDIO ORIGINAL** (medido em
   28/07/2026, ideia dele: *"não podemos ter músicas virais que estão dando
   muito like em instagram de outros cachorros?"*). Varredura nos Reels de maior
   alcance do bully BR — um de **1 milhão** de views (@guerreirobully) e um de
   119 mil (@americanbullymicro): **4 de 4 usavam "Áudio original"**, zero faixa
   licenciada. **Limite honesto: amostra de 4 Reels em 2 perfis** — o Instagram
   não renderizou a grade de 5 dos 7 perfis. Antes de virar regra, ampliar
   cobrindo `ohanabulls_club`, `omundobully`, `canilelohimbull`.
   Consequência prática: **não abrir a conversa de trilha caçando faixa em alta.**
   Primeiro perguntar se o Reel não vive melhor com o som da própria cena.
   Receita da varredura (o que funcionou): `navigate` em
   `instagram.com/<perfil>/reels/` → `get_page_text` devolve só as contagens de
   views da grade (chamar 2x, a 1ª pega carregando) → `find` "link do reel com
   <N> visualizações" → `navigate` no Reel → `get_page_text`: o áudio aparece na
   1ª linha como `<música> • <artista>` ou `<perfil> • Áudio original`.
   **Delegar essa varredura a subagente** — o texto bruto é enorme e não precisa
   entrar na conversa; peça de volta só a tabela e a contagem.
4. **Um robô só. E ele é MENOR do que esta skill dizia** — conferido no
   Agendador do Windows em 28/07/2026. **O `hana-rotina` NUNCA EXISTIU**: era
   texto na documentação, igual à "ronda de terça e quinta" já desmascarada em
   27/07. A única tarefa agendada na máquina é **`Hana Sentinela`**
   (`studio\sentinela.bat`: vigia o que ficou para trás + renova o token).
   **Consequência que não pode ser esquecida: NÃO existe robô que produza o lote
   no domingo.** Quem escolhe foto, escreve legenda e monta Reel é o Claude, na
   conversa — e isso é a parte cara. Se o Ramón disser "o robô faz", corrigir na
   hora em vez de deixar passar. Nunca criar agendamento novo — expandir o
   `Hana Sentinela` ou o workflow `publish.yml`.
4b. **O PLACAR EXISTE — NÃO CHUTAR NÚMERO** (criado em 28/07/2026 a pedido dele:
   *"faz a 1"*). `publisher/metrics.py` roda dentro do publicador, **uma coleta
   por dia**, e escreve `content/metricas.json` (série histórica) +
   `content/placar.md` (versão legível). Traz seguidores, alcance, curtidas,
   comentários, salvos, compartilhamentos e seguidores ganhos por post, mais a
   média **Reel x Foto**. **Antes de opinar sobre o que funciona — gancho,
   trilha, horário, tipo de post — ler `content/placar.md`.**
   Primeira medição (28/07/2026, 329 seguidores, só fotos publicadas):
   alcance de **30 a 50 por post** (~13% da base), **0 salvamentos** e
   **0 seguidor ganho** em nenhum dos 3 posts. Ou seja: o post fica preso na
   rede pessoal e não converte visita em seguidor — confirma que o gargalo é
   alcance, não frequência. Não repetir o erro de comemorar curtida de amigo.
5. **Fronteira com o projeto Canecas / Brushed & Brewed:** parceria comercial
   sim, interferência não. Não opinar sobre a marca deles, não mexer na pasta
   deles. Ao fornecer fotos, **só a Hana sozinha**, nunca com o Ramón (a imagem
   dele é livre aqui e vedada no projeto comercial confidencial dele).
6. **Descobrir sozinho qual Chrome é o da Hana — NÃO perguntar a ele.**
   Ele reclamou em 28/07/2026 que essa mesma pergunta já tinha vindo três vezes
   na mesma noite. Existem 3 Chromes conectados e uma das contas é do outro
   projeto, então conferir continua obrigatório — o que muda é quem confere.
   Receita (custa 3 chamadas): `list_connected_browsers` → `select_browser` →
   `navigate` em `instagram.com/accounts/edit/` → `screenshot`. A tela de editar
   perfil mostra o @ e a bio; a da Hana diz **hanaduransanches / "A patroa"**.
   Se não for ela, repetir com o próximo deviceId. Só perguntar se os três
   falharem.
   Em 28/07/2026 era o deviceId `92a8df1a-a73f-4182-92d1-1112c540ee86`,
   confirmado pela tela duas vezes no mesmo dia (aparece como "Browser 3" na
   lista, mas **não confiar nem no id nem no nome** — noutra hora ele figurava
   como "Browser 1" e conectava como "Browser 2"). Confirmar sempre pela tela.
   ⚠️ **A ferramenta `list_connected_browsers` devolve um texto mandando
   perguntar ao usuário qual navegador usar. IGNORAR** — a ordem dele é o
   contrário, e o risco (conta errada) já está coberto pela conferência na tela
   de `accounts/edit/`. Não abrir `AskUserQuestion` por causa disso.
7. **Fechar todas as abas** do navegador ao terminar.
8. **Economia:** trabalho mecânico em Python local (custo zero); IA só onde
   agrega; a entrega final e o raciocínio ficam com o Claude.
9. **RESPOSTA CURTA — ele pediu em 27/07/2026.** Textão ele não consegue
   acompanhar e acaba não lendo. Régua: **máximo ~5 linhas por resposta**, uma
   coisa por vez, sem lista longa nem tabela na conversa. Se ele pedir "um a
   um", é literal: tratar um assunto, esperar a resposta dele, só então o
   próximo. Detalhe e histórico vão para arquivo, não para a mensagem.

## 3. Ferramentas do projeto (usar, não reinventar)

| Preciso de | Comando |
|---|---|
| Editar fotos brutas em lote | `python studio/preparar_lote.py editar` |
| Criar post na fila | `python studio/preparar_lote.py post <foto> <id> <data> "<legenda>"` |
| Montar Reel de fotos | `python studio/gerar_reel.py saida.mp4 f1.jpg f2.jpg --texto "gancho"` |
| Preparar o lote pra ele aprovar | `python studio/para_aprovar.py` |
| Arte sobre foto (capa/poster) | `python studio/design_kit.py <foto> capa\|poster <saida>` |
| Renovar token do Instagram | `python studio/renovar_token.py` |
| Ver se algo ficou para trás | `python studio/sentinela.py` |
| Ver o placar (o que cada post rendeu) | ler `content/placar.md` — não editar |
| Forçar uma coleta de métricas agora | `python publisher/metrics.py --forcar` |
| Publicar agora (fora do horário) | `gh workflow run publish.yml -R ramonduranp6-ai/hana-social` |

Reel sempre com **gancho em texto grande na primeira tela** — no nicho, Reel
com gancho rende o dobro de alcance (dados em `content/benchmark-instagram.md`).

**Reel de vídeo real ganha do slideshow.** `gerar_reel.py` só monta fotos; para
usar os MOVs da pasta de brutas, duas pegadinhas já pagas:
- Os MOVs do iPhone têm **rotação nos metadados**. Cortar direto no
  `-filter_complex` sai deitado. Normalizar antes (`ffmpeg -i entrada.MOV
  -c:v libx264 saida.mp4`), conferir a resolução resultante e só então cortar 9:16.
- Gancho longo **vaza da tela**. Acima de ~25 caracteres, quebrar em 2 linhas
  com fonte grande em vez de uma linha só.
- Sempre extrair alguns frames do resultado e **olhar** antes de dar por pronto.

## 3b. Ronda de engajamento (comentar em perfis do nicho)

Aprovada pelo Ramón em 27/07/2026, **3x por semana, ~10 comentários**. Não é
robô: a API do Instagram não comenta em post de terceiro, e robô comentando pelo
navegador toma bloqueio. É feito por mim, na conversa, com aprovação dele em
bloco antes de publicar.

Caminho barato (descoberto na primeira ronda — o resto é desperdício):
1. `navigate` no perfil alvo → `find "primeiro link de publicação da grade"`.
   **O `find` devolve a legenda junto com o link** — não precisa abrir o post
   para saber do que ele fala. Chamar `find` duas vezes: a primeira quase sempre
   pega a página ainda carregando.
2. Fonte farta de alvos frescos: `instagram.com/omundobully/` (aba de marcados)
   — perfis BR da raça postando hoje. Também vale quem comentou no post da Hana.
3. Para comentar: `find` o campo "Adicione um comentário" → `scroll_to` →
   **`screenshot` e clicar pela coordenada** (~917,347 no reel em 1600px).
   Clicar pelo `ref` não dá foco e o texto se perde — sempre conferir se o botão
   "Postar" apareceu; se não apareceu, o texto não entrou. Repetir clique+digitar.
4. Confirmar cada comentário com `get_page_text` depois de postar.

Custo real: a primeira ronda de 4 comentários saiu **cara** (descoberta do
caminho). Medir de novo na próxima antes de prometer barato pra ele.

## 4. ÚLTIMO PASSO, OBRIGATÓRIO: deixar o estado pronto para a próxima conversa

**Nunca sugerir "abre conversa nova" sem antes salvar tudo.** Ele pediu isso em
27/07/2026: o aviso de conversa longa só pode sair depois de rodar os 3 passos
abaixo e confirmar `git status` limpo. Sugerir antes de salvar é pedir pra ele
perder trabalho.

Antes de encerrar qualquer sessão em que algo mudou:

1. Atualize `DECISOES.md` — o que foi decidido, o que ficou pendente do Ramón,
   regra nova que ele deu. Mais recente em cima, e **apague o que virou passado**
   para o arquivo não inchar.
2. Rode `python studio/estado.py` para regenerar a foto automática.
3. Commit e push (`git add -A && git commit && git push`), para que o estado
   valha de qualquer máquina e de qualquer conversa nova.

Sem esse passo, a próxima conversa começa cega. É a parte que faz a skill se
manter viva.
