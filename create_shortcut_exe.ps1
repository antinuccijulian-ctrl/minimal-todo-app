$appDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$exe = Join-Path $appDir 'dist\todo.exe'
if (-not (Test-Path $exe)) {
    Write-Error "dist\todo.exe not found at $exe"
    exit 1
}
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'Minimal To-Do (exe).lnk'
$shell = New-Object -ComObject WScript.Shell
$sc = $shell.CreateShortcut($shortcutPath)
$sc.TargetPath = $exe
$sc.WorkingDirectory = $appDir
$icon = Join-Path $appDir 'assets\icon.ico'
if (Test-Path $icon) { $sc.IconLocation = $icon }
$sc.Save()
Write-Output "Created shortcut: $shortcutPath"