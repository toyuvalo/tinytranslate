# TinyTranslate installer
# Registers right-click context menu for .txt, .docx, .pdf
# No admin required — uses HKCU registry.
# Run once after cloning: powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host ""
Write-Host "TinyTranslate Installer" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan
Write-Host ""

# ---- 1. Python check ---------------------------------------------------------
$PythonExe = $null
foreach ($candidate in @('python', 'python3', 'py')) {
    try {
        $ver = & $candidate --version 2>&1
        if ($ver -match 'Python 3\.[89]|Python 3\.1[0-9]') {
            $PythonExe = $candidate; break
        }
    } catch {}
}
if (-not $PythonExe) {
    Write-Host "ERROR: Python 3.8+ not found." -ForegroundColor Red
    Write-Host "       Install from https://python.org and re-run this script." -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Python: $PythonExe" -ForegroundColor Green

# ---- 2. Create virtualenv ---------------------------------------------------
$VenvDir     = Join-Path $ScriptDir '.venv'
$VenvPython  = Join-Path $VenvDir 'Scripts\python.exe'
$VenvPythonW = Join-Path $VenvDir 'Scripts\pythonw.exe'

if (-not (Test-Path $VenvPython)) {
    Write-Host "[..] Creating virtual environment..." -ForegroundColor Yellow
    & $PythonExe -m venv $VenvDir
    Write-Host "[OK] Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment exists." -ForegroundColor Green
}

# ---- 3. Install dependencies ------------------------------------------------
Write-Host "[..] Installing Python dependencies (first run may take a minute)..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip --quiet
& $VenvPython -m pip install -r (Join-Path $ScriptDir 'requirements.txt') --quiet
Write-Host "[OK] Dependencies installed." -ForegroundColor Green

# ---- 4. Language pack -------------------------------------------------------
Write-Host ""
Write-Host "  Default translation: English → French (EN→FR, ~100 MB one-time download)" -ForegroundColor White
Write-Host "  More languages can be installed from the Settings window later." -ForegroundColor Gray
Write-Host ""
$dl = Read-Host "  Download EN→FR language pack now? [Y/n]"
if ($dl -ne 'n' -and $dl -ne 'N') {
    Write-Host "[..] Downloading EN→FR language pack (~100 MB)..." -ForegroundColor Yellow
    & $VenvPython (Join-Path $ScriptDir 'download_model.py') en fr
    Write-Host "[OK] Language pack installed." -ForegroundColor Green
} else {
    Write-Host "[--] Skipped. Open TinyTranslate Settings to install packs later." -ForegroundColor Gray
}

# ---- 5. Generate icon -------------------------------------------------------
Write-Host "[..] Generating icon..." -ForegroundColor Yellow
& $VenvPython (Join-Path $ScriptDir 'make_icon.py')
$IconPath = Join-Path $ScriptDir 'assets\icon.ico'
Write-Host "[OK] Icon: $IconPath" -ForegroundColor Green

# ---- 6. Register context menu (HKCU, no admin) ------------------------------
$PsScript  = Join-Path $ScriptDir 'tinytranslate.ps1'
$MenuName  = "TinyTranslate"
$MenuLabel = "Translate with TinyTranslate"
$Command   = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PsScript`" `"%1`""

foreach ($ext in @('.txt', '.docx', '.pdf')) {
    $Key = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\$MenuName"
    if (-not (Test-Path $Key)) { New-Item -Path $Key -Force | Out-Null }
    Set-ItemProperty -Path $Key -Name '(Default)' -Value $MenuLabel
    Set-ItemProperty -Path $Key -Name 'Icon'      -Value $IconPath

    $CmdKey = "$Key\command"
    if (-not (Test-Path $CmdKey)) { New-Item -Path $CmdKey -Force | Out-Null }
    Set-ItemProperty -Path $CmdKey -Name '(Default)' -Value $Command
}
Write-Host "[OK] Context menu registered for .txt, .docx, .pdf" -ForegroundColor Green

# ---- 7. Write config.json ---------------------------------------------------
$ConfigPath  = Join-Path $ScriptDir 'config.json'
$ExamplePath = Join-Path $ScriptDir 'config.json.example'
if (-not (Test-Path $ConfigPath)) {
    Copy-Item $ExamplePath $ConfigPath
    Write-Host "[OK] config.json created from example." -ForegroundColor Green
} else {
    Write-Host "[OK] config.json already exists." -ForegroundColor Green
}

# ---- 8. Desktop shortcut ----------------------------------------------------
$SettingsScript = Join-Path $ScriptDir 'settings.py'
$WshShell       = New-Object -ComObject WScript.Shell
$DesktopPath    = $WshShell.SpecialFolders("Desktop")

$DeskLnk = $WshShell.CreateShortcut("$DesktopPath\TinyTranslate.lnk")
$DeskLnk.TargetPath       = $VenvPythonW
$DeskLnk.Arguments        = "`"$SettingsScript`""
$DeskLnk.WorkingDirectory = $ScriptDir
$DeskLnk.IconLocation     = "$IconPath,0"
$DeskLnk.Description      = "TinyTranslate Settings"
$DeskLnk.Save()
Write-Host "[OK] Desktop shortcut created." -ForegroundColor Green

# ---- 9. Start Menu shortcut -------------------------------------------------
$StartMenuDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'
$StartLnk     = $WshShell.CreateShortcut("$StartMenuDir\TinyTranslate.lnk")
$StartLnk.TargetPath       = $VenvPythonW
$StartLnk.Arguments        = "`"$SettingsScript`""
$StartLnk.WorkingDirectory = $ScriptDir
$StartLnk.IconLocation     = "$IconPath,0"
$StartLnk.Description      = "TinyTranslate Settings"
$StartLnk.Save()
Write-Host "[OK] Start menu shortcut created." -ForegroundColor Green

# ---- Done -------------------------------------------------------------------
Write-Host ""
Write-Host "All done!" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Right-click any .txt, .docx, or .pdf" -ForegroundColor White
Write-Host "  → 'Translate with TinyTranslate'" -ForegroundColor White
Write-Host ""
Write-Host "  Config:   $ConfigPath" -ForegroundColor Gray
Write-Host "  Settings: Double-click TinyTranslate on your Desktop" -ForegroundColor Gray
Write-Host "  Disk use: ~100 MB (EN→FR pack) + ~50 MB (.venv)" -ForegroundColor Gray
Write-Host ""
