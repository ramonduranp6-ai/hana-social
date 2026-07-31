# -*- coding: utf-8 -*-
"""
Reel a partir de VÍDEO REAL — Python local, custo zero, sem IA.

O `gerar_reel.py` monta slideshow de fotos. Este monta o Reel do jeito que o
nicho realmente cresce: vídeo de verdade, vertical, com gancho grande na
primeira tela e o som da própria cena.

Pegadinhas já pagas (estão na skill hana-social):
  - MOV de iPhone traz rotação nos metadados; cortar direto sai deitado. Aqui a
    rotação é aplicada e zerada antes do corte.
  - Gancho acima de ~25 caracteres vaza da tela: quebra automática em 2 linhas.
  - O texto é desenhado com PIL num PNG transparente e sobreposto — escapar
    acento e aspas no drawtext do ffmpeg no Windows dá errado calado.

Uso:
    python studio/reel_de_video.py entrada.MOV saida.mp4 --texto "GANCHO" \
        [--inicio 0] [--duracao 11] [--trilha musica.wav] [--volume-trilha 0.15]
"""

import argparse
import os
import subprocess
import sys
import textwrap

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONTE = r"C:\Windows\Fonts\arialbd.ttf"
TAM_FONTE = 78
MAX_COLUNA = 18          # caracteres por linha antes de quebrar
# 10% do topo cai DENTRO da interface do Reels e o texto ainda passa por cima da
# cadela — defeito apontado pelo auditor em 31/07/2026. Padrao agora e 16%.
TOPO_TEXTO = 0.16


def _ffmpeg():
    return imageio_ffmpeg.get_ffmpeg_exe()


def cartela(texto, destino, topo=TOPO_TEXTO):
    """PNG transparente 1080x1920 só com o gancho, sombra inclusa."""
    linhas = textwrap.wrap(texto.upper(), width=MAX_COLUNA) or [""]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(FONTE, TAM_FONTE)
    altura_linha = int(TAM_FONTE * 1.22)
    y = int(H * topo)
    for linha in linhas:
        largura = d.textlength(linha, font=fnt)
        x = (W - largura) / 2
        for dx, dy in ((4, 4), (-4, 4), (4, -4), (-4, -4)):
            d.text((x + dx, y + dy), linha, font=fnt, fill=(0, 0, 0, 210))
        d.text((x, y), linha, font=fnt, fill=(255, 255, 255, 255))
        y += altura_linha
    img.save(destino)
    return len(linhas)


def montar(entrada, saida, texto=None, inicio=0.0, duracao=11.0,
           trilha=None, volume_trilha=0.15, topo=TOPO_TEXTO):
    ff = _ffmpeg()
    tmp = os.path.join(os.path.dirname(os.path.abspath(saida)) or ".", "_reelv_tmp")
    os.makedirs(tmp, exist_ok=True)
    png = os.path.join(tmp, "gancho.png")

    # 1) normaliza: aplica a rotação do iPhone e zera os metadados.
    normal = os.path.join(tmp, "normal.mp4")
    r = subprocess.run([ff, "-y", "-ss", str(inicio), "-t", str(duracao), "-i", entrada,
                        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                        "-c:a", "aac", "-b:a", "160k", "-metadata:s:v", "rotate=0",
                        normal], capture_output=True, text=True, errors="ignore")
    if r.returncode != 0:
        print(r.stderr[-1200:])
        sys.exit("[erro] falhou ao normalizar o video")

    # 2) corta 9:16 cobrindo o quadro, sem deformar.
    vf = ("scale=%d:%d:force_original_aspect_ratio=increase,"
          "crop=%d:%d,setsar=1" % (W, H, W, H))

    entradas = ["-i", normal]
    if texto:
        cartela(texto, png, topo)
        entradas += ["-i", png]
    if trilha:
        entradas += ["-i", trilha]

    if texto:
        filtro = "[0:v]%s[base];[base][1:v]overlay=0:0[v]" % vf
    else:
        filtro = "[0:v]%s[v]" % vf

    idx_trilha = 2 if texto else 1
    if trilha:
        # Som da cena por cima, trilha baixinha por baixo (regra do projeto).
        filtro += (";[%d:a]volume=%s[t];[0:a][t]amix=inputs=2:duration=first:"
                   "dropout_transition=0[a]" % (idx_trilha, volume_trilha))
        mapa_audio = ["-map", "[a]"]
    else:
        mapa_audio = ["-map", "0:a?"]

    cmd = ([ff, "-y", *entradas, "-filter_complex", filtro, "-map", "[v]", *mapa_audio,
            "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", saida])
    r = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    # O OneDrive as vezes segura a pasta temporaria; limpeza nunca derruba o job.
    for f in (png, normal):
        try:
            os.remove(f)
        except OSError:
            pass
    try:
        os.rmdir(tmp)
    except OSError:
        pass
    if r.returncode != 0:
        print(r.stderr[-1500:])
        sys.exit("[erro] falhou ao montar o Reel")
    print("[ok] %s — %.1f MB" % (saida, os.path.getsize(saida) / 1048576))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("entrada")
    p.add_argument("saida")
    p.add_argument("--texto", default=None)
    p.add_argument("--inicio", type=float, default=0.0)
    p.add_argument("--duracao", type=float, default=11.0)
    p.add_argument("--trilha", default=None)
    p.add_argument("--volume-trilha", type=float, default=0.15)
    p.add_argument("--topo-texto", type=float, default=TOPO_TEXTO)
    a = p.parse_args()
    montar(a.entrada, a.saida, a.texto, a.inicio, a.duracao, a.trilha,
           a.volume_trilha, a.topo_texto)
