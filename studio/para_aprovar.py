"""
Monta a pasta que o Ramón abre no celular para aprovar o lote.

Uso (a partir da raiz do repo):
    python studio/para_aprovar.py

Copia tudo que está na fila para
"Fotos da Hana/03 - APROVAR (semana)" — dentro do próprio projeto, que por sua
vez mora no OneDrive e sincroniza no celular dele. Numerado na ordem de
publicação, com 00_LEGENDAS.txt trazendo as legendas na mesma numeração.
Reel também ganha uma capa .jpg, senão não aparece na galeria do celular.

Por que existe (aprendido em 26-27/07/2026): o Ramón NÃO enxerga link do
raw.githubusercontent.com, nem arquivo anexado na conversa, nem link de
página publicada. A pasta do OneDrive é o canal que funciona no celular
dele. Ele responde pelos números.
"""

import json
import os
import shutil
import subprocess
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(RAIZ, "content", "queue")
DESTINO = os.path.join(RAIZ, "Fotos da Hana", "03 - APROVAR (semana)")


def capa_do_reel(video, destino):
    """Primeiro frame legível do Reel, para a galeria do celular mostrar algo."""
    try:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        print("[aviso] imageio-ffmpeg ausente: Reel vai sem capa")
        return
    subprocess.run([ff, "-y", "-ss", "1", "-i", video, "-frames:v", "1",
                    "-vf", "scale=1080:-2", destino], capture_output=True)


def main():
    if not os.path.isdir(QUEUE) or not os.listdir(QUEUE):
        print("Fila vazia — nada para aprovar.")
        return

    os.makedirs(DESTINO, exist_ok=True)
    for f in os.listdir(DESTINO):          # começa limpo, senão sobra lote velho
        os.remove(os.path.join(DESTINO, f))

    linhas = ["LOTE PARA APROVAR — Hana", "",
              "Responda pro Claude com os números (ex.: 1,2,4 sim / 3 não).", ""]

    for i, pid in enumerate(sorted(os.listdir(QUEUE)), 1):
        pj = os.path.join(QUEUE, pid, "post.json")
        if not os.path.isfile(pj):
            continue
        with open(pj, encoding="utf-8") as f:
            meta = json.load(f)
        quando = meta["scheduled_for"]
        dia = f"{quando[8:10]}-{quando[5:7]}"
        origem = os.path.join(QUEUE, pid, meta["media_file"])
        if not os.path.isfile(origem):
            print(f"[ERRO] mídia sumiu: {origem}")
            continue

        if meta.get("type") == "reel":
            shutil.copy(origem, os.path.join(DESTINO, f"{i:02d}_{dia}_REEL.mp4"))
            capa_do_reel(origem, os.path.join(DESTINO, f"{i:02d}_{dia}_REEL_capa.jpg"))
            tipo = "REEL (vídeo)"
        else:
            Image.open(origem).save(os.path.join(DESTINO, f"{i:02d}_{dia}.jpg"),
                                    quality=92)
            tipo = "Foto"

        linhas += [f"--- {i} --- {dia} · {tipo} · {meta.get('status','?')}",
                   meta.get("caption", ""), ""]

    with open(os.path.join(DESTINO, "00_LEGENDAS.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print(f"[ok] {DESTINO}")
    for f in sorted(os.listdir(DESTINO)):
        print("   ", f)
    # Ele pediu em 27/07/2026: o caminho COMPLETO tem que ir na mensagem dele.
    # Descrever a pasta so pelo nome ja fez ele nao achar.
    print("\nMandar pra ele o caminho COMPLETO abaixo (nao resumir, nao dizer "
          "'a pasta de sempre') e pedir a resposta pelos numeros:")
    print(f"\n    {DESTINO}\n")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
