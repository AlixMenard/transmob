Set WshShell = CreateObject("WScript.Shell")
DesktopPath = WshShell.SpecialFolders("Desktop")
ShortcutPath = DesktopPath & "\Start IA.lnk"

' Check if the shortcut already exists
If Not CreateObject("Scripting.FileSystemObject").FileExists(ShortcutPath) Then
    ' Create a shortcut on the desktop
    Set Shortcut = WshShell.CreateShortcut(ShortcutPath)
    Shortcut.TargetPath = WScript.ScriptFullName
    Shortcut.WorkingDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
    Shortcut.WindowStyle = 1
    Shortcut.Description = "Shortcut to start GUI with auto-update"
    Shortcut.Save
End If

' Run the batch file in hidden mode
WshShell.Run chr(34) & "execution.bat" & Chr(34), 1
Set WshShell = Nothing