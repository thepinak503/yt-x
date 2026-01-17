@echo off
setlocal enabledelayedexpansion
set "ECHO_STATE=ON"

REM Check for administrator privileges
reg query "HKU\S-1-5-21" >nul 2>&1
if %errorLevel% equ 0 (
    set "IS_ADMIN=1"
) else (
    set "IS_ADMIN=0"
)

REM Step 1: Install Python
echo.
echo [1/7] Installing Python 3.10...
winget install --id Python.Python.3.10 --accept-package-agreements --silent 2>nul || (
    winget install --id Python.Python.3.11 --accept-package-agreements --silent 2>nul
)
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install Python
    pause
    exit /b 1
)
echo [OK] Python installed
echo.

REM Step 2: Install yt-dlp
echo [2/7] Installing yt-dlp...
winget install --id yt-dlp --accept-package-agreements --silent 2>nul
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install yt-dlp
    pause
    exit /b 1
)
echo [OK] yt-dlp installed
echo.

REM Step 3: Install VLC
echo [3/7] Installing VLC...
winget install --id VideoLAN.VLC --accept-package-agreements --silent 2>nul
if %errorLevel% neq 0 (
    echo [WARN] VLC installation failed (optional)
) else (
    echo [OK] VLC installed
)
echo.

REM Step 4: Install mpv
echo [4/7] Installing mpv...
winget install --id mpv-player.mpv --accept-package-agreements --silent 2>nul
if %errorLevel% neq 0 (
    echo [WARN] mpv installation failed (optional)
) else (
    echo [OK] mpv installed
)
echo.

REM Step 5: Install Python packages
echo [5/7] Installing Python packages...
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)
pip install -q textual rich requests platformdirs 2>nul
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install Python packages
    pause
    exit /b 1
)
echo [OK] Python packages installed
echo.

REM Step 6: Install yt-x
echo [6/7] Installing yt-x...

if "%IS_ADMIN%"=="1" (
    set "INSTALL_DIR=C:\Program Files\yt-x"
) else (
    set "INSTALL_DIR=%LOCALAPPDATA%\Programs\yt-x"
)

if not exist "!INSTALL_DIR!" mkdir "!INSTALL_DIR!" 2>nul
xcopy /E /I /Y /Q "%~dp0*" "!INSTALL_DIR!" 2>nul
if %errorLevel% neq 0 (
    echo [ERROR] Failed to copy files
    pause
    exit /b 1
)
echo [OK] yt-x installed to !INSTALL_DIR!
echo.

REM Step 7: Create launcher
echo [7/7] Creating launcher...
(
    echo @echo off
    echo setlocal enabledelayedexpansion
    echo for %%%%P in ^(python python3^) do ^(
    echo     where %%%%P ^>nul 2^>^&1
    echo     if !errorlevel! equ 0 ^(
    echo         set PYTHON_CMD=%%%%P
    echo         goto :found
    echo     ^)
    echo ^)
    echo :found
    echo "!PYTHON_CMD!" "%~dp0yt_x\app.py" %%*
) > "!INSTALL_DIR!\yt-x.bat"
echo [OK] Launcher created
echo.

REM Step 8: Add to PATH
echo [8/7] Adding to PATH...

if "%IS_ADMIN%"=="1" (
    for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul ^| findstr /i "INSTALL_DIR"') do (
        reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /f 2>nul
    )
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%PATH%;!INSTALL_DIR!" /f 2>nul
    echo [OK] Added to system PATH
) else (
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul ^| findstr /i "INSTALL_DIR"') do (
        reg delete "HKCU\Environment" /v Path /f 2>nul
    )
    reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%PATH%;!INSTALL_DIR!" /f 2>nul
    echo [OK] Added to user PATH
)
echo.

REM Step 9: Create shortcuts
echo [9/7] Creating shortcuts...
powershell -NoProfile -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\yt-x.lnk'); $Shortcut.TargetPath = '!INSTALL_DIR!\yt-x.bat'; $Shortcut.WorkingDirectory = '!INSTALL_DIR!'; $Shortcut.Description = 'YouTube Terminal Browser'; $Shortcut.Save()" 2>nul
powershell -NoProfile -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Programs') + '\yt-x.lnk'); $Shortcut.TargetPath = '!INSTALL_DIR!\yt-x.bat'; $Shortcut.WorkingDirectory = '!INSTALL_DIR!'; $Shortcut.Description = 'YouTube Terminal Browser'; $Shortcut.Save()" 2>nul
echo [OK] Shortcuts created
echo.

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Location: !INSTALL_DIR!
echo.
echo To run yt-x:
echo   1. Close and reopen this window
echo   2. Type: yt-x
echo.
echo Or use shortcuts:
echo   - Desktop: yt-x
echo   - Start Menu: yt-x
echo.
echo To uninstall:
echo   Run: !INSTALL_DIR!\uninstall.bat
echo.
pause
