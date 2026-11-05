@echo off
REM Script de démarrage du backend AgroNavig
REM Assurez-vous que PostgreSQL est en cours d'exécution sur le port 5432

echo ========================================
echo   AgroNavig Backend - Démarrage
echo ========================================
echo.

cd agronavig-backend

echo Activation de l'environnement virtuel...
call .\venv\Scripts\activate.bat

echo.
echo Lancement du serveur FastAPI...
echo Backend accessible sur: http://127.0.0.1:8000
echo Documentation Swagger: http://127.0.0.1:8000/docs
echo.

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
