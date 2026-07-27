"""
Confere se alguma foto da fila já foi publicada — por semelhança de imagem.

Regra do projeto (DECISOES.md): nunca propor foto repetida. Olhar o grid a olho
nu já falhou uma vez, então aqui a comparação é objetiva: baixa tudo o que está
publicado no perfil pela API e compara com a fila usando "dHash" (impressão
digital da imagem, tolerante a corte, brilho e recompressão).

Também compara os posts da fila entre si — dois posts do mesmo passeio, com dias
de diferença, contam como repetido.

Uso:
    python studio/checar_repetida.py
"""

import io
import json
import os
import urllib.request

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FILA = os.path.join(RAIZ, "content", "queue")
TOKEN_ARQ = os.path.join(AQUI, ".token")

# distância de Hamming entre os hashes: <= 10 bits é "olhar humano diria: é a mesma"
LIMITE = 10


def token():
    with open(TOKEN_ARQ, encoding="utf-8-sig") as f:
        for linha in f:
            if linha.startswith("IG_ACCESS_TOKEN="):
                return linha.split("=", 1)[1].strip()
    raise SystemExit("[ERRO] token nao encontrado em studio/.token")


def dhash(img, lado=8):
    """Impressão digital: compara cada pixel com o vizinho da direita."""
    img = img.convert("L").resize((lado + 1, lado), Image.LANCZOS)
    bits = 0
    for y in range(lado):
        for x in range(lado):
            bits = (bits << 1) | (img.getpixel((x, y)) > img.getpixel((x + 1, y)))
    return bits


def distancia(a, b):
    return bin(a ^ b).count("1")


def publicados(tk):
    url = ("https://graph.instagram.com/me/media"
           f"?fields=id,caption,media_type,media_url,timestamp&limit=100&access_token={tk}")
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r).get("data", [])


def baixar_hash(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return dhash(Image.open(io.BytesIO(r.read())))


def main():
    tk = token()
    print("baixando o que ja esta publicado no perfil...")
    itens = publicados(tk)
    fotos = [m for m in itens if m.get("media_type") == "IMAGE" and m.get("media_url")]
    print(f"  {len(itens)} publicacoes no perfil, {len(fotos)} sao foto comparavel")

    no_ar = []
    for m in fotos:
        try:
            no_ar.append((m["timestamp"][:10], baixar_hash(m["media_url"])))
        except Exception as e:
            print(f"  [aviso] nao consegui ler a publicacao {m['id']}: {e}")

    da_fila = []
    for pasta in sorted(os.listdir(FILA)):
        img = os.path.join(FILA, pasta, "image.jpg")
        if os.path.isfile(img):
            da_fila.append((pasta, dhash(Image.open(img))))

    print(f"\ncomparando {len(da_fila)} fotos da fila contra {len(no_ar)} publicadas:")
    achou = False
    for pasta, h in da_fila:
        pares = sorted(((distancia(h, h2), data) for data, h2 in no_ar))
        d, data = pares[0] if pares else (99, "-")
        if d <= LIMITE:
            achou = True
            print(f"  [REPETIDA] {pasta} == publicado em {data} (distancia {d})")
        else:
            print(f"  [ok] {pasta} — mais parecida: {data}, distancia {d}")

    print("\ncomparando a fila entre si:")
    for i in range(len(da_fila)):
        for j in range(i + 1, len(da_fila)):
            d = distancia(da_fila[i][1], da_fila[j][1])
            if d <= LIMITE:
                achou = True
                print(f"  [REPETIDA] {da_fila[i][0]} == {da_fila[j][0]} (distancia {d})")
    if not achou:
        print("  nenhuma repeticao encontrada")


if __name__ == "__main__":
    main()
