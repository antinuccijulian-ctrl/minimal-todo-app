$appDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$oneDirExe = Join-Path $appDir 'dist\todo\todo.exe'
$singleExe = Join-Path $appDir 'dist\todo.exe'
if (Test-Path $oneDirExe) {
    $exe = $oneDirExe
} elseif (Test-Path $singleExe) {
    $exe = $singleExe
} else {
    Write-Error "No executable found. Build with 'pyinstaller todo.spec' or create dist\todo.exe."
    exit 1
}
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'Minimal To-Do (new note).lnk'
$shell = New-Object -ComObject WScript.Shell
$sc = $shell.CreateShortcut($shortcutPath)
$sc.TargetPath = $exe
$sc.Arguments = '--new'
$sc.WorkingDirectory = $appDir
$sc.Hotkey = 'Ctrl+Alt+N'
$icon = Join-Path $appDir 'assets\icon.ico'
if (Test-Path $icon) { $sc.IconLocation = $icon }
$sc.Save()
Write-Output "Created shortcut: $shortcutPath"