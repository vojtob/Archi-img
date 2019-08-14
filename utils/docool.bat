@ECHO OFF

if "%~1"=="" goto ERROR

set PROJECT_DIR=%~1
ECHO DOCumentation TOOLs run for project %PROJECT_DIR%
ECHO.

if "%~2"=="" goto BLANK
IF "%~2"=="archi" GOTO ARCHI
IF "%~2"=="icons" GOTO ICONS
IF "%~2"=="mm" GOTO MERMAID
IF "%~2"=="spec" GOTO SPECIFICATION
IF "%~2"=="clean" GOTO DELETE_GENERATED
IF "%~2"=="hugo2pdf" GOTO HUGO2PDF
IF "%~2"=="hugo2web" GOTO HUGO2WEB

ECHO Unknown parameter
GOTO BLANK

:BLANK

ECHO Usage: docool command
ECHO.      
ECHO commands:
ECHO    archi    - export images from archi model to png
ECHO    icons    - add icons to images
ECHO    mm       - generate mermaid images
ECHO    spec     - create specification
ECHO    hugo2pdf - generate pdf version of specification
ECHO    hugo2pdf - generate web version of specification, could be deployed anywhere
ECHO    clean    - delete all generated files
ECHO.

GOTO DONE

:ARCHI
ECHO Generate images from archimate model, swith to archi tool!
@call C:\Projects_src\Personal\Archi-img\utils\exportImages.bat %PROJECT_DIR%
GOTO DONE

:ICONS
ECHO Add icons to archimate images based on imagas.json
@ECHO ON
@call C:\Projects_src\Personal\Archi-img\utils\addIcons.bat %PROJECT_DIR%
@ECHO OFF
GOTO DONE

:MERMAID
ECHO Generate images from mermaid files
@ECHO ON
@call C:\Projects_src\Personal\Archi-img\utils\generateImages.bat %PROJECT_DIR%
@ECHO OFF
GOTO DONE

:SPECIFICATION
ECHO Generate specification
@ECHO ON
@call C:\Projects_src\Personal\Archi-img\utils\createSpec.bat %PROJECT_DIR%
@ECHO OFF
GOTO DONE

:HUGO2PDF
ECHO Generate pdf from specification, must call spec first!
ECHO NOT IMPLEMENTED !!
GOTO DONE

:HUGO2WEB
ECHO Generate web from specification, must call spec first!
ECHO NOT IMPLEMENTED !!
GOTO DONE

:DELETE_GENERATED
ECHO Delete generated files
@ECHO ON
@call C:\Projects_src\Personal\Archi-img\utils\deleteAll.bat %PROJECT_DIR%
@ECHO OFF
GOTO DONE

:ERROR
ECHO Must be initialized with directory parameter.
ECHO Usage: docool project_directory command
GOTO DONE

:DONE
ECHO.
ECHO Done!
