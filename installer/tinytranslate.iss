; TinyTranslate installer — registers HKCU shell-menu context actions (no admin required).
; Build with: ISCC.exe /DMyAppVersion=1.0.2 installer\tinytranslate.iss
; Requires dist\TinyTranslate.exe and dist\TinyTranslateSettings.exe already built by PyInstaller.

#ifndef MyAppVersion
  #define MyAppVersion "1.0.2"
#endif

#define MyAppName "TinyTranslate"
#define MyAppPublisher "dvlce.ca"
#define MyAppURL "https://github.com/dvlce/tinytranslate"
#define MyAppExeName "TinyTranslate.exe"
#define MyAppSettingsExe "TinyTranslateSettings.exe"

[Setup]
AppId={{7A2E1D6B-4C3F-4F52-9D64-7F3A0E8B2C11}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=TinyTranslate-Setup
OutputDir=.
SetupIconFile=..\assets\icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\{#MyAppSettingsExe}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\assets\icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\TinyTranslate Settings"; Filename: "{app}\{#MyAppSettingsExe}"; IconFilename: "{app}\assets\icon.ico"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\TinyTranslate Settings"; Filename: "{app}\{#MyAppSettingsExe}"; IconFilename: "{app}\assets\icon.ico"; Tasks: desktopicon

[Registry]
; Right-click menu for .txt
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.txt\shell\TinyTranslate"; ValueType: string; ValueName: ""; ValueData: "Translate with TinyTranslate"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.txt\shell\TinyTranslate"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.txt\shell\TinyTranslate\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

; Right-click menu for .docx
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.docx\shell\TinyTranslate"; ValueType: string; ValueName: ""; ValueData: "Translate with TinyTranslate"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.docx\shell\TinyTranslate"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.docx\shell\TinyTranslate\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

; Right-click menu for .pdf
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.pdf\shell\TinyTranslate"; ValueType: string; ValueName: ""; ValueData: "Translate with TinyTranslate"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.pdf\shell\TinyTranslate"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\.pdf\shell\TinyTranslate\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Run]
Filename: "{app}\{#MyAppSettingsExe}"; Description: "Open TinyTranslate Settings"; Flags: nowait postinstall skipifsilent
