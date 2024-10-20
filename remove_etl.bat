@echo off
setlocal

REM Remove the scheduled task
schtasks /delete /tn "ETL_Pipeline" /f

REM Verify the task has been removed
if %errorlevel% equ 0 (
    echo ETL task removed successfully.
) else (
    echo Failed to remove the ETL task.
)

endlocal
