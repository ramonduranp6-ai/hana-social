"""
Comandos por Telegram — o Ramón mandando o projeto pelo celular.

Pedido dele em 02/08/2026: *"Gostaria de poder te dar comandos dos Telegram."*

Como se encaixa: `telegram_approve.sync_approvals()` já lê toda mensagem de
texto dele e entrega para a `recepcionista` (que responde com o Gemini). Este
módulo entra ANTES da recepcionista: se a mensagem for um comando conhecido,
ele executa e responde na hora; se não for, deixa passar e a conversa segue
como antes. Assim "pausar" nunca vira papo do Gemini.

Duas coisas que ele precisa saber, e que a resposta de `ajuda` diz:
  1. **O robô acorda a cada 30 minutos.** Não é chat ao vivo — o comando entra
     na próxima rodada. Atraso de minutos, nunca de horas.
  2. **Nenhum comando publica nada.** O que publica continua sendo o botão
     Aprovar. Os comandos aqui só mostram coisa ou PARAM a publicação, que é o
     lado seguro de errar.

Por que "pausar" existe: hoje, se ele viajar ou se arrepender de um post
aprovado, a única saída é abrir o computador. Um freio pelo celular é a peça
que faltava — e ele bloqueia a publicação sem apagar nada, então é reversível
com "voltar".
"""

import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FREIO = os.path.join(RAIZ, "content", ".pausado")
PLACAR = os.path.join(RAIZ, "content", "placar.md")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def esta_pausado():
    """Lido pelo run.py antes de publicar qualquer coisa."""
    return os.path.isfile(FREIO)


def _normalizar(texto):
    """Tira acento, pontuação e caixa — ele escreve do celular, com pressa."""
    import unicodedata
    t = unicodedata.normalize("NFD", texto.strip().lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return "".join(c if c.isalnum() or c.isspace() else " " for c in t).split()


# Cada comando: (nomes que ele pode digitar, função, o que faz — para a ajuda).
# Sinônimos generosos de propósito: comando que só funciona com a palavra
# exata é comando que ele não usa.
def _cmd_ajuda(_):
    linhas = ["Comandos que eu entendo aqui no Telegram:", ""]
    for nomes, _f, desc in COMANDOS:
        linhas.append(f"• *{nomes[0]}* — {desc}")
    linhas += [
        "",
        "Duas coisas importantes:",
        "1) O robô acorda a cada 30 minutos, então o comando entra na próxima "
        "rodada — pode demorar alguns minutos.",
        "2) Nenhum comando publica nada. Quem publica é o botão Aprovar.",
        "",
        "Qualquer outra coisa que você escrever eu respondo normal, como sempre.",
    ]
    return "\n".join(linhas)


def _cmd_estado(_):
    import postqueue
    posts = sorted(postqueue.load_all(), key=lambda p: p.get("scheduled_for", ""))
    if not posts:
        corpo = "A fila está VAZIA — não tem post agendado."
    else:
        linhas = [f"Fila com {len(posts)} post(s):"]
        for p in posts:
            quando = p.get("scheduled_for", "?")[:10]
            marca = "OK" if p.get("status") == "approved" else p.get("status", "?").upper()
            linhas.append(f"• {quando} — {p['_id']} ({p.get('type')}) [{marca}]")
        corpo = "\n".join(linhas)
    if esta_pausado():
        corpo += "\n\n⏸ PUBLICAÇÃO PAUSADA por você. Mande 'voltar' para religar."
    return corpo


def _cmd_placar(_):
    if not os.path.isfile(PLACAR):
        return "Ainda não tem placar coletado."
    with open(PLACAR, encoding="utf-8") as f:
        texto = f.read().strip()
    # O limite do Telegram é 4096; corta pelo começo, que é o resumo.
    return texto[:3500] + ("\n\n(cortado — o resto está no arquivo)" if len(texto) > 3500 else "")


def _cmd_fila(_):
    """Reenvia a mídia da fila. Reusa o script que já existe."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    base = os.environ.get("MEDIA_BASE_URL")
    if not (token and chat and base):
        return "Não consigo mandar a fila agora — falta configuração do robô."
    try:
        import mostrar_fila
        n = mostrar_fila.mostrar(token, chat, base)
        return f"Mandei {n} post(s) da fila aí em cima."
    except Exception as exc:  # noqa: BLE001
        return f"Não consegui mandar a fila: {str(exc)[:150]}"


def _cmd_pausar(_):
    if esta_pausado():
        return "A publicação JÁ estava pausada. Mande 'voltar' para religar."
    with open(FREIO, "w", encoding="utf-8") as f:
        f.write("pausado por comando no Telegram\n")
    return ("⏸ PAUSADO. Nenhum post vai ao ar até você mandar 'voltar'.\n"
            "Nada foi apagado — a fila continua inteira.")


def _cmd_voltar(_):
    if not esta_pausado():
        return "A publicação já estava ligada — não havia nada pausado."
    os.remove(FREIO)
    return "▶ RELIGADO. Os posts voltam a sair no horário de sempre."


COMANDOS = [
    (("ajuda", "comandos", "help", "menu", "o que voce faz"), _cmd_ajuda,
     "esta lista"),
    (("estado", "status", "fila", "onde paramos", "como esta"), _cmd_estado,
     "o que está agendado e se está tudo certo"),
    (("ver fila", "mostrar fila", "me mostra a fila", "ver posts"), _cmd_fila,
     "reenvia as fotos e vídeos da fila para você olhar"),
    (("placar", "numeros", "metricas", "resultados"), _cmd_placar,
     "o que cada post rendeu de alcance, salvamento e seguidor"),
    (("pausar", "parar", "pausa", "para tudo", "suspender"), _cmd_pausar,
     "trava a publicação até você mandar voltar"),
    (("voltar", "retomar", "religar", "continuar"), _cmd_voltar,
     "destrava a publicação"),
]


def interpretar(texto):
    """
    Devolve (True, resposta) se for comando; (False, None) se não for.

    Casa por frase inteira, não por palavra solta: "pausar" é comando, mas
    "acho que a gente devia pausar os posts de foto" é conversa, e mandar isso
    para a recepcionista é o comportamento certo. A regra é simples de explicar
    para ele: comando é a palavra sozinha.
    """
    if not texto:
        return False, None
    palavras = _normalizar(texto)
    if not palavras or len(palavras) > 4:
        return False, None
    frase = " ".join(palavras)
    for nomes, funcao, _desc in COMANDOS:
        if frase in {" ".join(_normalizar(n)) for n in nomes}:
            try:
                return True, funcao(texto)
            except Exception as exc:  # noqa: BLE001 — comando nunca derruba o robô
                return True, f"Tentei rodar '{frase}' e deu erro: {str(exc)[:200]}"
    return False, None


if __name__ == "__main__":
    sys.path.insert(0, AQUI)
    alvo = " ".join(sys.argv[1:]) or "ajuda"
    achou, resposta = interpretar(alvo)
    print(f"[comando? {achou}]")
    print(resposta or "(não é comando — iria para a recepcionista)")
