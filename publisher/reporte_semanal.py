# -*- coding: utf-8 -*-
"""
Reporte semanal da Hana no Telegram — a pauta da reunião estratégica de segunda.

Pedido do Ramón em 31/07/2026: reunião estratégica toda semana para ver como o
plano está indo e decidir o que criar, manter ou descontinuar. O robô monta a
pauta com NÚMERO (nunca com opinião) e manda pronta no Telegram; o Claude entra
só para decidir em cima dela. Custo zero de token.

Roda dentro do publish.yml, que já bate a cada 30 min. O script sai calado se
não for segunda-feira ou se a pauta desta semana já foi enviada — mesmo padrão
do metrics.py.

Uso:
    python publisher/reporte_semanal.py            # manda se for a hora
    python publisher/reporte_semanal.py --simular  # so imprime, nao manda
    python publisher/reporte_semanal.py --forcar   # manda agora, qualquer dia
"""

import io
import json
import os
import sys
from datetime import datetime, timedelta, timezone

# O console do Windows quebra com emoji. `reconfigure` em vez de
# io.TextIOWrapper: ver a nota no diagnostico.py — dois wrappers no mesmo
# buffer fecham um ao outro.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
METRICAS = os.path.join(RAIZ, "content", "metricas.json")
FILA = os.path.join(RAIZ, "content", "queue")
PAUTA_EXTRA = os.path.join(RAIZ, "content", "pauta_extra.md")
ESTADO = os.path.join(RAIZ, "content", ".reporte_semanal")

# Segunda-feira, a partir das 11h UTC (8h em Itajai).
DIA_DA_REUNIAO = 0
HORA_MINIMA_UTC = 11


def _semana(dt):
    ano, semana, _ = dt.isocalendar()
    return "%d-W%02d" % (ano, semana)


def _ja_mandou(semana):
    return os.path.isfile(ESTADO) and open(ESTADO).read().strip() == semana


def _marcar(semana):
    with open(ESTADO, "w") as f:
        f.write(semana)


def _coletas():
    if not os.path.isfile(METRICAS):
        return []
    return json.load(open(METRICAS, encoding="utf-8")).get("coletas", [])


def _fila():
    posts = []
    if not os.path.isdir(FILA):
        return posts
    for nome in sorted(os.listdir(FILA)):
        meta = os.path.join(FILA, nome, "post.json")
        if os.path.isfile(meta):
            try:
                p = json.load(open(meta, encoding="utf-8"))
                p["_id"] = nome
                posts.append(p)
            except (ValueError, OSError):
                continue
    return posts


def _linha_post(pid, dados):
    m = dados.get("metricas", {})
    tipo = "Reel" if dados.get("tipo") in ("VIDEO", "REELS") else "Foto"
    return "• %s (%s): %s de alcance, %s curtidas, %s salvos, %s compart., %s seguidores" % (
        pid, tipo, m.get("reach", "?"), m.get("likes", "?"),
        m.get("saved", "?"), m.get("shares", "?"), m.get("follows", "?"))


def montar(agora=None):
    """Devolve o texto da pauta. So numero medido — nada estimado."""
    agora = agora or datetime.now(timezone.utc)
    coletas = _coletas()
    if not coletas:
        return "Reuniao de segunda: ainda nao ha metrica coletada. Nada a decidir."

    hoje = coletas[-1]
    limite = (agora - timedelta(days=7)).strftime("%Y-%m-%d")
    antigas = [c for c in coletas if c["data"] <= limite]
    base = antigas[-1] if antigas else coletas[0]

    seg_hoje = hoje.get("seguidores", 0)
    seg_antes = base.get("seguidores", 0)
    delta = seg_hoje - seg_antes

    L = []
    # O diagnóstico vem PRIMEIRO, antes da tabela: o Ramón lê no celular e para
    # de ler cedo. Ele pediu isso em 31/07/2026 — a pauta listava número e não
    # dizia se o projeto está melhorando ou piorando.
    try:
        import diagnostico
        diag = diagnostico.montar(agora)
        if diag:
            L += [diag, "", "─" * 28, ""]
    except Exception as exc:  # noqa: BLE001 — diagnóstico nunca derruba a pauta
        print("[aviso] diagnostico falhou (%s) — pauta segue sem ele." % str(exc)[:120])

    L.append("📋 REUNIÃO ESTRATÉGICA — semana %s" % _semana(agora))
    L.append("Fonte: API do Instagram, coleta de %s." % hoje["data"])
    L.append("")
    L.append("1) SEGUIDORES: %d (%+d em 7 dias, base %s)" % (delta and seg_hoje or seg_hoje, delta, base["data"]))
    L.append("")

    posts = hoje.get("posts", {})
    if posts:
        L.append("2) O QUE CADA POST RENDEU")
        ordenados = sorted(posts.items(),
                           key=lambda kv: kv[1].get("metricas", {}).get("reach", 0),
                           reverse=True)
        for pid, dados in ordenados:
            L.append(_linha_post(pid, dados))

        # Os tres sinais que decidem se o conteudo presta.
        tot_salvos = sum(d.get("metricas", {}).get("saved", 0) or 0 for d in posts.values())
        tot_shares = sum(d.get("metricas", {}).get("shares", 0) or 0 for d in posts.values())
        tot_follows = sum(d.get("metricas", {}).get("follows", 0) or 0 for d in posts.values())
        L.append("")
        L.append("3) OS TRÊS SINAIS QUE CONTAM (soma de todos os posts)")
        L.append("Salvos: %d · Compartilhamentos: %d · Seguidores ganhos: %d"
                 % (tot_salvos, tot_shares, tot_follows))
        if tot_salvos == 0 and tot_shares == 0 and tot_follows == 0:
            L.append("⚠️ Os três continuam em ZERO: quem vê não reage. "
                     "É problema de conteúdo, não de entrega.")

        reels = [d for d in posts.values() if d.get("tipo") in ("VIDEO", "REELS")]
        fotos = [d for d in posts.values() if d.get("tipo") not in ("VIDEO", "REELS")]
        L.append("")
        L.append("4) REEL x FOTO (alcance médio)")
        for rotulo, grupo in (("Reel", reels), ("Foto", fotos)):
            if grupo:
                media = sum(d.get("metricas", {}).get("reach", 0) or 0 for d in grupo) / len(grupo)
                L.append("%s: %.0f (%d post(s))" % (rotulo, media, len(grupo)))
            else:
                L.append("%s: ainda sem post publicado" % rotulo)

    fila = _fila()
    if fila:
        L.append("")
        L.append("5) FILA")
        for p in fila[:6]:
            L.append("• %s — %s — %s" % (p["_id"], p.get("type", "?"), p.get("status", "?")))
        pendentes = [p for p in fila if p.get("status") == "pending"]
        if pendentes:
            L.append("⏳ %d esperando o seu Aprovar/Recusar aqui no Telegram." % len(pendentes))

    if os.path.isfile(PAUTA_EXTRA):
        extra = open(PAUTA_EXTRA, encoding="utf-8").read().strip()
        if extra:
            L.append("")
            L.append("6) PARA VOCÊ DECIDIR")
            L.append(extra)

    # CONDIÇÃO DO CONSELHEIRO para o Diretor de Criação existir (31/07/2026):
    # "o Criador depende de alguém lembrar na segunda — e isso já quebrou aqui".
    # A pauta passa a cobrar o pacote da semana. Sem esta linha, o cargo é vetado.
    pacote = os.path.join(RAIZ, "content", "pacote-da-semana.md")
    L.append("")
    L.append("7) CHAMAR O DIRETOR DE CRIAÇÃO")
    if os.path.isfile(pacote):
        L.append("   Pacote da semana existe em content/pacote-da-semana.md — "
                 "conferir se é desta semana antes de usar.")
    else:
        L.append("   ⚠️ Pacote da semana PENDENTE. Sem ele, gancho e legenda "
                 "voltam a ser improviso na conversa.")

    L.append("")
    L.append("Régua: o que não mexer em salvos, compartilhamentos ou seguidores "
             "ganhos sai de cena. Respondo na segunda com a proposta de corte.")
    return "\n".join(L)


def main():
    simular = "--simular" in sys.argv
    forcar = "--forcar" in sys.argv
    agora = datetime.now(timezone.utc)
    semana = _semana(agora)

    if not (simular or forcar):
        if agora.weekday() != DIA_DA_REUNIAO or agora.hour < HORA_MINIMA_UTC:
            return
        if _ja_mandou(semana):
            return

    texto = montar(agora)
    if simular:
        print(texto)
        return

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        print("[aviso] sem TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID — pauta nao enviada")
        print(texto)
        return

    sys.path.insert(0, AQUI)
    from telegram_approve import notify
    notify(token, chat, texto)
    _marcar(semana)
    print("[ok] pauta da semana %s enviada no Telegram." % semana)


if __name__ == "__main__":
    main()
