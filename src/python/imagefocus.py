import sys
import os
import subprocess
import json
import cv2
import numpy as np
import rectRecognition as rr
import rect_areas as ra

def drawarea(polygons, imagepath, imagedestpath):
    print('create image', imagedestpath)
    img = cv2.imread(imagepath, cv2.IMREAD_UNCHANGED)

    mask = np.full((img.shape[0], img.shape[1]), 80, np.uint8)
    for polygon in polygons:
        points = np.array([[p[0],p[1]] for p in polygon], np.int32)
        points = points.reshape((-1,1,2))

        # draw red polygon
        img = cv2.polylines(img, [points], True, (0,0,255), 2)
        # use mask to set transparency
        mask = cv2.fillPoly(mask, [points], 255)

    img[:, :, 3] = mask
    cv2.imwrite(imagedestpath, img)


def processFile(imgdef):
    """read image and add focus to it"""

    print('decorate image', imgdef['fileName'])

    # this are global variables for whole project
    image_rect_path = os.path.join(projectDir, 'temp', 'img_exported', imgdef['fileName']) 
    image_path = os.path.join(projectDir, 'release', 'img', imgdef['fileName']) 
    image_dest_path = image_path.replace('.png', '_{0}.png'.format(imgdef['focus-name']))

    rectangles = rr.getRectangles(image_rect_path)

    polygons = []
    for area in imgdef['areas']:
        print('Area rectangles:')
        area_rectangles = []
        for r in area:
            print(r, rectangles[r-1])
            area_rectangles.append(rectangles[r-1])
        polygons.append(ra.find_traverse_points(area_rectangles))
    drawarea(polygons, image_path, image_dest_path)


if __name__ == '__main__':
    # read project dir from arguments
    if (len(sys.argv) < 2):
        print('usage: imagefocus.py projectPath <image_name>')
        projectDir = os.path.normpath('C:/Projects_src/Work/MoJ/cpp')
        # exit(1)
    else:
        projectDir = os.path.normpath(sys.argv[1])

    thisfileonly = None
    if (len(sys.argv) >= 3):
        thisfileonly = sys.argv[2]

    # read images icons definitions
    with open(os.path.join(projectDir, 'src', 'img', 'img_focus.json')) as imagesFile:
        image_parts_defs = json.load(imagesFile)
    for imgdef in image_parts_defs:
        if((thisfileonly is None) or (imgdef['fileName'] == thisfileonly)):
            processFile(imgdef)
    
    print('DONE focus image areas.py')