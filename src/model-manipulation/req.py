# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os
import os.path
import unidecode
import shutil

def getFileName(name):
    fileName = unidecode.unidecode(name)
    fileName = fileName.replace('.', '-').replace(' ', '-')
    return fileName
    
def processFolder(path, element, index):
    name = element.attrib['name']
    folderName = getFileName(name)
    print("process folder: " + name)

    # create folder
    if os.path.isdir(path+folderName):
        shutil.rmtree(path+folderName, ignore_errors=True)        
    os.mkdir(path+folderName)
    path = path + folderName + "/"

    # create index file
    with open(path + "_index.md", "w", encoding="utf-8") as f:
        f.write('---\n')
        f.write('title: ' + name + "\n")
        f.write('date: 2019-04-11T16:11:32+02:00\n')
        f.write('draft: true\n')
        f.write('weight: 1\n')
        f.write('---\n')
        # add documentation
        for d in element.findall('documentation'):
            f.write(d.text)
            f.write("\n\n")
        for req in element.findall('element'):
            f.write("\n")
            f.write("## " + req.attrib['name'] + "\n")
#            print("REQ " + req.attrib['name'])
            d = req.find('documentation')
#            print(d)
#            print(d.text)
            f.write("\n")
            f.write(d.text)
            f.write("\n")    
            
    c = 0
    for f in element.findall('folder'):
        processFolder(path, f, c)
        c += 1
    
    
    
tree = ET.parse('../Architecture_src/model/or.archimate')
poziadavky = tree.getroot()[4][0]
processFolder("../temp/", poziadavky, 0)


