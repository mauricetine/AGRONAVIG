@echo off
REM Script de démarrage du frontend AgroNavig

echo ========================================
echo   AgroNavig Frontend - Démarrage
echo ========================================
echo.

cd agronavig-frontend

echo Vérification des dépendances...
if not exist "node_modules" (
    echo Installation des dépendances npm...
    call npm install
)

echo.
echo Lancement du serveur Vite...
echo Frontend accessible sur: http://localhost:5173
echo.

call npm run dev

pause
