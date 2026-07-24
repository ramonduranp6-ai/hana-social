"""
Kit de design da Hana — templates de arte para os posts.

Uso (a partir da raiz do repo):
    python studio/design_kit.py <foto_editada_1080x1350> <layout> <saida.jpg>

Layouts disponíveis:
    capa    -> capa de revista "BULLY" (masthead Bodoni, coverlines, código de barras)
    poster  -> poster streetwear "A CHEFIA" (moldura lilás, faixa ticker, grão)

A paleta é extraída da própria foto (pelo lilac da Hana + parede), então as
artes sempre combinam com a imagem. Regra do brand-brief: nunca gerar imagem
falsa da Hana — estes templates só compõem por cima de foto real editada.
"""

import os
import random
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageStat

FONTS = r"C:\Windows\Fonts"
CHARCOAL = (38, 33, 32)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def palette(im):
    """Extrai lilás (pelo), lilás escuro e creme (parede) da própria foto."""
    def patch(box, mult=1.0):
        st = ImageStat.Stat(im.crop(box))
        return tuple(min(255, int(c * mult)) for c in st.median)

    lilac = patch((700, 500, 860, 620))
    return {
        "lilac": lilac,
        "lilac_dk": tuple(int(c * 0.52) for c in lilac),
        "cream": patch((120, 60, 320, 150), 1.04),
    }


def spaced(d, xy, text, fnt, fill, tracking=0, center_w=None):
    """Desenha texto com espaçamento entre letras; centraliza se center_w."""
    x, y = xy
    if center_w:
        total = sum(d.textlength(c, font=fnt) + tracking for c in text) - tracking
        x = (center_w - total) / 2
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill)
        x += d.textlength(c, font=fnt) + tracking
    return x


def capa(base, headline="HANA", linha1="Tri lilac merle: a cor mais rara do jogo",
         linha2="Pose séria — o expediente do assistente de palco"):
    W, H = base.size
    pal = palette(base)
    cover = base.copy()

    # gradiente escuro no rodapé para legibilidade das coverlines
    grad = Image.new("L", (1, 400), 0)
    for i in range(400):
        grad.putpixel((0, i), int(150 * (i / 400) ** 1.6))
    grad = grad.resize((W, 400))
    black = Image.new("RGB", (W, 400), (10, 8, 8))
    cover.paste(Image.composite(black, cover.crop((0, H - 400, W, H)), grad), (0, H - 400))

    d = ImageDraw.Draw(cover)
    spaced(d, (0, -18), "BULLY", font("BOD_B.TTF", 218), CHARCOAL, tracking=6, center_w=W)
    spaced(d, (0, 218), "A  REVISTA  DA  PATROA", font("seguisb.ttf", 30),
           pal["lilac_dk"], tracking=10, center_w=W)
    d.text((46, 268), "Nº 1 — ITAJAÍ, SC", font=font("seguisb.ttf", 26), fill=CHARCOAL)

    d.text((46, H - 320), headline, font=font("BOD_B.TTF", 92), fill=pal["cream"])
    d.text((46, H - 212), linha1, font=font("seguisb.ttf", 37), fill=pal["cream"])
    d.text((46, H - 158), linha2, font=font("segoeui.ttf", 33), fill=(226, 216, 208))

    # código de barras decorativo
    bx, by, bw, bh = W - 256, H - 118, 210, 74
    d.rectangle((bx - 10, by - 10, bx + bw + 10, by + bh + 26), fill=pal["cream"])
    random.seed(7)
    x = bx
    while x < bx + bw:
        w_ = random.choice((2, 2, 3, 5, 7))
        d.rectangle((x, by, x + w_, by + bh), fill=(20, 18, 18))
        x += w_ + random.choice((2, 3, 4))
    d.text((bx + 18, by + bh + 2), "7 742026 000001",
           font=font("OCRAEXT.TTF", 19), fill=(20, 18, 18))
    return cover


def poster(base, titulo="A CHEFIA", subtitulo="& O ASSISTENTE DE PALCO"):
    W, H = base.size
    pal = palette(base)
    art = Image.new("RGB", (W, H), pal["cream"])
    d = ImageDraw.Draw(art)

    spaced(d, (0, 48), titulo, font("FRAHV.TTF", 88), CHARCOAL, tracking=4, center_w=W)
    spaced(d, (0, 148), subtitulo, font("FRADMCN.TTF", 40),
           pal["lilac_dk"], tracking=6, center_w=W)

    pw, ph = 880, 930
    photo = base.crop((90, 130, 990, 1081)).resize((pw, ph), Image.LANCZOS)
    px, py = (W - pw) // 2, 226
    d.rectangle((px + 22, py + 22, px + 22 + pw, py + 22 + ph), fill=pal["lilac"])
    art.paste(photo, (px, py))
    d.rectangle((px, py, px + pw, py + ph), outline=CHARCOAL, width=5)

    spaced(d, (0, py + ph + 42), "EST. 2026  —  @HANADURANSANCHES",
           font("seguisb.ttf", 27), CHARCOAL, tracking=4, center_w=W)

    band_y = H - 100
    d.rectangle((0, band_y, W, H), fill=pal["lilac_dk"])
    t = "HANA  •  EXOTIC BULLY MICRO  •  TRI LILAC MERLE  •  ITAJAÍ SC  •  "
    tx = -12
    while tx < W:
        tx = spaced(d, (tx, band_y + 32), t, font("bahnschrift.ttf", 34),
                    pal["cream"], tracking=2)

    # grão de filme
    noise = Image.effect_noise((W, H), 22).convert("L")
    art = Image.composite(art, ImageEnhance.Brightness(art).enhance(0.86),
                          noise.point(lambda v: 255 - max(0, min(30, 255 - v))))
    return art


LAYOUTS = {"capa": capa, "poster": poster}

if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[2] not in LAYOUTS:
        print(__doc__)
        sys.exit(1)
    src, layout, dst = sys.argv[1:4]
    img = Image.open(src).convert("RGB")
    LAYOUTS[layout](img).save(dst, quality=92, optimize=True)
    print(f"ok: {dst}")
