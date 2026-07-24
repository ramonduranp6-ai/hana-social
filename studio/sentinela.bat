@echo off
cd /d "%~dp0.."
python studio\sentinela.py >> studio\sentinela.log 2>&1
