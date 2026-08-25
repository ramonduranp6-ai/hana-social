"""
Canal Claude -> Telegram do Ramón.

Por que existe: o bot `@Hanasocial_aproval_bot` só sabia falar sozinho (post
pra aprovar, pauta de segunda). Não havia jeito de EU mandar um recado pra ele
por lá — o token do bot mora nos secrets do GitHub, não na máquina dele.
Agora o workflow aceita a entrada `recado` e este script entrega o texto.

Uso (pela conversa):
    gh workflow run publish.yml -R ramonduranp6-ai/hana-social -f recado="texto"

Uso (local, se algum dia o token estiver no ambiente):
    TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python publisher/mandar_recado.py "texto"
"""

import os
import sys

import requests

API = "https://api.telegram.org/bot{token}/sendMessage"
LIMITE = 4096  # limite duro do Telegram por mensagem


def _credencial(nome):
    """Acha a credencial em 3 lugares, nesta ordem.

    ACHADO 21/08/2026: o ciclo automatico do VP (rotina agendada na maquina do
    Ramon) nao conseguiu mandar recado nenhum — reportou "so existe
    .env.example". Motivo: este script lia SO `os.environ`, e um processo
    disparado por agendador/ponte nem sempre herda as variaveis de USUARIO do
    Windows (elas existem, mas so entram em shell aberto depois delas). O
    recado morria no log e o Ramon nunca era avisado.

    1. `os.environ` — GitHub Actions e shell normal (caminho de sempre).
    2. `studio/.telegram` — arquivo local fora do git (mesmo padrao que o
       `studio/lote_automatico.py` ja usava).
    3. Registro do Windows (variavel de USUARIO) — pega o caso do agendador,
       sem precisar de arquivo nenhum. Leitura pura, nunca escreve.
    """
    valor = os.environ.get(nome)
    if valor:
        return valor

    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    arquivo = os.path.join(raiz, "studio", ".telegram")
    if os.path.isfile(arquivo):
        for linha in open(arquivo, encoding="utf-8", errors="ignore"):
            if linha.strip().startswith(f"{nome}="):
                return linha.split("=", 1)[1].strip()

    if sys.platform == "win32":
        import winreg
        locais = (
            (winreg.HKEY_CURRENT_USER, r"Environment"),
            (winreg.HKEY_LOCAL_MACHINE,
             r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
        )
        for raiz_reg, caminho in locais:
            try:
                with winreg.OpenKey(raiz_reg, caminho) as k:
                    valor = winreg.QueryValueEx(k, nome)[0]
                    if valor:
                        return valor
            except Exception:  # noqa: BLE001 — sem a variavel, tenta o proximo
                continue
    return None


def _pedacos(texto, tamanho=LIMITE):
    """Quebra o recado em mensagens, sem cortar linha no meio."""
    partes, atual = [], ""
    for linha in texto.split("\n"):
        if len(atual) + len(linha) + 1 > tamanho:
            partes.append(atual.rstrip("\n"))
            atual = ""
        atual += linha + "\n"
    if atual.strip():
        partes.append(atual.rstrip("\n"))
    return partes or [texto[:tamanho]]


# DESLIGADO em 25/08/2026, ordem direta dele: "não quero mais receber
# mensagens pelo telegram, lá não funciona, traga minhas pendências por
# aqui". Guarda ÚNICA aqui dentro de mandar() porque é a função que
# avisar_lote.py, cobertura_fila.py, leitura_d1.py, recepcionista.py e
# sentinel.py (token) importam e chamam — apagar/religar num lugar só.
# NÃO apaga o bot nem os secrets: só para de empurrar mensagem pra ele.
TELEGRAM_DESLIGADO = True


def mandar(token, chat_id, texto):
    if TELEGRAM_DESLIGADO:
        print("[telegram] desligado por ordem do Ramón (25/08/2026) — "
              "nada enviado. Recado: " + texto[:200])
        return True
    for parte in _pedacos(texto):
        r = requests.post(API.format(token=token), timeout=60,
                          data={"chat_id": chat_id, "text": parte})
        if not r.ok or not r.json().get("ok"):
            raise RuntimeError("Telegram recusou: %s" % r.text[:300])
    return True


def _mandar_pelo_github(texto):
    """Ultimo recurso: dispara o workflow, que tem os secrets do Telegram.

    E' o caminho que o docstring deste arquivo ja documentava para uso pela
    conversa; virou fallback automatico em 21/08/2026 para o recado nunca
    morrer calado num processo sem credencial (agendador, ponte, rotina).
    """
    import shutil
    import subprocess
    if not shutil.which("gh"):
        print("[erro] sem credencial local do Telegram e sem o 'gh' instalado "
              "— nao tenho por onde mandar o recado")
        return 1
    r = subprocess.run(
        ["gh", "workflow", "run", "publish.yml",
         "-R", "ramonduranp6-ai/hana-social", "-f", f"recado={texto}"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"[erro] nao consegui disparar o workflow: {r.stderr.strip()[:200]}")
        return 1
    print("[ok] sem credencial local — recado despachado pelo GitHub Actions "
          "(chega no Telegram na proxima rodada)")
    return 0


def main():
    texto = " ".join(sys.argv[1:]).strip() or os.environ.get("RECADO", "").strip()
    if not texto:
        print("[aviso] sem recado pra mandar — saindo calado")
        return 0

    token = _credencial("TELEGRAM_BOT_TOKEN")
    chat_id = _credencial("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        # Sem credencial local, o recado NAO morre no log: sai pelo GitHub
        # Actions, que tem os secrets. Conferido em 21/08/2026: as credenciais
        # do Telegram nunca existiram nesta maquina (nem em variavel de
        # ambiente, nem no registro, nem em studio/.telegram) — so como secret
        # do repositorio. Era por isso que o ciclo automatico do VP dizia
        # "Telegram nao saiu" e o Ramon nunca recebia o resumo.
        return _mandar_pelo_github(texto)

    # Etiqueta: ele precisa saber a QUE mensagem está respondendo (cobrança de
    # 01/08/2026). Ver publisher/etiqueta.py. Sem RECADO_ASSUNTO o texto sai
    # cru, como antes — assim os avisos automáticos antigos não quebram.
    assunto = os.environ.get("RECADO_ASSUNTO", "").strip()
    if assunto:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from etiqueta import etiquetar
        texto = etiquetar(assunto, texto,
                          os.environ.get("RECADO_RESPONDA", "").strip() or None)

    mandar(token, chat_id, texto)
    print("[ok] recado entregue (%d caractere(s))" % len(texto))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
