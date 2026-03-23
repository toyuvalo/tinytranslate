# TinyTranslate uninstaller — removes context menu entries and shortcuts from HKCU
$MenuName = "TinyTranslate"

Write-Host ""
Write-Host "TinyTranslate Uninstaller" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# ---- Context menu entries ---------------------------------------------------
foreach ($ext in @('.txt', '.docx', '.pdf')) {
    $Key = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\$MenuName"
    if (Test-Path $Key) {
        Remove-Item -Path $Key -Recurse -Force
        Write-Host "[OK] Removed context menu for $ext" -ForegroundColor Green
    } else {
        Write-Host "[--] Not found: $ext" -ForegroundColor Gray
    }
}

# ---- Desktop shortcut -------------------------------------------------------
$WshShell   = New-Object -ComObject WScript.Shell
$DesktopLnk = Join-Path $WshShell.SpecialFolders("Desktop") "TinyTranslate.lnk"
$StartLnk   = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\TinyTranslate.lnk'

foreach ($lnk in @($DesktopLnk, $StartLnk)) {
    if (Test-Path $lnk) {
        Remove-Item $lnk -Force
        Write-Host "[OK] Removed shortcut: $(Split-Path $lnk -Leaf)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "TinyTranslate context menu and shortcuts removed." -ForegroundColor Cyan
Write-Host ""
Write-Host "  Your config.json and .venv folder were left intact." -ForegroundColor Gray
Write-Host "  Delete the TinyTranslate folder to fully remove the tool." -ForegroundColor Gray
Write-Host "  Language models remain in: $env:LOCALAPPDATA\argos-translate" -ForegroundColor Gray
Write-Host "  To remove them: delete that folder manually." -ForegroundColor Gray
Write-Host ""
