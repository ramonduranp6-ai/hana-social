# -*- coding: utf-8 -*-
"""
Montador de Reel de VÁRIOS CLIPES — cortes, movimento e texto no tempo certo.

POR QUE EXISTE (02/08/2026). O `reel_de_video.py` pega UM vídeo, corta um trecho
e carimba UMA frase por cima. Foi o que entregamos ao Ramón e ele reprovou com
todas as letras: *"Tá horrível o conjunto do vídeo, coisa de amador, vc só
colocou um texto… vcs basicamente me proporiam o vídeo que mandei."* Ele estava
certo: aquilo não era montagem, era renomear arquivo.

O que faltava, e este script faz:
  - **CORTE.** Vários clipes emendados em corte seco, cada um com entrada e saída
    em segundos. Reel de plano único é o que parece amador.
  - **MOVIMENTO.** punch-in (fecha no rosto), zoom-out (abre e revela) e
    aceleração — o movimento é o que conta a piada, não a decoração.
  - **TEXTO NO TEMPO.** Cada frase aparece e some na hora marcada, com tarja
    atrás para ler sem som. Texto estático do começo ao fim entrega a piada no
    primeiro frame e o espectador rola.
  - **SOM DA CENA.** O áudio original de cada corte vem junto (o nicho roda em
    áudio original: 4 de 4 Reels de maior alcance medidos em 31/07/2026).

O roteiro NÃO fica no código — vem de um JSON, para dar para remontar variação
sem mexer em lógica. Mesma decisão do `reel_ritmado.py`.

Uso:
    python studio/montar_reel.py roteiro.json saida.mp4

Formato do roteiro (ver exemplo em `studio/roteiros/`):
{
  "cortes": [
    {"arquivo": "...mp4", "de": 0.4, "ate": 2.8, "movimento": "seco"},
    {"arquivo": "...mov", "de": 4.0, "ate": 8.0, "movimento": "acelerado",
     "fator": 2.0, "foco": 0.5},
    {"arquivo": "...mp4", "de": 3.2, "ate": 5.2, "movimento": "punch",
     "forca": 0.15}
  ],
  "textos": [
    {"de": 0.2, "ate": 2.0, "texto": "AVALIACAO DO FUNCIONARIO",
     "posicao": "baixo"}
  ]
}

`foco` (0 a 1) diz de que parte da largura sai o recorte 9:16 num vídeo deitado —
0 é a esquerda, 1 é a direita. Sem isso, vídeo horizontal perde o assunto.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W, H, FPS = 1080, 1920, 30
FONTE = r"C:\Windows\Fonts\arialbd.ttf"

# Onde cada faixa de texto fica, em fração da altura.
# Duas zonas são PROIBIDAS dentro do Reels e o texto tem que ficar entre elas:
#   - topo (~0 a 16%): barra de status e cabeçalho do Reels;
#   - rodapé (~a partir de 75%): nome do perfil, legenda e o áudio.
# O 0,20 do "alto" foi reprovado pelo auditor em 02/08/2026 por encostar no
# cabeçalho — por isso agora é 0,30.
POSICOES = {"alto": 0.30, "meio": 0.46, "baixo": 0.66}


def ff():
    return imageio_ffmpeg.get_ffmpeg_exe()


def _rodar(args):
    r = subprocess.run(args, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1500:])
    return r


def _filtro_video(corte):
    """Monta a cadeia de filtros de UM corte: recorte 9:16, movimento, tamanho."""
    mov = corte.get("movimento", "seco")
    dur = float(corte["ate"]) - float(corte["de"])
    fator = float(corte.get("fator", 1.0)) if mov == "acelerado" else 1.0
    dur_saida = dur / fator

    # Recorte 9:16 pegando o maior retângulo possível. `foco` desloca o recorte
    # na horizontal para vídeo deitado não cortar justamente a cachorra.
    foco = float(corte.get("foco", 0.5))
    crop = ("crop=w='min(iw,ih*9/16)':h='min(ih,iw*16/9)'"
            ":x='(iw-ow)*%.3f':y='(ih-oh)/2'" % foco)

    partes = [crop]

    # APROXIMAR: recorte fixo, feito ANTES do movimento. Existe porque o auditor
    # reprovou um corte em 02/08/2026 com "sobra muito chão" — o plano estava
    # certo, a cachorra é que era pequena no quadro. `aproximar: 1.4` joga fora
    # 40% da moldura e deixa ela grande, sem precisar trocar de clipe.
    # `foco_y` desce ou sobe o recorte (0 = topo, 1 = base) para não decepar o
    # assunto quando ele não está no meio da tela.
    aprox = float(corte.get("aproximar", 1.0))
    if aprox > 1.001:
        fy = float(corte.get("foco_y", 0.5))
        partes.append(
            "crop=w='2*trunc(iw/%.4f/2)':h='2*trunc(ih/%.4f/2)'"
            ":x='(iw-ow)/2':y='(ih-oh)*%.3f'" % (aprox, aprox, fy))

    if mov == "acelerado":
        partes.append("setpts=PTS/%.4f" % fator)

    quadros = max(int(round(dur_saida * FPS)), 1)
    forca = float(corte.get("forca", 0.15))

    if mov in ("punch", "zoomout"):
        # ⚠️ NÃO usar `zoompan` aqui. Foi a primeira tentativa (02/08/2026) e ela
        # ESTICA O CLIPE: um corte de 1,8s virou 36s e o Reel inteiro saiu com
        # 83 segundos em vez de 11,6. O zoompan cospe vários quadros por quadro
        # de entrada e o `d=1` não segurou. Recorte animado com `crop` faz o
        # mesmo efeito e mantém a duração — cada quadro entra e sai uma vez.
        #
        # Sobe a resolução antes: fechar 15% partindo de 1080 de largura deixa
        # a imagem visivelmente mole.
        partes.append("scale=%d:%d" % (int(W * 1.6), int(H * 1.6)))
        if mov == "punch":
            zoom = "(1+%.5f*min(t/%.4f,1))" % (forca, dur_saida)
        else:
            zoom = "(%.5f-%.5f*min(t/%.4f,1))" % (1 + forca, forca, dur_saida)
        # Largura e altura têm que ser PARES em yuv420p, por isso o 2*trunc(../2).
        partes.append(
            "crop=w='2*trunc(iw/%s/2)':h='2*trunc(ih/%s/2)'"
            ":x='(iw-ow)/2':y='(ih-oh)/2'" % (zoom, zoom))
        partes.append("scale=%d:%d" % (W, H))
    else:
        partes.append("scale=%d:%d" % (W, H))

    # EXPOSIÇÃO. Entrou em 03/08/2026: o clipe dela adulta com a bola é filmado
    # contra a janela, e ela saía como um vulto preto — a auditoria reprovou por
    # "não dá para confirmar que é a mesma cadela". Recortar não conserta luz.
    # `clarear` levanta as sombras com gamma (não com brightness, que lava a
    # imagem inteira e estoura a janela ao fundo).
    clarear = float(corte.get("clarear", 0.0))
    if clarear > 0.001:
        partes.append("eq=gamma=%.3f:saturation=%.3f:contrast=%.3f"
                      % (1.0 + clarear, 1.0 + clarear * 0.35, 1.0 + clarear * 0.12))

    # CINEMA. Pedido dele em 04/08/2026: "quero reels cinematograficos".
    # Nao e filtro de rede social: e o tratamento que faz material de celular
    # parecer filmado — contraste em S (preto mais fechado), leve dessaturacao
    # com realce de pele/pelo, e vinheta discreta puxando o olho para o centro.
    # Vem DEPOIS do movimento para o grade valer na imagem final.
    if corte.get("cinema"):
        f = float(corte.get("cinema")) if not isinstance(corte["cinema"], bool) else 1.0
        partes.append("curves=master='0/0 0.25/%.3f 0.5/0.5 0.75/%.3f 1/1'"
                      % (0.25 - 0.05 * f, 0.75 + 0.04 * f))
        partes.append("eq=saturation=%.3f:contrast=%.3f:gamma=%.3f"
                      % (1 - 0.12 * f, 1 + 0.10 * f, 1 - 0.03 * f))
        partes.append("vignette=angle=PI/%.2f" % (5.5 - 0.8 * f))

    partes += ["setsar=1", "fps=%d" % FPS, "format=yuv420p"]
    return ",".join(partes), dur_saida


def _filtro_audio(corte):
    mov = corte.get("movimento", "seco")
    partes = ["aresample=44100"]
    if mov == "acelerado":
        f = float(corte.get("fator", 1.0))
        # atempo só aceita 0,5 a 2,0 por instância; encadeia se passar disso.
        resto = f
        while resto > 2.0:
            partes.append("atempo=2.0")
            resto /= 2.0
        while resto < 0.5:
            partes.append("atempo=0.5")
            resto /= 0.5
        partes.append("atempo=%.4f" % resto)
    if corte.get("mudo"):
        partes.append("volume=0")
    # Nivela o volume entre cortes de cenas diferentes: sem isso a emenda de um
    # clipe alto com um baixo vira um susto.
    partes.append("dynaudnorm=f=250:g=15")
    partes.append("aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo")
    return ",".join(partes)


FOTO_EXT = (".jpg", ".jpeg", ".png", ".webp")


def _e_foto(caminho):
    """Foto entra como corte igual a vídeo.

    Faltava, e a falta custou caro: em 04/08/2026 ele cobrou —
    *"Para fazer reel vc não usa apenas vídeo, vc tb pode fazer com fotos, e vc
    tem portfólio de fotos bem grande"*. O projeto tem 62 fotos utilizáveis e
    eu vinha montando tudo com os mesmos cinco clipes de vídeo.

    Numa foto, `de`/`ate` deixam de ser trecho do arquivo e passam a ser
    simplesmente quanto tempo ela fica na tela. Foto SEMPRE com movimento
    (punch ou zoomout): foto parada em Reel é o que ele chama de amador, e o
    movimento é o que transforma retrato em plano de cinema.
    """
    return caminho.lower().endswith(FOTO_EXT)


def _tem_audio(caminho):
    r = subprocess.run([ff(), "-i", caminho], capture_output=True, text=True,
                       errors="replace")
    return "Audio:" in r.stderr


def _cartela(texto, destino, posicao="baixo", px=72, cor=(255, 255, 255, 255)):
    """Desenha a frase num PNG transparente, com tarja atrás para ler sem som.

    `cor` existe por causa da "Yellow Font Theory", medida em julho/2026: texto
    AMARELO virou código de confissão / momento vulnerável no Instagram, e o
    público lê a cor antes de ler a frase. Usar só quando a peça for confissão —
    amarelo em tudo perde o significado.
    """
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        fonte = ImageFont.truetype(FONTE, px)
    except OSError:
        fonte = ImageFont.load_default()

    largura_col = max(int(W * 0.86 / (px * 0.56)), 8)
    linhas = textwrap.wrap(texto, width=largura_col) or [texto]
    alturas = []
    for ln in linhas:
        caixa = d.textbbox((0, 0), ln, font=fonte)
        alturas.append(caixa[3] - caixa[1])
    passo = max(alturas) + int(px * 0.42)
    total = passo * len(linhas)

    y0 = int(H * POSICOES.get(posicao, 0.72)) - total // 2
    margem = int(px * 0.42)
    d.rounded_rectangle(
        [int(W * 0.05), y0 - margem, int(W * 0.95), y0 + total + margem],
        radius=int(px * 0.35), fill=(0, 0, 0, 170))

    y = y0
    for ln in linhas:
        caixa = d.textbbox((0, 0), ln, font=fonte)
        x = (W - (caixa[2] - caixa[0])) // 2 - caixa[0]
        d.text((x, y - caixa[1]), ln, font=fonte, fill=cor)
        y += passo
    img.save(destino)


REGISTRO_FOTOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "content", "fotos-usadas.json")


def _fotos_usadas():
    """Fotos que já foram ao ar ou já estão na fila, por nome de arquivo."""
    try:
        with open(REGISTRO_FOTOS, encoding="utf-8") as f:
            return {k: v for k, v in json.load(f).items()}
    except (OSError, ValueError):
        return {}


def registrar_fotos(roteiro, onde):
    """Marca as fotos deste roteiro como usadas. Chamar ao criar o post."""
    usadas = _fotos_usadas()
    for c in roteiro.get("cortes", []):
        if _e_foto(c.get("arquivo", "")):
            usadas.setdefault(os.path.basename(c["arquivo"]), []).append(onde)
    os.makedirs(os.path.dirname(REGISTRO_FOTOS), exist_ok=True)
    with open(REGISTRO_FOTOS, "w", encoding="utf-8") as f:
        json.dump(usadas, f, ensure_ascii=False, indent=1, sort_keys=True)
    return usadas


def _conferir_repetida(roteiro):
    """RECUSA montar se uma foto já usada voltar sem autorização.

    Cobrança dele em 04/08/2026: *"Vc está usando as mesma fotos sempre.
    Quantas fotos da hana vc tem?"* — e ele tinha razão: eram 70 fotos
    distintas no acervo e eu tinha usado 5. Regra escrita não bastou (o
    projeto já tinha a regra de não repetir e eu repeti mesmo assim), então
    agora quem recusa é o código.

    Para reusar de propósito, o roteiro declara `"permitir_repetir": true` —
    fica explícito no arquivo, e não acontece por distração.
    """
    if roteiro.get("permitir_repetir"):
        return
    usadas = _fotos_usadas()
    repetidas = [os.path.basename(c["arquivo"]) for c in roteiro.get("cortes", [])
                 if _e_foto(c.get("arquivo", ""))
                 and os.path.basename(c["arquivo"]) in usadas]

    # Comparar por NOME nao basta, e isso deixou passar o erro que ele viu:
    # as fotos sao EDITADAS antes de virar post, entao o arquivo publicado tem
    # outro nome e outro hash — e a mesma imagem voltava como se fosse nova.
    # Agora a comparacao e por IMPRESSAO DIGITAL DA IMAGEM (dhash), a mesma que
    # o checar_repetida.py ja usava contra o perfil.
    try:
        from PIL import Image as _Im
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from checar_repetida import dhash as _dh
        import glob as _g
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ja = []
        for base in ("content/posted", "content/queue"):
            for d in _g.glob(os.path.join(raiz, base, "*", "")):
                for f in os.listdir(d):
                    if f.lower().endswith((".jpg", ".jpeg", ".png")):
                        try:
                            ja.append((os.path.basename(d.rstrip("/\\")),
                                       _dh(_Im.open(os.path.join(d, f)))))
                        except Exception:
                            pass
        for c in roteiro.get("cortes", []):
            if not _e_foto(c.get("arquivo", "")):
                continue
            try:
                h = _dh(_Im.open(c["arquivo"]))
            except Exception:
                continue
            for onde, hs in ja:
                if bin(h ^ hs).count("1") <= 6:
                    repetidas.append("%s (mesma imagem do post %s)"
                                     % (os.path.basename(c["arquivo"]), onde))
                    break
    except Exception as exc:  # noqa: BLE001 — a checagem por nome ja rodou acima
        print("[aviso] nao consegui conferir por imagem (%s)" % str(exc)[:80])

    if repetidas:
        raise SystemExit(
            "[recusado] estas fotos JA foram usadas: %s\n"
            "           O acervo tem dezenas de fotos — escolha outra.\n"
            "           Se for reuso de proposito, ponha \"permitir_repetir\": true"
            " no roteiro." % ", ".join(sorted(set(repetidas))))


def montar(roteiro, saida):
    _conferir_repetida(roteiro)
    cortes = roteiro["cortes"]
    textos = roteiro.get("textos", [])
    tmp = tempfile.mkdtemp(prefix="reel_")
    try:
        pedacos, marcas, t = [], [], 0.0
        for i, c in enumerate(cortes):
            vf, dur = _filtro_video(c)
            destino = os.path.join(tmp, "seg%02d.mp4" % i)
            if _e_foto(c["arquivo"]):
                # Foto vira clipe de `dur` segundos, com silêncio do mesmo
                # tamanho para o concat não perder o sincronismo do áudio.
                args = [ff(), "-y", "-loop", "1", "-t", "%.3f" % dur,
                        "-i", c["arquivo"],
                        "-f", "lavfi", "-t", "%.3f" % dur,
                        "-i", "anullsrc=r=44100:cl=stereo",
                        "-vf", vf, "-map", "0:v:0", "-map", "1:a:0"]
                args += ["-c:v", "libx264", "-preset", "medium", "-crf", "19",
                         "-pix_fmt", "yuv420p", "-r", str(FPS),
                         "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2",
                         destino]
                _rodar(args)
                pedacos.append(destino)
                marcas.append((t, t + dur, c.get("arquivo")))
                t += dur
                continue
            args = [ff(), "-y", "-ss", str(c["de"]), "-to", str(c["ate"]),
                    "-i", c["arquivo"], "-vf", vf]
            if _tem_audio(c["arquivo"]):
                args += ["-af", _filtro_audio(c)]
            else:
                # Silêncio do tamanho certo, senão o concat perde o sincronismo
                # e o áudio dos cortes seguintes anda para trás.
                args = [ff(), "-y", "-ss", str(c["de"]), "-to", str(c["ate"]),
                        "-i", c["arquivo"],
                        "-f", "lavfi", "-t", "%.3f" % dur,
                        "-i", "anullsrc=r=44100:cl=stereo",
                        "-vf", vf, "-map", "0:v:0", "-map", "1:a:0"]
            args += ["-c:v", "libx264", "-preset", "medium", "-crf", "19",
                     "-pix_fmt", "yuv420p", "-r", str(FPS),
                     "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2",
                     destino]
            _rodar(args)
            pedacos.append(destino)
            marcas.append((t, t + dur, c.get("arquivo")))
            t += dur

        lista = os.path.join(tmp, "lista.txt")
        with open(lista, "w", encoding="utf-8") as f:
            for p in pedacos:
                f.write("file '%s'\n" % p.replace("\\", "/"))
        emendado = os.path.join(tmp, "emendado.mp4")
        _rodar([ff(), "-y", "-f", "concat", "-safe", "0", "-i", lista,
                "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                "-pix_fmt", "yuv420p", "-r", str(FPS),
                "-c:a", "aac", "-b:a", "160k", emendado])

        # TRILHA. Entrou em 03/08/2026 a pedido dele: *"Cadê a música, não era pra
        # ser algo divertido?"*. A música NÃO apaga o som da cena — as duas
        # convivem: `abafar_ate` deixa a trilha baixa enquanto o áudio da cena
        # importa (a mastigada da cenoura é o gancho sonoro da abertura) e sobe
        # depois. `inicio` corta a trilha mais para a frente, e é assim que a
        # virada dela cai no corte certo em vez de cair em qualquer lugar.
        trilha = roteiro.get("trilha")
        if trilha:
            com_musica = os.path.join(tmp, "com_musica.mp4")
            vol_alto = float(roteiro.get("volume_trilha", 0.85))
            vol_baixo = float(roteiro.get("volume_trilha_abafada", 0.30))
            abafar_ate = float(roteiro.get("abafar_ate", 0.0))
            ini = float(roteiro.get("inicio_trilha", 0.0))
            if abafar_ate > 0:
                vol = "volume='if(lt(t,%.2f),%.3f,%.3f)':eval=frame" % (
                    abafar_ate, vol_baixo, vol_alto)
            else:
                vol = "volume=%.3f" % vol_alto
            filtro_a = (
                "[1:a]atrim=start=%.3f,asetpts=PTS-STARTPTS,%s,"
                "afade=t=out:st=%.2f:d=0.6[m];"
                "[0:a][m]amix=inputs=2:duration=first:dropout_transition=0,"
                "alimiter=limit=0.95[a]" % (ini, vol, max(t - 0.6, 0.1)))
            _rodar([ff(), "-y", "-i", emendado, "-stream_loop", "-1", "-i", trilha,
                    "-filter_complex", filtro_a, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", "%.3f" % t, com_musica])
            emendado = com_musica

        if not textos:
            shutil.copy2(emendado, saida)
            print("[ok] %s — %.1fs, %d cortes, sem texto%s"
                  % (saida, t, len(cortes), ", com trilha" if trilha else ""))
            return t

        entradas = [emendado]
        filtro, atual = [], "0:v"
        for i, tx in enumerate(textos):
            png = os.path.join(tmp, "txt%02d.png" % i)
            cor = (255, 214, 0, 255) if tx.get("amarelo") else (255, 255, 255, 255)
            _cartela(tx["texto"], png, tx.get("posicao", "baixo"),
                     int(tx.get("px", 72)), cor)
            entradas.append(png)
            prox = "v%d" % i
            filtro.append(
                "[%s][%d:v]overlay=0:0:enable='between(t,%.3f,%.3f)'[%s]"
                % (atual, i + 1, float(tx["de"]), float(tx["ate"]), prox))
            atual = prox

        args = [ff(), "-y"]
        for e in entradas:
            args += ["-i", e]
        args += ["-filter_complex", ";".join(filtro),
                 "-map", "[%s]" % atual, "-map", "0:a?",
                 "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                 "-pix_fmt", "yuv420p", "-r", str(FPS),
                 "-c:a", "aac", "-b:a", "160k", saida]
        _rodar(args)
        print("[ok] %s — %.1fs, %d cortes, %d entradas de texto%s"
              % (saida, t, len(cortes), len(textos),
                 ", com trilha" if roteiro.get("trilha") else ""))
        for ini, fim, arq in marcas:
            print("     %5.1fs a %5.1fs  %s" % (ini, fim, os.path.basename(arq)))
        return t
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        roteiro = json.load(f)
    montar(roteiro, sys.argv[2])


if __name__ == "__main__":
    main()
