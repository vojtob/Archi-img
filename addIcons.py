import sys
import os
import json
import shutil
import cv2
import numpy as np
import rectRecognition as rr


def addIcons2image(srcImagePath, destImagePath, imageDef, iconsPath):
    img = cv2.imread(srcImagePath, cv2.IMREAD_UNCHANGED)
    # identify rectangles
    cv2.imwrite(destImagePath, rr.identifyRectangles(img))


    # add all icons
    # icon = cv2.imread(os.path.join(iconsPath, imageDef['icons'][0]['iconName']), cv2.IMREAD_UNCHANGED)
    # img2 = addIcon2Image(img, icon)
    # cv2.imwrite(destImagePath, img2)
    return

if (len(sys.argv) < 2):
    print('usage: generateUMLETimages.py projectPath')
else:
    projectDir = sys.argv[1]
dirExportedImages = os.path.join(projectDir, 'temp', 'img_exported')
dirReleasedImages = os.path.join(projectDir,'release', 'img')

with open(os.path.join(projectDir, 'src', 'img', 'images.json')) as imagesFile:
    imageDefs = json.load(imagesFile)

# go throug all exported files
# if there is imageDef then add icons to image
# else copy image do release
for (dirpath, dirnames, filenames) in os.walk(dirExportedImages):
    destDirPath = dirpath.replace(dirExportedImages, dirReleasedImages)
    for f in filenames:
        if(not os.path.exists(destDirPath)):
            os.makedirs(destDirPath)
        imageSrcPath = os.path.join(dirpath,f)
        imageDestPath = os.path.join(destDirPath,f)
        imageRelFilePah = imageSrcPath.replace(dirExportedImages,'')[1:]
        if(imageRelFilePah == 'Calibration.png'):
            continue
        defs = [imageDef for imageDef in imageDefs if os.path.normpath(imageDef['fileName'])==imageRelFilePah]
        if(len(defs)):
            print('add icons to file', imageRelFilePah)
            addIcons2image(imageSrcPath, imageDestPath, defs[0], os.path.join(projectDir, 'src', 'res', 'icons'))
        else:
            print('copy file', imageRelFilePah)
            # shutil.copyfile(imageSrcPath, imageDestPath)


print('DONE addIcons.py')