@SET PROJECT_DIR=%1
@set SPEC_DIR=%PROJECT_DIR%\temp\spec_local

REM ******** copy content
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\src\specifikacia %SPEC_DIR%\content /E

REM ******** Copy images to documentation
@set IMG_DIR=%SPEC_DIR%\static\img
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\release\img %IMG_DIR% /E