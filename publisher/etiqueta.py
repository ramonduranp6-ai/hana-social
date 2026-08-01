"""
Etiqueta das mensagens do bot — para o Ramón sempre saber o que está respondendo.

Cobrança dele, 01/08/2026: *"Corrija um ponto, voce manda muita mensagem e as
vezes não sabe nem qual eu estou respondendo, organiza isso"*.

O problema real: o bot manda recado, prévia, pauta de segunda, leitura do dia 1
e post pra aprovar — tudo com cara de mensagem solta. Quando ele responde
"aprova" três mensagens depois, ninguém sabe a qual se refere.

A regra que este módulo IMPÕE (não sugere):
  1. Toda mensagem começa com uma ETIQUETA: `[ASSUNTO · dia/mês hh:mm]`.
     O assunto é obrigatório — sem ele o envio falha, de propósito, em vez de
     sair mais uma mensagem sem identidade.
  2. Se a mensagem espera resposta, ela TERMINA com a pergunta em uma linha
     começando por "👉 Responda:" — e diz as palavras exatas que ele pode usar.
     Mensagem que não espera resposta não leva essa linha, e aí ele sabe que é
     só informação e pode ignorar sem culpa.

Não guarda contador em disco de propósito: contador exigiria commit de volta
pelo workflow, e um número que se perde é pior do que não ter número. Data e
hora já distinguem, e o assunto é o que ele lê de verdade.
"""

from datetime import datetime, timedelta, timezone

# Itajaí (UTC-3). O bot roda em UTC no GitHub; ele lê no horário dele.
FUSO = timezone(timedelta(hours=-3))


def etiquetar(assunto, texto, responda=None, agora=None):
    """
    Monta a mensagem final com etiqueta e, se houver, a linha de resposta.

    assunto: 2 a 4 palavras em MAIÚSCULAS que dizem do que se trata
             (ex.: "TRILHA 10/08", "PREVIA DE REEL", "PAUTA DE SEGUNDA").
    responda: o que ele deve responder (ex.: "APROVA ou NAO APROVA").
              None = mensagem só informativa, não espera resposta.
    """
    assunto = (assunto or "").strip()
    if not assunto:
        raise ValueError("mensagem sem ASSUNTO — a etiqueta e obrigatoria "
                         "(regra dele de 01/08/2026)")
    quando = (agora or datetime.now(FUSO)).strftime("%d/%m %H:%M")
    cabeca = f"[{assunto.upper()} · {quando}]"
    partes = [cabeca, "", texto.strip()]
    if responda:
        partes += ["", f"👉 Responda: {responda.strip()}"]
    else:
        partes += ["", "(só pra você saber — não precisa responder)"]
    return "\n".join(partes)
