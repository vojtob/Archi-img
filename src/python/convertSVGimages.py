import sys
import fileinput
import os
import subprocess

if (len(sys.argv) < 2):
    print('usage: generateSVGimages.py projectPath')
else:
    projectDir = sys.argv[1]
    srcDir = os.path.join(projectDir, 'temp', 'img_exported_svg')
    destDir = os.path.join(projectDir, 'temp', 'img_exported')
    
    for (dirpath, dirnames, filenames) in os.walk(srcDir):
        for f in filenames:
            if(f.endswith('svg')):
                fileName = f[:-4]
                orig_file_path = os.path.join(dirpath, f)
                dest_file_dir = dirpath.replace(srcDir, destDir)
                dest_file_path = os.path.join(dest_file_dir, f[:-4]+'.png')
                # print(filePath, fileName)
                if(not os.path.exists(dest_file_dir)):
                    #print('create directory', dest_file_dir)
                    os.makedirs(dest_file_dir)
                print('convert SVG file', f)
                cmd = os.environ['IM_HOME'] + '/convert.exe  -density 144 ' + orig_file_path + ' ' + dest_file_path
                # print(cmd)
                subprocess.run(cmd, shell=False)

print ("SVG images converted")
