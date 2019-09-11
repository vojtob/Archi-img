@set SRC_DIR=%~dp0
@set SRC_DIR=%SRC_DIR:~0,-7%

mkdir C:\prg\docool

mkdir C:\prg\docool\python
robocopy /np /nfl /njh /njs /ndl /nc /ns %SRC_DIR%\src\python C:\prg\docool\python /E

mkdir C:\prg\docool\scripts
robocopy /np /nfl /njh /njs /ndl /nc /ns %SRC_DIR%\src\scripts C:\prg\docool\scripts /E
mv C:\prg\docool\scripts\docool.bat C:\prg\docool\docool.bat

mkdir C:\prg\docool\res
mkdir C:\prg\docool\res\themes
robocopy /np /nfl /njh /njs /ndl /nc /ns %SRC_DIR%\res\themes C:\prg\docool\res\themes /E
