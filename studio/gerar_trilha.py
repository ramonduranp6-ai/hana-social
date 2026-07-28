"""
Gerador de trilha para os Reels da Hana — Lyria 3 pela Gemini API.

Por que existe: os Reels montados por `gerar_reel.py` saem SEM musica (ou com o
audio cru do celular). Audio de tendencia do Instagram nao existe via API (limite
da Meta), entao a alternativa e trilha propria, livre de direitos.

Custo (jul/2026): US$ 0,04 por clipe de 30s (lyria-3-clip-preview).
A chave vive em chaves-api.txt do IA-Hub — nunca dentro do script.

Uso:
    python studio/gerar_trilha.py "descricao da musica" [nome-do-arquivo]
    python studio/gerar_trilha.py --lote        # gera as 3 opcoes padrao

Saida: content/trilhas/<nome>.mp3
"""

import base64
import json
import os
import sys
import urllib.error
import urllib.request

CHAVES = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop",
                      "Claude code APIs", "Documents", "IA-Hub", "chaves-api.txt")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "content", "trilhas")
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODELO = "lyria-3-clip-preview"

# As 3 direcoes propostas para o Reel da Hana (14s, ela assistindo TV no sofa).
# Instrumental sempre: voz cantada rouba a atencao da legenda e da cena.
LOTE = [
    ("01-fofo-ukulele",
     "Upbeat cheerful ukulele instrumental, light whistling melody, hand claps, "
     "soft shaker percussion, playful and warm, feel-good pet video vibe, "
     "major key, 110 bpm, no vocals, loopable."),
    ("02-lofi-sofa",
     "Cozy lo-fi hip hop instrumental, warm mellow electric piano, soft vinyl "
     "crackle, relaxed head-nod drums, lazy sunday afternoon on the couch mood, "
     "80 bpm, no vocals, loopable."),
    ("03-comico-pizzicato",
     "Playful comedic instrumental, pizzicato strings, bouncy marimba, cheeky "
     "bassoon accents, cartoon sneaking-around feel with a wink, light and funny, "
     "120 bpm, no vocals, loopable."),
]


def ler_chave():
    chaves = {}
    with open(CHAVES, encoding="utf-8-sig") as f:
        for linha in f:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                chaves[k.strip()] = v.strip()
    chave = chaves.get("GEMINI_API_KEY")
    if not chave:
        raise SystemExit("ERRO: GEMINI_API_KEY vazia em chaves-api.txt")
    return chave


def extrair_audio(dados):
    """Varre os blocos da resposta atras do audio em base64.

    O formato do Interactions API ainda e preview e ja mudou de nome de campo,
    entao aqui a busca e generica: qualquer bloco que carregue dados de audio.
    """
    achados = []

    def andar(o):
        if isinstance(o, dict):
            for chave in ("data", "audio_data", "bytes_base64_encoded", "inline_data"):
                v = o.get(chave)
                if isinstance(v, str) and len(v) > 5000:
                    achados.append(v)
                elif isinstance(v, dict) and isinstance(v.get("data"), str):
                    achados.append(v["data"])
            for v in o.values():
                andar(v)
        elif isinstance(o, list):
            for v in o:
                andar(v)

    andar(dados)
    return achados[0] if achados else None


def gerar(descricao, nome, chave):
    corpo = json.dumps({"model": MODELO, "input": descricao}).encode()
    req = urllib.request.Request(
        ENDPOINT, data=corpo,
        headers={"Content-Type": "application/json", "x-goog-api-key": chave})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            dados = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"[FALHOU] {nome} — HTTP {e.code}: {e.read().decode()[:400]}")
        return None

    b64 = extrair_audio(dados)
    if not b64:
        print(f"[FALHOU] {nome} — resposta sem audio. Estrutura recebida:")
        print(json.dumps(dados, indent=2)[:1500])
        return None

    os.makedirs(SAIDA, exist_ok=True)
    caminho = os.path.join(SAIDA, f"{nome}.mp3")
    with open(caminho, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"[ok] {caminho} — {os.path.getsize(caminho)//1024} KB")
    return caminho


if __name__ == "__main__":
    args = sys.argv[1:]
    chave = ler_chave()
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "--lote":
        for nome, desc in LOTE:
            gerar(desc, nome, chave)
    else:
        nome = args[1] if len(args) > 1 else "trilha"
        gerar(args[0], nome, chave)
