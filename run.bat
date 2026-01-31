@echo off
echo ==========================================
echo AI Voice Generation System - Setup ^& Run
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python found

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    pause
    exit /b 1
)

echo [OK] pip found

:: Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg is not installed
    echo Audio processing may not work properly
    echo Download FFmpeg from: https://ffmpeg.org/download.html
    echo.
    set /p continue="Continue anyway? (Y/N): "
    if /i not "%continue%"=="Y" exit /b 1
) else (
    echo [OK] FFmpeg found
)

:: Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully

:: Create necessary directories
echo.
echo Creating necessary directories...
if not exist "static\audio" mkdir "static\audio"
if not exist "static\css" mkdir "static\css"
if not exist "static\js" mkdir "static\js"
if not exist "templates" mkdir "templates"
echo [OK] Directories created

:: Run the application
echo.
echo ==========================================
echo Starting AI Voice Generation System...
echo ==========================================
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
pause
