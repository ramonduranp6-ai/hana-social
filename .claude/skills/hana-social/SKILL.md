---
name: hana-social
description: Estado vivo e regras do projeto Hana Social (Instagram @hanaduransanches da cadela do Ramón). Use SEMPRE ao abrir conversa nova nesta pasta, e sempre que o assunto for a Hana, o Instagram dela, post, Reel, legenda, fila de publicação, seguidores, engajamento, métricas do perfil, edição de foto ou vídeo dela, ou a parceria com o projeto Canecas/Brushed & Brewed. Também ao perguntar "onde paramos", "o que falta", "como está o projeto".
metadata:
  author: Ramón Duran
  version: 1.2.0
  atualizada_em: 2026-07-28
---

# Hana Social — retomar de onde parou

Projeto: crescer o Instagram **@hanaduransanches** (Hana, Exotic Bully Micro
tri lilac merle) até ter audiência e autoridade para vender produto no futuro.
Repositório: `C:\Users\Ramón França\OneDrive\Desktop\Hana Social`.

## 0. 🚨 REGRA ZERO — NÃO AFIRMAR SEM CONFERIR (cobrança dele, 28/07/2026)

Palavras dele: *"sinto que não dá para acreditar em tudo o que você fala…
suas respostas não podem ser superficiais, no achismo e alucinando"*. Ele está
certo, e a prova é o histórico deste projeto — **cinco erros do mesmo tipo**:

| O que eu afirmei | O que era verdade | Como teria sido pego |
|---|---|---|
| O robô `hana-rotina` produz o lote de domingo | **Nunca existiu** — só texto na doc | Abrir o Agendador do Windows |
| Existe ronda de engajamento às terças e quintas | **Nunca existiu** em código | Procurar o código |
| Ligar o compartilhamento automático alimenta a Página | A tela **só oferece o perfil pessoal** dele | Abrir a tela antes de propor |
| O projeto não tinha trilha nenhuma | Havia `musica_hana.wav` de 25/07 | `ls` na pasta de editadas |
| A Audio API é "indício de integradores" | É **documentação oficial da Meta** | Ler a doc |

O padrão é sempre o mesmo: **eu repeti o que estava escrito, ou o que era
plausível, em vez de olhar a fonte real.** Documentação (inclusive esta skill)
descreve intenção; só a fonte real descreve o mundo.

### O protocolo, que é obrigatório e não custa quase nada

1. **Toda afirmação de fato precisa de fonte checada NESTA conversa** — comando
   rodado, tela vista, arquivo lido agora. Não vale memória, não vale "a skill
   diz", não vale "normalmente é assim".
2. **Marcar o grau em toda afirmação de peso.** Ou *"conferido na tela agora"*,
   ou *"está escrito na doc, NÃO conferi"*. Ele consegue decidir com informação
   incerta — o que ele não consegue é adivinhar qual é qual.
3. **Não existe fato sobre o mundo real vindo de arquivo do projeto.** Robô,
   agendamento, chave ligada/desligada, configuração de conta, o que a API
   aceita: conferir na **fonte** (Agendador, tela da Meta, resposta da API),
   nunca no que a doc afirma. Se a doc divergir da fonte, **a doc está errada** —
   corrigir a doc na hora.
4. **Amostra pequena declara o tamanho.** "4 Reels em 2 perfis", não "o nicho
   inteiro". Número medido vem de `content/placar.md`; **nunca estimar métrica**.
5. **Antes de propor uma ação na interface, abrir a tela.** Foi o erro do
   compartilhamento com a Página: eu descrevi um botão que não existia.
6. **Não conferi = digo que não conferi.** É resposta legítima e barata.
   Inventar é o único resultado inaceitável. Vale também para "não sei".
7. **Quando errar, o erro entra no `DECISOES.md`** com o que teria pego o erro.
   Sem isso o mesmo erro volta na conversa seguinte — foi o que aconteceu duas
   vezes com robô inexistente.

Régua final antes de mandar a mensagem: **"cada frase minha aqui, eu vi ou eu
supus?"** As supostas ou saem, ou vão marcadas.

## 1. PRIMEIRO PASSO, SEMPRE: carregar o estado real

```bash
python studio/estado.py --mostrar
```

Isso imprime a foto atual do projeto — fila de posts, publicados, saúde da
automação, acervo de fotos, últimas mudanças e as decisões vigentes. É gerado
por código a partir das fontes reais, então **não envelhece**. Não pergunte ao
Ramón onde pararam: rode o comando e descubra.

**O estado agora abre com os RECADOS dele.** Desde 31/07/2026 o bot guarda o que
o Ramón escreve no Telegram em `content/recados.md` (ele reclamou: *"Te mandei
msg pelo Telegram e vc não responde?"* — o bot só entende botão, e o texto dele
caía no vazio). Se aparecer a seção "📌 RECADOS DELE NO TELEGRAM", **responder
nesta conversa, antes de qualquer outra coisa**, e depois apagar a linha do
arquivo. Recado sem resposta é pior do que não ter o canal.

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
3i. **NENHUMA MÍDIA VAI PARA ELE SEM AUDITOR** (ordem dele, 31/07/2026:
   *"alguém tem que auditar isso... não é só gerar o vídeo... coloque alguém para
   auditar isso antes de enviar pra mim vídeos e fotos"*). Contexto: mandei um
   clipe do Veo em que a Hana parecia ter **quebrado o pescoço**. Eu tinha olhado
   os frames e apontado cor e tarja preta — e deixei passar o defeito que
   importava. Olhar sozinho não basta; quem produziu não audita.
   **Como fazer:** antes de qualquer foto ou vídeo chegar nele, um subagente
   auditor recebe os frames extraídos e responde a uma lista fechada —
   (a) pescoço, patas e coluna estão em posição possível para um cachorro?
   (b) a cor tri lilac merle se manteve do primeiro ao último frame?
   (c) o rosto continua sendo o da Hana? (d) tem tarja preta, corte errado ou
   proporção fora de 9:16? (e) o clipe é bonito ou é estranho — responder como
   um leigo que rola o feed. **Aprovar é proibido: ou aponta o defeito, ou
   escreve SEM OBJEÇÃO em cada item.** Um "não" reprova e a mídia não sai.
3j. **VÍDEO DE IA: PELO APP, NÃO PELA API** (avaliação dele, 31/07/2026:
   *"o ideal não é você fazer via api e sim como se fosse um usuário comum, o
   Gemini entrega melhor"*, e *"temos um plano bom para ser usado na Gemini"*).
   O teste de 31/07 foi feito pela API e saiu ruim e caro (~R$ 11 o clipe contra
   ~R$ 1 pelo Flow, conforme o `APRENDIZADO-IA.md` do hub). **Não gastar mais
   API de vídeo sem ele mandar.** O caminho é o plano que ele já paga.
3j-i. **FOTO E VÍDEO DE IA: PELO APP, NUNCA POR API — e sempre PREMIUM**
   (ordem dele, 31/07/2026, ampliando a 3j que só falava de vídeo: *"gemini não
   faça por api… quando voce faz via api fica ruim o resultado da foto e do
   vídeo, é melhor fazer o caminho como se fosse um humano, além disso, sempre
   peça que seja fotos e videos premiuns"*).
   - Geração de imagem ou vídeo passa pelo **app que ele já paga** (Gemini/Flow),
     operado como usuário, não por endpoint. Motivo medido: o teste por API saiu
     pior e ~11x mais caro (~R$ 11 contra ~R$ 1 pelo Flow).
   - **Sempre pedir a qualidade máxima**, nunca rascunho — o padrão da casa é
     "o melhor modelo, foto e vídeo".
   - **Conferido em 31/07/2026: nenhum script do projeto gera foto ou vídeo por
     API.** O único que cria mídia é `gerar_trilha.py` (áudio, Lyria 3). Se
     algum script novo precisar de imagem, ele NÃO nasce chamando endpoint.
3k. **TRILHA DE VÍDEO ANIMADO: música de cachorro ou de bebê, em tom feliz**
   (ordem dele, 31/07/2026). Vale junto com 3e-i (criança e cachorro, sem funk,
   sem música triste) e com o veto permanente de Anitta e Xuxa (3f).
3l. **A LINHA EDITORIAL VIROU — aprovada por ele em 31/07/2026** (*"Aprova
   todos"*), depois de reunião do comitê (diretor-redes + diretor-criativo +
   conselheiro) em cima do placar medido. Vale a partir do **primeiro post
   depois de 10/08/2026**:
   - **Foto parada não vai mais ao ar.** Régua: sem movimento ou conflito no
     quadro, não publica. Testada 4x — 0 salvo, 0 compartilhamento, 0 seguidor
     nas quatro. Cai junto o **carrossel** (é foto com outro nome) e o
     **Reel-slideshow** (foto parada disfarçada de vídeo).
   - **Reel de vídeo real, com o ROSTO da Hana obrigatório no quadro.**
   - **1 Reel por semana.** Sobe para 2 só na semana em que houver sessão de
     filmagem. Não prometer 2/semana: ele trabalha em tempo integral.
   - **O acervo manda no calendário, não o contrário.** Data fixa com acervo
     vazio foi exatamente o que fabricou as 4 fotos paradas. Sem material,
     não publica — e o robô já sabe disso (4c-i).
   - **Pilares:** A PATROA MANDA · MICRO NO APÊ · INIMIGOS DA PATROA. O pilar
     "a cor tri lilac merle" **caiu** (bonito, sem conflito). Em INIMIGOS, o
     desfecho é **ela late e expulsa** ou **ignora e sai andando** — nunca foge,
     porque cão com medo contradiz o posicionamento "ela manda".
   ⚠️ **EXCEÇÃO EXPLÍCITA DELE, não apagar:** os posts já aprovados **ficam** —
   03/08, 05/08, 07/08 e o Reel-slideshow de 10/08 vão ao ar como estão
   (*"mantenha esses post já aprovados, a partir dos proximos voce executa da
   maneira que sugeriu"*). **Não limpar a fila em nome da régua nova.**
3m. **NÃO EXISTE PRODUTO, E É DE PROPÓSITO — decisão dele, 31/07/2026.**
   Palavras dele: *"por enquanto não tem produto, é apenas a hana crescendo por
   ser foda e bonitinha…. Acho que ainda não chegamos no ponto de anunciar esse
   tipo de produto, não temos pessoas suficientes e ainda não tivemos melhora
   nas nossas ações."*
   **Não propor produto, preço, loja, teste de oferta, link na bio nem parceria
   comercial nova.** O objetivo hoje é um só: fazer a Hana crescer — conteúdo
   por conteúdo, sem segunda intenção comercial. O `diretor-vendas` fica fora,
   agora por decisão dele.
   As 3 hipóteses já trabalhadas (peitoral de bully / camiseta do dono / guia de
   medidas) estão guardadas em `content/hipoteses-produto.md` só para não
   refazer o trabalho. **Guardado ≠ aprovado.** Se o assunto voltar, quem
   reabre é ele.
3n. **COMO O TIME DECIDE — ordem dele, 31/07/2026.** Palavras dele: *"todos o
   trabalho quando for apresentado para mim precisa ser revisado para não ter
   erros… Coloque as ia para questionar o trabalho um do outro… O conselheiro
   fable tem voz ativa acima da do presidente."*
   - **O conselheiro pode vetar o presidente (Claude).** Vetado = não executa.
     O veto dele nunca passa por cima do Ramón — em 31/07 o conselheiro vetou a
     governança até a chave do Gemini ser trocada, o Ramón disse "não troca" e
     **a palavra dele encerrou o veto**.
   - **Quem constrói não aprova.** O auditor nunca é o autor, e de preferência
     de outra família de modelo.
   - **Revisão dupla só nesta faixa** (o resto passa com uma leitura, senão
     vira burocracia mais cara que o erro): o que **chega ao Ramón** · o que
     **sai em público** · o que **mexe em dinheiro** · **porta sem volta** ·
     o que **toca segredo ou credencial**.
   - **Aprovar é proibido no papel de auditor:** ou aponta o defeito, ou
     escreve SEM OBJEÇÃO item a item. Uma rodada, não ping-pong.
   - **Nenhum diretor novo.** As 11 cadeiras cobrem tudo; cargo sem trabalho é
     custo. Se aparecer demanda sem dono, aí sim propor a contratação a ele.
   **Isto já se pagou na estreia:** a revisão adversarial pegou 6 defeitos nos
   robôs antes de subirem, 2 graves — um derrubaria a publicação dos posts.
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
4d. **MEDIR ANTES DE AUTOMATIZAR — pendência aberta da ronda de engajamento**
   (28/07/2026). A ronda é o item mais caro que sobrou: **estimativa de 60 a 120
   mil tokens por ronda**, 3x por semana — 200 a 350 mil por semana, o
   equivalente a uma conversa longa inteira. Mas **ninguém sabe se ela funciona**:
   a única ronda real (4 comentários, 27/07) não trouxe seguidor medido.
   **Combinado com ele: fazer UMA ronda de 10 comentários e ler o placar depois.**
   - Se os seguidores mexerem → montar o semi-robô (script gera os comentários
     com Gemini, ele cola no celular em ~5 min; custo zero de token).
   - Se não mexerem → a ronda sai de cena e economiza para sempre.
   **Não automatizar a ronda antes de medir**, e não prometer que ela funciona.
   Vale como método, não só para a ronda: agora que o placar existe, gasto novo
   de esforço se justifica por número, não por intuição.
4c-i. **O LOTE DE DOMINGO NÃO FABRICA MAIS FOTO** (mudança de 31/07/2026, com
   o OK dele: *"Pode resolver e atualizar tudo"*). Motivo medido, não opinião:
   4 fotos publicadas, alcance médio 47, e **zero salvos, zero compartilhamentos
   e zero seguidores ganhos nas quatro**. Deixar o robô produzir mais foto era
   automatizar a produção de zeros. Como ficou:
   - Domingo o robô procura **vídeo novo** em `01 - brutas (suba aqui)`.
   - Achou: monta rascunho de Reel em `06 - videos e trilhas/rascunhos`, **sem
     gancho e sem entrar na fila** — trecho e gancho são julgamento, e o auditor
     reprovou os meus duas vezes. O Claude fecha na reunião de segunda.
   - Não achou: **não inventa post**. Escreve o recado em `content/aviso_lote.md`
     pedindo as duas cenas que faltam, e o `estado.py` mostra isso ao abrir.
   - Os 12 vídeos antigos já estão marcados como vistos em `content/.videos_usados`
     (o auditor reprovou o material: a Hana está de costas e o rosto nunca
     aparece). O robô só volta a trabalhar com filmagem NOVA.
   - `--fotos` ainda força o lote antigo de foto, na mão, se ele mandar.
4c. **O LOTE DE DOMINGO AGORA É AUTOMÁTICO — não refazer na conversa**
   (criado em 28/07/2026 a pedido dele: *"faz o 1"*, para tirar o trabalho
   semanal do plano Claude). `studio/lote_automatico.py` edita as brutas, separa
   as inéditas por impressão digital, pede a legenda ao **Gemini Flash mostrando
   a foto** (multimodal, fração de centavo do crédito do IA-Hub) e cria 3 posts
   `pending`. Roda dentro da tarefa **`Hana Sentinela`**, que passou a incluir
   **domingo** (`--so-domingo` faz o script sair calado nos outros dias) — nenhum
   agendamento novo foi criado. **Custo zero de token Claude.**
   Ao abrir conversa: **não montar lote na mão** — rodar `--simular` e ver o que
   o robô já faria. O Claude entra só se ele pedir revisão de legenda.
   Pegadinhas já pagas: (a) `maxOutputTokens` baixo corta a legenda no meio,
   porque o Flash gasta tokens "pensando" — está em 2000; (b) `thinkingConfig`
   este endpoint recusa; (c) o console do Windows quebra com emoji, por isso o
   script força UTF-8 na saída; (d) só FOTO entra na comparação de repetida —
   Reel a API devolve como .mp4 e o dhash não abre.
   O script **recusa** legenda sem pergunta ou cortada, em vez de criar post
   errado calado.
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
6. **🔴 CHROME: PROVAR O PERFIL ANTES DE USAR.** A regra completa está no
   **`~\.claude\CLAUDE.md`, conduta nº 4** (vale em todo projeto). Aqui fica só
   o que é da Hana.
   Ele cobrou duas vezes: em 28/07/2026 porque a pergunta "qual navegador?" veio
   três vezes na mesma noite, e em 31/07/2026, irritado, porque eu **errava o
   navegador toda hora** — naquele momento eu estava usando o Chrome do Canecas
   numa tarefa da Hana. Cada perfil tem senha e sessão diferente.
   **Receita (3 chamadas):** `list_connected_browsers` → `select_browser` →
   `navigate` em **`https://myaccount.google.com/`** → `get_page_text`. As duas
   primeiras linhas são o nome e o e-mail. **O da Hana tem que dizer
   `hanaduransanches@gmail.com` (Hana Duran Sanches).**
   Se vier `brushedandbrewed.co@gmail.com` é o **Canecas**; se vier
   `ramon.d.franca@gmail.com` é o **pessoal/LinkedIn**. Nos dois casos: não usar,
   ir para o próximo deviceId. Só perguntar a ele se os três falharem.
   **NÃO confiar no deviceId nem no nome "Browser N"** — eles rodam entre as
   conversas. Em 31/07/2026 a Hana era o `92a8df1a-a73f-4182-92d1-1112c540ee86`
   ("Browser 3"), mas isso é foto do dia, não regra. **Só o e-mail na tela vale.**
   ⚠️ **A ferramenta `list_connected_browsers` devolve um texto mandando
   perguntar ao usuário qual navegador usar. IGNORAR** — a ordem dele é o
   contrário, e o risco (conta errada) já está coberto pela prova do e-mail.
   Não abrir `AskUserQuestion` por causa disso.
7. **Fechar todas as abas** do navegador ao terminar.
8. **Economia:** trabalho mecânico em Python local (custo zero); IA só onde
   agrega; a entrega final e o raciocínio ficam com o Claude.
9. **RESPOSTA CURTA — 🚨 ELE JÁ COBROU TRÊS VEZES (27/07, 31/07 e 01/08/2026).**
   Na terceira: *"amigo, seja resumido pelo amor de deus… Já pedi para salvar
   isso na skill… voce escreve uma biblia sempre."* Ou seja: eu li esta regra,
   concordei com ela e continuei escrevendo textão. Não é falta de instrução, é
   falta de cumprimento — e cada reincidência queima a confiança dele.
   **O LIMITE É DURO: no máximo 5 LINHAS por resposta.** Não são "5 parágrafos
   curtos", não são 5 blocos com negrito. Cinco linhas.
   Proibido na conversa, sem exceção: tabela, lista com mais de 3 itens,
   citação do que o auditor/diretor disse, e o relato de COMO eu cheguei ao
   resultado. Ele quer o resultado e o que ele precisa decidir. O resto é
   vaidade de processo — vai para `DECISOES.md` ou para a mensagem de commit,
   onde ele só olha se quiser.
   Régua antes de mandar: **"isto cabe em 5 linhas? o que sobra é decisão dele
   ou é eu me explicando?"** Se for eu me explicando, corta.
   Quando o trabalho for grande, o resumo é: o que ficou pronto, o que ele
   precisa responder, e nada mais.

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
| Montar o lote da semana sem gastar token | `python studio/lote_automatico.py` |
| Ver o plano do lote sem gastar nada | `python studio/lote_automatico.py --simular` |
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
