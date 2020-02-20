@SET PROJECT_DIR=%1
@set SPEC_DIR=%PROJECT_DIR%\temp\spec_local
@set DOCOOL_DIR=%~dp0
@set DOCOOL_DIR=%DOCOOL_DIR:~0,-9%

call %PROJECT_DIR%\utils\specGenerator.bat %PROJECT_DIR%