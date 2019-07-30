@set PROJECT_DIR=%~dp0
@set PROJECT_DIR=%PROJECT_DIR:~0,-20%

REM ****************************************** 
REM create hugo site for specifikacia
REM rmdir %PROJECT_DIR%\Architecture\specifikacia /S /Q
REM hugo new site %PROJECT_DIR%\Architecture\specifikacia
robocopy /np /nfl /njh /njs /ndl /nc /ns %PROJECT_DIR%\Architecture_src\specifikacia %PROJECT_DIR%\Architecture\specifikacia\content /E

REM Setup theme for hugo
REM @set THEME_DIR=hugo-theme-docdock
REM copy %THEME_DIR%.toml %PROJECT_DIR%\Architecture\specifikacia\config.toml /Y
REM @set THEME_DIR=kraiklyn
REM @set THEME_DIR=kraiklyn
REM mkdir %PROJECT_DIR%\Architecture\specifikacia\themes\%THEME_DIR%
REM robocopy /np /nfl /njh /njs /ndl /nc /ns ..\resources\%THEME_DIR% %PROJECT_DIR%\Architecture\specifikacia\themes\%THEME_DIR% /E
@set THEME_DIR=onePageHtml
rmdir %PROJECT_DIR%\Architecture\specifikacia\themes\%THEME_DIR% /S /Q
mkdir %PROJECT_DIR%\Architecture\specifikacia\themes\%THEME_DIR%
robocopy /np /nfl /njh /njs /ndl /nc /ns ..\resources\%THEME_DIR% %PROJECT_DIR%\Architecture\specifikacia\themes\%THEME_DIR% /E
copy configNoTheme.toml %PROJECT_DIR%\Architecture\specifikacia\config.toml
REM copy configX.toml config.toml
REM mv config.toml %PROJECT_DIR%\Architecture\specifikacia\config.toml
REM C:\prg\fart\fart config.toml "theme = " "theme = \"%THEME_DIR%\""
REM mv config.toml %PROJECT_DIR%\Architecture\specifikacia\config.toml

REM **************
REM Copy & generate architecture images to documentation
REM @set IMG_SRC_DIR=%PROJECT_DIR%\Architecture
REM @set IMG_DIR=%PROJECT_DIR%\Architecture\specifikacia\static\img
REM mkdir %IMG_DIR%
REM robocopy /np /nfl /njh /njs /ndl /nc /ns %IMG_SRC_DIR%\01-Business %IMG_DIR%\01-Business /E
REM robocopy /np /nfl /njh /njs /ndl /nc /ns %IMG_SRC_DIR%\02-Application %IMG_DIR%\02-Application /E

REM Generate icons
REM call generateIcons.bat %PROJECT_DIR%

REM Generate Motivation layer
REM call generateMotivation.bat %PROJECT_DIR%

REM Generate BA
REM call generateBA.bat %PROJECT_DIR%

REM Generate AA
REM call generateAA.bat %PROJECT_DIR%

REM Generate Project doc
REM call generateProjectDoc.bat %PROJECT_DIR%
