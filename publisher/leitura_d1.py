# -*- coding: utf-8 -*-
"""
Empurra no Telegram a LEITURA DO DIA 1 de cada post — sem depender de o Ramón
abrir conversa.

Exigência do conselheiro em 31/07/2026, ao vetar parte do plano da semana:
*"a leitura de 11/08 não pode depender do Ramón abrir conversa — o robô de
métricas tem que empurrar os números de dia 1 no Telegram"*. Sem isso, a
decisão mais importante do mês (o Reel de 10/08 mudou alguma coisa ou não?)
ficava dependendo de alguém lembrar de perguntar.

Por que DIA 1 e não o acumulado: medido no próprio projeto em 31/07/2026 —
somando os três posts antigos, o alcance cresceu +21 depois do primeiro dia e
gerou **zero** visita nova ao perfil. Alcance tardio não vira nada. Quem decide
é o número do dia 1.

Por que comparar só com posts da MESMA IDADE: nenhum post do perfil estabilizou
(`bar-hana` ainda subia no 9º dia). Comparar um post de 2 dias com um de 9 é
comparar coisas diferentes — era o defeito do placar antigo.

Roda dentro do publish.yml, depois da coleta de métricas. Sai calado se não
houver post completando 1 dia, e nunca manda o mesmo post duas vezes.

Uso:
    python publisher/leitura_d1.py             # entrega se houver
    python publisher/leitura_d1.py --simular   # so imprime
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
METRICAS = os.path.join(RAIZ, "content", "metricas.json")
JA_LIDOS = os.path.join(RAIZ, "content", ".leitura_d1_enviada")
APRENDIZADO = os.path.join(RAIZ, "content", "aprendizado.md")

# Cabeçalho do caderno de aprendizado (BURACO 2 do conserto de 31/07/2026).
# Igual, caractere por caractere, ao de diagnostico.py — os dois escrevem no
# mesmo arquivo e precisam reconhecer o cabeçalho um do outro pra não duplicar.
CABECALHO_APRENDIZADO = (
    "# Caderno de aprendizado — Hana\n\n"
    "O que a automação já mandou pro Ramón, com data — pra próxima conversa "
    "não remontar do zero. Gravado por `publisher/diagnostico.py` e "
    "`publisher/leitura_d1.py`, sempre DEPOIS da entrega confirmada (nunca "
    "durante `--simular`). Mais recente em cima.\n\n"
)


def _prepend_aprendizado(bloco):
    """Insere `bloco` logo após o cabeçalho fixo, mais recente em cima."""
    corpo_atual = ""
    if os.path.isfile(APRENDIZADO):
        conteudo = open(APRENDIZADO, encoding="utf-8").read()
        corpo_atual = (conteudo[len(CABECALHO_APRENDIZADO):]
                       if conteudo.startswith(CABECALHO_APRENDIZADO) else conteudo)
    with open(APRENDIZADO, "w", encoding="utf-8") as f:
        f.write(CABECALHO_APRENDIZADO + bloco + "\n---\n\n" + corpo_atual)


def _registrar_aprendizado(texto, agora, ids):
    """Grava a leitura do dia 1 no caderno — só chamada DEPOIS do Telegram confirmar."""
    try:
        bloco = "## %s — Leitura do dia 1 (%s)\n\n%s\n" % (
            agora.strftime("%Y-%m-%d %H:%M UTC"), ", ".join(ids), texto)
        _prepend_aprendizado(bloco)
        print("[leitura_d1][aprendizado] registrado em content/aprendizado.md.")
    except Exception as exc:  # noqa: BLE001 — nao pode derrubar uma entrega ja feita
        print("[leitura_d1][aprendizado][FALHA] nao consegui gravar: %s" % str(exc)[:160])

# Janela de tolerância: a coleta roda 1x/dia, então "1 dia de vida" na prática
# cai em qualquer coisa entre ~20h e ~48h. Fora disso não é mais dia 1.
MIN_HORAS, MAX_HORAS = 20, 48


def _coletas():
    if not os.path.isfile(METRICAS):
        return []
    return json.load(open(METRICAS, encoding="utf-8")).get("coletas", [])


def _ja_lidos():
    if not os.path.isfile(JA_LIDOS):
        return set()
    return {l.strip() for l in open(JA_LIDOS, encoding="utf-8") if l.strip()}


def _marcar(pid):
    with open(JA_LIDOS, "a", encoding="utf-8") as f:
        f.write(pid + "\n")


def _idade_horas(publicado_em, agora):
    try:
        pub = datetime.fromisoformat(publicado_em.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    return (agora - pub).total_seconds() / 3600


def _e_reel(dados):
    return dados.get("tipo") in ("VIDEO", "REELS")


def _referencias(coletas, e_reel, excluir):
    """
    Leituras de dia 1 já registradas de posts do MESMO tipo, para comparar.
    Percorre todas as coletas e guarda, por post, a medição mais próxima de 24h.
    """
    melhor = {}
    for c in coletas:
        try:
            quando = datetime.strptime(c["data"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except (ValueError, KeyError):
            continue
        hora = c.get("hora_utc")
        if hora:
            try:
                h, m = hora.split(":")
                quando = quando.replace(hour=int(h), minute=int(m))
            except ValueError:
                pass
        for pid, dados in (c.get("posts") or {}).items():
            if pid in excluir or _e_reel(dados) != e_reel:
                continue
            idade = _idade_horas(dados.get("publicado_em"), quando)
            if idade is None or not (MIN_HORAS <= idade <= MAX_HORAS):
                continue
            # fica com a leitura mais perto de 24h
            anterior = melhor.get(pid)
            if anterior is None or abs(idade - 24) < abs(anterior[0] - 24):
                melhor[pid] = (idade, dados.get("metricas", {}))
    return melhor


def montar(agora=None):
    """Devolve (texto, [ids]) ou (None, []) se não houver nada a reportar."""
    agora = agora or datetime.now(timezone.utc)
    coletas = _coletas()
    if not coletas:
        return None, []

    hoje = coletas[-1]
    lidos = _ja_lidos()
    novos = []
    for pid, dados in (hoje.get("posts") or {}).items():
        if pid in lidos:
            continue
        idade = _idade_horas(dados.get("publicado_em"), agora)
        if idade is not None and MIN_HORAS <= idade <= MAX_HORAS:
            novos.append((pid, dados, idade))
    if not novos:
        return None, []

    L = []
    for pid, dados, idade in sorted(novos):
        m = dados.get("metricas", {})
        reel = _e_reel(dados)
        rotulo = "REEL" if reel else "Foto"
        L.append("📈 LEITURA DO DIA 1 — %s (%s, %.0fh no ar)" % (pid, rotulo, idade))
        L.append("Alcance %s · visitas ao perfil %s · seguidores ganhos %s"
                 % (m.get("reach", "?"), m.get("profile_visits", "?"),
                    m.get("follows", "?")))
        L.append("Curtidas %s · comentários %s · salvos %s · compartilh. %s"
                 % (m.get("likes", "?"), m.get("comments", "?"),
                    m.get("saved", "?"), m.get("shares", "?")))

        refs = _referencias(coletas, reel, {pid})
        if refs:
            alcances = [v[1].get("reach") or 0 for v in refs.values()]
            media = sum(alcances) / len(alcances)
            L.append("Comparando só com %s da mesma idade (%d medido(s)): média %.0f."
                     % ("Reels" if reel else "fotos", len(alcances), media))
            atual = m.get("reach") or 0
            if media:
                L.append("Este está %+.0f%% em relação a essa média." % ((atual - media) / media * 100))
        else:
            L.append("⚠️ Ainda não há outro %s medido com 1 dia de vida — sem "
                     "base de comparação honesta." % ("Reel" if reel else "foto"))
        L.append("")

    L.append("Régua: alcance depois do dia 1 não gerou visita nova em nenhum "
             "post medido — por isso só este número decide.")
    return "\n".join(L).strip(), [p for p, _, _ in novos]


def main():
    simular = "--simular" in sys.argv
    texto, ids = montar()
    if not texto:
        print("[leitura_d1] nenhum post completando 1 dia — saindo calado.")
        return 0
    if simular:
        print(texto)
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        print("[leitura_d1][aviso] sem credencial do Telegram — nao entreguei.")
        return 0
    try:
        sys.path.insert(0, AQUI)
        from mandar_recado import mandar
        mandar(token, chat_id, texto)
    except Exception as exc:  # noqa: BLE001 — nunca derruba o job
        print(f"[leitura_d1][aviso] Telegram recusou ({str(exc)[:150]}) — tento amanha.")
        return 0

    # BURACO 2 do conserto de 31/07/2026: só grava em disco DEPOIS que o
    # Telegram confirmou o envio (nunca antes — um --simular ou uma falha de
    # entrega não pode sujar o caderno). Falha aqui nunca desfaz a entrega que
    # já aconteceu.
    _registrar_aprendizado(texto, datetime.now(timezone.utc), ids)

    # So marca DEPOIS de entregar: se marcasse antes e a entrega falhasse, a
    # leitura do dia 1 sumia e nao volta mais (a janela passa).
    for pid in ids:
        _marcar(pid)
    print("[leitura_d1][ok] %d leitura(s) de dia 1 entregues." % len(ids))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
