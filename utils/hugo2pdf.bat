@set PROJECT_DIR=%~dp0
@set PROJECT_DIR=%PROJECT_DIR:~0,-20%
@set SPEC_DIR=%PROJECT_DIR%\release\docPdf


REM ******** export as single html
rmdir %SPEC_DIR% /S /Q
mkdir %SPEC_DIR%
hugo -D -s ..\..\release\spec_local\ -t onePageHtml -d ..\docPdf

REM ******** replace references
%PROJECT_DIR%\src\generateDocs\replace.py %SPEC_DIR%\index.html %SPEC_DIR%\index2.html "img src=\"/" "img src=\"%SPEC_DIR%\"

REM ******** generate docx
pandoc %SPEC_DIR%\index2.html -f html -t docx -o %PROJECT_DIR%\release\specifikacia.docx
