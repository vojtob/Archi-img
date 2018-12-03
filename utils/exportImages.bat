SET PROJECT_DIR=%1
mkdir %PROJECT_DIR%\Architecture_temp\exported\01-Business
mkdir %PROJECT_DIR%\Architecture_temp\exported\02-Application
call "C:\Program Files (x86)\AutoIt3\AutoIt3_x64.exe" %~dp0\autoit\exportImages.au3 %PROJECT_DIR%