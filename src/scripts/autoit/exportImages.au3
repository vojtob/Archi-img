#include <MsgBoxConstants.au3>
Local $hWnd = WinWaitActive("Archi - " & $CmdLine[1] & "\src\model\");
Local $imageScale = 100;
Local $projectDir = $CmdLine[1] & "\temp\img_exported";
Sleep(200);

; export ALL
exportItem("#0|#8", "");

; export BA image 
;exportImage("#0|#8|#0|#8", "\01-Business\BA 05 sprava registra");

; export AA image
;exportItem("#0|#8|#1|#3", "\02-Application\AA 00c compoments functions");

; export BA layer
;~ exportLayer("#0|#8|#0", "01-Business");
; export AA layer
;~ exportLayer("#0|#8|#1", "02-Application");

Func exportItem($itemID, $pathName)
	Local $itemCount = ControlTreeView($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]", "GetItemCount", $itemID);
	Local $itemName = ControlTreeView($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]", "GetText", $itemID);
	
	; ignore old views
	If ($itemName == 'xOld') Then
		Return;
	EndIf;

	If ($itemCount > 0) Then
		; process layer
		exportLayer($itemID, $pathName);
	Else
		; process image
		exportImage($itemID, $pathName);
	EndIf;
EndFunc

Func exportLayer($layerID, $layerName)
	If ($layerName <> "" ) Then
		DirCreate($projectDir & $layerName);
	EndIf;
	Local $itemCount = ControlTreeView($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]", "GetItemCount", $layerID);
	For $i = 0 To ($itemCount-1) Step 1
		Local $itemID = $layerID & "|#" & String($i);
		Local $itemName = ControlTreeView($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]", "GetText", $itemID);
		exportItem($itemID, $layerName & '\' & $itemName);
	Next
EndFunc

Func exportImage($itemID, $itemName)
	;MsgBox($MB_SYSTEMMODAL, "Title", "itemID : " & $itemID, 10)
	;MsgBox($MB_SYSTEMMODAL, "Title", "itemName : " & $sText, 10)
	; select item
	ControlFocus($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]");
	ControlTreeView($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]", "Select", $itemID);
	Sleep(200);
	; open view
	Send("{ENTER}");
	Sleep(600);
	; open export dialog
	Send("!fe{UP}{ENTER}");
	; fill export data
	;~ Sleep(2000);
	Send("^a{DEL}");
	Send($projectDir & $itemName & ".png");
	Send("{TAB}{TAB}{HOME} {DOWN} {DOWN} {DOWN}");
	Send("{TAB}" & $imageScale);
	;~ Sleep(2000);
	Send("{ENTER}{ENTER}");
	Sleep(500);
EndFunc