@echo off
REM ========================================
REM yt-x Windows Uninstaller
REM ========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo yt-x Windows Uninstaller
echo ========================================
echo.

REM Find installation directory
set "INSTALL_DIR="

REM Check system-wide installation
if exist "C:\Program Files\yt-x" (
    set "INSTALL_DIR=C:\Program Files\yt-x"
    set "PATH_TYPE=system"
)

REM Check user installation
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\yt-x" (
    set "INSTALL_DIR=C:\Users\%USERNAME%\AppData\Local\Programs\yt-x"
    set "PATH_TYPE=user"
)

if "!INSTALL_DIR!"=="" (
    echo [ERROR] Could not find yt-x installation
    pause
    exit /b 1
)

echo Found installation at: !INSTALL_DIR!
echo.

REM Check for administrator privileges
echo Checking administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARN] Not running as administrator
    echo Cannot remove from PATH without admin privileges
    echo.
    echo You will need to manually remove from PATH:
    echo   !INSTALL_DIR!
    echo.
    set "SKIP_PATH=1"
)

REM Confirm uninstallation
set /p CONFIRM="Uninstall yt-x from !INSTALL_DIR!? (Y/N): " Y
if /i not "%CONFIRM%"=="Y" (
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

REM Step 1: Stop any running yt-x processes
echo [1/4] Stopping yt-x processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq yt-x*" >nul 2>&1
taskkill /F /IM yt-x.exe >nul 2>&1
echo [OK] Processes stopped
echo.

REM Step 2: Remove desktop shortcut
echo [2/4] Removing desktop shortcut...
if exist "%USERPROFILE%\Desktop\yt-x.lnk" (
    del "%USERPROFILE%\Desktop\yt-x.lnk"
    echo [OK] Desktop shortcut removed
) else (
    echo [INFO] Desktop shortcut not found
)
echo.

REM Step 3: Remove Start Menu shortcut
echo [3/4] Removing Start Menu shortcut...
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\yt-x.lnk" (
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\yt-x.lnk"
    echo [OK] Start Menu shortcut removed
) else (
    echo [INFO] Start Menu shortcut not found
)
echo.

REM Step 4: Remove from PATH
echo [4/4] Removing from PATH...
if not "!SKIP_PATH!"=="1" (
    if "!PATH_TYPE!"=="system" (
        REM Remove from system PATH (requires admin)
        for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| findstr /i "INSTALL_DIR"') do (
            reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /f
        )
        echo [OK] Removed from system PATH
    ) else (
        REM Remove from user PATH
        for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path ^| findstr /i "INSTALL_DIR"') do (
            reg delete "HKCU\Environment" /v Path /f
        )
        echo [OK] Removed from user PATH
    )
) else (
    echo [INFO] Skipping PATH removal (no admin)
    echo.
    echo Please manually remove !INSTALL_DIR! from PATH
)
echo.

REM Step 5: Remove installation directory
echo Removing installation directory...
rmdir /S /Q "!INSTALL_DIR!"
if errorlevel 1 (
    echo [ERROR] Failed to remove installation directory
    echo.
    echo Please manually delete: !INSTALL_DIR!
) else (
    echo [OK] Installation directory removed
)
echo.

REM Step 6: Clean up cache and config
set /p CLEAN="Remove cache and configuration files? (Y/N): " N
if /i "%CLEAN%"=="Y" (
    echo Removing cache and config...
    if exist "%APPDATA%\yt-x" (
        rmdir /S /Q "%APPDATA%\yt-x"
        echo [OK] Config removed
    )
    if exist "%LOCALAPPDATA%\yt-x" (
        rmdir /S /Q "%LOCALAPPDATA%\yt-x"
        echo [OK] Cache removed
    )
) else (
    echo [INFO] Cache and config kept
)
echo.

echo ========================================
echo Uninstallation Complete!
echo ========================================
echo.
echo yt-x has been uninstalled.
echo.
echo To complete uninstallation:
echo   1. Restart command prompt (for PATH to take effect)
echo   2. Optional: Uninstall Python, yt-dlp, VLC if not needed
echo.

pause
