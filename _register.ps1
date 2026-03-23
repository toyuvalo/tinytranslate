$ScriptDir  = "C:\Users\toyuv\TinyTranslate"
$VenvPython = "$ScriptDir\.venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Host "ERROR: .venv not found. Run install.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "Rebuilding context menu from installed language packs..." -ForegroundColor Yellow
& $VenvPython "$ScriptDir\core\registry.py"
Write-Host "Done." -ForegroundColor Cyan
