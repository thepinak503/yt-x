$ErrorActionPreference = "Stop"

function Write-Status {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Status,
        [Parameter(Mandatory=$false)]
        [string]$Message = ""
    )

    $Color = if ($Status -eq "[OK]") { "Green" } elseif ($Status -eq "[ERROR]") { "Red" } elseif ($Status -eq "[WARN]") { "Yellow" } else { "White" }
    Write-Host "[$Status] $Message" -ForegroundColor $Color
}

function Test-Admin {
    $isAdmin = ([Security.Principal.WindowsPrincipal]::GetCurrentPrincipal().IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
    if ($isAdmin) {
        Write-Status "[OK]" "Running as administrator"
    } else {
        Write-Status "[WARN]" "Not running as administrator - Some installations may fail"
    }
    return $isAdmin
}

function Install-Winget {
    param(
        [string]$PackageId,
        [string]$PackageName
    )

    Write-Host "`n[1/7] Installing $PackageName..."
    try {
        winget install --id $PackageId --accept-package-agreements --silent --override
        Write-Status "[OK]" "$PackageName installed"
        return $true
    }
    catch {
        Write-Status "[ERROR]" "Failed to install $PackageName"
        return $false
    }
}

function Install-PythonPackages {
    Write-Host "`n[5/7] Installing Python packages..."
    try {
        pip install -q textual rich requests platformdirs
        Write-Status "[OK]" "Python packages installed"
        return $true
    }
    catch {
        Write-Status "[ERROR]" "Failed to install Python packages"
        return $false
    }
}

function Create-Shortcuts {
    param([string]$InstallDir)

    Write-Host "`n[8/7] Creating shortcuts..."
    try {
        $desktop = [Environment]::GetFolderPath("Desktop")
        $programs = [Environment]::GetFolderPath("Programs")
        $launcher = Join-Path $InstallDir "yt-x.bat"

        $wsh = New-Object -ComObject WScript.Shell

        $desktopShortcut = $wsh.CreateShortcut((Join-Path $desktop "yt-x.lnk"))
        $desktopShortcut.TargetPath = $launcher
        $desktopShortcut.WorkingDirectory = $InstallDir
        $desktopShortcut.Description = "YouTube Terminal Browser"
        $desktopShortcut.Save()

        $programsShortcut = $wsh.CreateShortcut((Join-Path $programs "yt-x.lnk"))
        $programsShortcut.TargetPath = $launcher
        $programsShortcut.WorkingDirectory = $InstallDir
        $programsShortcut.Description = "YouTube Terminal Browser"
        $programsShortcut.Save()

        Write-Status "[OK]" "Shortcuts created"
        return $true
    }
    catch {
        Write-Status "[ERROR]" "Failed to create shortcuts"
        return $false
    }
}

function Add-ToPath {
    param([string]$InstallDir, [bool]$IsAdmin)

    Write-Host "`n[7/7] Adding to PATH..."
    try {
        if ($IsAdmin) {
            $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
            if ($currentPath -notlike "*$InstallDir*")) {
                [Environment]::SetEnvironmentVariable("Path", "$currentPath;$InstallDir", "Machine")
            }
        } else {
            $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
            if ($currentPath -notlike "*$InstallDir*")) {
                [Environment]::SetEnvironmentVariable("Path", "$currentPath;$InstallDir", "User")
            }
        }
        Write-Status "[OK]" "Added to PATH"
        return $true
    }
    catch {
        Write-Status "[ERROR]" "Failed to add to PATH"
        return $false
    }
}

function Copy-Files {
    param([string]$SourceDir, [string]$TargetDir)

    Write-Host "`n[6/7] Installing yt-x to $TargetDir..."
    try {
        if (-not (Test-Path $TargetDir)) {
            New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
        }

        Copy-Item -Path "$SourceDir\*" -Destination $TargetDir -Recurse -Force | Out-Null
        Write-Status "[OK]" "yt-x installed to $TargetDir"
        return $true
    }
    catch {
        Write-Status "[ERROR]" "Failed to copy files"
        return $false
    }
}

function Create-Launcher {
    param([string]$InstallDir)

    Write-Host "`n[7/7] Creating launcher..."
    try {
        $launcherPath = Join-Path $InstallDir "yt-x.bat"
        $launcherContent = @"
@echo off
setlocal enabledelayedexpansion
for %%%%P in ^(python python3^) do ^(
    where %%%%P ^>nul 2^>^&1
    if !errorlevel! equ 0 ^(
        set PYTHON_CMD=%%%%P
        goto :found
    ^)
^)
:found
"!PYTHON_CMD!" "%SourceDir%\yt_x\app.py" %%*
"@

        Set-Content -Path $launcherPath -Value $launcherContent -Force
        Write-Status "[OK]" "Launcher created"
        return $true
    }
    catch {
        Write-Status "[ERROR]" "Failed to create launcher"
        return $false
    }
}

Main {
    $ErrorActionPreference = "Stop"
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

    Write-Host ""
    Write-Host "========================================"
    Write-Host "  yt-x Windows Installer (PowerShell)"
    Write-Host "========================================"
    Write-Host ""

    Test-Admin
    $isAdmin = [Security.Principal.WindowsPrincipal]::GetCurrentPrincipal().IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

    Write-Host ""
    $success = $true

    Install-Winget "Python.Python.3.10" "Python 3.10"
    $success = $success -and (Install-Winget "yt-dlp" "yt-dlp")
    $success = $success -and (Install-Winget "VideoLAN.VLC" "VLC")
    $success = $success -and (Install-Winget "mpv-player.mpv" "mpv")

    if (-not $success) {
        Write-Status "[ERROR]" "Installation failed"
        Read-Host "Press any key to exit..."
        exit 1
    }

    Write-Host ""
    $success = Install-PythonPackages
    $success = $success -and (Copy-Files $scriptDir $env:LOCALAPPDATA\Programs\yt-x)

    if (-not $success) {
        Write-Status "[ERROR]" "Installation failed"
        Read-Host "Press any key to exit..."
        exit 1
    }

    $installDir = Join-Path $env:LOCALAPPDATA "Programs\yt-x"
    $success = $success -and (Create-Launcher $installDir)
    $success = $success -and (Add-ToPath $installDir $isAdmin)

    if (-not $success) {
        Write-Status "[ERROR]" "Installation failed"
        Read-Host "Press any key to exit..."
        exit 1
    }

    $success = Create-Shortcuts $installDir

    Write-Host ""
    Write-Host "========================================"
    Write-Host "  Installation Complete!"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Location: $installDir"
    Write-Host ""
    Write-Host "To run yt-x:"
    Write-Host "  1. Close and reopen this window"
    Write-Host "  2. Type: yt-x"
    Write-Host ""
    Write-Host "Or use shortcuts:"
    Write-Host "  - Desktop: yt-x"
    Write-Host "  - Start Menu: yt-x"
    Write-Host ""
    Write-Host "To uninstall:"
    Write-Host "  Run: $installDir\uninstall.bat"
    Write-Host ""

    $restart = Read-Host "Restart now? (Y/N): "
    if ($restart -eq "Y" -or $restart -eq "y") {
        Start-Process "cmd.exe" -Argument "/c exit" -Wait
    }
}

Main
