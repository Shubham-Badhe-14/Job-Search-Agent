@echo off
setlocal

:: Get project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
cd /d "%PROJECT_ROOT%\frontend\vanilla-ui"

echo Starting Vanilla JS UI at http://localhost:8080...
echo (Ensure the backend is running for the UI to work)

:: Run simple python server
python -m http.server 8080

pause
