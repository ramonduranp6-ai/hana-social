"""
Lote automático de domingo — o robô monta a fila, o Ramón só aprova.

Existe para tirar do Claude (e do plano dele) o trabalho semanal repetitivo:
editar as fotos, escolher as inéditas, escrever legenda e criar os posts.
Quem escreve a legenda é o **Gemini Flash** (crédito do IA-Hub, fração de
centavo por foto) — e ele VÊ a foto, porque é multimodal. O Claude só entra se
o Ramón pedir revisão.

Uso:
    python studio/lote_automatico.py --simular   # mostra o plano, não gasta nada
    python studio/lote_automatico.py             # monta o lote de verdade

Depois de rodar, os posts ficam em content/queue/ com status "pending" e o
publicador manda no Telegram para o Ramón aprovar. **Nada é publicado sem o
"aprovado" dele** — este script não muda status nem publica.

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
    Manda o recado curto no Telegram do Ramón. NUNCA derruba o lote: sem
    credencial ou com falha de rede, só avisa no log (stdout, que cai no
    sentinela.log) e segue — `content/aviso_lote.md` já foi escrito antes
    desta chamada de qualquer jeito, então o recado não se perde de vez.
    """
    token, chat_id = _credenciais_telegram()
    if not (token and chat_id):
        print("      [aviso] sem TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID nesta máquina "
              "— ninguém foi avisado no Telegram. O recado ficou só em "
              "content/aviso_lote.md, que o Claude só lê quando a conversa abre.")
        return
    try:
        sys.path.insert(0, os.path.join(RAIZ, "publisher"))
        from mandar_recado import mandar
        mandar(token, chat_id, texto)
        print("      [ok] avisei no Telegram.")
    except Exception as exc:  # noqa: BLE001 — aviso nunca pode derrubar o lote
        print(f"      [aviso] Telegram falhou ({str(exc)[:120]}) — recado "
              f"ficou só em content/aviso_lote.md.")


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
    """Recado do robô de domingo — o estado.py mostra ao abrir a conversa."""
    os.makedirs(os.path.dirname(AVISO), exist_ok=True)
    with open(AVISO, "w", encoding="utf-8") as f:
        f.write("# Recado do robô do lote (domingo)\n\n%s\n" % texto)


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
    # roda; --so-domingo faz ele trabalhar uma vez por semana e sair calado nos
    # outros dias, sem precisar de agendamento novo (regra do robô único).
    if "--so-domingo" in sys.argv and datetime.now().weekday() != 6:
        return
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
            recado = (
                "Nenhum vídeo novo em `01 - brutas (suba aqui)` — **não montei "
                "lote esta semana**, de propósito.\n\n"
                "Foto avulsa dela parada já foi testada 4 vezes e deu zero em "
                "salvos, compartilhamentos e seguidores ganhos nas quatro. "
                "Produzir mais foto seria fabricar mais zero.\n\n"
                "O que destrava: as duas cenas que faltam — (1) a Hana obrigando "
                "o Ramón a alguma coisa, com o momento em que ela ganha; "
                "(2) a Hana contra o aspirador ou o secador. "
                "Celular na vertical, parado, ~15 segundos, **com o rosto dela "
                "em quadro**.")
            print("[ok] sem vídeo novo — nada foi criado. Recado escrito em content/aviso_lote.md")
            if not simular:
                _escrever_aviso(recado)
                _avisar_telegram(
                    "🎬 Lote de domingo rodou: nenhum vídeo novo, não montei nada "
                    "esta semana.\n"
                    "Faltam 2 cenas: (1) a Hana obrigando você a alguma coisa, com "
                    "o momento em que ela ganha; (2) a Hana contra o aspirador ou "
                    "o secador.\n"
                    "Celular na vertical, parado, uns 15 segundos, com o rosto "
                    "dela em quadro.\n"
                    "Salve os vídeos aqui: "
                    r"C:\Users\Ramón França\OneDrive\Desktop\Hana Social\Fotos da Hana\01 - brutas (suba aqui)"
                )
            return
        print("[1/2] montando rascunho de Reel dos vídeos novos (%d encontrado(s))..." % len(videos))
        if simular:
            for v in videos[:2]:
                print("      [simulação] viraria rascunho: %s" % os.path.basename(v))
            print("[simulação] nada montado, nada gasto.")
            return
        feitos = montar_rascunhos(videos)
        print("[2/2] %d rascunho(s) em '06 - videos e trilhas/rascunhos'." % len(feitos))
        _escrever_aviso(
            "%d rascunho(s) de Reel prontos em `Fotos da Hana/06 - videos e "
            "trilhas/rascunhos`, montados dos vídeos novos.\n\n"
            "**Ainda não entraram na fila** — falta escolher o trecho e o gancho, "
            "que é julgamento, e passar pelo auditor. Fazer na reunião de segunda."
            % len(feitos))
        _avisar_telegram(
            "🎬 Lote de domingo rodou.\n"
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
