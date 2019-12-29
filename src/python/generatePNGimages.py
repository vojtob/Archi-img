import sys
import fileinput
import os
import subprocess
import shutil

if (len(sys.argv) < 2):
    print('usage: generateMMimages.py projectPath')
else:
    mmPath = os.path.join('C:/', 'prg', 'mermaid', 'node_modules', 'mermaid.cli', 'index.bundle.js')

    projectDir = sys.argv[1]
    srcDir = os.path.join(projectDir, 'src', 'img')
    # destDir = os.path.join(projectDir, 'release', 'img')
    destDir = os.path.join(projectDir, 'temp', 'img_exported')
    
    for (dirpath, dirnames, filenames) in os.walk(srcDir):
        for f in filenames:
            if(f.endswith('png') or f.endswith('jpg') or f.endswith('jpeg')):
                # fileName = f[:-4]
                filePath = dirpath.replace(srcDir, destDir)
                # print(filePath, fileName)
                if(not os.path.exists(filePath)):
                    # print('create directory', filePath)
                    os.makedirs(filePath)
                print('copy image file', os.path.join(dirpath,f), os.path.join(filePath,f))
                shutil.copyfile(os.path.join(dirpath,f), os.path.join(filePath,f))

print ("PNG images copied")
