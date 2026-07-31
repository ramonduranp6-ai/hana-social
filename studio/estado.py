"""
Gera ESTADO-ATUAL.md — a foto viva do projeto, feita por código e não de memória.

Uso:
    python studio/estado.py            # regenera o arquivo
    python studio/estado.py --mostrar  # imprime na tela (para ler em sessão nova)

Lê a verdade das fontes reais: fila de posts, arquivo publicado, git, agendador
e acervo de fotos. A parte que código não sabe (decisões, o que o Ramón pediu)
fica em DECISOES.md e é anexada no fim. Custo zero, sem IA.
"""

import datetime as dt
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS = os.path.join(RAIZ, "Fotos da Hana")
ICLOUD = os.path.join(os.path.expanduser("~"), "iCloudPhotos", "Photos")
SAIDA = os.path.join(RAIZ, "ESTADO-ATUAL.md")


def sh(*args, cwd=RAIZ):
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
        return r.stdout.strip()
    except Exception:
        return ""


def posts(pasta):
    """Lê os post.json de content/<pasta>."""
    base = os.path.join(RAIZ, "content", pasta)
    out = []
    if not os.path.isdir(base):
        return out
    for nome in sorted(os.listdir(base)):
        pj = os.path.join(base, nome, "post.json")
        if os.path.isfile(pj):
            try:
                with open(pj, encoding="utf-8") as f:
                    d = json.load(f)
                out.append((nome, d))
            except Exception:
                pass
    return out


def contar(pasta, exts):
    if not os.path.isdir(pasta):
        return 0
    return sum(1 for f in os.listdir(pasta) if f.lower().endswith(exts))


def gerar():
    agora = dt.datetime.now()
    L = []
    add = L.append

    add("# ESTADO ATUAL — Hana Social")
    add("")
    add(f"Gerado automaticamente por `studio/estado.py` em "
        f"{agora.strftime('%d/%m/%Y %H:%M')}. **Não editar à mão** — para registrar")
    add("decisões, use `DECISOES.md`.")
    add("")

    # --- fila ---
    fila = posts("queue")
    add("## Fila (o que ainda vai ao ar)")
    if not fila:
        add("Vazia. **Sem post agendado — produzir lote novo.**")
    else:
        add("")
        add("| Quando (UTC) | Post | Tipo | Status |")
        add("|---|---|---|---|")
        for nome, d in fila:
            add(f"| {d.get('scheduled_for','?')} | {nome} | {d.get('type','?')} | "
                f"{d.get('status','?')} |")
    add("")

    # --- publicados ---
    pub = posts("posted")
    add(f"## Publicados: {len(pub)}")
    for nome, d in pub[-5:]:
        add(f"- {nome} — IG `{d.get('instagram_id','?')}`")
    add("")

    # --- automação ---
    add("## Automação")
    runs = sh("gh", "run", "list", "-R", "ramonduranp6-ai/hana-social", "--limit", "3",
              "--json", "createdAt,event,conclusion",
              "-q", '.[] | "\\(.createdAt) \\(.event) \\(.conclusion)"')
    add("Últimas execuções do publicador no GitHub:")
    add("```")
    add(runs or "(não consegui consultar — checar 'gh auth status')")
    add("```")
    tarefa = sh("powershell", "-NoProfile", "-Command",
                "(Get-ScheduledTaskInfo -TaskName 'Hana Sentinela').NextRunTime")
    add(f"- Vigia local (Agendador do Windows): próxima execução {tarefa or 'não encontrada'}")
    add(f"- Token renovável automático: "
        f"{'CONFIGURADO' if os.path.isfile(os.path.join(RAIZ, 'studio', '.token')) else 'FALTA criar studio/.token'}")
    add("")

    # --- pasta de aprovação (o canal que o Ramón enxerga) ---
    aprov = os.path.join(FOTOS, "05 - APROVAR (semana)")
    add("## Esperando o OK do Ramón")
    if os.path.isdir(aprov) and os.listdir(aprov):
        add(f"Mídias numeradas em `{aprov}` (ele abre no OneDrive do celular):")
        add("")
        for f in sorted(os.listdir(aprov)):
            add(f"- {f}")
        add("")
        add("Ele responde pelos números. Enquanto não responder, **não commitar**")
        add("mudança de status nem publicar.")
    else:
        add("Nada esperando aprovação (pasta vazia ou inexistente).")
    add("")

    # --- acervo ---
    add("## Acervo de fotos")
    add(f"- Brutas a processar: {contar(os.path.join(FOTOS, '01 - brutas (suba aqui)'), ('.jpg','.jpeg','.png','.heic','.mov','.mp4'))} arquivos")
    add(f"- Editadas prontas: {contar(os.path.join(FOTOS, '03 - editadas'), ('.jpg','.mp4'))}")
    add(f"- Artes recebidas do outro projeto: {contar(os.path.join(FOTOS, '04 - artes recebidas'), ('.png','.jpg'))}")
    add(f"- Fotos do iPhone sincronizadas (iCloud): {contar(ICLOUD, ('.jpg','.jpeg','.heic','.png','.mov','.mp4'))}")
    add("")

    # --- recado do robô do lote (domingo) ---
    aviso = os.path.join(RAIZ, "content", "aviso_lote.md")
    if os.path.isfile(aviso):
        with open(aviso, encoding="utf-8") as f:
            texto_aviso = f.read().strip()
        if texto_aviso:
            add("## 🤖 O que o robô do lote fez no domingo")
            add(texto_aviso)
            add("")

    # --- recados que ele mandou pelo Telegram ---
    # O bot nao conversa: ele guarda o texto e quem responde e o Claude, aqui.
    recados = os.path.join(RAIZ, "content", "recados.md")
    if os.path.isfile(recados):
        abertos = [l.rstrip() for l in open(recados, encoding="utf-8")
                   if l.startswith("- [ ]")]
        if abertos:
            add("## 📌 RECADOS DELE NO TELEGRAM — responder nesta conversa")
            for linha in abertos:
                add(linha)
            add("")
            add("Depois de responder, apague a linha de `content/recados.md`.")
            add("")

    # --- git ---
    add("## Últimas mudanças no projeto")
    add("```")
    add(sh("git", "log", "--oneline", "-8"))
    add("```")
    sujo = sh("git", "status", "--short")
    if sujo:
        add("Alterações não commitadas:")
        add("```")
        add(sujo)
        add("```")
    add("")

    # --- decisões (parte humana) ---
    dec = os.path.join(RAIZ, "DECISOES.md")
    add("## Decisões e contexto")
    if os.path.isfile(dec):
        with open(dec, encoding="utf-8") as f:
            add(f.read().strip())
    else:
        add("(DECISOES.md ainda não existe)")

    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return "\n".join(L)


if __name__ == "__main__":
    # o console do Windows usa cp1252 e engasga com seta/emoji
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    texto = gerar()
    if "--mostrar" in sys.argv:
        print(texto)
    else:
        print(f"[ok] {SAIDA} atualizado")
