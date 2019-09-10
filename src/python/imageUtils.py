import numpy as np
import cv2

def convertImage(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)[1]
    # edges = cv2.Canny(gray,100,200)
    # blur = cv2.blur(edges,(4,4))
    # cv2.imshow(cv2.namedWindow("addIcons"), gray)
    # cv2.waitKey()
    return thresh

def overlayImageOverImage(bigImg, smallImage, smallImageOrigin):
    x1 = smallImageOrigin[0]
    x2 = x1 + smallImage.shape[0]
    y1 = smallImageOrigin[1]
    y2 = y1 + smallImage.shape[0]

    alpha_smallImage = smallImage[:, :, 3] / 255.0
    alpha_bigImage = 1.0 - alpha_smallImage

    for c in range(0, 3):
        bigImg[y1:y2, x1:x2, c] = (alpha_smallImage * smallImage[:, :, c] + alpha_bigImage * bigImg[y1:y2, x1:x2, c])

    return bigImg

def addIcon2Image(img, rectangle, iconFilePath, iconSize, xAlign, yAlign, marginSize=5):
    icon = cv2.imread(iconFilePath, cv2.IMREAD_UNCHANGED)
    icon = cv2.resize(icon, (iconSize,iconSize))

    # calculate x position of icon
    if(xAlign == 'left'):
        x = rectangle[0][0] + marginSize
    elif(xAlign == 'right'):
        x = rectangle[1][0] - iconSize - marginSize
    elif (xAlign == 'center'):
        x = (rectangle[1][0]+rectangle[0][0]-iconSize) // 2
    else:
        # relative
        if(not xAlign.isnumeric()):
            print('       icon x align bad format')
        q = float(xAlign)
        x = int( (1-q)*rectangle[0][0] + q*rectangle[1][0] - iconSize/2 )

    # calculate y position of icon
    if(yAlign == 'top'):
        y = rectangle[0][1] + marginSize
    elif(yAlign == 'bottom'):
        y = rectangle[1][1] - iconSize - marginSize
    elif (yAlign == 'center'):
        y = (rectangle[1][1]+rectangle[0][1]-iconSize) // 2
    else:
        # relative
        if(not yAlign.isnumeric()):
            print('       icon y align bad format')
        q = float(yAlign)
        y = int( (1-q)*rectangle[0][1] + q*rectangle[1][1] - iconSize/2 )

    return overlayImageOverImage(img, icon, (x,y))
    

            

