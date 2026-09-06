@echo off
title CloneStudio PT-BR
echo ================================================================
echo    🎬 CloneStudio PT-BR - Estúdio Open Source de Clones com IA
echo ================================================================
echo.
echo [*] Iniciando o servidor local leve...
cd /d "%~dp0backend"

:: Instalar dependencias se necessario
python -m pip install -q -r requirements.txt

:: Iniciar o backend em segundo plano e abrir o navegador
start "" http://localhost:8000
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause
