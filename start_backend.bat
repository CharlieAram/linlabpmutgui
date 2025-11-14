@echo off
REM Startup script for backend server (Windows)

echo ========================================
echo TX7332 PMUT Control - Starting Backend
echo ========================================

cd backend
echo Starting FastAPI server on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

python run.py
pause

