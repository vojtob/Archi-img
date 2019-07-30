@set PROJECT_DIR=%1

REM **************
REM generate icons
@set ICONS_SRC_DIR=%PROJECT_DIR%\resources\icons
@set ICONS_DIR=%PROJECT_DIR%\temp\specifikacia\static\icons
mkdir %ICONS_DIR%
magick convert -resize 60x60 %ICONS_SRC_DIR%\riskmanagement.png %ICONS_DIR%\icon60_riskmanagement.png 
magick convert -resize 60x60 %ICONS_SRC_DIR%\contactus.png %ICONS_DIR%\icon60_contactus.png 
magick convert -resize 60x60 %ICONS_SRC_DIR%\blogpost.png %ICONS_DIR%\icon60_blogpost.png 
magick convert -resize 60x60 %ICONS_SRC_DIR%\publicsector.png %ICONS_DIR%\icon60_publicsector.png 
magick convert -resize 60x60 %ICONS_SRC_DIR%\OK.png %ICONS_DIR%\icon60_OK.png 

mkdir %ICONS_DIR%\customerJourney
py ../../Implementation/generateDocs/generateCj.py