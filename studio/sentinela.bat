@echo off
cd /d "%~dp0.."
python studio\renovar_token.py >> studio\sentinela.log 2>&1
python studio\sentinela.py >> studio\sentinela.log 2>&1
rem Lote da semana: o proprio script sai calado se nao for domingo.
python studio\lote_automatico.py --so-domingo >> studio\sentinela.log 2>&1
