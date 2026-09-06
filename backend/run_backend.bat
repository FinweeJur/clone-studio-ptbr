@echo off
title CloneStudio PT-BR - Servidor Backend
echo ======================================================
echo    🚀 Iniciando CloneStudio PT-BR (Backend)
echo ======================================================

cd /d "%~dp0"

echo [*] Verificando dependencias...
pip install -r requirements.txt

echo [*] Iniciando servidor FastAPI em http://localhost:8000 ...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
