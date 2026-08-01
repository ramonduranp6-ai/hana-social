"""
Reel-slideshow RITMADO — a receita do Diretor de Criação (01/08/2026).

Por que existe, se já havia `gerar_reel.py`:
o `gerar_reel.py` monta 4s fixos por foto, zoom lento sempre igual, transição
fade de 0,8s, texto só na primeira tela e SEM ÁUDIO. Foi exatamente esse
resultado que o Ramón barrou em 31/07 ("você tinha feito um muito ruim, por
isso barrei"). Ele reabriu o assunto em 01/08 pedindo um teste medido, mas
"que seja legal". Este script é a receita nova, e as 4 diferenças são:

  1. DURAÇÃO POR SLIDE, não fixa — os cortes ACELERAM (2,0s → 1,5s → 1,0s →
     1,0s) e param no desfecho (3,0s). Ritmo em cima do BPM da trilha.
  2. CORTE SECO, sem xfade. O fade de 0,8s comia quase um quinto de cada
     slide e era o que dava a sensação de arrastado.
  3. MOVIMENTO DIFERENTE POR SLIDE — e no slide 4 é ZOOM-OUT, de propósito:
     é a câmera abrindo que revela o sofá inteiro ocupado, ou seja, é o
     movimento que conta a piada.
  4. TEXTO EM TODAS AS TELAS, com tarja atrás — quem assiste sem som (a
     maioria) lê a piada inteira — e TRILHA colada com `-shortest`.

O roteiro não fica no código: vem de um dicionário que o Claude escreve na
conversa a partir do pacote do Criador. Assim dá para remontar variação sem
mexer em lógica.

Uso:
    python studio/reel_ritmado.py saida.mp4
"""

import os
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageOps

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H = 1080, 1920
FPS = 30

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FOTOS = os.path.join(RAIZ, "Fotos da Hana", "02 - selecionadas")
TRILHA = os.path.join(RAIZ, "content", "trilhas", "03-comico-pizzicato.mp3")

# ---------------------------------------------------------------------------
# ROTEIRO — pacote fechado do Diretor de Criação, 01/08/2026.
# Conceito: "como o dono perdeu a casa" — pilar A PATROA MANDA.
# `mov`: dentro = zoom-in (aproxima) · fora = zoom-out (revela o quadro todo)
# ---------------------------------------------------------------------------
ROTEIRO = [
    {"arq": "garimpo_23_08211450-26dd-468e-a477-7b093d72ccf6.jpg",
     "seg": 2.034, "mov": "dentro", "texto": "ERA PRA SER\nMEU CACHORRO", "px": 96},
    {"arq": "garimpo_09_0440D040-DD38-40D4-965A-C0D0B1DF00F6.jpg",
     "seg": 1.6, "mov": "dentro", "texto": "aí ela cresceu", "px": 74},
    # A auditoria de 01/08/2026 derrubou o slide que ficava aqui
    # (garimpo_03, "e tomou o sofá"): naquela foto a luz quente puxa a cor
    # para dourado e a mancha lilac merle SOME — e preservar a cor é regra da
    # marca. De quebra o cenário se confundia com o da cama do slide seguinte
    # e a pata saía borrada. Tirar resolveu 3 dos 4 defeitos de uma vez; o 4º
    # (ritmo apertado de 1s) morreu junto, porque sobrou tempo para os outros.
    # O zoom-out aqui é a piada: abre e mostra a cama inteira ocupada por ela.
    {"arq": "garimpo_14_06bae585-c1d3-4b7c-bcdb-ebd79a657435.jpg",
     "seg": 1.7, "mov": "fora", "texto": "e tomou a cama inteira", "px": 68,
     "wb": 0.75},
    # `foco` puxa o enquadramento para a direita ao longo do slide: na 1ª
    # montagem o Ramón dominava o quadro no slide mais longo do Reel, e a
    # regra da marca é que a estrela é a Hana. Agora a câmera termina nela.
    {"arq": "13_IMG_3306.jpg",
     "seg": 2.6, "mov": "dentro", "texto": "eu virei o mordomo", "px": 74,
     "foco": 0.62},
]


def _fonte(px):
    return ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", px)


def equilibrar_branco(im, forca=1.0):
    """
    Neutraliza dominante de cor pelo método do cinza-médio.

    Existe por causa de um defeito real apontado pela auditoria de 01/08/2026:
    a foto da cama é noturna, sob luz quente, e a dominante amarela COMIA a
    marcação tri lilac merle — a Hana saía dourada. Como preservar essa cor é
    regra da marca, corrigir o branco não é "filtro", é devolver a cor
    verdadeira dela. `forca` entre 0 e 1 evita correção agressiva, que deixaria
    a cena com cara de laboratório em vez de quarto à noite.
    """
    canais = im.split()
    medias = [c.resize((1, 1), Image.BOX).getpixel((0, 0)) for c in canais]
    alvo = sum(medias) / 3.0
    corrigidos = []
    for c, m in zip(canais, medias):
        if m <= 0:
            corrigidos.append(c)
            continue
        ganho = 1.0 + (alvo / m - 1.0) * forca
        corrigidos.append(c.point(lambda v, g=ganho: max(0, min(255, int(v * g)))))
    return Image.merge("RGB", corrigidos)


def preparar(caminho, destino, texto, px, wb=0.0):
    """Recorta em 9:16 e grava o texto com tarja atrás (legível sem som)."""
    im = ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")
    if wb:
        im = equilibrar_branco(im, wb)
    im = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(0.5, 0.4))
    if texto:
        d = ImageDraw.Draw(im, "RGBA")
        fnt = _fonte(px)
        linhas = texto.split("\n")
        alt_linha = int(px * 1.25)
        bloco = alt_linha * len(linhas)
        topo = H - 430 - bloco
        larguras = [d.textlength(l, font=fnt) for l in linhas]
        # Tarja: sem ela o texto branco some em foto clara (a da mesa e a do
        # sofá bege são exatamente esse caso).
        pad = 26
        d.rectangle(
            [(W - max(larguras)) / 2 - pad, topo - pad,
             (W + max(larguras)) / 2 + pad, topo + bloco + pad // 2],
            fill=(0, 0, 0, 130))
        for i, linha in enumerate(linhas):
            x = (W - larguras[i]) / 2
            y = topo + i * alt_linha
            d.text((x + 3, y + 3), linha, font=fnt, fill=(0, 0, 0))
            d.text((x, y), linha, font=fnt, fill=(255, 255, 255))
    im.save(destino, quality=94)
    return max(larguras) if texto else 0


def montar(saida, roteiro=ROTEIRO, trilha=TRILHA):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    tmp = os.path.join(os.path.dirname(os.path.abspath(saida)) or ".", "_ritmado_tmp")
    os.makedirs(tmp, exist_ok=True)

    entradas, filtros, rotulos = [], [], []
    for i, s in enumerate(roteiro):
        origem = s["arq"] if os.path.isabs(s["arq"]) else os.path.join(FOTOS, s["arq"])
        if not os.path.isfile(origem):
            raise SystemExit(f"[erro] foto nao encontrada: {origem}")
        pronta = os.path.join(tmp, f"s{i:02d}.jpg")
        larg = preparar(origem, pronta, s.get("texto"), s.get("px", 74), s.get("wb", 0.0))
        if larg > W - 40:
            raise SystemExit(f"[erro] o texto do slide {i+1} vaza da tela "
                             f"({int(larg)}px de {W}) — quebre em 2 linhas")
        frames = max(1, round(s["seg"] * FPS))
        # `-framerate 1 -t 1` garante UM frame de entrada: o `d` do zoompan
        # conta por frame de entrada, e sem isso o slide sai com dezenas de
        # vezes a duração pedida (pegadinha já paga em gerar_reel.py).
        entradas += ["-loop", "1", "-framerate", "1", "-t", "1", "-i", pronta]
        if s["mov"] == "fora":
            # Começa fechado e ABRE — é a revelação do sofá ocupado.
            z = f"z='if(lte(on,1),1.30,max(zoom-{0.30/frames:.6f},1.001))'"
        else:
            z = f"z='min(zoom+{0.18/frames:.6f},1.18)'"
        # `foco` = para onde a câmera caminha (0,5 = centro; >0,5 puxa p/ direita).
        fx = s.get("foco", 0.5)
        filtros.append(
            f"[{i}:v]scale={int(W*1.5)}:{int(H*1.5)},"
            f"zoompan={z}:d={frames}:"
            f"x='iw*{fx}-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
            f"setsar=1[v{i}]"
        )
        rotulos.append(f"[v{i}]")

    # Corte seco: concat puro, sem xfade.
    cadeia = ";".join(filtros) + ";" + "".join(rotulos) + \
             f"concat=n={len(roteiro)}:v=1:a=0[vout]"

    tem_audio = trilha and os.path.isfile(trilha)
    if tem_audio:
        entradas += ["-i", trilha]

    cmd = [ffmpeg, "-y", *entradas, "-filter_complex", cadeia, "-map", "[vout]"]
    if tem_audio:
        cmd += ["-map", f"{len(roteiro)}:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-r", str(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "high", "-crf", "18", saida]

    r = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    if r.returncode != 0:
        print(r.stderr[-2500:])
        raise SystemExit("[erro] ffmpeg falhou")

    total = sum(s["seg"] for s in roteiro)
    print(f"[ok] {saida} — {len(roteiro)} slides, {total:.2f}s, "
          f"trilha: {'sim' if tem_audio else 'NAO'}")
    return saida


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    montar(sys.argv[1])
