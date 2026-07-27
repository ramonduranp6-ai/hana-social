"""
Painel de aprovação — mostra a fila com FOTO + legenda numa página local.

Canal que funciona para o Ramón ver no PC: arquivo local aberto no navegador.
Link de internet e anexo na conversa já falharam (ver DECISOES.md), por isso
as imagens vão embutidas no próprio arquivo (base64) — nada depende de rede.
O vídeo do Reel fica por referência ao arquivo local (pesado demais para embutir).

Uso:
    python studio/painel_aprovacao.py           # gera e abre no navegador
    python studio/painel_aprovacao.py --so-gerar
"""

import base64
import datetime as dt
import json
import mimetypes
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FILA = os.path.join(RAIZ, "content", "queue")
SAIDA = os.path.join(AQUI, "aprovar.html")

# Sempre o Chrome do perfil da Hana (hanaduransanches@gmail.com), NUNCA o padrão
# do Windows — o padrão é o perfil da marca Canecas. Regra dada pelo Ramón em
# 27/07/2026 depois de o painel abrir na janela errada.
PERFIL_HANA = "Profile 2"

ROTULO = {
    "pending": ("aguardando você", "#b45309", "#fef3c7"),
    "approved": ("aprovado", "#15803d", "#dcfce7"),
    "rejected": ("recusado", "#b91c1c", "#fee2e2"),
}


def embutir(caminho):
    """Devolve a imagem como data: URI, para a página não depender de nada."""
    tipo = mimetypes.guess_type(caminho)[0] or "image/jpeg"
    with open(caminho, "rb") as f:
        return f"data:{tipo};base64," + base64.b64encode(f.read()).decode()


def quando_br(iso):
    d = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    local = d - dt.timedelta(hours=3)  # UTC -> horário de Itajaí
    dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    return f"{dias[local.weekday()]} {local.strftime('%d/%m')} às {local.strftime('%Hh')}"


def cartao(n, pasta, dados):
    rotulo, cor, fundo = ROTULO.get(dados.get("status", "pending"), ROTULO["pending"])
    img = os.path.join(FILA, pasta, "image.jpg")
    vid = os.path.join(FILA, pasta, "video.mp4")

    if os.path.isfile(img):
        midia = f'<img src="{embutir(img)}" alt="post {n}">'
    elif os.path.isfile(vid):
        src = "file:///" + vid.replace("\\", "/")
        midia = f'<video src="{src}" controls preload="metadata"></video>'
    else:
        midia = '<div class="semmidia">mídia não encontrada</div>'

    legenda, _, tags = dados["caption"].partition("\n\n")
    return f"""
    <article class="card">
      <div class="media">{midia}<span class="num">{n}</span></div>
      <div class="txt">
        <div class="meta">
          <span class="quando">{quando_br(dados['scheduled_for'])}</span>
          <span class="tag" style="color:{cor};background:{fundo}">{rotulo}</span>
        </div>
        <p class="legenda">{legenda}</p>
        <p class="tags">{tags}</p>
      </div>
    </article>"""


def main():
    pastas = sorted(p for p in os.listdir(FILA) if os.path.isdir(os.path.join(FILA, p)))
    cartoes = []
    for i, pasta in enumerate(pastas, 1):
        with open(os.path.join(FILA, pasta, "post.json"), encoding="utf-8") as f:
            cartoes.append(cartao(i, pasta, json.load(f)))

    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Hana — fila para aprovar</title>
<style>
  :root {{ color-scheme: light dark; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding:48px 24px; font:16px/1.6 -apple-system,"Segoe UI",system-ui,sans-serif;
         background:#faf9f7; color:#1c1917; }}
  header {{ max-width:960px; margin:0 auto 40px; }}
  h1 {{ font-size:32px; font-weight:600; letter-spacing:-.02em; margin:0 0 8px; }}
  .sub {{ color:#78716c; margin:0; }}
  .grid {{ max-width:960px; margin:0 auto; display:flex; flex-direction:column; gap:24px; }}
  .card {{ display:flex; gap:24px; background:#fff; border:1px solid #e7e5e4; border-radius:16px;
           overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,.04); }}
  .media {{ position:relative; flex:0 0 280px; background:#f5f5f4; }}
  .media img, .media video {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .num {{ position:absolute; top:12px; left:12px; width:32px; height:32px; border-radius:50%;
          background:rgba(28,25,23,.85); color:#fff; font-weight:600; font-size:15px;
          display:grid; place-items:center; }}
  .txt {{ padding:24px 24px 24px 0; display:flex; flex-direction:column; justify-content:center; }}
  .meta {{ display:flex; align-items:center; gap:12px; margin-bottom:12px; }}
  .quando {{ font-size:13px; text-transform:uppercase; letter-spacing:.06em; color:#78716c; }}
  .tag {{ font-size:12px; font-weight:600; padding:3px 10px; border-radius:99px; }}
  .legenda {{ margin:0 0 10px; font-size:17px; }}
  .tags {{ margin:0; color:#a8a29e; font-size:14px; }}
  .semmidia {{ display:grid; place-items:center; height:100%; color:#a8a29e; font-size:14px; }}
  @media (max-width:720px) {{ .card {{ flex-direction:column; }} .media {{ flex:none; height:280px; }}
                              .txt {{ padding:0 20px 24px; }} }}
  @media (prefers-color-scheme: dark) {{
    body {{ background:#1c1917; color:#f5f5f4; }}
    .card {{ background:#292524; border-color:#44403c; }}
    .media, .semmidia {{ background:#1c1917; }}
    .tags {{ color:#78716c; }}
  }}
</style></head><body>
<header>
  <h1>Fila da Hana — {len(cartoes)} posts para aprovar</h1>
  <p class="sub">Nada sobe sem o seu OK. Responda na conversa pelos números: “aprovo 1, 2 e 4”.</p>
</header>
<div class="grid">{''.join(cartoes)}</div>
</body></html>"""

    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[ok] painel gerado: {SAIDA} ({os.path.getsize(SAIDA)/1024:.0f} KB, {len(cartoes)} posts)")

    if "--so-gerar" not in sys.argv:
        abrir_no_chrome_da_hana(SAIDA)


def abrir_no_chrome_da_hana(caminho):
    """Abre no Chrome do perfil da Hana. Se não achar o Chrome, avisa alto."""
    candidatos = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    chrome = next((c for c in candidatos if os.path.isfile(c)), None)
    if not chrome:
        print("[FALHA] nao achei o chrome.exe — abra na mao:", caminho)
        return
    subprocess.Popen([chrome, f"--profile-directory={PERFIL_HANA}", caminho])
    print(f"[ok] aberto no Chrome perfil da Hana ({PERFIL_HANA})")


if __name__ == "__main__":
    main()
