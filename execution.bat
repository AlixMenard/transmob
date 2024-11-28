@echo off
set "script_path=GUI.py"
set "desired_ultralytics_version=8.3.33"

echo Updating pip...
py -m pip install --upgrade pip

echo Installing Ultralytics version %desired_ultralytics_version%...
py -m pip install ultralytics==%desired_ultralytics_version% --upgrade

echo Pulling the latest code from Git...
git pull

REM Check if torch is installed in the 'py' launcher
py -c "import torch" 2>nul
if not errorlevel 1 (
    cls
    echo Running script with 'py'...
    py "%script_path%"
    goto :end
)

REM Check if torch is installed in the 'python' command
python -c "import torch" 2>nul
if not errorlevel 1 (
    cls
    echo Running script with 'python'...
    python "%script_path%"
    goto :end
)

echo Neither 'py' nor 'python' has torch installed. Please install torch and try again.

:end
echo Script finished. Press any key to exit...
pause
