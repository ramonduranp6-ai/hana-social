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


def main():
    simular = "--simular" in sys.argv
    # O robô da máquina (tarefa "Hana Sentinela") chama este script todo dia que
    # roda; --so-domingo faz ele trabalhar uma vez por semana e sair calado nos
    # outros dias, sem precisar de agendamento novo (regra do robô único).
    if "--so-domingo" in sys.argv and datetime.now().weekday() != 6:
        return
    limite = 3  # um lote de uma semana: seg, qua, sex

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
