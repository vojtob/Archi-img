@set PROJECT_DIR=%~dp0
@set PROJECT_DIR=%PROJECT_DIR:~0,-20%
@set SPEC_DIR=%PROJECT_DIR%\release\spec_web

REM ******** export as html documentation
rmdir %SPEC_DIR% /S /Q
mkdir %SPEC_DIR%

hugo -D -s ..\..\release\spec_local\ -t hugo-theme-docdock -d ..\..\release\spec_web -b "http://localhost:8080/cpp/"

REM asi este treba nastavit baseURL = "http://example.org/"
REM %PROJECT_DIR%\Implementation\generateDocs\replace.py %PROJECT_DIR%\temp\docPdf\index.html %PROJECT_DIR%\temp\docPdf\index2.html "img src=\"/" "img src=\"%PROJECT_DIR%\temp\docPdf\\"
