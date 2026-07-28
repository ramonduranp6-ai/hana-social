"""
Coletor de métricas — o placar do projeto.

Responde, com número em vez de chute: o que cada post rendeu, e se Reel rende
mais que foto. Roda junto com o publicador (mesmo robô, regra do Ramón: um só).

O que faz:
  1. Pergunta à API quantos seguidores a conta tem hoje.
  2. Para cada post já publicado (content/posted/*/post.json com instagram_id),
     pede alcance, curtidas, comentários, salvamentos e afins.
  3. Guarda a série histórica em content/metricas.json (uma coleta por dia).
  4. Reescreve content/placar.md, que é a versão legível para o Ramón.

Regra 2 do projeto (falhar visível): métrica que a API recusar entra em
"faltando" no relatório, com o motivo. Nada é omitido para o placar ficar bonito.

Config (mesmas variáveis do publicador):
  IG_USER_ID, IG_ACCESS_TOKEN, GRAPH_BASE
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ig_api

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTED_DIR = os.path.join(ROOT, "content", "posted")
SERIE_PATH = os.path.join(ROOT, "content", "metricas.json")
PLACAR_PATH = os.path.join(ROOT, "content", "placar.md")

# Métricas pedidas por tipo de mídia. A API rejeita o lote inteiro se uma delas
# não existir para aquele tipo, então em caso de erro tentamos uma a uma.
METRICAS = {
    "REELS": ["reach", "likes", "comments", "saved", "shares", "views"],
    "VIDEO": ["reach", "likes", "comments", "saved", "shares", "views"],
    "IMAGE": ["reach", "likes", "comments", "saved", "shares", "profile_visits", "follows"],
    "CAROUSEL_ALBUM": ["reach", "likes", "comments", "saved", "shares"],
}
PADRAO = ["reach", "likes", "comments", "saved"]

ROTULOS = {
    "reach": "alcance",
    "likes": "curtidas",
    "comments": "comentários",
    "saved": "salvos",
    "shares": "compartilh.",
    "views": "views",
    "profile_visits": "visitas ao perfil",
    "follows": "seguidores ganhos",
}


def hoje():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def posts_publicados():
    """Lê content/posted/, devolve os posts que têm id do Instagram."""
    saida = []
    if not os.path.isdir(POSTED_DIR):
        return saida
    for nome in sorted(os.listdir(POSTED_DIR)):
        meta = os.path.join(POSTED_DIR, nome, "post.json")
        if not os.path.isfile(meta):
            continue
        with open(meta, encoding="utf-8") as f:
            dados = json.load(f)
        if dados.get("instagram_id"):
            dados["_id"] = nome
            saida.append(dados)
    return saida


def seguidores(ig_user, token):
    dados = ig_api._get(ig_user, {"fields": "followers_count,media_count", "access_token": token})
    return dados.get("followers_count"), dados.get("media_count")


def tipo_da_midia(media_id, token):
    """media_type real segundo a API (REELS/IMAGE/...). None se a API recusar."""
    try:
        dados = ig_api._get(media_id, {"fields": "media_type,media_product_type", "access_token": token})
    except Exception:  # noqa: BLE001
        return None
    if dados.get("media_product_type") == "REELS":
        return "REELS"
    return dados.get("media_type")


def insights(media_id, tipo, token):
    """
    Devolve (valores, faltando). Tenta o lote; se a API recusar, vai uma a uma
    para não perder as métricas que existem por causa de uma que não existe.
    """
    pedidas = METRICAS.get(tipo or "", PADRAO)
    try:
        dados = ig_api._get(
            f"{media_id}/insights",
            {"metric": ",".join(pedidas), "access_token": token},
        )
        return {m["name"]: m["values"][0]["value"] for m in dados.get("data", [])}, {}
    except Exception:  # noqa: BLE001
        pass

    valores, faltando = {}, {}
    for metrica in pedidas:
        try:
            dados = ig_api._get(
                f"{media_id}/insights", {"metric": metrica, "access_token": token}
            )
            for m in dados.get("data", []):
                valores[m["name"]] = m["values"][0]["value"]
        except Exception as exc:  # noqa: BLE001
            faltando[metrica] = str(exc)[:120]
    return valores, faltando


def carregar_serie():
    if os.path.isfile(SERIE_PATH):
        with open(SERIE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"coletas": []}


def salvar_serie(serie):
    with open(SERIE_PATH, "w", encoding="utf-8") as f:
        json.dump(serie, f, ensure_ascii=False, indent=2)


def coletar(ig_user, token):
    """Uma coleta completa. Devolve o registro do dia."""
    seg, midias = seguidores(ig_user, token)
    registro = {
        "data": hoje(),
        "seguidores": seg,
        "midias_no_perfil": midias,
        "posts": {},
        "faltando": {},
    }
    for post in posts_publicados():
        mid = post["instagram_id"]
        tipo = tipo_da_midia(mid, token) or post.get("type", "").upper()
        valores, faltando = insights(mid, tipo, token)
        registro["posts"][post["_id"]] = {
            "instagram_id": mid,
            "tipo": tipo,
            "publicado_em": post.get("scheduled_for"),
            "metricas": valores,
        }
        if faltando:
            registro["faltando"][post["_id"]] = faltando
    return registro


def _num(valor):
    return valor if isinstance(valor, (int, float)) else 0


def montar_placar(serie):
    """Gera o markdown legível a partir da série completa."""
    coletas = serie.get("coletas", [])
    if not coletas:
        return "# Placar da Hana\n\nAinda não houve coleta.\n"

    atual = coletas[-1]
    anterior = coletas[-2] if len(coletas) > 1 else None

    linhas = [
        "# Placar da Hana — o que cada post rendeu",
        "",
        "Gerado por `publisher/metrics.py` a cada coleta. **Não editar à mão.**",
        f"Última coleta: **{atual['data']}** · fonte: API do Instagram.",
        "",
        "## Seguidores",
        "",
    ]

    seg = atual.get("seguidores")
    if anterior and isinstance(seg, int) and isinstance(anterior.get("seguidores"), int):
        delta = seg - anterior["seguidores"]
        sinal = "+" if delta >= 0 else ""
        linhas.append(f"**{seg}** ({sinal}{delta} desde {anterior['data']})")
    else:
        linhas.append(f"**{seg}**")
    linhas.append("")

    posts = atual.get("posts", {})
    if posts:
        colunas = ["reach", "likes", "comments", "saved", "shares", "views", "follows"]
        usadas = [c for c in colunas if any(c in p["metricas"] for p in posts.values())]
        linhas += [
            "## Post a post (mais alcance em cima)",
            "",
            "| Post | Tipo | " + " | ".join(ROTULOS.get(c, c) for c in usadas) + " |",
            "|---|---|" + "---|" * len(usadas),
        ]
        ordenados = sorted(
            posts.items(), key=lambda kv: _num(kv[1]["metricas"].get("reach")), reverse=True
        )
        for pid, dados in ordenados:
            tipo = "Reel" if dados.get("tipo") == "REELS" else "Foto"
            celulas = [str(dados["metricas"].get(c, "—")) for c in usadas]
            linhas.append(f"| {pid} | {tipo} | " + " | ".join(celulas) + " |")
        linhas.append("")

        # Reel x foto: a pergunta que o Ramón faz toda semana.
        reels = [p for p in posts.values() if p.get("tipo") == "REELS"]
        fotos = [p for p in posts.values() if p.get("tipo") != "REELS"]
        linhas += ["## Reel x Foto (média de alcance)", ""]
        for nome, grupo in (("Reel", reels), ("Foto", fotos)):
            if grupo:
                media = sum(_num(p["metricas"].get("reach")) for p in grupo) / len(grupo)
                linhas.append(f"- **{nome}**: {media:.0f} de alcance médio ({len(grupo)} post(s))")
            else:
                linhas.append(f"- **{nome}**: ainda sem post publicado")
        linhas.append("")

    if len(coletas) > 1:
        linhas += ["## Seguidores ao longo do tempo", "", "| Data | Seguidores |", "|---|---|"]
        for c in coletas[-12:]:
            linhas.append(f"| {c['data']} | {c.get('seguidores', '—')} |")
        linhas.append("")

    faltando = atual.get("faltando") or {}
    linhas += ["## Limites desta coleta", ""]
    if faltando:
        linhas.append("Métricas que a API **recusou** (o placar está incompleto nestes pontos):")
        linhas.append("")
        for pid, metricas in faltando.items():
            for metrica, motivo in metricas.items():
                linhas.append(f"- `{pid}` · **{metrica}**: {motivo}")
    else:
        linhas.append("Nenhuma. Todas as métricas pedidas vieram.")
    linhas.append("")
    linhas.append(
        "Lembrete honesto: o Instagram só dá insights de posts publicados **pela conta**, "
        "e alguns números só existem depois de algumas horas no ar."
    )
    linhas.append("")
    return "\n".join(linhas)


def main():
    ig_user = os.environ.get("IG_USER_ID")
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not ig_user or not token:
        print("[ERRO] IG_USER_ID e IG_ACCESS_TOKEN são obrigatórios.")
        sys.exit(1)

    serie = carregar_serie()
    forcar = "--forcar" in sys.argv
    if not forcar and any(c.get("data") == hoje() for c in serie["coletas"]):
        print(f"[metricas] já coletado hoje ({hoje()}); nada a fazer.")
        return

    try:
        registro = coletar(ig_user, token)
    except Exception as exc:  # noqa: BLE001
        # Falhar visível, mas sem derrubar o publicador (regra 2).
        print(f"[metricas][FALHA] não consegui coletar: {exc}")
        sys.exit(0)

    serie["coletas"] = [c for c in serie["coletas"] if c.get("data") != registro["data"]]
    serie["coletas"].append(registro)
    serie["coletas"].sort(key=lambda c: c["data"])
    salvar_serie(serie)

    with open(PLACAR_PATH, "w", encoding="utf-8") as f:
        f.write(montar_placar(serie))

    print(
        f"[metricas] coleta de {registro['data']}: {registro.get('seguidores')} seguidores, "
        f"{len(registro['posts'])} post(s) medido(s)."
    )
    if registro.get("faltando"):
        print(f"[metricas][AVISO] métricas recusadas pela API: {registro['faltando']}")


if __name__ == "__main__":
    main()
