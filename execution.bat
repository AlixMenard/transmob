@echo off
set "script_path=GUI.py"
set "desired_ultralytics_version=8.3.24"

py -m pip install --upgrade pip 2>nul
py -m pip install ultralytics==%desired_ultralytics_version% --upgrade 2>nul
git pull

REM Check if torch is installed in the 'py' launcher
py -c "import torch" 2>nul
if not errorlevel 1 (
    py "%script_path%"
    exit /b
)

REM Check if torch is installed in the 'python' command
python -c "import torch" 2>nul
if not errorlevel 1 (
    python "%script_path%"
    exit /b
)

echo Neither 'py' nor 'python' has torch installed. Please install torch and try again.
pause
