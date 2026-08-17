# -*- coding: utf-8 -*-
"""
Veredito da semana passada — o bloco que abre a pauta da reunião.

Pedido do Ramón em 02/08/2026: *"Importante na semana que vem, na próxima
reunião, revisar como foi o andamento da estratégia dessa semana que passou.
Assim conseguimos decidir, e ir melhorando semana a semana a estratégia."*

O problema que isto resolve: a pauta automática sabia dizer QUANTO deu, mas não
sabia dizer SE A DECISÃO DA SEMANA PASSADA FUNCIONOU — ninguém guardava o que
tinha sido decidido, então toda reunião recomeçava do zero e a gente
racionalizava o resultado depois de vê-lo.

Como funciona, e por que assim:

1. Ao fim de cada reunião o Claude grava UM arquivo `estrategia/decisoes-<data>.json`
   com as decisões da semana. Cada decisão nasce com quatro coisas obrigatórias:
   o que se espera que mexa, qual número, a PRÉ-CONDIÇÃO checável por código, e a
   REGRA DE MORTE — escrita ANTES de saber o resultado. Essa ordem é o ponto todo:
   regra de morte escrita depois do resultado é desculpa, não regra.

2. Este módulo lê o arquivo mais recente, confere no mundo real (arquivo existe?
   post foi publicado? o número mexeu?) e devolve um veredito curto por decisão.
   Custo de token: ZERO. Quem julga é código; o Claude só escreve a nota uma vez.

3. Três vereditos possíveis, e o terceiro é o que faz o mecanismo sobreviver a
   semanas em que nada foi feito:
   - MEXEU / NÃO MEXEU: a pré-condição aconteceu, dá para julgar o resultado.
   - NÃO TESTADO: a pré-condição não aconteceu (ele não filmou, o post não foi
     ao ar). **Nunca vira "falhou"** — falhar e não ter sido tentado são coisas
     diferentes, e tratar uma como a outra mataria ideia boa por engano. O
     contador de semanas sem execução sobe e a decisão CONTINUA na pauta.

Uso:
    python publisher/veredito.py            # imprime o bloco
    python publisher/veredito.py --simular  # idem, sem gravar contador
"""

import glob
import json
import os
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ESTRATEGIA = os.path.join(RAIZ, "estrategia")
METRICAS = os.path.join(RAIZ, "content", "metricas.json")
FILA = os.path.join(RAIZ, "content", "queue")
PUBLICADOS = os.path.join(RAIZ, "content", "posted")
# O publicador grava "posted"; aceitar "published" também, para o dia em que
# alguém padronizar o nome e este arquivo não virar mentira silenciosa.
STATUS_NO_AR = ("posted", "published")
BRUTAS = os.path.join(RAIZ, "Fotos da Hana", "01 - brutas (suba aqui)")

VIDEO_EXT = (".mp4", ".mov", ".m4v")

# Clipe companheiro de Live Photo do iPhone: tem um .HEIC de mesmo nome ao lado
# e dura ~2s. Descoberto em 02/08/2026 — o acervo que todo mundo chamava de
# "12 vídeos" eram 3 vídeos e 9 destes. Não contam como material filmado.
FOTO_EXT = (".heic", ".jpg", ".jpeg", ".png")


def _ultimo_arquivo_de_decisoes():
    arquivos = sorted(glob.glob(os.path.join(ESTRATEGIA, "decisoes-*.json")))
    return arquivos[-1] if arquivos else None


def _carregar(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def _coletas():
    if not os.path.isfile(METRICAS):
        return []
    with open(METRICAS, encoding="utf-8") as f:
        return json.load(f).get("coletas", [])


def _e_live_photo(pasta, nome):
    base = os.path.splitext(nome)[0]
    for ext in FOTO_EXT:
        if os.path.isfile(os.path.join(pasta, base + ext)):
            return True
        if os.path.isfile(os.path.join(pasta, base + ext.upper())):
            return True
    return False


def _ja_vistos():
    """Arquivos que o projeto já conhece — o robô do lote marca aqui."""
    caminho = os.path.join(RAIZ, "content", ".videos_usados")
    if not os.path.isfile(caminho):
        return set()
    with open(caminho, encoding="utf-8") as f:
        return {l.strip() for l in f if l.strip()}


def _videos_novos_desde(desde):
    """Vídeo DE VERDADE que apareceu nas brutas depois da data da reunião."""
    if not os.path.isdir(BRUTAS):
        return []
    corte = datetime.strptime(desde, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    vistos = _ja_vistos()
    achados = []
    for nome in sorted(os.listdir(BRUTAS)):
        if not nome.lower().endswith(VIDEO_EXT):
            continue
        if _e_live_photo(BRUTAS, nome):
            continue
        # A data de modificação sozinha não basta: o OneDrive reescreve mtime
        # ao ressincronizar entre o celular e o PC, e um vídeo velho voltaria
        # a parecer filmagem nova. Arquivo que o projeto já conhece nunca conta
        # como cena nova, por mais recente que o carimbo esteja.
        if nome in vistos:
            continue
        caminho = os.path.join(BRUTAS, nome)
        try:
            m = datetime.fromtimestamp(os.path.getmtime(caminho), timezone.utc)
        except OSError:
            continue
        if m >= corte:
            achados.append(nome)
    return achados


def _post(post_id):
    """Acha o post na fila OU na pasta dos já publicados.

    Pegadinha que quase passou (achada ao testar em 02/08/2026): quando um post
    vai ao ar, o publicador MOVE a pasta de `content/queue` para `content/posted`
    e o status vira `"posted"`, não `"published"`. Procurar só na fila fazia toda
    decisão sobre post publicado ficar eternamente em "NÃO TESTADO" — o veredito
    nunca julgaria o Reel, calado.
    """
    for base in (FILA, PUBLICADOS):
        meta = os.path.join(base, post_id, "post.json")
        if os.path.isfile(meta):
            try:
                with open(meta, encoding="utf-8") as f:
                    return json.load(f)
            except (ValueError, OSError):
                return None
    return None


def _posts_no_ar():
    """Todo post que já foi publicado, com o `_id` preenchido.

    Varre as DUAS pastas pela mesma razão do `_post()` acima: o publicador move
    a pasta para `content/posted` quando o post vai ao ar, então olhar só a fila
    faria a contagem de Reels publicados dar sempre zero.
    """
    achados = []
    for base in (FILA, PUBLICADOS):
        if not os.path.isdir(base):
            continue
        for pid in sorted(os.listdir(base)):
            meta = os.path.join(base, pid, "post.json")
            if not os.path.isfile(meta):
                continue
            try:
                with open(meta, encoding="utf-8") as f:
                    p = json.load(f)
            except (ValueError, OSError):
                continue
            if p.get("status") in STATUS_NO_AR:
                p["_id"] = pid
                achados.append(p)
    return achados


def _metricas_do_post(post_id):
    coletas = _coletas()
    if not coletas:
        return None
    return (coletas[-1].get("posts", {}).get(post_id) or {}).get("metricas")


def _checar(decisao):
    """Devolve (veredito, explicacao). Veredito: MEXEU / NAO MEXEU / NAO TESTADO."""
    pre = decisao.get("precondicao") or {}
    tipo = pre.get("tipo")

    if tipo == "video_novo_em_brutas":
        achados = _videos_novos_desde(pre.get("desde", "1970-01-01"))
        if not achados:
            return "NAO TESTADO", "nenhum vídeo novo chegou nas brutas"
        return "MEXEU", "chegou vídeo novo: %s" % ", ".join(achados[:3])

    if tipo == "post_publicado":
        pid = pre.get("post_id", "")
        p = _post(pid)
        if not p or p.get("status") not in STATUS_NO_AR:
            return "NAO TESTADO", "o post %s ainda não foi ao ar" % pid
        m = _metricas_do_post(pid)
        # DEFEITO PEGO PELA AUDITORIA (02/08/2026): sem esta guarda, post recém
        # publicado — ou semana em que o metrics.py falhou — vinha com métricas
        # vazias, os zeros caíam no `else` e o veredito dizia "NÃO MEXEU". Ou
        # seja: declarava fracasso definitivo de algo que ninguém tinha medido
        # ainda, e a regra de morte disparava por engano. Post sem medição é
        # NÃO TESTADO, igual a post que não foi ao ar.
        if not m:
            return "NAO TESTADO", "publicado, mas a coleta ainda não trouxe os números dele"
        if not m.get("reach"):
            return "NAO TESTADO", "publicado, ainda sem alcance medido"
        shares = m.get("shares") or 0
        follows = m.get("follows") or 0
        saved = m.get("saved") or 0
        resumo = "alcance %s · %s salvos · %s compart. · %s seguidores" % (
            m.get("reach"), saved, shares, follows)
        if shares or follows or saved:
            return "MEXEU", resumo
        return "NAO MEXEU", resumo

    if tipo == "arquivo_existe":
        # ⚠️ Este tipo só sabe responder MEXEU ou NÃO TESTADO — existir não é
        # resultado, é entrega. Só use quando a própria existência for a métrica
        # (ex.: "o plano B está pronto e guardado"). Para medir se algo FUNCIONOU,
        # use `post_publicado`, senão o fracasso nunca aparece.
        caminho = os.path.join(RAIZ, pre.get("caminho", ""))
        if os.path.isfile(caminho):
            return "MEXEU", "pronto e guardado"
        return "NAO TESTADO", "ainda não existe"

    if tipo == "cancelado":
        # Decisão derrubada antes de virar resultado. Fica visível de propósito —
        # decisão que some da pauta é decisão que ninguém cobra depois.
        return "CANCELADO", "derrubada antes de ser testada"

    if tipo == "reels_publicados_minimo":
        # BURACO PEGO EM 17/08/2026: a reunião de 09/08 escreveu as decisões com
        # este tipo, mas ele nunca existiu aqui. Resultado: as 2 decisões que
        # sustentam a estratégia de crescimento caíam no "tipo desconhecido" e
        # ficavam NÃO TESTADO para sempre — o mecanismo de revisão semanal, que
        # foi construído justamente para responder "funcionou?", estava mudo.
        minimo = int(pre.get("quantidade") or 0)
        desde = pre.get("desde", "1970-01-01")
        reels = [p for p in _posts_no_ar()
                 if p.get("type") == "reel" and (p.get("scheduled_for") or "")[:10] >= desde]
        if len(reels) < minimo:
            return "NAO TESTADO", (
                "%d de %d Reels publicados desde %s — falta publicar para poder julgar"
                % (len(reels), minimo, desde))
        medidos = [(p["_id"], _metricas_do_post(p["_id"])) for p in reels]
        medidos = [(pid, m) for pid, m in medidos if m and m.get("reach")]
        if not medidos:
            return "NAO TESTADO", "%d Reels no ar, mas a coleta ainda não trouxe os números" % len(reels)
        alcance = sum(m["reach"] for _, m in medidos) / len(medidos)
        shares = sum((m.get("shares") or 0) for _, m in medidos)
        follows = sum((m.get("follows") or 0) for _, m in medidos)
        saved = sum((m.get("saved") or 0) for _, m in medidos)
        resumo = ("%d Reels medidos · alcance médio %d · %d salvos · %d compart. · %d seguidores"
                  % (len(medidos), alcance, saved, shares, follows))
        if shares or follows or saved:
            return "MEXEU", resumo
        return "NAO MEXEU", resumo

    if tipo == "ok_do_ramon":
        # Só ele destrava. Enquanto não destravar, a pendência aparece escrita
        # na pauta em vez de virar "falhou" — decisão parada por falta de
        # resposta dele não é decisão testada e reprovada.
        if not decisao.get("ok_em"):
            pendente = "; ".join(pre.get("pendente") or []) or "sem detalhe"
            return "NAO TESTADO", "esperando a palavra dele sobre: %s" % pendente
        return "NAO TESTADO", (
            "ele liberou em %s — falta a execução gerar número para julgar"
            % decisao["ok_em"])

    return "NAO TESTADO", "pré-condição de tipo desconhecido (%s)" % tipo


ICONE = {"MEXEU": "✅", "NAO MEXEU": "❌", "NAO TESTADO": "⏸️", "CANCELADO": "🚫"}


def _semana_iso(dt):
    ano, semana, _ = dt.isocalendar()
    return "%d-W%02d" % (ano, semana)


def montar(gravar=False, agora=None):
    """Devolve o bloco de texto do veredito, ou '' se não houver decisão gravada."""
    agora = agora or datetime.now(timezone.utc)
    semana_atual = _semana_iso(agora)
    caminho = _ultimo_arquivo_de_decisoes()
    if not caminho:
        return ""
    try:
        dados = _carregar(caminho)
    except (ValueError, OSError) as exc:
        return "⚠️ Não consegui ler as decisões da semana passada (%s)." % str(exc)[:80]

    decisoes = dados.get("decisoes") or []
    if not decisoes:
        return ""

    L = ["🔁 A SEMANA PASSADA FUNCIONOU?",
         "Decidido em %s. Cada linha é uma decisão daquele dia." % dados.get("data_reuniao", "?")]

    mudou = False
    for d in decisoes:
        veredito, porque = _checar(d)
        if veredito == "NAO TESTADO":
            # DEFEITO PEGO PELA AUDITORIA (02/08/2026): o contador subia a cada
            # EXECUÇÃO, não a cada semana. Como o publish.yml bate de 30 em 30
            # minutos e um envio que falha no Telegram não marca a semana, duas
            # tentativas seguidas faziam o contador ir a 2 e a pauta anunciar
            # "2ª semana seguida sem sair do papel" em minutos. Agora a semana
            # ISO em que ele subiu fica gravada, e ele só sobe uma vez por semana.
            if d.get("ultima_semana_contada") != semana_atual:
                d["contador_nao_testado"] = int(d.get("contador_nao_testado", 0)) + 1
                d["ultima_semana_contada"] = semana_atual
                mudou = True
            extra = ""
            if d["contador_nao_testado"] >= 2:
                extra = " — %da semana seguida sem sair do papel" % d["contador_nao_testado"]
            L.append("%s %s: NÃO TESTADO (%s)%s" % (
                ICONE[veredito], d.get("titulo", d.get("id", "?")), porque, extra))
            L.append("   Continua na pauta. Regra combinada: %s" % d.get("regra_de_morte", "—"))
        elif veredito == "CANCELADO":
            L.append("%s %s: CANCELADO (%s)" % (
                ICONE[veredito], d.get("titulo", d.get("id", "?")), d.get("nota", porque)))
        elif veredito == "NAO MEXEU":
            L.append("%s %s: NÃO MEXEU (%s)" % (
                ICONE[veredito], d.get("titulo", d.get("id", "?")), porque))
            L.append("   👉 O que combinamos fazer agora: %s" % d.get("regra_de_morte", "—"))
        else:
            L.append("%s %s: MEXEU (%s)" % (
                ICONE[veredito], d.get("titulo", d.get("id", "?")), porque))

    # Os contadores só valem se ficarem gravados — senão toda semana recomeça do
    # zero e "2ª semana seguida sem filmar" nunca aparece, que é justamente o
    # sinal que o Ramón precisa ver.
    if gravar and mudou:
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
        except OSError as exc:  # noqa: BLE001 — nunca derrubar a pauta por isto
            L.append("(aviso: não consegui gravar o contador — %s)" % str(exc)[:60])

    return "\n".join(L)


def main():
    print(montar(gravar="--simular" not in sys.argv))


if __name__ == "__main__":
    main()
