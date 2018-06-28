#include <MsgBoxConstants.au3>

Local $hWnd = WinWaitActive("Archi - C:\Users\balintv\OneDrive - Hewlett Packard Enterprise\Projects\MoJ\ORSR\Architecture\model\orsr.archimate");
Sleep(200);

; export BA views
exportLayer(0, "01-Business", "100");
;exportLayer(1, "02-Application", "100");
;exportImage("#0|#8|#1|#0", "02-Application", "100");
;exportImage("#0|#8|#1|#0", "02-Application", "100");
;exportImage("#0|#8|#0|#0", "01-Business", "100");


Func exportLayer($layerIndex, $layerName, $layerScale)
	; 0 - Root | 8 - Views | 0 - 01 BA |
	Local $layerID = "#0|#8|#" &  String($layerIndex);
	;MsgBox($MB_SYSTEMMODAL, "Title", "layerID : " & $layerID, 10)
	Local $itemCount = ControlTreeView($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]", "GetItemCount", $layerID);
	For $i = 0 To ($itemCount-1) Step 1
		Local $itemID = $layerID & "|#" & String($i);
		exportImage($itemID, $layerName, $layerScale);
	Next
EndFunc

Func exportImage($itemID, $layerName, $imageScale)
	;MsgBox($MB_SYSTEMMODAL, "Title", "itemID : " & $itemID, 10)
	Local $sText = ControlTreeView($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]", "GetText", $itemID);
	;MsgBox($MB_SYSTEMMODAL, "Title", "itemName : " & $sText, 10)
	; select item
	ControlFocus($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]");
	ControlTreeView($hWnd, "", "[CLASS:SysTreeView32; INSTANCE:1]", "Select", $itemID);
	Sleep(100);
	; open view
	Send("{ENTER}");
	Sleep(500);
	; open export dialog
	Send("!fe{UP}{ENTER}");
	; fill export data
	Send("^a{DEL}");
	Send("C:\Projects_src\ORSR\Architecture\" & $layerName & "\" & $sText & ".png");
	Send("{TAB}{TAB}{TAB}" & $imageScale);
	Send("{ENTER}{ENTER}");
	Sleep(500);
EndFunc

