            @echo off
setlocal

echo ===================================================
echo   CareerAgent AI - One-Click Launcher
echo ===================================================

:: 1. Run Setup
echo [1/3] Ensuring environment is ready...
call scripts\setup_env.bat
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Setup failed. Please check the errors above.
    pause
    exit /b %ERRORLEVEL%
)

:: 2. Start Backend
echo [2/3] Launching Backend Server in a new window...
start "CareerAgent AI - Backend" cmd /c "scripts\run_backend.bat"

:: 3. Start Frontend
echo [3/3] Launching Vanilla UI in a new window...
start "CareerAgent AI - UI" cmd /c "scripts\run_vanilla_ui.bat"

echo ===================================================
echo   Services are starting! 🚀
echo   - Backend: http://localhost:8000/docs
echo   - UI:      http://localhost:8080
echo ===================================================
echo Press any key to stop this script (won't stop the background services).
pause
