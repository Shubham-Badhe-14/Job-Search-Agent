@echo off
setlocal

:: Get project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
cd /d "%PROJECT_ROOT%"

echo ===================================================
echo   CareerAgent AI - Environment Setup
echo ===================================================

:: Check for virtual environment
if not exist "agent_env" (
    echo [1/3] Creating virtual environment...
    python -m venv agent_env
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment. Ensure Python is installed.
        exit /b 1
    )
) else (
    echo [1/3] Virtual environment already exists.
)

:: Install dependencies
echo [2/3] Installing/Updating dependencies...
call agent_env\Scripts\activate.bat
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to install dependencies.
    exit /b 1
)

:: Setup .env if missing
if not exist ".env" (
    echo [3/3] Initializing .env from example...
    if exist "configs\.env.example" (
        copy "configs\.env.example" ".env"
        echo [DONE] Created .env. Please update it with your API keys.
    ) else (
        echo [WARNING] configs\.env.example not found. Creating empty .env...
        type nul > ".env"
    )
) else (
    echo [3/3] .env file already exists.
)

echo ===================================================
echo   Setup Complete!
echo ===================================================
exit /b 0
