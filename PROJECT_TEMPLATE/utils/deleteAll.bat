set PROJECT_DIR=%~dp0
set PROJECT_DIR=%PROJECT_DIR:~0,-7%
call C:\Projects_src\Personal\Archi-img\utils\deleteAll.bat %PROJECT_DIR%
del %PROJECT_DIR%\release\*.*

REM rmdir ..\Architecture_temp /s/q  rmdir ..\Architecture /s/q