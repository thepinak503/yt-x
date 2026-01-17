@echo off
REM ========================================
REM yt-x Windows Installer
REM ========================================
REM This script installs yt-x and all dependencies

setlocal enabledelayedexpansion

REM Check for administrator privileges
echo Checking administrator privileges...
net session >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Running with administrator privileges
) else (
    echo [WARN] Not running as administrator
    echo Some installations may fail
    echo.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo.
echo ========================================
echo yt-x Windows Installer
echo ========================================
echo.

REM Step 1: Install Python 3.10 (minimum stable version)
echo [1/7] Installing Python 3.10...
winget install Python.Python.3.10 --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo [WARN] Python 3.10 installation may have issues
    echo Trying Python 3.11...
    winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements
    if errorlevel 1 (
        echo [ERROR] Failed to install Python
        pause
        exit /b 1
    )
)
echo [OK] Python installed
echo.

REM Step 2: Install yt-dlp
echo [2/7] Installing yt-dlp...
winget install yt-dlp --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo [ERROR] Failed to install yt-dlp
    pause
    exit /b 1
)
echo [OK] yt-dlp installed
echo.

REM Step 3: Install VLC (for m3u8 playlist support)
echo [3/7] Installing VLC...
winget install VideoLAN.VLC --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo [WARN] Failed to install VLC
    echo VLC is recommended but not required
) else (
    echo [OK] VLC installed
)
echo.

REM Step 4: Install mpv (alternative player)
echo [4/7] Installing mpv...
winget install mpv-player.mpv --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo [WARN] Failed to install mpv
    echo mpv is optional but recommended
) else (
    echo [OK] mpv installed
)
echo.

REM Step 5: Refresh environment variables
echo [5/7] Refreshing environment variables...
call refreshenv >nul 2>&1
if errorlevel 1 (
    echo [WARN] Could not refresh environment variables
    echo You may need to restart command prompt
) else (
    echo [OK] Environment variables refreshed
)
echo.

REM Step 6: Install Python dependencies
echo [6/7] Installing Python packages...
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found after installation
    pause
    exit /b 1
)

pip install -q textual rich requests platformdirs
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [OK] Python dependencies installed
echo.

REM Step 7: Install yt-x to PATH
echo [7/7] Installing yt-x to PATH...

REM Determine installation directory
REM Install to C:\Program Files\yt-x (system-wide) or C:\Users\%USERNAME%\AppData\Local\Programs\yt-x (user)
if exist "C:\Program Files\yt-x" (
    set "INSTALL_DIR=C:\Program Files\yt-x"
    set "PATH_TYPE=system"
) else (
    set "INSTALL_DIR=C:\Users\%USERNAME%\AppData\Local\Programs\yt-x"
    set "PATH_TYPE=user"
)

echo Installation directory: !INSTALL_DIR!
echo Installation type: !PATH_TYPE!
echo.

REM Create installation directory
if not exist "!INSTALL_DIR!" mkdir "!INSTALL_DIR!"

REM Copy all files to installation directory
echo Copying files to installation directory...
xcopy /E /I /Y /Q "%~dp0*" "!INSTALL_DIR!" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to copy files
    pause
    exit /b 1
)
echo [OK] Files copied
echo.

REM Create batch file launcher in installation directory
echo Creating launcher...
set "LAUNCHER=!INSTALL_DIR!\yt-x.bat"
(
echo @echo off
echo REM yt-x Launcher
echo.
echo REM Find Python in PATH
echo for %%%%P in ^(python python3^) do ^(
echo     where %%%%P ^>nul 2^>^&1
echo     if !errorlevel! equ 0 ^(
echo         set "PYTHON_CMD=%%%%P"
echo         goto :found
echo     ^)
echo ^)
echo.
echo :found
echo "!LAUNCHER!\!PYTHON_CMD!" "%~dp0yt_x\app.py" %%*
) > "!LAUNCHER!"

REM Add installation directory to PATH
echo Adding yt-x to PATH...

REM For system-wide installation (requires admin)
if "!PATH_TYPE!"=="system" (
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%PATH%;!INSTALL_DIR!" /f
    echo [OK] Added to system PATH
) else (
    REM For user installation
    reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%PATH%;!INSTALL_DIR!" /f
    echo [OK] Added to user PATH
)
echo.

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\yt-x.lnk'); $Shortcut.TargetPath = '!INSTALL_DIR!\yt-x.bat'; $Shortcut.WorkingDirectory = '!INSTALL_DIR!'; $Shortcut.Description = 'YouTube Terminal Browser'; $Shortcut.Save()"
if errorlevel 1 (
    echo [WARN] Failed to create desktop shortcut
) else (
    echo [OK] Desktop shortcut created
)
echo.

REM Create Start Menu shortcut
echo Creating Start Menu shortcut...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs" mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\yt-x.lnk'); $Shortcut.TargetPath = '!INSTALL_DIR!\yt-x.bat'; $Shortcut.WorkingDirectory = '!INSTALL_DIR!'; $Shortcut.Description = 'YouTube Terminal Browser'; $Shortcut.Save()"
if errorlevel 1 (
    echo [WARN] Failed to create Start Menu shortcut
) else (
    echo [OK] Start Menu shortcut created
)
echo.

REM Installation complete
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Installation location: !INSTALL_DIR!
echo Added to PATH: Yes
echo Desktop shortcut: Created
echo Start Menu shortcut: Created
echo.
echo To run yt-x:
echo   1. Restart command prompt (for PATH to take effect)
echo   2. Type: yt-x
echo   3. Or double-click: Desktop\yt-x.lnk
echo.
echo To uninstall yt-x:
echo   1. Delete: !INSTALL_DIR!
echo   2. Remove: Desktop\yt-x.lnk
echo   3. Remove: Start Menu\Programs\yt-x.lnk
echo   4. Remove from PATH (use: PATH editor or System Properties)
echo.

REM Optional: Ask to restart
set /p RESTART="Restart command prompt now? (Y/N): " Y
if /i "%RESTART%"=="Y" (
    echo Restarting...
    cmd /c "exit /b"
)

echo.
echo Installation finished. Press any key to exit...
pause >nul
