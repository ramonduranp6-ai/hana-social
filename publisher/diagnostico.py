# -*- coding: utf-8 -*-
"""
Robô de diagnóstico semanal — mede a EVOLUÇÃO, não só o número do dia.

Pedido do Ramón em 31/07/2026: *"Sinto que faltou um robo de inteligencia para
analisar os resultados da semana, medir a evolução"*. Ele estava certo: o
`reporte_semanal.py` listava número e não dizia se o projeto está melhorando ou
piorando — quem tinha que perceber isso era o Claude, olhando a tabela.

O que este arquivo faz é a parte que NÃO precisa de IA: comparar a semana com a
anterior e aplicar regras fixas de leitura. **Custo zero de token.** A parte de
julgamento (o que fazer com o diagnóstico) continua com o comitê, na conversa.

Divisão que vale a pena lembrar: aqui só entra conta que dá para conferir na
mão. Se um dia alguém quiser colocar IA nesta função, o lugar é DEPOIS, lendo o
texto que sai daqui — nunca no lugar da conta.
"""

import io
import json
import os
import sys
from datetime import datetime, timedelta, timezone

# O console do Windows quebra com emoji. Usar `reconfigure` e NAO
# io.TextIOWrapper: o wrapper cria um objeto novo em cima do mesmo buffer, e
# quando dois modulos fazem isso (aqui e no reporte_semanal, que importa este)
# o segundo derruba o primeiro — "I/O operation on closed file". Aconteceu de
# verdade em 31/07/2026, na primeira execucao. `reconfigure` altera o objeto
# existente, entao pode ser chamado quantas vezes for.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
METRICAS = os.path.join(RAIZ, "content", "metricas.json")
APRENDIZADO = os.path.join(RAIZ, "content", "aprendizado.md")
ESTADO_REPORTE = os.path.join(RAIZ, "content", ".reporte_semanal")
MARCADOR_APRENDIZADO = os.path.join(RAIZ, "content", ".aprendizado_diagnostico_semana")

# Os três sinais que decidem se o conteúdo presta. Curtida não entra: no placar
# medido, curtida é de amigo e não mexe em alcance.
SINAIS = ("saved", "shares", "follows")

# BURACO (a) do conserto de 31/07/2026 (prioridade máxima do conselho): se o
# passo "Coletar métricas" do workflow morrer (ele tem continue-on-error de
# propósito, pra não derrubar a publicação), a última coleta para de andar.
# Sem este limite, "hoje" e "7 dias atrás" viram o MESMO registro e o robô
# imprime "estável"/"ZERO" pra sempre — a auditoria testou com data falsa e
# ele mandou mudar a estratégia em cima de um número que nunca se moveu.
LIMITE_HORAS_SENSOR = 36

# Cabeçalho do caderno de aprendizado (BURACO 2). Igual, caractere por
# caractere, ao de leitura_d1.py — os dois escrevem no mesmo arquivo e
# precisam reconhecer o cabeçalho um do outro para não duplicá-lo.
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


def _coletas():
    if not os.path.isfile(METRICAS):
        return []
    return json.load(open(METRICAS, encoding="utf-8")).get("coletas", [])


def _coleta_em_ou_antes(coletas, limite):
    """A coleta mais recente que não passa de `limite` (string AAAA-MM-DD)."""
    anteriores = [c for c in coletas if c["data"] <= limite]
    return anteriores[-1] if anteriores else None


def _idade_horas_coleta(coleta, agora):
    """
    Quantas horas se passaram desde que essa coleta foi feita. None se a data
    vier num formato que não dá pra entender (nunca inventa idade).
    Usa `hora_utc` quando existe (campo novo desde 31/07/2026); coleta antiga
    sem essa hora é tratada como tendo sido feita à meia-noite UTC — o que só
    torna a checagem MAIS cautelosa (idade um pouco maior do que a real),
    nunca menos.
    """
    try:
        quando = datetime.strptime(coleta["data"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (ValueError, KeyError, TypeError):
        return None
    hora = coleta.get("hora_utc")
    if hora:
        try:
            h, m = hora.split(":")
            quando = quando.replace(hour=int(h), minute=int(m))
        except (ValueError, AttributeError):
            pass
    return (agora - quando).total_seconds() / 3600


def _soma(coleta, campo):
    return sum((p.get("metricas", {}).get(campo) or 0)
               for p in (coleta.get("posts") or {}).values())


def _media_alcance(coleta, so_tipo=None):
    posts = list((coleta.get("posts") or {}).values())
    if so_tipo == "reel":
        posts = [p for p in posts if p.get("tipo") in ("VIDEO", "REELS")]
    elif so_tipo == "foto":
        posts = [p for p in posts if p.get("tipo") not in ("VIDEO", "REELS")]
    if not posts:
        return None
    return sum((p.get("metricas", {}).get("reach") or 0) for p in posts) / len(posts)


def _seta(hoje, antes):
    """Setinha de tendência. Devolve string curta — o Ramón lê no celular."""
    if antes is None or hoje is None:
        return "—"
    if antes == 0:
        return "novo" if hoje else "0"
    var = (hoje - antes) / antes * 100
    if var >= 10:
        return "↑ %+.0f%%" % var
    if var <= -10:
        return "↓ %+.0f%%" % var
    return "→ estável"


def montar(agora=None):
    """
    Devolve o texto do diagnóstico, ou None se ainda não há histórico suficiente.

    Honestidade obrigatória: com poucos dias de coleta, comparar semana com
    semana é chute. Enquanto não houver uma coleta de 7 dias atrás, o robô diz
    isso em vez de inventar tendência — foi a regra zero deste projeto que se
    quebrou cinco vezes por afirmar sem base.
    """
    agora = agora or datetime.now(timezone.utc)
    coletas = _coletas()
    if not coletas:
        return None

    hoje = coletas[-1]
    limite = (agora - timedelta(days=7)).strftime("%Y-%m-%d")
    antes = _coleta_em_ou_antes(coletas, limite)

    # BURACO (a) — RECUSAR VEREDITO se o sensor parece morto. Duas provas,
    # qualquer uma basta: (1) a última coleta é velha demais (o coletor parou
    # de rodar, mesmo com histórico bonito guardado); (2) "hoje" e "7 dias
    # atrás" caíram no MESMO registro (sem coleta nova há mais de uma semana,
    # o `_coleta_em_ou_antes` de baixo acaba devolvendo a própria coleta de
    # hoje como base de comparação — dá "estável"/"zero" sempre, mesmo que
    # nada tenha sido medido). Nunca inventar tendência em cima de silêncio.
    idade_sensor = _idade_horas_coleta(hoje, agora)
    parado_demais = idade_sensor is not None and idade_sensor > LIMITE_HORAS_SENSOR
    mesmo_registro = antes is not None and antes.get("data") == hoje.get("data")
    if parado_demais or mesmo_registro:
        motivos = []
        if parado_demais:
            motivos.append("a última coleta tem %.0fh de idade (limite: %dh)"
                            % (idade_sensor, LIMITE_HORAS_SENSOR))
        if mesmo_registro:
            motivos.append("'hoje' e '7 dias atrás' caem no mesmo registro (%s)"
                            % hoje.get("data"))
        return "\n".join([
            "📊 DIAGNÓSTICO DA SEMANA",
            "🔴 SENSOR DE MÉTRICAS PARADO — SEM VEREDITO.",
            "",
            "Motivo: " + "; ".join(motivos) + ".",
            "",
            "Comparar 'hoje' com '7 dias atrás' desse jeito compara o número "
            "com ele mesmo — sempre dá 'estável' ou 'zero', mesmo que nada "
            "tenha sido medido de verdade. NÃO é a estratégia que travou, é o "
            "sensor. Conserte a coleta (o passo \"Coletar métricas\" do "
            "workflow, publisher/metrics.py) antes de confiar em qualquer "
            "veredito daqui — inclusive o de mudar a abordagem de conteúdo.",
        ])

    L = ["📊 DIAGNÓSTICO DA SEMANA", "Fonte: API do Instagram, coleta de %s." % hoje["data"]]

    if antes is None:
        dias = (datetime.strptime(hoje["data"], "%Y-%m-%d")
                - datetime.strptime(coletas[0]["data"], "%Y-%m-%d")).days
        L += ["",
              "⚠️ Ainda não dá para comparar semana com semana: o histórico tem "
              "só %d dia(s) de medição. O primeiro diagnóstico de verdade sai "
              "quando fechar 7 dias." % (dias + 1),
              "",
              "Foto de hoje: %d seguidores, alcance médio %s."
              % (hoje.get("seguidores", 0),
                 ("%.0f" % _media_alcance(hoje)) if _media_alcance(hoje) else "—")]
        return "\n".join(L)

    seg_h, seg_a = hoje.get("seguidores", 0), antes.get("seguidores", 0)
    alc_h, alc_a = _media_alcance(hoje), _media_alcance(antes)

    L += ["", "1) SEGUIDORES: %d (%+d em 7 dias) %s"
          % (seg_h, seg_h - seg_a, _seta(seg_h, seg_a)),
          "2) ALCANCE MÉDIO: %s %s"
          % (("%.0f" % alc_h) if alc_h else "—", _seta(alc_h, alc_a))]

    # Os três sinais, que são o que decide se o conteúdo presta.
    L.append("3) OS TRÊS SINAIS (semana vs. semana anterior)")
    total_hoje = 0
    for campo, nome in (("saved", "Salvos"), ("shares", "Compartilh."),
                        ("follows", "Seguidores ganhos")):
        h, a = _soma(hoje, campo), _soma(antes, campo)
        total_hoje += h
        L.append("   %s: %d (era %d) %s" % (nome, h, a, _seta(h, a)))

    # Reel x Foto — a comparação que decide o formato.
    L.append("4) REEL x FOTO (alcance médio)")
    for rotulo, chave in (("Reel", "reel"), ("Foto", "foto")):
        m = _media_alcance(hoje, chave)
        L.append("   %s: %s" % (rotulo, ("%.0f" % m) if m else "ainda sem post publicado"))

    # VEREDITO por regra fixa. Nada de IA aqui: são cortes que dá para conferir
    # na mão, e por isso o robô pode afirmar sem risco de alucinar.
    L.append("")
    L.append("5) VEREDITO")
    if total_hoje == 0:
        semanas = _semanas_zeradas(coletas, agora)
        L.append("   ⚠️ Salvos, compartilhamentos e seguidores ganhos seguem em "
                 "ZERO há %d semana(s). Quem vê não reage — isso é conteúdo, "
                 "não entrega." % semanas)
        if semanas >= 3:
            L.append("   🔴 Três semanas de zero é o corte combinado: a abordagem "
                     "de conteúdo muda, não a frequência.")
    elif seg_h <= seg_a:
        L.append("   ⚠️ Já há reação nos posts, mas a base não cresceu. O conteúdo "
                 "prende quem já segue e não converte quem chega.")
    else:
        L.append("   ✅ Base cresceu E houve reação. É o único cenário em que "
                 "vale repetir a fórmula da semana.")

    m_reel, m_foto = _media_alcance(hoje, "reel"), _media_alcance(hoje, "foto")
    if m_reel and m_foto:
        vezes = m_reel / m_foto if m_foto else 0
        L.append("   Reel está entregando %.1fx o alcance da foto." % vezes)

    L.append("")
    L.append("O comitê lê isto na conversa de segunda e traz o plano.")
    return "\n".join(L)


def _semanas_zeradas(coletas, agora):
    """Há quantas semanas os três sinais estão em zero. Conta simples e conferível."""
    semanas = 0
    for k in range(0, 12):
        limite = (agora - timedelta(days=7 * k)).strftime("%Y-%m-%d")
        c = _coleta_em_ou_antes(coletas, limite)
        if c is None:
            break
        if sum(_soma(c, campo) for campo in SINAIS) > 0:
            break
        semanas += 1
    return max(semanas, 1)


def _semana(d):
    ano, semana, _ = d.isocalendar()
    return "%d-W%02d" % (ano, semana)


def _pauta_ja_foi_enviada(semana):
    """
    reporte_semanal.py grava sua PRÓPRIA marca (`content/.reporte_semanal`)
    só DEPOIS de mandar a pauta no Telegram — nunca antes, nunca em
    `--simular`. Este arquivo só LÊ essa marca (não escreve, não importa o
    módulo) para saber se pode confiar que a entrega aconteceu de verdade,
    sem precisar mexer em reporte_semanal.py (fora do escopo deste conserto).
    """
    if not os.path.isfile(ESTADO_REPORTE):
        return False
    try:
        return open(ESTADO_REPORTE, encoding="utf-8").read().strip() == semana
    except OSError:
        return False


def _ja_registrado(semana):
    if not os.path.isfile(MARCADOR_APRENDIZADO):
        return False
    return open(MARCADOR_APRENDIZADO, encoding="utf-8").read().strip() == semana


def _marcar_registrado(semana):
    with open(MARCADOR_APRENDIZADO, "w", encoding="utf-8") as f:
        f.write(semana)


def registrar_se_enviado(agora=None):
    """
    BURACO 2 do conserto de 31/07/2026: o veredito da reunião de segunda ia
    pro Telegram e evaporava — a conversa da semana seguinte remontava tudo
    do zero. Grava em content/aprendizado.md, mas só DEPOIS que
    reporte_semanal.py já provou (pelo próprio marcador dele) que a pauta
    desta semana foi enviada — nunca antes, senão um teste em `--simular`
    também sujaria o caderno. Roda como passo separado no workflow, DEPOIS de
    "Pauta da reunião de segunda". Nunca derruba o job.
    """
    agora = agora or datetime.now(timezone.utc)
    semana = _semana(agora)
    if not _pauta_ja_foi_enviada(semana):
        print("[diagnostico][aprendizado] pauta desta semana ainda nao foi "
              "confirmada como enviada - nao registro.")
        return
    if _ja_registrado(semana):
        print("[diagnostico][aprendizado] semana %s ja registrada." % semana)
        return
    texto = montar(agora)
    if not texto:
        print("[diagnostico][aprendizado] sem diagnostico para registrar.")
        return
    try:
        bloco = "## %s — Diagnóstico da semana %s\n\n%s\n" % (
            agora.strftime("%Y-%m-%d"), semana, texto)
        _prepend_aprendizado(bloco)
        _marcar_registrado(semana)
        print("[diagnostico][aprendizado] semana %s registrada em "
              "content/aprendizado.md." % semana)
    except Exception as exc:  # noqa: BLE001 — aviso nunca derruba o job
        print("[diagnostico][aprendizado][FALHA] nao consegui gravar: %s"
              % str(exc)[:160])


def main():
    if "--registrar-se-enviado" in sys.argv:
        registrar_se_enviado()
        return
    texto = montar()
    print(texto if texto else "[diagnostico] ainda nao ha metrica coletada.")


if __name__ == "__main__":
    main()
