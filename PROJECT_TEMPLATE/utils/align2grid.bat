set PROJECT_DIR=%~dp0
set PROJECT_DIR=%PROJECT_DIR:~0,-7%

REM get last part of path as a project name
set str=%PROJECT_DIR:\= %
for %%A in (%str%) do set PROJECT_NAME=%%A

call C:\Projects_src\Personal\Archi-img\utils\align2grid.bat %PROJECT_DIR% %PROJECT_NAME%