; Inno Setup Script for NARONG CCTV TEAM - Camera Monitor
; Creates a professional Windows installer with proper update handling

#define MyAppName "NARONG CCTV TEAM - Camera Monitor"
#define MyAppVersion "8.1.0"
#define MyAppPublisher "NARONG CCTV TEAM"
#define MyAppURL "https://github.com/chhany007/narong-cctv-team"
#define MyAppExeName "NARONG_CCTV_TEAM.exe"

[Setup]
; App identification
AppId={{A1B2C3D4-E5F6-4A5B-8C7D-9E0F1A2B3C4D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation paths
DefaultDirName={autopf}\{#MyAppPublisher}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=installer_output
OutputBaseFilename=NARONG_CCTV_Team_Setup_v{#MyAppVersion}
SetupIconFile=sky-tech logo.png
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Version info
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoCopyright=Copyright (C) 2025 {#MyAppPublisher}

; Uninstall
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; UI
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Data files (preserve if already exists)
Source: "ip.xlsx"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "sky-tech logo.png"; DestDir: "{app}"; Flags: ignoreversion

; Configuration (preserve user data)
Source: "version_config.json"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "UPDATE_SYSTEM_README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion

; NOTE: Don't use "Flags: ignoreversion" on files you want to preserve during updates:
; - camera_monitor.log
; - check_history.json
; - creds_*.json
; - exported_cameras.csv
; These will be automatically preserved

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop icon (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Quick Launch (optional)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Option to launch after install
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up generated files on uninstall (but preserve user data by default)
Type: files; Name: "{app}\camera_monitor.log"
Type: files; Name: "{app}\*.pyc"
Type: files; Name: "{app}\*.pyo"

[Code]
/////////////////////////////////////////////////////////////////////
// Custom code for update handling
/////////////////////////////////////////////////////////////////////

function IsAppRunning(): Boolean;
var
  WMI, WMIService, ObjectSet, Instance: Variant;
  ExeName: String;
begin
  Result := False;
  ExeName := '{#MyAppExeName}';
  
  try
    WMI := CreateOleObject('WbemScripting.SWbemLocator');
    WMIService := WMI.ConnectServer('', 'root\CIMV2');
    ObjectSet := WMIService.ExecQuery('SELECT * FROM Win32_Process WHERE Name="' + ExeName + '"');
    Result := ObjectSet.Count > 0;
  except
    // If WMI fails, assume not running
    Result := False;
  end;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // Check if app is running
  if IsAppRunning() then
  begin
    if MsgBox('The application is currently running.' + #13#10 + 
              'Please close it before continuing.' + #13#10 + #13#10 +
              'Do you want to close it now?', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Try to close the app gracefully
      // User should close it manually
      MsgBox('Please close the application and click OK to continue.', mbInformation, MB_OK);
      
      // Check again
      if IsAppRunning() then
      begin
        MsgBox('The application is still running. Installation cannot continue.', mbError, MB_OK);
        Result := False;
      end;
    end
    else
    begin
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  UserDataDir: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Create AppData directory for user data
    UserDataDir := ExpandConstant('{userappdata}\{#MyAppPublisher}');
    if not DirExists(UserDataDir) then
      CreateDir(UserDataDir);
      
    // Add registry entry for updates
    RegWriteStringValue(HKLM, 'Software\{#MyAppPublisher}\{#MyAppName}', 'InstallPath', ExpandConstant('{app}'));
    RegWriteStringValue(HKLM, 'Software\{#MyAppPublisher}\{#MyAppName}', 'Version', '{#MyAppVersion}');
    RegWriteStringValue(HKLM, 'Software\{#MyAppPublisher}\{#MyAppName}', 'InstallDate', GetDateTimeString('yyyy-mm-dd', #0, #0));
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  NeedsRestart := False;
  
  // Check if this is an update
  if FileExists(ExpandConstant('{app}\{#MyAppExeName}')) then
  begin
    // This is an update - preserve user data
    Log('Detected existing installation - performing update');
  end
  else
  begin
    // Fresh install
    Log('Fresh installation detected');
  end;
end;

[Messages]
WelcomeLabel1=Welcome to the [name] Setup Wizard
WelcomeLabel2=This will install [name/ver] on your computer.%n%nAll your existing data and settings will be preserved during the update.
FinishedHeadingLabel=Completing the [name] Setup Wizard
FinishedLabel=The application has been installed on your computer.%n%nYou can now launch [name] from the Start Menu or Desktop.
