@echo off
REM Startup script for frontend application (Windows)

echo =========================================
echo TX7332 PMUT Control - Starting Frontend
echo =========================================

cd frontend
echo Starting React development server
echo Application will open at http://localhost:5173
echo.

npm run dev
pause

