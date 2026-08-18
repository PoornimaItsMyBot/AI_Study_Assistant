#define MyAppName "AI Study Assistant"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "ItsMyBot"
#define MyAppExeName "AI_Study_Asst.exe"

[Setup]
AppId={{AI-STUDY-ASSISTANT-V2}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\AI Study Assistant
DefaultGroupName=AI Study Assistant

OutputDir=.
OutputBaseFilename=AI_Study_Asst_Setup_v2.0.0

SetupIconFile=..\app.ico

Compression=lzma
SolidCompression=yes

WizardStyle=modern

[Files]
Source: "..\AI_Study_Assistant_v2.0\AI_Study_Asst.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\AI Study Assistant"; Filename: "{app}\AI_Study_Asst.exe"
Name: "{autodesktop}\AI Study Assistant"; Filename: "{app}\AI_Study_Asst.exe"

[Run]
Filename: "{app}\AI_Study_Asst.exe"; Description: "Launch AI Study Assistant"; Flags: nowait postinstall skipifsilent