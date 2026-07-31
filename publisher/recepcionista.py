# -*- coding: utf-8 -*-
"""
Recepcionista do Telegram — o "primeiro atendimento" do bot da Hana.

Por que existe: o Ramón manda mensagem de texto pro bot @Hanasocial_aproval_bot
e, até 31/07/2026, ninguém respondia de verdade — `telegram_approve.py` só
guardava o texto em content/recados.md e devolvia uma frase fixa. Ele
reclamou duas vezes ("Te mandei msg pelo Telegram e vc não responde?") e
mandou: "Vou te mandar msg pelo telegram e voce precisa receber por lá tb".

O que este robô faz, em uma frase: ele lê o estado REAL do projeto (placar,
fila, publicados, decisões) e usa o Gemini Flash pra responder na hora o que
dá pra responder com isso — e escala pro Claude, sem inventar, o que exige
julgamento. Custo: fração de centavo por mensagem, ZERO token de Claude.

REGRA DE OURO (regra zero do projeto, cobrada pelo Ramón em 28/07/2026): este
robô NUNCA pode afirmar o que não estiver no CONTEXTO que ele mesmo montou
lendo os arquivos agora. O prompt (ver SISTEMA) instrui o Gemini a começar a
resposta com o marcador [ESCALAR] sempre que a pergunta pedir ação, opinião
de estratégia, ou a resposta não estiver no que foi lido — nesses casos o
robô grava o recado (como já fazia) e avisa que o Claude vai ver.

Como ele se encaixa no fluxo (NÃO cria um segundo consumidor do getUpdates):
`telegram_approve.sync_approvals()` já lê as mensagens de texto do Telegram;
em vez de gravar recado direto, ela agora chama `responder_mensagem()` daqui
(import local, ver o comentário lá no telegram_approve.py). Continua sendo
UM SÓ lugar lendo getUpdates — este arquivo não toca na API do Telegram além
de mandar a resposta.

Uso:
    python publisher/recepcionista.py --simular "pergunta de teste"
        Monta o contexto, chama o Gemini, imprime o resultado. NÃO toca no
        Telegram, NÃO grava recado — é o modo de teste com dado de mentira
        que a regra da casa exige antes de qualquer robô ir pro ar.

Pegadinhas do Gemini já pagas neste projeto (copiadas de studio/lote_automatico.py):
  - `maxOutputTokens` baixo corta a resposta no meio, porque o Flash gasta
    tokens "pensando" antes de escrever — por isso 2000, não menos.
  - `thinkingConfig` este endpoint RECUSA (erro "invalid argument").
  - O console do Windows é cp1252 e quebra com emoji — por isso o reconfigure
    de stdout/stderr logo abaixo.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

# Console do Windows engasga com emoji (legenda de Instagram e as respostas do
# Gemini têm emoji) — sem isto o script morre ao IMPRIMIR, não ao trabalhar.
for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

PLACAR = os.path.join(RAIZ, "content", "placar.md")
FILA = os.path.join(RAIZ, "content", "queue")
POSTADOS = os.path.join(RAIZ, "content", "posted")
ESTADO_ATUAL = os.path.join(RAIZ, "ESTADO-ATUAL.md")
DECISOES = os.path.join(RAIZ, "DECISOES.md")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-flash-latest:generateContent"
)

MARCADOR_ESCALAR = "[ESCALAR]"

# Mensagem que ele vê no Telegram quando o Gemini escala (ou quando tudo
# falha e o robô cai no comportamento antigo de só anotar).
MSG_ESCALADO = (
    "🐾 Essa eu não sei responder só com o que tenho aqui — anotei e o "
    "Claude vê isso na próxima conversa."
)


SISTEMA = """Você é o recepcionista do projeto Hana Social — perfil do Instagram
@hanaduransanches, da cadela do Ramón. Você fala DIRETO com o Ramón. Ele é
leigo em tecnologia: escreva em português simples, sem jargão de programador,
como quem manda mensagem curta de WhatsApp.

QUEM VOCÊ É (e quem você NÃO é):
- Você é só o primeiro atendimento — o "alô" do robô. Quem decide, executa e
  opina sobre estratégia é o Claude e os diretores dele, não você.
- Você NUNCA publica, aprova, recusa, apaga, agenda ou muda nada no projeto.
  Você só lê o estado atual (o CONTEXTO abaixo) e conversa sobre ele.

REGRAS DURAS — comece a resposta com o marcador [ESCALAR] sozinho (sem mais
nada antes dele) sempre que pelo menos uma destas for verdade:
1. A pergunta pede uma AÇÃO (publicar, aprovar, recusar, apagar, mudar,
   agendar, comentar em nome dele, mexer em configuração).
2. A pergunta pede OPINIÃO, ESTRATÉGIA ou JULGAMENTO (o que funciona, o que
   postar, se vale a pena, preço, o que fazer para melhorar o conteúdo).
3. A resposta simplesmente NÃO está escrita no CONTEXTO abaixo. NUNCA
   deduza, estime ou chute — principalmente número (seguidores, alcance,
   curtidas, salvos, compartilhamentos). Se não está no placar, você não sabe.

Quando NENHUMA das três se aplica, responda DIRETO — sem o marcador — só com
o que está literalmente no CONTEXTO (ex.: quantos seguidores tem agora, o que
está na fila, quando sai o próximo post, o que já foi publicado).

FORMATO DA RESPOSTA (quando não escalar):
- Máximo 5 linhas.
- Português simples, direto, sem tecniquês.
- Nunca prometa fazer algo — se a pergunta pedir ação, é [ESCALAR], não
  "vou fazer" nem "já fiz".
"""


def _cortar(texto, limite):
    texto = texto.strip()
    if len(texto) <= limite:
        return texto
    return texto[:limite].rstrip() + "\n[...cortado aqui, o arquivo real é maior...]"


def _ler(caminho, limite_linhas=None, limite_chars=4000):
    """Lê um arquivo de estado real, truncado — regra 2 da encomenda: nunca
    deixar o contexto estourar."""
    if not os.path.isfile(caminho):
        return "(arquivo não existe: %s)" % os.path.basename(caminho)
    with open(caminho, encoding="utf-8", errors="replace") as f:
        linhas = f.readlines()
    if limite_linhas:
        linhas = linhas[:limite_linhas]
    return _cortar("".join(linhas), limite_chars)


def _fila_compacta():
    """Lista curta da fila (id, tipo, status, quando, começo da legenda). A
    legenda inteira não importa pro recepcionista responder "quando sai o
    próximo post" — só inflaria o contexto à toa."""
    if not os.path.isdir(FILA):
        return "(pasta content/queue não existe — fila vazia)"
    linhas = []
    for nome in sorted(os.listdir(FILA)):
        caminho = os.path.join(FILA, nome, "post.json")
        if not os.path.isfile(caminho):
            continue
        try:
            with open(caminho, encoding="utf-8") as f:
                post = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        legenda = post.get("caption", "").split("\n")[0][:70]
        linhas.append(
            '- %s | tipo=%s | status=%s | agendado(UTC)=%s | legenda começa: "%s..."'
            % (nome, post.get("type"), post.get("status"),
               post.get("scheduled_for"), legenda)
        )
    return "\n".join(linhas) if linhas else "(fila vazia agora)"


def _publicados_compacto(limite=10):
    """Últimos publicados, mais compacto ainda — só o suficiente pra
    responder "o que já saiu"."""
    if not os.path.isdir(POSTADOS):
        return "(nada publicado ainda)"
    nomes = sorted(os.listdir(POSTADOS))[-limite:]
    linhas = []
    for nome in nomes:
        caminho = os.path.join(POSTADOS, nome, "post.json")
        if not os.path.isfile(caminho):
            continue
        try:
            with open(caminho, encoding="utf-8") as f:
                post = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        linhas.append(
            "- %s | tipo=%s | agendado(UTC)=%s | instagram_id=%s"
            % (nome, post.get("type"), post.get("scheduled_for"),
               post.get("instagram_id", "?"))
        )
    return "\n".join(linhas) if linhas else "(nada publicado ainda)"


def montar_contexto(agora=None):
    """
    Monta o CONTEXTO real que vai pro Gemini — lendo os arquivos AGORA,
    nesta execução (regra zero do projeto: nada de memória, nada de achismo).
    """
    agora = agora or datetime.now(timezone.utc)
    return f"""AGORA (data/hora UTC de verdade — use isto pra calcular "quando", o Gemini não sabe a hora sozinho): {agora.strftime('%Y-%m-%dT%H:%M:%SZ')}

=== PLACAR (content/placar.md) — métricas medidas, NUNCA estime além disto ===
{_ler(PLACAR, limite_chars=3000)}

=== FILA DE POSTS (content/queue/*/post.json) — o que ainda vai ao ar ===
{_fila_compacta()}

=== ÚLTIMOS PUBLICADOS (content/posted/*/post.json) ===
{_publicados_compacto()}

=== ESTADO-ATUAL.md (foto automática do projeto, gerada por código) ===
{_ler(ESTADO_ATUAL, limite_linhas=90, limite_chars=4000)}

=== DECISOES.md (decisões vigentes do Ramón, só o topo/mais recente) ===
{_ler(DECISOES, limite_linhas=120, limite_chars=6000)}
"""


def _chave_local():
    """
    Fallback só pra TESTE LOCAL (--simular) na máquina do Ramón — em produção
    (dentro do publish.yml no GitHub Actions) GEMINI_API_KEY já vem pronta do
    secret do repo, isto aqui nunca roda lá. Mesmos locais que o ask-ai.py do
    hub (~/.claude/ia-hub/) procura — as chaves são dele, moram no OneDrive
    pessoal, não duplico a lógica inteira, só os caminhos mais prováveis.
    """
    casa = os.path.expanduser("~")
    candidatos = [
        os.path.join(casa, "OneDrive", "IA-Hub", "chaves-api.txt"),
        os.path.join(casa, "OneDrive", "Desktop", "Claude Code", "IA-Hub", "chaves-api.txt"),
        os.path.join(casa, "OneDrive", "Desktop", "Crescimento IA", "Documents", "IA-Hub", "chaves-api.txt"),
    ]
    for caminho in candidatos:
        if not os.path.isfile(caminho):
            continue
        for linha in open(caminho, encoding="utf-8", errors="ignore"):
            if linha.strip().startswith("GEMINI_API_KEY="):
                return linha.split("=", 1)[1].strip()
    return None


def chave_gemini():
    return os.environ.get("GEMINI_API_KEY") or _chave_local() or (
        _erro_sem_chave()
    )


def _erro_sem_chave():
    raise RuntimeError(
        "GEMINI_API_KEY não encontrada (nem em os.environ, nem em "
        "chaves-api.txt local)"
    )


def gerar_resposta(pergunta, agora=None):
    """
    Manda a pergunta pro Gemini Flash junto com o CONTEXTO real do projeto.
    Devolve (escalar: bool, texto: str).

    Levanta exceção se algo TÉCNICO falhar (sem chave, timeout, Gemini fora
    do ar, resposta vazia/cortada) — quem chama decide o que fazer com isso
    (regra 8 da encomenda: publicar posts é mais importante que responder
    mensagem, então esta função nunca pode travar o robô sozinha; quem
    encapsula o try/except é responder_mensagem()).
    """
    contexto = montar_contexto(agora)
    chave = chave_gemini()
    prompt = SISTEMA + "\n\n" + contexto + "\n\nPERGUNTA DO RAMÓN AGORA:\n" + pergunta.strip()
    corpo = {
        "contents": [{"parts": [{"text": prompt}]}],
        # temperature baixa: aqui é resposta factual sobre o estado do
        # projeto, não legenda criativa (que no lote_automatico.py usa 0.9).
        # maxOutputTokens em 2000 e SEM thinkingConfig — pegadinha já paga.
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2000},
    }
    r = requests.post(
        GEMINI_URL, params={"key": chave}, json=corpo,
        headers={"Content-Type": "application/json"}, timeout=60,
    )
    dados = r.json()
    if "error" in dados:
        raise RuntimeError(dados["error"].get("message", str(dados["error"]))[:200])
    candidato = dados["candidates"][0]
    texto = "".join(
        p.get("text", "") for p in candidato.get("content", {}).get("parts", [])
    ).strip()
    if candidato.get("finishReason") == "MAX_TOKENS" or not texto:
        raise RuntimeError("resposta do Gemini veio vazia ou cortada no meio")

    # Deteccao do marcador tolerante a formatacao. Achado na revisao de
    # 31/07/2026: `startswith` cru devolvia False para `**[ESCALAR]**` e para
    # `"[ESCALAR]"`, e o Flash pontua e coloca negrito por conta propria. Um
    # falso negativo aqui e o pior caso: a mensagem NAO e escalada e o texto
    # que explicava o motivo da escalada e mandado pro Ramon como se fosse a
    # resposta. Por isso olhamos o comeco do texto sem pontuacao nem markdown.
    limpo = re.sub(r"^[\s*_`\"'>#-]+", "", texto).upper()
    escalar = limpo.startswith(MARCADOR_ESCALAR)
    if escalar:
        corte = texto.upper().find(MARCADOR_ESCALAR) + len(MARCADOR_ESCALAR)
        texto = texto[corte:].strip(" :–-*_`\"'\n")
    return escalar, texto


def responder_mensagem(texto, quando, token=None, chat_id=None):
    """
    Ponto de entrada chamado de dentro de telegram_approve.sync_approvals()
    para cada mensagem de texto que o Ramón manda pro bot.

    Fluxo: tenta responder pelo Gemini. Se ele escalar (ação, opinião, ou
    resposta fora do contexto) OU se qualquer coisa técnica falhar, cai no
    comportamento antigo — grava o recado e avisa que o Claude vai ver.

    Esta função NUNCA deixa exceção escapar, e agora isso é verdade de fato: o
    corpo inteiro está dentro de um try. A revisão de 31/07/2026 pegou que a
    promessa estava no texto e não no código — `_guardar_recado` e o envio ao
    Telegram ficavam FORA do try e os dois fazem chamada de rede. Um timeout do
    Telegram subia por `sync_approvals` até o `run.py` e **os posts do dia não
    eram publicados**. Robô de recepção não pode derrubar publicação.
    """
    try:
        _responder(texto, quando, token, chat_id)
    except Exception as exc:  # noqa: BLE001 — ultima linha de defesa, ver docstring
        print(f"[recepcionista][ERRO] engoli para nao derrubar a publicacao: {str(exc)[:200]}")


def _responder(texto, quando, token, chat_id):
    from telegram_approve import _guardar_recado  # import local: ver nota no telegram_approve.py
    from mandar_recado import mandar

    try:
        escalar, resposta = gerar_resposta(texto)
    except Exception as exc:  # noqa: BLE001 — qualquer falha aqui cai pro recado simples
        print(f"[recepcionista][aviso] Gemini falhou ({str(exc)[:150]}) — caiu pro recado simples.")
        _guardar_recado(texto, quando, token, chat_id)
        return

    if escalar:
        print(f"[recepcionista] escalou pro Claude: {texto[:60]!r}")
        _guardar_recado(texto, quando, token, chat_id, resposta_fixa=MSG_ESCALADO)
        return

    print(f"[recepcionista] respondeu direto: {resposta[:80]!r}")
    # Entrega pelo mandar_recado, não pelo `_call` cru: ele quebra em 4096
    # caracteres (limite duro do Telegram) e LEVANTA erro quando a API recusa.
    # Com o `_call` cru, uma resposta longa demais era descartada em silêncio.
    # E se a entrega falhar por qualquer motivo, o recado vira linha para o
    # Claude ver — mensagem do Ramón não pode sumir. Este era o cenário que a
    # revisão chamou de "perda definitiva e silenciosa" assim que o bug do
    # offset fosse corrigido (e ele foi, na mesma leva).
    if not (token and chat_id):
        _guardar_recado(texto, quando, token, chat_id)
        return
    try:
        mandar(token, chat_id, resposta)
    except Exception as exc:  # noqa: BLE001
        print(f"[recepcionista][aviso] Telegram recusou a resposta ({str(exc)[:150]}) — virou recado.")
        _guardar_recado(texto, quando, token, chat_id)


def main():
    if "--simular" not in sys.argv:
        print('uso: python publisher/recepcionista.py --simular "pergunta de teste"\n'
              "(em produção quem chama é telegram_approve.sync_approvals — "
              "não roda sozinho no cron)")
        return 1

    i = sys.argv.index("--simular")
    pergunta = " ".join(sys.argv[i + 1:]).strip()
    if not pergunta:
        print('uso: python publisher/recepcionista.py --simular "pergunta de teste"')
        return 1

    print(f"[pergunta] {pergunta}")
    print("[montando contexto e chamando o Gemini — nada de Telegram é tocado neste modo]\n")
    try:
        escalar, texto = gerar_resposta(pergunta)
    except Exception as exc:  # noqa: BLE001
        print(f"[FALHA] não consegui chamar o Gemini: {exc}")
        return 1

    if escalar:
        print("[resultado] ESCALARIA pro Claude (em produção: grava recado + avisa no Telegram)")
        if texto:
            print(f"[motivo que o Gemini deu] {texto}")
    else:
        print("[resultado] responderia DIRETO no Telegram:")
        print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
