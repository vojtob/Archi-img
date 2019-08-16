@SET PROJECT_DIR=%1
@SET PROJECT_NAME=%~n1
@set DOCOOL_DIR=%~dp0
@set DOCOOL_DIR=%DOCOOL_DIR:~0,-7%

rmdir %PROJECT_DIR%\release\spec_web /S /Q
mkdir %PROJECT_DIR%\release\spec_web\%PROJECT_NAME%

REM ******** export as html documentation
if "%~2"=="" goto DEFAULT_URL
@SET DEST_PATH=%~2
:GENERATEWEB
@SET DEST_PATH=%DEST_PATH%/%PROJECT_NAME%/
hugo -D -s ..\temp\spec_local\ -t hugo-theme-docdock -d ..\..\release\spec_web\%PROJECT_NAME% -b "%DEST_PATH%"

GOTO DONE

:DEFAULT_URL
@SET DEST_PATH=http://localhost:8080
GOTO GENERATEWEB

:DONE