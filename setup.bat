@echo off
echo ========================================
echo ZustellApp - Setup Script
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error creating virtual environment!
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies!
    pause
    exit /b 1
)

echo [4/4] Installing MapView...
garden install mapview
if errorlevel 1 (
    echo Warning: MapView installation failed. You may need to install it manually.
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To create demo data, run:
echo   venv\Scripts\activate
echo   cd ZustellApp
echo   python create_demo_data.py
echo.
echo To start the app, run:
echo   venv\Scripts\activate
echo   cd ZustellApp
echo   python main.py
echo.
pause
