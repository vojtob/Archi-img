@set SRC_DIR=%~dp0
@set SRC_DIR=%SRC_DIR:~0,-7%

mkdir C:\prg\docool
robocopy /np /nfl /njh /njs /ndl /nc /ns %SRC_DIR%\src C:\prg\docool /E

mv C:\prg\docool\scripts\docool.bat C:\prg\docool\docool.bat

