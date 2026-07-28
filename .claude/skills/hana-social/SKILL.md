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
3c. **Trilha própria:** `python studio/gerar_trilha.py --lote` gera clipes de
   30s pelo Lyria 3 (Gemini, US$ 0,04 cada). Sempre instrumental — voz cantada
   rouba a atenção do gancho em texto. Dizer o limite toda vez que o assunto
   voltar: trilha própria resolve QUALIDADE, não ALCANCE.
4. **Um robô só** (`hana-rotina`: domingo produz o lote, terça e quinta faz a
   ronda de engajamento). Nunca criar agendamento novo — expandir esse.
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
   Em 28/07/2026 era o deviceId `92a8df1a-a73f-4182-92d1-1112c540ee86` — mas
   **não confiar nem no id nem no nome**: ele aparecia como "Browser 1" na lista
   e conectou como "Browser 2". Confirmar sempre pela tela.
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
