@set PROJECT_DIR=%~dp0
@set PROJECT_DIR=%PROJECT_DIR:~0,-20%

REM ******** export as html documentation
rmdir %PROJECT_DIR%\release\spec /S /Q
mkdir %PROJECT_DIR%\release\spec
hugo -D -s ..\..\temp\specifikacia\ -t hugo-theme-docdock -d ..\..\release\spec -b "http://localhost:8080/cpp/"

REM asi este treba nastavit baseURL = "http://example.org/"
REM %PROJECT_DIR%\Implementation\generateDocs\replace.py %PROJECT_DIR%\temp\docPdf\index.html %PROJECT_DIR%\temp\docPdf\index2.html "img src=\"/" "img src=\"%PROJECT_DIR%\temp\docPdf\\"
