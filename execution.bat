@echo off
set "GUI.py"

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
