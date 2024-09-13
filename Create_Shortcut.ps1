::Script to create a WinFunct Shortcut on Desktop with the correct .ico
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path -Path $DesktopPath -ChildPath 'WinFunct.lnk'
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
$Shortcut.Arguments = "-ExecutionPolicy Bypass -NoProfile -Command ""& '$PSScriptRoot\Run.bat'"""
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.IconLocation = "$PSScriptRoot\WinFunct.ico"
$Shortcut.Save()
