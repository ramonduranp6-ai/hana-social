"""
Preparador de lote — faz o trabalho mecânico do estúdio de graça (Python local).

Uso (a partir da raiz do repo):

1. Editar tudo que estiver em "01 - brutas" e gerar folha de contato:
       python studio/preparar_lote.py editar
   -> corrige rotação EXIF, corta 4:5, aplica o tratamento "clean premium",
      exporta 1080x1350 em "OneDrive/Fotos da Hana/02 - selecionadas/" e
      salva contact_sheet.jpg lá (grade numerada para escolher no celular).

2. Criar um post na fila a partir de uma foto editada:
       python studio/preparar_lote.py post <arquivo.jpg> <id-do-post> <2026-08-05T21:00> "legenda..."
   -> cria content/queue/<id-do-post>/{image.jpg,post.json} (status pending).
      Lembrete: 21:00 UTC = 18:00 em Itajaí.

O que continua com o Claude: curadoria, legendas, criativos IA e a revisão final.
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONEDRIVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Fotos da Hana")
BRUTAS = os.path.join(ONEDRIVE, "01 - brutas (suba aqui)")
SELECIONADAS = os.path.join(ONEDRIVE, "02 - selecionadas")
QUEUE = os.path.join(ROOT, "content", "queue")
FOTO_EXTS = (".jpg", ".jpeg", ".png", ".heic")


def warmth(im, r, g, b):
    ch = [c.point(lambda v, f=f: min(255, int(v * f))) for c, f in zip(im.split(), (r, g, b))]
    return Image.merge("RGB", ch)


def clean(im):
    im = ImageEnhance.Brightness(im).enhance(1.03)
    im = ImageEnhance.Contrast(im).enhance(1.07)
    im = ImageEnhance.Color(im).enhance(1.06)
    return warmth(im, 1.015, 1.0, 0.985)


def crop45(im, anchor=0.5):
    w, h = im.size
    ch = int(w * 5 / 4)
    if ch <= h:
        top = int((h - ch) * anchor)
        return im.crop((0, top, w, top + ch))
    cw = int(h * 4 / 5)
    left = int((w - cw) * 0.5)
    return im.crop((left, 0, left + cw, h))


def editar():
    os.makedirs(SELECIONADAS, exist_ok=True)
    fotos = sorted(f for f in os.listdir(BRUTAS) if f.lower().endswith(FOTO_EXTS))
    thumbs = []
    for i, nome in enumerate(fotos, 1):
        img = ImageOps.exif_transpose(Image.open(os.path.join(BRUTAS, nome))).convert("RGB")
        out = crop45(clean(img)).resize((1080, 1350), Image.LANCZOS)
        out = out.filter(ImageFilter.UnsharpMask(2, 60, 3))
        destino = os.path.join(SELECIONADAS, f"{i:02d}_{os.path.splitext(nome)[0]}.jpg")
        out.save(destino, quality=90, optimize=True, progressive=True)
        thumbs.append((i, out))
        print(f"editada: {os.path.basename(destino)}")

    # folha de contato numerada (para escolher pelo celular)
    if thumbs:
        cols = 4
        cw, chh = 320, 440
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cw, rows * chh), (24, 24, 24))
        d = ImageDraw.Draw(sheet)
        fnt = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
        for i, t in thumbs:
            x, y = ((i - 1) % cols) * cw, ((i - 1) // cols) * chh
            mini = t.copy()
            mini.thumbnail((300, 375))
            sheet.paste(mini, (x + 10, y + 10))
            d.text((x + 18, y + 385), str(i), font=fnt, fill=(255, 235, 120))
        sheet.save(os.path.join(SELECIONADAS, "contact_sheet.jpg"), quality=85)
        print(f"contact_sheet.jpg com {len(thumbs)} fotos")


def post(arquivo, post_id, quando, legenda):
    pasta = os.path.join(QUEUE, post_id)
    os.makedirs(pasta, exist_ok=True)
    Image.open(arquivo).save(os.path.join(pasta, "image.jpg"), quality=90, optimize=True)
    meta = {
        "type": "image",
        "media_file": "image.jpg",
        "caption": legenda,
        "scheduled_for": quando + (":00Z" if len(quando) == 16 else ""),
        "status": "pending",
    }
    with open(os.path.join(pasta, "post.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"post criado: content/queue/{post_id} ({meta['scheduled_for']})")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "editar":
        editar()
    elif len(sys.argv) == 6 and sys.argv[1] == "post":
        post(*sys.argv[2:6])
    else:
        print(__doc__)
