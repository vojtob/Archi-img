import sys
import fileinput
import os
import subprocess

if (len(sys.argv) < 2):
    print('usage: generateMMimages.py projectPath')
else:
    mmPath = os.path.join('C:/', 'prg', 'mermaid', 'node_modules', 'mermaid.cli', 'index.bundle.js')

    projectDir = sys.argv[1]
    srcDir = os.path.join(projectDir, 'src', 'img')
    destDir = os.path.join(projectDir, 'release', 'img')
    # destDir = os.path.join(projectDir, 'release', 'spec_local', 'static', 'img')
    
    for (dirpath, dirnames, filenames) in os.walk(srcDir):
        for f in filenames:
            if(f.endswith('mmd')):
                fileName = f[:-4]
                filePath = dirpath.replace(srcDir, destDir)
                # print(filePath, fileName)
                if(not os.path.exists(filePath)):
                    # print('create directory', filePath)
                    os.makedirs(filePath)
                print('convert MM file', fileName)
                cmd = 'node ' + mmPath + ' -w 1400 -i ' + os.path.join(dirpath,fileName) + '.mmd -o ' + os.path.join(filePath,fileName) + '.png'
                subprocess.run(cmd, shell=False)

print ("MM images generated")
