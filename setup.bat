@echo off

REM Check if Python is installed
where python > nul 2>&1
if %errorlevel% equ 0 (
    echo Python is installed.
    goto install_libraries
) else (
    echo Python is not installed.
    goto exit
)

:install_libraries
REM Install libraries from requirements.txt
if exist requirements.txt (
    echo Installing libraries from requirements.txt...
    pip install -r requirements.txt
    goto exit
) else (
    echo requirements.txt not found.
    goto exit
)

:exit
echo Script execution completed.
pause
