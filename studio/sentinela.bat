@echo off
cd /d "%~dp0.."
python studio\renovar_token.py >> studio\sentinela.log 2>&1
python studio\sentinela.py >> studio\sentinela.log 2>&1
