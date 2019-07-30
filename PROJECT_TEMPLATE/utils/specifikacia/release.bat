@set PROJECT_DIR=%~dp0
@set PROJECT_DIR=%PROJECT_DIR:~0,-20%

REM ******** create hugo site for specifikacia
rmdir %PROJECT_DIR%\temp\specifikacia /S /Q
hugo new site %PROJECT_DIR%\temp\specifikacia

REM ******** copy content
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\Architecture_src\specifikacia %PROJECT_DIR%\temp\specifikacia\content /E

REM ******** Setup theme
@set THEME_NAME=hugo-theme-docdock
mkdir %PROJECT_DIR%\temp\specifikacia\themes\%THEME_NAME%
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\resources\themes\%THEME_NAME% %PROJECT_DIR%\temp\specifikacia\themes\%THEME_NAME% /E
@set THEME_NAME=onePageHtml
mkdir %PROJECT_DIR%\temp\specifikacia\themes\%THEME_NAME%
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\resources\themes\%THEME_NAME% %PROJECT_DIR%\temp\specifikacia\themes\%THEME_NAME% /E
copy %PROJECT_DIR%\resources\hugo-config\configNoTheme.toml %PROJECT_DIR%\temp\specifikacia\config.toml
REM copy %PROJECT_DIR%\resources\hugo-config\config.toml %PROJECT_DIR%\temp\specifikacia\config.toml
REM C:\prg\fart\fart %PROJECT_DIR%\temp\specifikacia\config.toml "theme = " "theme = \"%THEME_NAME%\""

REM ******** Copy & generate architecture images to documentation
@set IMG_SRC_DIR=%PROJECT_DIR%\Architecture
@set IMG_DIR=%PROJECT_DIR%\temp\specifikacia\static\img
mkdir %IMG_DIR%
robocopy /np /nfl /njh /njs /ndl /nc /ns %IMG_SRC_DIR%\01-Business %IMG_DIR%\01-Business /E
robocopy /np /nfl /njh /njs /ndl /nc /ns %IMG_SRC_DIR%\02-Application %IMG_DIR%\02-Application /E

REM ******** Generate icons
call %PROJECT_DIR%\utils\specifikacia\generateIcons.bat %PROJECT_DIR%

REM Generate Motivation layer
REM call generateMotivation.bat %PROJECT_DIR%

REM Generate BA
REM call generateBA.bat %PROJECT_DIR%

REM Generate AA
REM call generateAA.bat %PROJECT_DIR%

REM Generate Project doc
REM call generateProjectDoc.bat %PROJECT_DIR%
