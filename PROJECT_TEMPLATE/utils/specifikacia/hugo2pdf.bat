@set PROJECT_DIR=%~dp0
@set PROJECT_DIR=%PROJECT_DIR:~0,-20%

REM ******** export as single html
rmdir %PROJECT_DIR%\temp\docPdf /S /Q
mkdir %PROJECT_DIR%\temp\docPdf
hugo -D -s ..\..\temp\specifikacia\ -t onePageHtml -d ..\docPdf

REM ******** replace references
%PROJECT_DIR%\Implementation\generateDocs\replace.py %PROJECT_DIR%\temp\docPdf\index.html %PROJECT_DIR%\temp\docPdf\index2.html "img src=\"/" "img src=\"%PROJECT_DIR%\temp\docPdf\\"

REM ******** generate docx
pandoc %PROJECT_DIR%\temp\docPdf\index2.html -f html -t docx -o %PROJECT_DIR%\release\cpp.docx
