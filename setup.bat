@echo off
REM Windows batch script for setting up the project
echo ============================================================
echo Enterprise LangChain AI Workbench - Setup (Windows)
echo ============================================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or 3.12 from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Checking Python version...
python --version

REM Create virtual environment
if exist venv (
    echo Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
echo This may take several minutes...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo To activate the virtual environment in the future:
echo   venv\Scripts\activate
echo.
echo To run the Streamlit app:
echo   streamlit run streamlit_app.py
echo.
pause
