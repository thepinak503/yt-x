@echo off
REM yt-x Launcher - Windows Portable Package
REM This batch file serves as the executable for yt-x

setlocal enabledelayedexpansion

REM Find Python interpreter
set PYTHON_CMD=
for %%p in (python python3 py python3.11 python3.10 python3.9 python3.8) do (
    where %%p >nul 2>&1
    if !errorlevel! equ 0 (
        set PYTHON_CMD=%%p
        goto :found_python
    )
)

:not_found
echo Error: Python not found in PATH
echo.
echo Please install Python 3.8 or higher from: https://www.python.org/downloads/
echo.
pause
exit /b 1

:found_python
echo Found Python: %PYTHON_CMD%
echo.

REM Check if yt-x.py exists
if not exist "%~dp0yt-x.py" (
    echo Error: yt-x.py not found
    echo Make sure this batch file is in the same directory as yt-x.py
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
"%PYTHON_CMD%" -c "import textual" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    "%PYTHON_CMD%" -m pip install -q -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed.
)

REM Run yt-x
echo Starting yt-x...
echo.
"%PYTHON_CMD%" "%~dp0yt-x.py" %*

REM If there was an error, pause to let user see it
if errorlevel 1 (
    echo.
    echo yt-x exited with an error.
    pause
)
