@echo off
cd /d "%~dp0.."
python studio\renovar_token.py >> studio\sentinela.log 2>&1
python studio\sentinela.py >> studio\sentinela.log 2>&1
rem Lote da semana: o proprio script sai calado se nao for domingo.
python studio\lote_automatico.py --so-domingo >> studio\sentinela.log 2>&1
rem GARIMPO (entrou em 04/08/2026). O rolo do Ramon tem 34 mil arquivos e so 17%%
rem tinham sido varridos - era eu religando na mao a cada rodada, e isso custava
rem uma conversa por vez. Agora avanca sozinho, 40 min por dia, custo zero: e
rem deteccao local, nenhuma foto sai da maquina. E retomavel, entao cada dia
rem continua de onde parou.
python studio\garimpo.py --minutos 40 --workers 3 >> studio\garimpo_rodada.log 2>&1
