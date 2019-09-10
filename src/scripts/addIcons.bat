SET PROJECT_DIR=%1
mkdir %PROJECT_DIR%\release
mkdir %PROJECT_DIR%\release\img
call node %~dp0\..\lines.js %PROJECT_DIR%