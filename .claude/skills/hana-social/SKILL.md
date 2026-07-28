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

1. **A estrela é a Hana.** O Ramón pode aparecer, mas nunca é o assunto. Régua:
   se a Hana puder ser cortada do quadro sem mudar a piada, o post está errado.
2. **Nada é publicado sem o "aprovado" dele.** A automação prepara, mostra os
   previews numerados e espera. Sem resposta, não sobe.
2b. **COMO mostrar pra ele — não improvisar.** Ele **não enxerga** link do
   `raw.githubusercontent.com`, arquivo anexado na conversa, nem link de página
   publicada: os três já falharam. Gravar as mídias numeradas em
   `OneDrive\Fotos da Hana\03 - APROVAR (semana)` com um `00_LEGENDAS.txt` na
   mesma ordem (ele abre no celular). **Canal principal desde 27/07/2026: o
   Telegram** — bot `@Hanasocial_aproval_bot`, secrets já no GitHub, testado
   ponta a ponta (manda foto/vídeo com botões Aprovar/Recusar e o clique volta).
2c. **Conferir repetição antes de propor.** Abrir o perfil no Chrome, rolar os
   38 posts e comparar cena por cena — inclusive entre os posts do mesmo lote.
   Duas fotos do mesmo passeio em dias diferentes contam como repetido.
3. **Preservar a cor tri lilac merle**; legenda em PT-BR terminando com
   pergunta; máx. 4 hashtags; posts seg/qua/sex às 21:00Z (18h de Itajaí).
4. **Um robô só** (`hana-rotina`: domingo produz o lote, terça e quinta faz a
   ronda de engajamento). Nunca criar agendamento novo — expandir esse.
5. **Fronteira com o projeto Canecas / Brushed & Brewed:** parceria comercial
   sim, interferência não. Não opinar sobre a marca deles, não mexer na pasta
   deles. Ao fornecer fotos, **só a Hana sozinha**, nunca com o Ramón (a imagem
   dele é livre aqui e vedada no projeto comercial confidencial dele).
6. **Verificar qual conta do Instagram está ativa** no Chrome antes de qualquer
   ação — ele alterna entre 3 contas e uma delas é do outro projeto.
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

## 4. ÚLTIMO PASSO, OBRIGATÓRIO: deixar o estado pronto para a próxima conversa

Antes de encerrar qualquer sessão em que algo mudou:

1. Atualize `DECISOES.md` — o que foi decidido, o que ficou pendente do Ramón,
   regra nova que ele deu. Mais recente em cima, e **apague o que virou passado**
   para o arquivo não inchar.
2. Rode `python studio/estado.py` para regenerar a foto automática.
3. Commit e push (`git add -A && git commit && git push`), para que o estado
   valha de qualquer máquina e de qualquer conversa nova.

Sem esse passo, a próxima conversa começa cega. É a parte que faz a skill se
manter viva.
