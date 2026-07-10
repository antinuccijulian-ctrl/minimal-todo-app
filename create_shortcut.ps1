$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$target = Join-Path $scriptPath "run_todo.bat"
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Minimal To-Do.lnk"

if (-not (Test-Path $target)) {
    Write-Error "Target not found: $target. Ensure run_todo.bat is in the same folder as this script."
    exit 1
}

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = $scriptPath
$icon = Join-Path $scriptPath "assets\icon.ico"
if (Test-Path $icon) { $shortcut.IconLocation = $icon }
$shortcut.Save()

Write-Output "Shortcut created at: $shortcutPath"