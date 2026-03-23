# TinyTranslate launcher — called by Windows Explorer context menu
# Do not run this directly; use install.ps1 to register it.
param([string]$FilePath)

$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VenvPythonW = Join-Path $ScriptDir '.venv\Scripts\pythonw.exe'
$MainScript  = Join-Path $ScriptDir 'tinytranslate.py'

if (-not (Test-Path $VenvPythonW)) {
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show(
        "TinyTranslate is not installed.`nRun install.ps1 first.",
        "TinyTranslate", "OK", "Error"
    ) | Out-Null
    exit 1
}

& $VenvPythonW $MainScript $FilePath
