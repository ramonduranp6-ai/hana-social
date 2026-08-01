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

# Os três sinais que decidem se o conteúdo presta. Curtida não entra: no placar
# medido, curtida é de amigo e não mexe em alcance.
SINAIS = ("saved", "shares", "follows")


def _coletas():
    if not os.path.isfile(METRICAS):
        return []
    return json.load(open(METRICAS, encoding="utf-8")).get("coletas", [])


def _coleta_em_ou_antes(coletas, limite):
    """A coleta mais recente que não passa de `limite` (string AAAA-MM-DD)."""
    anteriores = [c for c in coletas if c["data"] <= limite]
    return anteriores[-1] if anteriores else None


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


if __name__ == "__main__":
    texto = montar()
    print(texto if texto else "[diagnostico] ainda nao ha metrica coletada.")
