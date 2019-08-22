import sys
import fileinput
import os
import subprocess
import time

if (len(sys.argv) < 2):
    print('usage: generateUMLETimages.py projectPath')
else:
    umletPath = os.path.join('C:/', 'prg', 'Umlet', 'Umlet')

    projectDir = sys.argv[1]
    srcDir = os.path.join(projectDir, 'src', 'Architecture', 'img')
    destDir = os.path.join(projectDir, 'Architecture')
    # destDir = os.path.join(projectDir, 'release', 'spec_local', 'static', 'img')
    
    moveFile = []

    for (dirpath, dirnames, filenames) in os.walk(srcDir):
        for f in filenames:
            if(f.endswith('uxf')):
                fileName = f[:-4]
                filePath = dirpath.replace(srcDir, destDir)
                # print(filePath, fileName)
                if(not os.path.exists(filePath)):
                    # print('create directory', filePath)
                    os.makedirs(filePath)
                print('convert UXF file', fileName)
                cmd = umletPath + ' -action=convert -format=png -filename="' + os.path.join(dirpath,fileName) + '.uxf"'
                subprocess.run(cmd, shell=False)
                while(not os.path.exists(os.path.join(dirpath,fileName) + '.png')):
                    pass
                moveFile.append((os.path.join(dirpath,fileName) + '.png', os.path.join(filePath,fileName) + '.png'))
    time.sleep(5)
    for (fromFile, toFile) in moveFile:
        # print(fromFile, toFile)
        os.rename(fromFile, toFile)				
				
print ("UXF images generated")
