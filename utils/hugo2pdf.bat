@SET PROJECT_DIR=%1
@SET PROJECT_NAME=%~n1
@set DOCOOL_DIR=%~dp0
@set DOCOOL_DIR=%DOCOOL_DIR:~0,-7%

@set SPEC_DIR=%PROJECT_DIR%\temp\docPdf
rmdir %SPEC_DIR% /S /Q
mkdir %SPEC_DIR%
mkdir %PROJECT_DIR%\release

REM ******** export as single html
hugo -D -s ..\temp\spec_local\ -t onePageHtml -d ..\docPdf -b "%SPEC_DIR%"

REM ******** generate docx
pandoc %SPEC_DIR%\index.html -f html -t docx -o %PROJECT_DIR%\release\%PROJECT_NAME%.docx --verbose
