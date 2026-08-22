@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0.."
set "LOG=studio\sentinela.log"
call :rodar "renovar token" python studio\renovar_token.py
if errorlevel 1 exit /b %errorlevel%
call :rodar "sentinela" python studio\sentinela.py
if errorlevel 1 exit /b %errorlevel%
rem Lote da semana: o proprio script sai calado se nao for domingo.
call :rodar "lote semanal" python studio\lote_automatico.py --so-domingo
if errorlevel 1 exit /b %errorlevel%
rem GARIMPO (entrou em 04/08/2026). O rolo do Ramon tem 34 mil arquivos e so 17%%
rem tinham sido varridos - era eu religando na mao a cada rodada, e isso custava
rem uma conversa por vez. Agora avanca sozinho, 40 min por dia, custo zero: e
rem deteccao local, nenhuma foto sai da maquina. E retomavel, entao cada dia
rem continua de onde parou.
call :rodar "garimpo" python studio\garimpo.py --minutos 40 --workers 3
if errorlevel 1 exit /b %errorlevel%
call :rodar "estado atual" python studio\estado.py
if errorlevel 1 exit /b %errorlevel%
exit /b 0

:rodar
set "NOME=%~1"
shift
echo [%date% %time%] INICIO: %NOME% >> "%LOG%"
%* >> "%LOG%" 2>&1
set "CODIGO=!errorlevel!"
if not "!CODIGO!"=="0" (
  echo [%date% %time%] ERRO: %NOME% (codigo !CODIGO!) >> "%LOG%"
  exit /b !CODIGO!
)
echo [%date% %time%] OK: %NOME% >> "%LOG%"
exit /b 0
