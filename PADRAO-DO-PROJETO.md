# PADRÃO DO PROJETO — o mínimo que TODA pasta segue

> Fonte oficial: hub Crescimento IA (`06-SISTEMAS/maquina/PADRAO-DO-PROJETO.md`).
> Instalado nos projetos na auditoria única de 23/08/2026 autorizada pelo Ramón.
> O hub é o CONSULTOR: avisa o que existe; quem aplica é a conversa desta pasta.

## As 10 regras que não se erram

1. **Resposta curta e objetiva, POR TEMA** (Ordem nº 1 dele) — 1 bloco por
   assunto, máx. 3 assuntos; relatório vai pra arquivo, nunca pro chat.
2. **AUTOSSUFICIÊNCIA 24/7** — o `vigia-saude.py` desta pasta roda 3x/dia e
   escreve `SAUDE-DO-PROJETO.md`. Erro aberto lá se conserta NA HORA, nesta
   conversa, sem avisar o Ramón. **Proibido** mandar e-mail/Telegram/chat de
   quebra consertável. O trabalho não para esperando mensagem dele.
3. **A ÚNICA trava é DINHEIRO** — saldo já pago (APIs, Apify, créditos) pode
   usar à vontade: ele deixou disponível pra isso. Acabou ou precisa comprar
   mais → avisar e ESPERAR o OK. Nunca gastar novo no cartão sem ele saber.
4. **Chrome: validar o perfil logado ANTES de usar, SEMPRE** — abrir o menu do
   avatar e conferir nome/e-mail do perfil DESTE projeto. Perfil errado = conta
   errada = trabalho travado (o erro que mais custa tempo). Automação de
   navegador é sempre Playwright; SendKeys/mouse por coordenada, nunca.
5. **IA-Hub antes de gastar token caro** — `ask-ai.py` (Gemini longos, DeepSeek
   volume, ChatGPT criativo, Grok atualidades, Kimi 2ª opinião, NIM/OpenRouter
   grátis). O crédito é checado sozinho por hook; se barrar, trocar de IA.
6. **Escada de custo** — 1º robô-script (zero token) · 2º IA local (Ollama) ·
   3º DeepSeek/grátis · 4º Claude. Subagente barato (Haiku/Sonnet) pro
   mecânico; o motor da conversa faz só o raciocínio nobre.
7. **Git contínuo** — commit+push a cada bloco concluído, não só no fim.
   Robô do projeto mora NA pasta do projeto.
8. **Painel da frota na abertura** — conversa nova em pasta com robôs abre com
   tabela robô/frequência/status real do Agendador, sem esperar pedido.
9. **Consultar o hub, nunca reinventar** — antes de construir, ler o mural
   `COMUNICADOS.md` do hub (o vigia avisa sozinho). Aprendeu algo que serve a
   todos? Depositar com `aprender.py` (caixa de entrada). Nunca editar o hub.
10. **Uma pasta por conversa** — esta conversa só fala e mexe NESTA pasta.
    Hooks globais que já protegem aqui: RTK (economia de comando), sugestor de
    motor, vigia de conversa longa + janela nova, trava de crédito, guardião de
    arquivos, autoteste de Python.

## Se algo travar

1. `SAUDE-DO-PROJETO.md` diz o quê. 2. Consertar (regra 37: sem pedir
permissão). 3. Se a causa for acesso/login vencido: refazer o login pelo
Playwright/perfil certo; só envolver o Ramón se for 2FA/senha que apenas ele
tem — e aí em UM pedido único e completo. 4. Registrar a lição na caixa de
entrada do hub se servir a outros projetos.
