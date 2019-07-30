#include <MsgBoxConstants.au3>

;Local $hWnd = WinWaitActive("Archi - " & $CmdLine[1] & "\Architecture_src\model\");
Local $hWnd = WinWaitActive("[CLASS:VirtualConsoleClass]");
Local $projectDir = $CmdLine[1];
Sleep(500);

; setup utils tab
Send("cd " & $projectDir & "\utils\{ENTER}");
Sleep(200);
Send("{F2}utils{ENTER}");
Sleep(200);

; setup specifikacia tab
Send("^t");
Sleep(500);
Send("{TAB}" & $projectDir & "\utils\specifikacia{ENTER}");
Sleep(1000);
Send("{F2}specifikacia{ENTER}");
