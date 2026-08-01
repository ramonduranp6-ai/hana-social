"""
Lote automático semanal — o robô monta a fila, o Ramón só aprova.

Existe para tirar do Claude (e do plano dele) o trabalho semanal repetitivo:
editar as fotos, escolher as inéditas, escrever legenda e criar os posts.
Quem escreve a legenda é o **Gemini Flash** (crédito do IA-Hub, fração de
centavo por foto) — e ele VÊ a foto, porque é multimodal. O Claude só entra se
o Ramón pedir revisão.

Uso:
    python studio/lote_automatico.py --simular     # mostra o plano, não gasta nada
    python studio/lote_automatico.py               # monta o lote de verdade
    python studio/lote_automatico.py --so-domingo   # só roda 1x por semana (ver abaixo)

Depois de rodar, os posts ficam em content/queue/ com status "pending" e o
publicador manda no Telegram para o Ramón aprovar. **Nada é publicado sem o
"aprovado" dele** — este script não muda status nem publica.

--so-domingo, desde 31/07/2026, NÃO significa mais "só roda se hoje for
domingo" — significa "só roda 1x por semana" (controlado pelo arquivo local
`content/.lote_semana_executada`). O nome da flag ficou igual porque
`studio/sentinela.bat` já chama assim; o que mudou foi o SIGNIFICADO: antes,
notebook desligado no domingo fazia a semana inteira sumir sem aviso nenhum
(o script só sabia checar "hoje é domingo?"). Agora o robô cumpre a semana no
primeiro dia em que a máquina estiver ligada, seja qual for.

O pedido de cena (quando falta filmagem) vem de `content/pedido-de-cena.md`,
escrito pelo comitê/Diretor de Criação — NUNCA inventado pelo código. Sem esse
arquivo, o robô cai num texto de reserva e AVISA que é reserva. Ele repete o
mesmo pedido toda semana enquanto não houver filmagem nova, com um contador
("2ª semana sem filmagem") em `content/.semanas_sem_cena` — porque robô
cutuca; quem decide reduzir o pedido é o comitê, nunca o robô sozinho (veto
explícito do conselheiro).

Regras do perfil que vão no prompt (fonte: .claude/skills/hana-social/SKILL.md):
  - A estrela é a Hana; posicionamento "a patroa mimada"
  - Tom criança e cachorro, nunca adulto
  - PT-BR, termina com pergunta, no máximo 4 hashtags
"""

import base64
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# O console do Windows é cp1252 e engasga com emoji — e legenda de Instagram tem
# emoji. Sem isto o script morre na hora de IMPRIMIR, não de trabalhar.
for fluxo in (sys.stdout, sys.stderr):
    try:
        fluxo.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

import requests
from PIL import Image

import checar_repetida as rep
import preparar_lote as lote

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SELECIONADAS = os.path.join(RAIZ, "Fotos da Hana", "02 - selecionadas")
FILA = os.path.join(RAIZ, "content", "queue")
PUBLICADOS = os.path.join(RAIZ, "content", "posted")
CHAVES = os.path.join(
    os.path.expanduser("~"),
    "OneDrive", "Desktop", "Claude code APIs", "Documents", "IA-Hub", "chaves-api.txt",
)

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-flash-latest:generateContent"
)

# Dias de publicação: segunda, quarta e sexta às 21:00Z (18h em Itajaí).
DIAS = (0, 2, 4)
HORA_UTC = 21

BRIEFING = """Você escreve legendas para o Instagram @hanaduransanches, perfil da
cachorra Hana — uma Exotic Bully Micro tri lilac merle, de Itajaí/SC.

POSICIONAMENTO (obrigatório): "a patroa mimada". A Hana manda na casa e o dono
obedece; ela é a chefe, ele é o funcionário. Humor com atitude.

TOM: criança e cachorro — leve, engraçado, infantil. NUNCA tom adulto,
romântico, melancólico ou sensual.

REGRAS DA LEGENDA:
- Português do Brasil, 2 a 4 linhas.
- A Hana é sempre a estrela. O dono pode aparecer, mas nunca é o assunto.
- Termina OBRIGATORIAMENTE com uma pergunta para quem lê.
- No máximo 4 hashtags, na última linha, todas em minúsculas.
- Pode usar 1 ou 2 emojis, sem exagero.
- Não invente fato que não está na foto (raça, lugar ou objeto que não aparecem).

Responda APENAS com a legenda pronta. Sem aspas, sem explicação, sem título."""


def chave_gemini():
    if not os.path.isfile(CHAVES):
        raise RuntimeError(f"não achei o arquivo de chaves em {CHAVES}")
    for linha in open(CHAVES, encoding="utf-8", errors="ignore"):
        if linha.strip().startswith("GEMINI_API_KEY="):
            return linha.split("=", 1)[1].strip()
    raise RuntimeError("GEMINI_API_KEY não está em chaves-api.txt")


def legenda_da_foto(caminho, chave):
    """Pede a legenda ao Gemini Flash mostrando a foto. Devolve texto ou erro."""
    with open(caminho, "rb") as f:
        imagem = base64.b64encode(f.read()).decode()
    corpo = {
        "contents": [
            {
                "parts": [
                    {"text": BRIEFING},
                    {"inline_data": {"mime_type": "image/jpeg", "data": imagem}},
                ]
            }
        ],
        # Orçamento folgado de propósito: o Flash gasta boa parte dos tokens
        # "pensando" antes de escrever, e com 300 a legenda voltou cortada no
        # meio (primeiro teste, 28/07/2026). `thinkingConfig` este endpoint
        # recusa ("invalid argument"), então a saída é dar espaço.
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 2000},
    }
    r = requests.post(
        GEMINI_URL, params={"key": chave}, json=corpo,
        headers={"Content-Type": "application/json"}, timeout=120,
    )
    dados = r.json()
    if "error" in dados:
        raise RuntimeError(dados["error"].get("message", str(dados["error"]))[:200])
    candidato = dados["candidates"][0]
    texto = "".join(
        p.get("text", "") for p in candidato.get("content", {}).get("parts", [])
    ).strip()
    # Legenda sem pergunta quebra a regra do perfil — melhor falhar e avisar do
    # que criar post errado calado (regra 2). A pergunta vem antes das hashtags,
    # então o teste é "tem '?' no texto", não "termina com '?'".
    if candidato.get("finishReason") == "MAX_TOKENS" or "?" not in texto:
        raise RuntimeError(
            f"legenda veio incompleta ou sem pergunta: {texto[:80]!r}"
        )
    return texto


def proximas_datas(quantas):
    """Próximos seg/qua/sex às 21:00Z que ainda não estão ocupados na fila."""
    ocupadas = set()
    for base in (FILA, PUBLICADOS):
        if not os.path.isdir(base):
            continue
        for nome in os.listdir(base):
            meta = os.path.join(base, nome, "post.json")
            if os.path.isfile(meta):
                with open(meta, encoding="utf-8") as f:
                    ocupadas.add(json.load(f).get("scheduled_for"))

    datas, dia = [], datetime.now(timezone.utc).date() + timedelta(days=1)
    while len(datas) < quantas and dia < datetime.now(timezone.utc).date() + timedelta(days=90):
        if dia.weekday() in DIAS:
            quando = f"{dia.isoformat()}T{HORA_UTC:02d}:00:00Z"
            if quando not in ocupadas:
                datas.append(quando)
        dia += timedelta(days=1)
    return datas


def ineditas():
    """
    Fotos editadas que ainda não foram ao ar nem estão na fila.
    Usa a mesma impressão digital do checar_repetida.py (dhash).
    """
    if not os.path.isdir(SELECIONADAS):
        return [], "a pasta '02 - selecionadas' não existe"

    # Só FOTO é comparável por impressão digital — vídeo/Reel a API devolve como
    # .mp4 e o dhash não abre. Mesmo filtro do checar_repetida.py.
    conhecidos, ilegiveis = [], 0
    try:
        publicadas = rep.publicados(rep.token())
    except Exception as exc:  # noqa: BLE001
        return [], f"não consegui ler o que já está no ar ({str(exc)[:90]})"
    for m in publicadas:
        if m.get("media_type") != "IMAGE" or not m.get("media_url"):
            continue
        try:
            conhecidos.append(rep.baixar_hash(m["media_url"]))
        except Exception:  # noqa: BLE001
            ilegiveis += 1
    if ilegiveis:
        print(f"      [aviso] {ilegiveis} publicação(ões) do perfil não deram para comparar.")

    for base in (FILA, PUBLICADOS):
        if not os.path.isdir(base):
            continue
        for nome in sorted(os.listdir(base)):
            img = os.path.join(base, nome, "image.jpg")
            if os.path.isfile(img):
                conhecidos.append(rep.dhash(Image.open(img)))

    novas = []
    for nome in sorted(os.listdir(SELECIONADAS)):
        if not nome.lower().endswith(".jpg") or nome == "contact_sheet.jpg":
            continue
        caminho = os.path.join(SELECIONADAS, nome)
        h = rep.dhash(Image.open(caminho))
        if any(rep.distancia(h, c) <= rep.LIMITE for c in conhecidos):
            continue
        conhecidos.append(h)  # evita duas quase-iguais no mesmo lote
        novas.append(caminho)
    return novas, None


def id_do_post(caminho, quando):
    base = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(caminho))[0].lower())
    base = re.sub(r"^\d+-", "", base).strip("-")[:28] or "hana"
    return f"{quando[:10]}_{base}"


BRUTAS = os.path.join(RAIZ, "Fotos da Hana", "01 - brutas (suba aqui)")
RASCUNHOS = os.path.join(RAIZ, "Fotos da Hana", "06 - videos e trilhas", "rascunhos")
REGISTRO_VIDEOS = os.path.join(RAIZ, "content", ".videos_usados")
AVISO = os.path.join(RAIZ, "content", "aviso_lote.md")
EXT_VIDEO = (".mp4", ".mov", ".m4v")

# --- Conserto de 31/07/2026: o pedido de cena morava DENTRO do código, só ---
# chegava uma vez, e o robô ficava calado se o notebook estivesse desligado no
# domingo. Três arquivos locais novos (nenhum vai para o repo — são estado da
# MÁQUINA do Ramón, igual a REGISTRO_VIDEOS acima):
PEDIDO_CENA = os.path.join(RAIZ, "content", "pedido-de-cena.md")
CONTADOR_SEM_CENA = os.path.join(RAIZ, "content", ".semanas_sem_cena")
ESTADO_SEMANA = os.path.join(RAIZ, "content", ".lote_semana_executada")

# Credencial local do Telegram (furo 1 do conserto de 31/07/2026): este script
# roda na MÁQUINA do Ramón, dentro da tarefa "Hana Sentinela" — sem os secrets
# do GitHub Actions, que só existem lá. Mesmo formato do studio/.token (fora
# do git). Sem essa credencial, o robô continua calado — regra dele: nunca
# inventar, nunca gravar chave no repositório.
TELEGRAM_LOCAL = os.path.join(AQUI, ".telegram")


def _credenciais_telegram():
    """
    Token/chat do bot da Hana pra avisar por aqui. Ordem de busca: variável de
    ambiente primeiro (se um dia existir nesta máquina), depois o arquivo local
    `studio/.telegram`. Sem os dois, devolve (None, None) e quem chama decide
    degradar (regra: falha de aviso nunca derruba o robô).
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat_id:
        return token, chat_id
    if os.path.isfile(TELEGRAM_LOCAL):
        dados = {}
        with open(TELEGRAM_LOCAL, encoding="utf-8-sig") as f:
            for linha in f:
                if "=" in linha and not linha.strip().startswith("#"):
                    k, v = linha.strip().split("=", 1)
                    dados[k.strip()] = v.strip()
        if dados.get("TELEGRAM_BOT_TOKEN") and dados.get("TELEGRAM_CHAT_ID"):
            return dados["TELEGRAM_BOT_TOKEN"], dados["TELEGRAM_CHAT_ID"]
    return None, None


def _avisar_telegram(texto):
    """
    Faz o recado do lote semanal chegar no Telegram do Ramón.

    DUAS ROTAS, nesta ordem — mudança de 31/07/2026, quando o Ramón mandou
    "arrume" em vez de ir criar credencial na mão:

    1. Se esta máquina tiver credencial (`studio/.telegram` ou variável de
       ambiente), manda direto. É o caminho rápido.
    2. Se NÃO tiver — que é o caso normal, porque o token do bot mora nos
       secrets do GitHub —, o recado é EMPURRADO para o repositório. O robô do
       GitHub (`publisher/avisar_lote.py`, que roda a cada rodada do
       publish.yml) vê o arquivo novo e manda ele no Telegram com o token que
       só existe lá.

    A rota 2 é a que faz este robô parar de depender de o Ramón guardar uma
    senha na máquina. NUNCA derruba o lote: se as duas rotas falharem, o
    recado continua escrito em `content/aviso_lote.md`, que o `estado.py`
    mostra quando a conversa abre.
    """
    token, chat_id = _credenciais_telegram()
    if token and chat_id:
        try:
            sys.path.insert(0, os.path.join(RAIZ, "publisher"))
            from mandar_recado import mandar
            mandar(token, chat_id, texto)
            print("      [ok] avisei no Telegram (credencial local).")
            return
        except Exception as exc:  # noqa: BLE001 — aviso nunca pode derrubar o lote
            print(f"      [aviso] Telegram local falhou ({str(exc)[:120]}) — "
                  f"tentando pela rota do GitHub.")
    _empurrar_para_o_github()


def _empurrar_para_o_github():
    """
    Rota 2: commita e empurra `content/aviso_lote.md`. Quem entrega no Telegram
    é o robô do GitHub, que tem o token nos secrets.

    Só empurra ESTE arquivo (`git add` do caminho específico, não `-A`): o robô
    semanal não pode arrastar junto trabalho não salvo do Ramón ou meu.
    """
    import subprocess

    def git(*args):
        return subprocess.run(("git",) + args, cwd=RAIZ, capture_output=True,
                              text=True, timeout=120)

    try:
        if not git("add", "content/aviso_lote.md").returncode == 0:
            raise RuntimeError("git add falhou")
        if git("diff", "--cached", "--quiet").returncode == 0:
            print("      [ok] recado igual ao que já está no GitHub — nada a empurrar.")
            return
        git("commit", "-m", "chore: recado do lote semanal [skip ci]")
        for _ in range(3):
            if git("push").returncode == 0:
                print("      [ok] recado empurrado — o robô do GitHub avisa no "
                      "Telegram na próxima rodada (até 30 min).")
                return
            git("pull", "--rebase", "--autostash")
        raise RuntimeError("push rejeitado 3 vezes")
    except Exception as exc:  # noqa: BLE001 — aviso nunca pode derrubar o lote
        print(f"      [aviso] não consegui empurrar o recado ({str(exc)[:120]}). "
              f"Ele ficou em content/aviso_lote.md e o Claude lê ao abrir a conversa.")


def videos_ineditos():
    """Vídeos brutos que ainda não viraram rascunho de Reel."""
    if not os.path.isdir(BRUTAS):
        return []
    usados = set()
    if os.path.isfile(REGISTRO_VIDEOS):
        usados = {l.strip() for l in open(REGISTRO_VIDEOS, encoding="utf-8") if l.strip()}
    achados = [f for f in sorted(os.listdir(BRUTAS))
               if f.lower().endswith(EXT_VIDEO) and f not in usados]
    return [os.path.join(BRUTAS, f) for f in achados]


def _marcar_video(caminho):
    with open(REGISTRO_VIDEOS, "a", encoding="utf-8") as f:
        f.write(os.path.basename(caminho) + "\n")


def _escrever_aviso(texto):
    """Recado do robô do lote semanal — o estado.py mostra ao abrir a conversa."""
    os.makedirs(os.path.dirname(AVISO), exist_ok=True)
    with open(AVISO, "w", encoding="utf-8") as f:
        f.write("# Recado do robô do lote (semanal)\n\n%s\n" % texto)


# Texto de RESERVA — só entra quando o comitê ainda não escreveu o pedido da
# semana em content/pedido-de-cena.md. Cobre os 3 pilares vigentes e o
# desfecho fixo de INIMIGOS DA PATROA (regra permanente do DECISOES.md, não
# muda semana a semana), mas NUNCA finge que veio do plano — quem chama
# _ler_pedido_de_cena() sempre sabe se está usando isto (usando_reserva=True).
RESERVA_PEDIDO = (
    "Preciso de filmagem NOVA da Hana — sem cena nova, a linha editorial não "
    "tem Reel pra publicar (regra do comitê: só vídeo real, com o rosto dela "
    "em quadro).\n\n"
    "Sugestão por pilar — grave o que der, o ideal é 1 cena de cada:\n"
    "1. A PATROA MANDA — ela manda em alguma coisa e você obedece.\n"
    "2. MICRO NO APÊ — o dia a dia dela em casa.\n"
    "3. INIMIGOS DA PATROA — ela contra algo que não gosta. Desfecho "
    "OBRIGATÓRIO: ela LATE E EXPULSA, ou IGNORA E SAI ANDANDO — nunca foge.\n\n"
    "Celular na vertical, parado, ~15 segundos, com o ROSTO dela em quadro."
)


def _ler_pedido_de_cena():
    """
    Devolve (texto, usando_reserva). O pedido de verdade é escrito pelo
    comitê/Diretor de Criação, uma vez por semana, em content/pedido-de-cena.md
    — o robô NUNCA inventa cena (regra do veto do conselheiro: "robô cutuca,
    robô não reduz estratégia sozinho" vale também ao contrário — ele não CRIA
    estratégia). Se o arquivo não existe ou está vazio, cai no texto de reserva
    e avisa — nunca finge que o texto veio do plano (regra zero da skill: não
    afirmar sem conferir).
    """
    try:
        if os.path.isfile(PEDIDO_CENA):
            texto = open(PEDIDO_CENA, encoding="utf-8").read().strip()
            if texto:
                return texto, False
    except Exception:  # noqa: BLE001 — leitura de aviso nunca derruba o lote
        pass
    return RESERVA_PEDIDO, True


def _semana_de(data):
    """Chave estável da semana: a segunda-feira ISO daquele dia, em texto
    (ex.: '2026-08-03'). Rodar terça ou sexta na mesma semana devolve a mesma
    chave — é o que permite 'uma vez por semana' independente do dia exato."""
    segunda = data - timedelta(days=data.weekday())
    return segunda.isoformat()


def _ja_rodou_essa_semana():
    """Substitui o antigo 'hoje é domingo?'. Notebook desligado no domingo não
    faz a semana sumir: o robô roda no primeiro dia em que a máquina ligar."""
    if not os.path.isfile(ESTADO_SEMANA):
        return False
    try:
        salvo = open(ESTADO_SEMANA, encoding="utf-8").read().strip()
    except Exception:  # noqa: BLE001
        return False
    return salvo == _semana_de(datetime.now().date())


def _marcar_semana_rodada():
    try:
        with open(ESTADO_SEMANA, "w", encoding="utf-8") as f:
            f.write(_semana_de(datetime.now().date()))
    except Exception as exc:  # noqa: BLE001 — marcador nunca derruba o lote
        print(f"      [aviso] não consegui gravar o marcador de semana ({str(exc)[:100]}).")


def _estado_contador_sem_cena():
    """(semana da última contagem, contagem naquela semana) — ("", 0) se nunca
    gravou ou se o arquivo estiver corrompido (nunca derruba o lote)."""
    if os.path.isfile(CONTADOR_SEM_CENA):
        try:
            with open(CONTADOR_SEM_CENA, encoding="utf-8") as f:
                dados = json.load(f)
            return dados.get("semana", ""), int(dados.get("contagem", 0))
        except Exception:  # noqa: BLE001
            return "", 0
    return "", 0


def _semanas_sem_cena_agora():
    """Só LEITURA — usado no --simular pra mostrar o número sem gravar nada."""
    semana_salva, contagem = _estado_contador_sem_cena()
    semana_atual = _semana_de(datetime.now().date())
    return contagem + 1 if semana_salva != semana_atual else contagem


def _registrar_semana_sem_cena():
    """
    Soma 1 na contagem de semanas seguidas sem vídeo novo — é isso que muda o
    texto do recado toda semana e destrava sozinho os dois bloqueios de
    repetição (o `git diff --cached --quiet` do _empurrar_para_o_github e o
    hash de content/.aviso_lote_enviado no avisar_lote.py): texto diferente,
    os dois deixam passar sem precisar mexer neles.
    Idempotente dentro da mesma semana (chave = segunda-feira ISO): rodar duas
    vezes na mesma semana não soma duas vezes.
    """
    semana_salva, contagem = _estado_contador_sem_cena()
    semana_atual = _semana_de(datetime.now().date())
    if semana_salva == semana_atual:
        return contagem
    nova = contagem + 1
    try:
        with open(CONTADOR_SEM_CENA, "w", encoding="utf-8") as f:
            json.dump({"semana": semana_atual, "contagem": nova}, f)
    except Exception as exc:  # noqa: BLE001 — contador nunca derruba o lote
        print(f"      [aviso] não consegui gravar o contador de semanas sem cena ({str(exc)[:100]}).")
    return nova


def _zerar_semanas_sem_cena():
    """Cena nova chegou — a contagem volta a zero."""
    try:
        with open(CONTADOR_SEM_CENA, "w", encoding="utf-8") as f:
            json.dump({"semana": _semana_de(datetime.now().date()), "contagem": 0}, f)
    except Exception as exc:  # noqa: BLE001 — contador nunca derruba o lote
        print(f"      [aviso] não consegui zerar o contador de semanas sem cena ({str(exc)[:100]}).")


def montar_rascunhos(videos, limite=2):
    """
    Monta rascunho de Reel a partir dos vídeos novos — SEM gancho e SEM entrar
    na fila. O gancho e o corte exigem julgamento (o auditor reprovou os meus
    duas vezes em 31/07/2026), então o robô prepara e o Claude decide na
    reunião de segunda. Robô não publica conteúdo que ninguém olhou.
    """
    sys.path.insert(0, AQUI)
    from reel_de_video import montar

    os.makedirs(RASCUNHOS, exist_ok=True)
    feitos = []
    for caminho in videos[:limite]:
        nome = os.path.splitext(os.path.basename(caminho))[0]
        saida = os.path.join(RASCUNHOS, "rascunho_%s.mp4" % nome)
        try:
            montar(caminho, saida, texto=None, inicio=0, duracao=10)
            _marcar_video(caminho)
            feitos.append(saida)
        except SystemExit as exc:
            print("      [FALHA] %s: %s" % (nome, exc))
    return feitos


def main():
    simular = "--simular" in sys.argv
    # O robô da máquina (tarefa "Hana Sentinela") chama este script todo dia que
    # roda; --so-domingo faz ele trabalhar uma vez por semana, sem precisar de
    # agendamento novo (regra do robô único). ATÉ 31/07/2026 a condição era
    # "hoje é domingo?" — notebook desligado no domingo fazia a semana inteira
    # sumir, sem ninguém perceber. Desde 31/07/2026 a condição é "já rodei
    # nesta semana?" (_ja_rodou_essa_semana, arquivo local
    # .lote_semana_executada): ligar o PC terça, quarta, o dia que for, o robô
    # ainda cumpre a semana. O nome da flag continua --so-domingo (é o que
    # studio/sentinela.bat já chama) — só o SIGNIFICADO mudou.
    if "--so-domingo" in sys.argv:
        if _ja_rodou_essa_semana():
            return
        if not simular:
            _marcar_semana_rodada()
    limite = 3  # um lote de uma semana: seg, qua, sex

    # --- 31/07/2026: o lote deixou de fabricar FOTO por padrão. -------------
    # Medido em content/placar.md: 4 fotos publicadas, alcance médio 47, e
    # ZERO salvos, ZERO compartilhamentos e ZERO seguidores ganhos nas quatro.
    # Deixar o robô produzir mais foto era automatizar a produção de zeros.
    # Agora ele trabalha com VÍDEO; sem vídeo novo, ele não inventa post —
    # avisa que falta filmagem. Foto avulsa só com --fotos, na mão.
    if "--fotos" not in sys.argv:
        videos = videos_ineditos()
        if not videos:
            pedido_texto, usando_reserva = _ler_pedido_de_cena()
            n_semanas = _semanas_sem_cena_agora() if simular else _registrar_semana_sem_cena()
            aviso_reserva = (
                "\n\n⚠️ *Texto de RESERVA* — o comitê ainda não escreveu o "
                "pedido desta semana em `content/pedido-de-cena.md`. Isto NÃO "
                "veio do plano."
            ) if usando_reserva else ""
            aviso_contador = (
                f"\n\n⏳ **{n_semanas}ª semana sem filmagem nova.** Quem decide "
                "se muda a estratégia é o comitê — o robô só cutuca, nunca "
                "reduz o pedido sozinho."
            )
            recado = (
                "**Não montei lote esta semana** — nenhum vídeo novo em "
                "`01 - brutas (suba aqui)`, de propósito (foto parada já deu "
                "zero em salvos, compartilhamentos e seguidores ganhos, 4 "
                "vezes seguidas — regra fixa desde 31/07/2026).\n\n"
                f"{pedido_texto}"
                f"{aviso_reserva}"
                f"{aviso_contador}"
            )
            print("[ok] sem vídeo novo — nada foi criado. Recado escrito em content/aviso_lote.md")
            if usando_reserva:
                print("      [aviso] content/pedido-de-cena.md não existe (ou está vazio) — usando texto de reserva.")
            print(f"      {n_semanas}ª semana sem filmagem nova.")
            if not simular:
                _escrever_aviso(recado)
                _avisar_telegram("🎬 Lote semanal rodou: nenhum vídeo novo.\n\n" + recado)
            return
        print("[1/2] montando rascunho de Reel dos vídeos novos (%d encontrado(s))..." % len(videos))
        if simular:
            for v in videos[:2]:
                print("      [simulação] viraria rascunho: %s" % os.path.basename(v))
            print("[simulação] nada montado, nada gasto.")
            return
        feitos = montar_rascunhos(videos)
        _zerar_semanas_sem_cena()  # cena chegou — a contagem de semanas paradas volta a zero
        print("[2/2] %d rascunho(s) em '06 - videos e trilhas/rascunhos'." % len(feitos))
        _escrever_aviso(
            "%d rascunho(s) de Reel prontos em `Fotos da Hana/06 - videos e "
            "trilhas/rascunhos`, montados dos vídeos novos. Contador de "
            "semanas sem filmagem voltou a zero.\n\n"
            "**Ainda não entraram na fila** — falta escolher o trecho e o gancho, "
            "que é julgamento, e passar pelo auditor. Fazer na reunião de segunda."
            % len(feitos))
        _avisar_telegram(
            "🎬 Lote semanal rodou.\n"
            "Achei %d vídeo(s) novo(s) e já montei %d rascunho(s) de Reel em "
            "\"06 - videos e trilhas/rascunhos\".\n"
            "Falta só o corte final e o gancho — o Claude fecha isso na reunião "
            "de segunda." % (len(videos), len(feitos))
        )
        return
    # ------------------------------------------------------------------------

    print("[1/4] editando as fotos de '01 - brutas'...")
    lote.editar()

    print("[2/4] separando as que ainda não foram ao ar...")
    novas, erro = ineditas()
    if erro:
        # Falhar visível (regra 2): sem essa checagem eu poderia repetir foto.
        print(f"[FALHA] {erro}. Não vou montar lote no escuro — nada foi criado.")
        sys.exit(1)
    if not novas:
        print("[ok] nenhuma foto inédita em '02 - selecionadas'. Nada a fazer.")
        return

    datas = proximas_datas(min(limite, len(novas)))
    escolhidas = list(zip(novas, datas))
    print(f"      {len(novas)} inédita(s); vou usar {len(escolhidas)} neste lote.")

    if simular:
        for caminho, quando in escolhidas:
            print(f"      [simulação] {os.path.basename(caminho)} -> {quando}")
        print("[simulação] nenhuma legenda pedida, nenhum post criado, nada gasto.")
        return

    print("[3/4] pedindo as legendas ao Gemini Flash (ele vê a foto)...")
    chave = chave_gemini()
    prontos, falhas = [], []
    for caminho, quando in escolhidas:
        try:
            texto = legenda_da_foto(caminho, chave)
            prontos.append((caminho, quando, texto))
            print(f"      ok: {os.path.basename(caminho)}")
        except Exception as exc:  # noqa: BLE001
            falhas.append((os.path.basename(caminho), str(exc)[:140]))
            print(f"      [FALHA] {os.path.basename(caminho)}: {exc}")

    print("[4/4] criando os posts na fila (status pending)...")
    for caminho, quando, texto in prontos:
        lote.post(caminho, id_do_post(caminho, quando), quando[:16], texto)

    print()
    print(f"[resumo] {len(prontos)} post(s) na fila esperando o 'aprovado' do Ramón.")
    if falhas:
        print("[resumo][AVISO] falharam e NÃO entraram na fila:")
        for nome, motivo in falhas:
            print(f"  - {nome}: {motivo}")
    print("O publicador avisa no Telegram no próximo ciclo (a cada 30 min).")


if __name__ == "__main__":
    main()
