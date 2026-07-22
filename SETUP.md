# SETUP — o que só o Ramón pode fazer

O código está pronto. Falta a parte que exige as suas contas. Faça na ordem.

> **A verdade sobre a Meta:** para publicar de forma contínua, a Meta exige
> **App Review**, que leva **2 a 4 semanas** e é obrigatório pra produção.
> Enquanto isso, você consegue **testar publicando na sua própria conta** em
> modo de desenvolvimento, na hora. Ou seja: dá pra validar já, e a produção
> "full" espera a aprovação. Enquanto a review não sai, o Meta Business Suite
> (grátis, sem código) segue como plano B pra não ficar sem postar.

---

## Decisão que simplifica tudo: precisa de aprovação por Telegram?

- **Modo simples (recomendado pra começar):** sem Telegram. Você aprova o lote
  aqui comigo quando a gente monta os posts, e o sistema publica no horário.
  Menos coisas pra configurar (3 segredos em vez de 5).
  → Basta definir a variável `REQUIRE_APPROVAL = 0` no passo 4.
- **Modo com aprovação no celular:** o bot te manda cada post e você toca ✅.
  Exige criar o bot do Telegram (passo 3B). Dá pra ligar depois.

---

## 1. Conta Instagram (5 min)
No app do Instagram da Hana: **Configurações → Tipo de conta → Comercial
(Business) ou Criador**. Pelo caminho novo, **não precisa de Página do Facebook**.

## 2. App na Meta + token (a parte chata, ~30–60 min)
1. Entre em https://developers.facebook.com → **My Apps → Create App**.
2. Escolha o produto **Instagram → API with Instagram Login** (caminho novo,
   sem Facebook).
3. Configure o **Business Login for Instagram** e conecte a conta da Hana.
4. Peça as permissões (escopos novos): `instagram_business_basic` e
   `instagram_business_content_publish`.
5. Gere o token e troque por um **token de longa duração** (~60 dias).
   → é o `IG_ACCESS_TOKEN`.
6. Pegue o **id da conta** (`IG_USER_ID`): a própria tela de login/te retorna,
   ou chame `GET https://graph.instagram.com/v21.0/me?fields=user_id`.
7. **App Review:** submeta as duas permissões pra revisão (2–4 semanas). Até lá,
   teste no modo desenvolvimento com a sua conta.

> ⚠️ O token vence a cada ~60 dias. Quando vencer, os posts param calados.
> Anote pra renovar (depois a gente automatiza a renovação).

## 3A. (Modo simples) — nada a fazer aqui. Pule pro passo 4.

## 3B. (Opcional) Bot do Telegram — só se quiser aprovar pelo celular (10 min)
1. No Telegram, fale com **@BotFather** → `/newbot` → dê um nome. Ele te dá o
   **token** → `TELEGRAM_BOT_TOKEN`.
2. Mande qualquer mensagem pro seu bot novo.
3. Pegue seu **chat id**: abra no navegador
   `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates` e copie o número em
   `chat.id` → `TELEGRAM_CHAT_ID`.

## 4. Deixar o repositório público (pra hospedar a mídia)
A Meta baixa a imagem/vídeo de uma **URL pública**. O jeito grátis é este repo
ser público (o conteúdo vai pro Instagram mesmo, não é sigiloso).
- No GitHub: **Settings → General → Danger Zone → Change visibility → Public**.
- Aí o valor de `MEDIA_BASE_URL` já é conhecido (eu te passo pronto).
- Se preferir manter privado, me avisa que eu troco pra um bucket grátis.

## 5. Cadastrar os Secrets no GitHub (5 min)
No repo: **Settings → Secrets and variables → Actions → New repository secret**.

Modo simples (3 secrets):

| Secret | Valor |
|---|---|
| `IG_USER_ID` | id da conta Instagram |
| `IG_ACCESS_TOKEN` | token de longa duração |
| `MEDIA_BASE_URL` | (eu te passo depois do repo virar público) |

Ainda em **Variables** (aba ao lado de Secrets), crie:
- `REQUIRE_APPROVAL = 0` (modo simples, sem Telegram)
- `GRAPH_BASE = https://graph.instagram.com/v21.0`

Se for usar Telegram, adicione também os secrets `TELEGRAM_BOT_TOKEN` e
`TELEGRAM_CHAT_ID`, e deixe `REQUIRE_APPROVAL = 1`.

## 6. Testar
- **Actions → Publicar posts da Hana → Run workflow** (disparo manual).
- Modo simples: ele publica o post cujo horário já venceu.
- Modo Telegram: você recebe o post pra aprovar; depois de aprovar, publica.

---

### O que me traz de volta
Quando tiver o **`IG_USER_ID`** e o **`IG_ACCESS_TOKEN`**, e o repo estiver
público, me avisa. Eu te passo o `MEDIA_BASE_URL` pronto e a gente dispara o
teste. Se a Meta travar em algum passo, manda o print do erro.
