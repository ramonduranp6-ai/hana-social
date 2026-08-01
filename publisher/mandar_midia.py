"""
Canal Claude -> Telegram para MÍDIA avulsa (prévia, teste, rascunho).

Por que existe: `mandar_recado.py` só manda texto e `mostrar_fila.py` só manda
o que já está na fila. Faltava o caso mais comum na conversa — "montei uma
prévia, me manda pra ver" — e o Ramón foi explícito em 01/08/2026 sobre onde
quer ver: "Eu vi pelo telegram, muito melhor olhar por lá."

O token do bot mora nos secrets do GitHub, então isto roda pelo workflow:
    gh workflow run publish.yml -R ramonduranp6-ai/hana-social \
       -f midia="content/previas/arquivo.mp4" -f midia_texto="o que é isto"

Manda o ARQUIVO (upload multipart), não a URL: assim o vídeo aparece tocável
no celular dele mesmo que o repositório mude de lugar depois.

Regra da casa que este script NÃO substitui: nenhuma mídia vai para ele sem
passar por um auditor que não seja quem produziu. Isto aqui é só o cano.
"""

import os
import sys

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API = "https://api.telegram.org/bot{token}/{method}"
LIMITE_MB = 50  # limite duro de upload da Bot API


def mandar(token, chat_id, caminho, texto=""):
    if not os.path.isfile(caminho):
        print(f"[erro] arquivo nao existe: {caminho}")
        return False
    mb = os.path.getsize(caminho) / (1024 * 1024)
    if mb > LIMITE_MB:
        print(f"[erro] {mb:.1f} MB passa do limite de {LIMITE_MB} MB da Bot API")
        return False

    ext = os.path.splitext(caminho)[1].lower()
    if ext in (".mp4", ".mov"):
        metodo, campo = "sendVideo", "video"
    elif ext in (".jpg", ".jpeg", ".png"):
        metodo, campo = "sendPhoto", "photo"
    elif ext in (".mp3", ".wav", ".m4a"):
        metodo, campo = "sendAudio", "audio"
    else:
        metodo, campo = "sendDocument", "document"

    # Etiqueta obrigatória: ele precisa saber a QUE mensagem está respondendo
    # (cobrança de 01/08/2026). Ver publisher/etiqueta.py.
    assunto = os.environ.get("MIDIA_ASSUNTO", "").strip()
    responda = os.environ.get("MIDIA_RESPONDA", "").strip() or None
    if assunto:
        from etiqueta import etiquetar
        texto = etiquetar(assunto, texto, responda)

    with open(caminho, "rb") as f:
        r = requests.post(API.format(token=token, method=metodo),
                          data={"chat_id": chat_id, "caption": texto[:1024]},
                          files={campo: (os.path.basename(caminho), f)},
                          timeout=300)
    resp = r.json()
    if resp.get("ok"):
        print(f"[ok] entregue: {caminho} ({mb:.1f} MB) via {metodo}")
        return True
    print(f"[erro] telegram recusou: {resp.get('description')}")
    return False


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    caminho = os.environ.get("MIDIA") or (sys.argv[1] if len(sys.argv) > 1 else "")
    texto = os.environ.get("MIDIA_TEXTO", "")
    if not token or not chat_id:
        print("[erro] faltam TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID")
        return 1
    if not caminho:
        print("[erro] falta o caminho da midia (variavel MIDIA)")
        return 1
    return 0 if mandar(token, chat_id, caminho, texto) else 1


if __name__ == "__main__":
    sys.exit(main())
