Write-Host "=== Registry ===" -ForegroundColor Cyan
foreach ($ext in @('.txt', '.docx', '.pdf')) {
    $base = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\TinyTranslate"
    if (-not (Test-Path $base)) { Write-Host "[MISSING] $ext top-level key" -ForegroundColor Red; continue }

    $muiverb = (Get-ItemPropertyValue $base 'MUIVerb' -ErrorAction SilentlyContinue)
    Write-Host "[OK] $ext  MUIVerb='$muiverb'" -ForegroundColor Green

    $shellBase = "$base\shell"
    if (Test-Path $shellBase) {
        foreach ($langKey in (Get-ChildItem $shellBase)) {
            $code    = $langKey.PSChildName
            $cmdPath = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\TinyTranslate\shell\$code\command"
            if (Test-Path $cmdPath) {
                $cmd = (Get-ItemPropertyValue $cmdPath '(Default)')
                Write-Host "    $code -> $cmd" -ForegroundColor DarkGreen
            } else {
                Write-Host "    $code -> [NO COMMAND KEY]" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "  [MISSING] shell subkeys" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Files ===" -ForegroundColor Cyan
@(
    "C:\Users\toyuv\TinyTranslate\.venv\Scripts\pythonw.exe",
    "C:\Users\toyuv\TinyTranslate\tinytranslate.py",
    "C:\Users\toyuv\TinyTranslate\assets\icon.ico",
    "C:\Users\toyuv\TinyTranslate\config.json"
) | ForEach-Object {
    if (Test-Path $_) { Write-Host "[OK] $_" -ForegroundColor Green }
    else              { Write-Host "[MISSING] $_" -ForegroundColor Red }
}

Write-Host ""
Write-Host "=== Argos model ===" -ForegroundColor Cyan
& "C:\Users\toyuv\TinyTranslate\.venv\Scripts\python.exe" -c "
from argostranslate import translate
pairs = [(l.code, t.to_lang.code) for l in translate.get_installed_languages() for t in l.translations_from if t.to_lang.code != l.code]
print('Installed pairs:', pairs if pairs else 'NONE')
"
