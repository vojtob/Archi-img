@SET PROJECT_DIR=%1
@set SPEC_DIR=%PROJECT_DIR%\temp\spec_local

REM ******** copy content
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\src\Architecture\specifikacia %SPEC_DIR%\content /E

REM ******** Copy images to documentation
@set IMG_DIR=%SPEC_DIR%\static\img
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\Architecture %IMG_DIR% /E

call %PROJECT_DIR%\utils\specGenerator.bat %PROJECT_DIR%