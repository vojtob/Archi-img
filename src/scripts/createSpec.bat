@SET PROJECT_DIR=%1
@set SPEC_DIR=%PROJECT_DIR%\temp\spec_local
@set DOCOOL_DIR=%~dp0
@set DOCOOL_DIR=%DOCOOL_DIR:~0,-9%

REM ******** create hugo site for specifikacia
rmdir %SPEC_DIR% /S /Q
hugo new site %SPEC_DIR%

REM ******** copy content
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\src\specifikacia %SPEC_DIR%\content /E

REM ******** Setup theme
@set THEME_NAME=hugo-theme-docdock
mkdir %SPEC_DIR%\themes\%THEME_NAME%
robocopy /np /nfl /njh /njs /ndl /nc /ns %DOCOOL_DIR%\res\themes\%THEME_NAME% %SPEC_DIR%\themes\%THEME_NAME% /E
@set THEME_NAME=onePageHtml
mkdir %SPEC_DIR%\themes\%THEME_NAME%
robocopy /np /nfl /njh /njs /ndl /nc /ns %DOCOOL_DIR%\res\themes\%THEME_NAME% %SPEC_DIR%\themes\%THEME_NAME% /E
copy %PROJECT_DIR%\src\res\hugo-config\configNoTheme.toml %SPEC_DIR%\config.toml
REM copy %PROJECT_DIR%\resources\hugo-config\config.toml %PROJECT_DIR%\temp\specifikacia\config.toml
REM C:\prg\fart\fart %PROJECT_DIR%\temp\specifikacia\config.toml "theme = " "theme = \"%THEME_NAME%\""

REM ******** Copy images to documentation
@set IMG_DIR=%SPEC_DIR%\static\img
mkdir %IMG_DIR%
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\release\img %IMG_DIR% /E /XD memos-temp

call %PROJECT_DIR%\utils\specGenerator.bat %PROJECT_DIR%