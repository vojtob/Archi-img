java -classpath xalan/xalan.jar;xalan/serializer.jar;xalan/xml-apis.jar;xalan/xercesImpl.jar org.apache.xalan.xslt.Process -IN ../Architecture_src/model/orsr.archimate -XSL xslt/useSK.xsl -OUT orsr.archimate
mv orsr.archimate ../Architecture_src/model