@echo off
setlocal

:: Get project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
cd /d "%PROJECT_ROOT%"

echo Starting CareerAgent AI Backend...

:: Activate venv
if exist "agent_env\Scripts\activate.bat" (
    call agent_env\Scripts\activate.bat
)

:: Set PYTHONPATH to ensure backend module is findable
set PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%

:: Run uvicorn
uvicorn backend.app:app --host 0.0.0.0 --port 8000

pause
