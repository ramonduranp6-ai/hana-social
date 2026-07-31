"""
Entrega no Telegram o recado que o robô de domingo deixou no repositório.

Por que existe: `studio/lote_automatico.py` roda na MÁQUINA do Ramón, onde não
existem os secrets do GitHub — ou seja, ele não tem o token do bot. A saída
óbvia seria pedir ao Ramón que guardasse o token num arquivo local, e foi o que
eu ia fazer. Ele respondeu "arrume meu amigo", com razão: senha guardada em dois
lugares é senha para vazar em dois lugares.

Então o desenho virou este: o robô local escreve `content/aviso_lote.md` e
empurra para o GitHub; este script, que roda dentro do publish.yml (onde o
token existe), vê que o arquivo mudou e entrega no Telegram.

Anti-repetição: guarda a impressão digital do último recado entregue em
`content/.aviso_lote_enviado`. Sem isso, o publicador bate a cada 30 minutos e
mandaria o mesmo recado 48 vezes por dia — mesmo padrão que o metrics.py e o
reporte_semanal.py já usam.

Uso:
    python publisher/avisar_lote.py             # entrega se houver recado novo
    python publisher/avisar_lote.py --simular   # so mostra o que sairia
"""

import hashlib
import io
import os
import sys

# O console do Windows quebra com emoji — pegadinha ja paga no lote_automatico.
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
AVISO = os.path.join(RAIZ, "content", "aviso_lote.md")
MARCADOR = os.path.join(RAIZ, "content", ".aviso_lote_enviado")


def _digital(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]


def _ja_entregue(digital):
    return os.path.isfile(MARCADOR) and open(MARCADOR).read().strip() == digital


def main():
    simular = "--simular" in sys.argv

    if not os.path.isfile(AVISO):
        print("[avisar_lote] nao ha recado do lote — saindo calado.")
        return 0

    texto = open(AVISO, encoding="utf-8").read().strip()
    if not texto:
        print("[avisar_lote] recado vazio — saindo calado.")
        return 0

    digital = _digital(texto)
    if _ja_entregue(digital):
        print("[avisar_lote] este recado ja foi entregue — nao repito.")
        return 0

    if simular:
        print("--- sairia no Telegram ---")
        print(texto)
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        print("[avisar_lote][aviso] sem TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID — nao entreguei.")
        return 0

    # Nunca derruba o job: publicar post e mais importante que entregar recado.
    try:
        sys.path.insert(0, AQUI)
        from mandar_recado import mandar
        mandar(token, chat_id, "🎬 Recado do robô de domingo:\n\n" + texto)
    except Exception as exc:  # noqa: BLE001
        print(f"[avisar_lote][aviso] Telegram recusou ({str(exc)[:150]}) — tento na proxima rodada.")
        return 0

    # So marca DEPOIS de entregar. Se marcasse antes e a entrega falhasse, o
    # recado sumia para sempre.
    with open(MARCADOR, "w") as f:
        f.write(digital)
    print("[avisar_lote][ok] recado do lote entregue no Telegram.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
