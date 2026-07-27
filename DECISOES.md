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
