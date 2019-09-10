SET PROJECT_DIR=%1
mkdir %PROJECT_DIR%\Architecture_temp\resources
mkdir %PROJECT_DIR%\Architecture_temp\resources\icons
mkdir %PROJECT_DIR%\Architecture\resources
xcopy %PROJECT_DIR%\Architecture_temp\resources %PROJECT_DIR%\Architecture\resources /S /Y 