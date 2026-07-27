"""
Renovação automática do token do Instagram — o post nunca mais para calado.

O token de longa duração vale 60 dias. Este script troca por um novo de 60 dias
e atualiza o secret no GitHub, sem ninguém precisar lembrar. Ideia trazida do
benchmark com o outro projeto do Ramón (25/07/2026), que testou o endpoint.

Uso:
    python studio/renovar_token.py            # renova se faltarem <= 20 dias
    python studio/renovar_token.py --forcar   # renova agora

Onde fica o token: studio/.token (arquivo local, fora do git). Formato:
    IG_ACCESS_TOKEN=<valor>
    EXPIRA_EM=2026-09-21

O valor do token nunca é impresso — só os 4 últimos caracteres, para conferência.
"""

import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request

REPO = "ramonduranp6-ai/hana-social"
AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(AQUI, ".token")
DIAS_ANTES = 20


def ler():
    if not os.path.isfile(ARQ):
        print(f"[ERRO] {ARQ} nao existe.")
        print("Crie o arquivo com duas linhas (o token vem do painel da Meta):")
        print("    IG_ACCESS_TOKEN=<cole aqui>")
        print("    EXPIRA_EM=2026-09-21")
        sys.exit(1)
    dados = {}
    with open(ARQ, encoding="utf-8-sig") as f:
        for linha in f:
            if "=" in linha and not linha.strip().startswith("#"):
                k, v = linha.strip().split("=", 1)
                dados[k.strip()] = v.strip()
    if not dados.get("IG_ACCESS_TOKEN"):
        print("[ERRO] IG_ACCESS_TOKEN vazio no arquivo.")
        sys.exit(1)
    return dados


def gravar(token, expira):
    with open(ARQ, "w", encoding="utf-8") as f:
        f.write(f"IG_ACCESS_TOKEN={token}\n")
        f.write(f"EXPIRA_EM={expira.isoformat()}\n")


def renovar(token):
    """Troca o token por um novo de 60 dias. Nao exige app secret."""
    url = ("https://graph.instagram.com/refresh_access_token"
           f"?grant_type=ig_refresh_token&access_token={token}")
    with urllib.request.urlopen(url, timeout=60) as r:
        d = json.load(r)
    if "access_token" not in d:
        raise RuntimeError(f"resposta inesperada: {str(d)[:200]}")
    return d["access_token"], int(d.get("expires_in", 60 * 86400))


def main():
    forcar = "--forcar" in sys.argv
    dados = ler()
    token = dados["IG_ACCESS_TOKEN"]

    if not forcar and dados.get("EXPIRA_EM"):
        faltam = (dt.date.fromisoformat(dados["EXPIRA_EM"]) - dt.date.today()).days
        if faltam > DIAS_ANTES:
            print(f"[ok] token valido por mais {faltam} dias — nada a fazer.")
            return

    novo, segundos = renovar(token)
    expira = dt.date.today() + dt.timedelta(seconds=segundos)
    gravar(novo, expira)
    print(f"[ok] token renovado ate {expira} (final ...{novo[-4:]})")

    r = subprocess.run(["gh", "secret", "set", "IG_ACCESS_TOKEN", "-R", REPO],
                       input=novo, capture_output=True, text=True)
    if r.returncode == 0:
        print("[ok] secret IG_ACCESS_TOKEN atualizado no GitHub")
    else:
        print("[FALHA] nao consegui atualizar o secret:", (r.stderr or "").strip()[:200])
        sys.exit(1)


if __name__ == "__main__":
    main()
