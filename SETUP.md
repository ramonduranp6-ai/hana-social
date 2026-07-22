# SETUP — o que só o Ramón pode fazer

O código está pronto. Falta a parte que exige suas contas e cliques.
Faça na ordem. No fim, cadastre tudo como **Secrets** no GitHub.

---

## 1. Conta Instagram (5 min)
- No app do Instagram da Hana: **Configurações → Tipo de conta → mudar para
  Comercial (Business)** ou Criador.
- Ligue a conta a uma **Página do Facebook** (crie uma grátis se não tiver;
  pode ser "Hana Duran Sanches").

## 2. App na Meta e token (a parte chata, ~30–60 min)
1. Entre em https://developers.facebook.com → **My Apps → Create App** → tipo
   "Business".
2. Adicione o produto **Instagram Graph API** (ou "Instagram" → API com login do Facebook).
3. Em **Graph API Explorer**, gere um token de usuário com as permissões:
   `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
   `pages_read_engagement`, `business_management`.
4. Troque o token curto por um **token de longa duração** (~60 dias):
   ver "Long-lived tokens" na doc. Guarde-o → vira `IG_ACCESS_TOKEN`.
5. Descubra o **id numérico** da conta Instagram (`IG_USER_ID`): no Graph API
   Explorer, chame `me/accounts` → pegue o id da Página → depois
   `<PAGE_ID>?fields=instagram_business_account`.
6. **App Review / Verificação de negócio:** pra publicar de forma contínua a
   Meta pode exigir revisão do app e verificação do seu negócio. É o único
   ponto imprevisível. Enquanto o app está em modo de desenvolvimento, você
   (como admin/testador) consegue publicar na sua própria conta pra testar.

> ⚠️ O token de longa duração **vence a cada ~60 dias**. Quando vencer, os posts
> param calados. Anote pra renovar, ou depois a gente automatiza a renovação.

## 3. Bot do Telegram (10 min) — o seu "só aceite"
1. No Telegram, fale com **@BotFather** → `/newbot` → dê um nome. Ele te dá o
   **token** → vira `TELEGRAM_BOT_TOKEN`.
2. Mande qualquer mensagem pro seu novo bot (pra abrir conversa).
3. Descubra seu **chat id**: acesse no navegador
   `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates` e pegue o número em
   `chat.id` → vira `TELEGRAM_CHAT_ID`.

## 4. Hospedagem da mídia (`MEDIA_BASE_URL`)
A Graph API baixa a imagem/vídeo de uma **URL pública**. Opção mais simples e
grátis: manter as mídias num repositório **público** e usar a URL `raw`.
- Se este repositório for público:
  `MEDIA_BASE_URL = https://raw.githubusercontent.com/<owner>/<repo>/<branch>`
- Se preferir manter privado, a gente usa um bucket público (Cloudflare R2 grátis)
  — me avisa que eu adapto o código.

## 5. Cadastrar os Secrets no GitHub (5 min)
No repositório: **Settings → Secrets and variables → Actions → New repository secret**.
Crie um secret pra cada:

| Secret | Valor |
|---|---|
| `IG_USER_ID` | id numérico da conta Instagram |
| `IG_ACCESS_TOKEN` | token de longa duração |
| `MEDIA_BASE_URL` | base pública das mídias |
| `TELEGRAM_BOT_TOKEN` | token do bot |
| `TELEGRAM_CHAT_ID` | seu chat id |

(Opcional) Em **Variables**, `REQUIRE_APPROVAL = 1` (aprovar antes) ou `0` (direto).

## 6. Testar
- Em **Actions → Publicar posts da Hana → Run workflow** (disparo manual).
- Você deve receber no Telegram o post de teste pra aprovar.
- Aprovando, na próxima rodada (ou se o horário já passou) ele publica.

---

### O que me traz de volta
Quando tiver os 5 valores da tabela, me avisa. Se a Meta travar na revisão do
app, me manda o print do erro que eu te ajudo a resolver. O resto do código
(publicar, agendar, aprovar) já está feito.
