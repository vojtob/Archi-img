SET PROJECT_DIR=%1
SET PROJECT_NAME=%~n1
java -classpath %~dp0/xalan/xalan.jar;%~dp0/xalan/serializer.jar;%~dp0/xalan/xml-apis.jar;%~dp0/xalan/xercesImpl.jar org.apache.xalan.xslt.Process -IN %PROJECT_DIR%/src/model/%PROJECT_NAME%.archimate -XSL %~dp0/xslt/align2grid.xsl -OUT %PROJECT_DIR%/src/model/%PROJECT_NAME%X.archimate
mv %PROJECT_DIR%/src/model/%PROJECT_NAME%X.archimate %PROJECT_DIR%/src/model/%PROJECT_NAME%.archimate