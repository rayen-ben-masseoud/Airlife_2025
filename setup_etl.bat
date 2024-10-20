@echo off
setlocal

REM Get the current directory (project root)
set PROJECT_ROOT=%~dp0

REM Define the paths to the virtual environment and Python script
set VENV_PATH=%PROJECT_ROOT%virtualenv\Scripts\python.exe
set SCRIPT_PATH=%PROJECT_ROOT%main.py
set LOG_FILE=%PROJECT_ROOT%etl_log.txt

REM Check if the virtual environment exists
if not exist "%VENV_PATH%" (
    echo Virtual environment not found at %VENV_PATH%. Please check the path.
    exit /b 1
)

REM Create a scheduled task to run the ETL every hour
schtasks /create /tn "ETL_Pipeline" /tr "\"%VENV_PATH%\" \"%SCRIPT_PATH%\" >> \"%LOG_FILE%\" 2>&1" /sc hourly /f

REM Verify the task has been created
if %errorlevel% equ 0 (
    echo ETL task scheduled to run every hour.
    echo Output will be logged in %LOG_FILE%.
) else (
    echo Failed to schedule the ETL task.
)

endlocal
