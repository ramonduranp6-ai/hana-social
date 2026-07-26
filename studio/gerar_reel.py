"""
Gerador de Reel a partir de fotos — Python local, custo zero, sem IA.

Usa o ffmpeg embutido do imageio-ffmpeg (pip install imageio-ffmpeg), então não
precisa instalar ffmpeg no sistema. Técnica trazida do benchmark com o outro
projeto do Ramón (25/07/2026): filtros zoompan + xfade direto no ffmpeg, em vez
de gerar frame a frame — muito mais rápido e sem lixo em disco.

Uso:
    python studio/gerar_reel.py saida.mp4 foto1.jpg [foto2.jpg ...] [--texto "gancho"]

Saída: 1080x1920 (9:16), h264, ~4s por foto, zoom lento e transição suave.
O texto entra como gancho no terço inferior — padrão dos perfis que crescem.
"""

import os
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1080, 1920
DUR = 4          # segundos por foto
FPS = 30
FADE = 0.8       # segundos de transição


def preparar(caminho, destino, texto=None):
    """Recorta em 9:16, cobre o quadro e grava o gancho, se houver."""
    im = ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")
    im = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(0.5, 0.4))
    if texto:
        d = ImageDraw.Draw(im)
        fnt = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 62)
        largura = d.textlength(texto, font=fnt)
        x, y = (W - largura) / 2, H - 430
        d.text((x + 3, y + 3), texto, font=fnt, fill=(0, 0, 0))
        d.text((x, y), texto, font=fnt, fill=(255, 255, 255))
    im.save(destino, quality=92)


def montar(saida, fotos, texto=None):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    tmp = os.path.join(os.path.dirname(os.path.abspath(saida)) or ".", "_reel_tmp")
    os.makedirs(tmp, exist_ok=True)
    prontas = []
    for i, f in enumerate(fotos):
        p = os.path.join(tmp, f"f{i:02d}.jpg")
        preparar(f, p, texto if i == 0 else None)
        prontas.append(p)

    entradas, filtros = [], []
    for i, p in enumerate(prontas):
        # ATENCAO: o 'd' do zoompan conta frames POR FRAME DE ENTRADA. Por isso
        # a entrada precisa ter exatamente 1 frame (-framerate 1 -t 1), senao o
        # video sai com dezenas de vezes a duracao pedida.
        entradas += ["-loop", "1", "-framerate", "1", "-t", "1", "-i", p]
        filtros.append(
            f"[{i}:v]scale={int(W*1.25)}:{int(H*1.25)},"
            f"zoompan=z='min(zoom+0.0012,1.18)':d={DUR*FPS}:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
            f"setsar=1[v{i}]"
        )

    if len(prontas) == 1:
        cadeia = ";".join(filtros) + ";[v0]null[out]"
    else:
        cadeia = ";".join(filtros) + ";"
        anterior = "v0"
        for i in range(1, len(prontas)):
            offset = i * DUR - FADE * i
            rotulo = "out" if i == len(prontas) - 1 else f"x{i}"
            cadeia += (f"[{anterior}][v{i}]xfade=transition=fade:"
                       f"duration={FADE}:offset={offset}[{rotulo}];")
            anterior = rotulo
        cadeia = cadeia.rstrip(";")

    cmd = [ffmpeg, "-y", *entradas, "-filter_complex", cadeia,
           "-map", "[out]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-crf", "21", "-movflags", "+faststart", saida]
    r = subprocess.run(cmd, capture_output=True, text=True)
    for p in prontas:
        os.remove(p)
    os.rmdir(tmp)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        sys.exit(1)
    print(f"[ok] {saida} — {os.path.getsize(saida)//1024} KB")


if __name__ == "__main__":
    args = sys.argv[1:]
    texto = None
    if "--texto" in args:
        i = args.index("--texto")
        texto = args[i + 1]
        args = args[:i] + args[i + 2:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    montar(args[0], args[1:], texto)
