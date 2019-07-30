set PROJECT_DIR=%~dp0
set PROJECT_DIR=%PROJECT_DIR:~0,-7%
call C:\Projects_src\Personal\Archi-img\utils\exportImages.bat %PROJECT_DIR%

REM mkdir ..\Architecture_temp\exported\01-Business mkdir ..\Architecture_temp\exported\02-Application call "C:\Program Files (x86)\AutoIt3\AutoIt3_x64.exe" autoit\exportImages.au3