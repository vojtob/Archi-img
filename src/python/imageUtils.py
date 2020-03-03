import numpy as np
import cv2

def convertImage(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 135, 255, cv2.THRESH_BINARY_INV)[1]
    # edges = cv2.Canny(gray,100,200)
    # blur = cv2.blur(edges,(4,4))
    # cv2.imshow(cv2.namedWindow("addIcons"), gray)
    # cv2.waitKey()
    return thresh

def overlayImageOverImage(bigImg, smallImage, smallImageOrigin):
    # print('overlay bigSize: {0[0]}x{0[1]}  iconSize: {1[0]}x{1[1]}  placement: {2[0]}x{2[1]}'.format(bigImg.shape, smallImage.shape, smallImageOrigin))
    x1 = smallImageOrigin[0]
    x2 = x1 + smallImage.shape[1]
    y1 = smallImageOrigin[1]
    y2 = y1 + smallImage.shape[0]

    alpha_smallImage = smallImage[:, :, 3] / 255.0
    alpha_bigImage = 1.0 - alpha_smallImage

    for c in range(0, 3):
        bigImg[y1:y2, x1:x2, c] = (alpha_smallImage * smallImage[:, :, c] + alpha_bigImage * bigImg[y1:y2, x1:x2, c])

    return bigImg

def addIcon2Image(img, rectangle, iconFilePath, iconSize, xAlign, yAlign, marginSize=5):
    icon = cv2.imread(iconFilePath, cv2.IMREAD_UNCHANGED)
    s = max(icon.shape[0], icon.shape[1])
    dy = int((iconSize*icon.shape[0])/s)
    dx = int((iconSize*icon.shape[1])/s)
    # print('rezise from {0[0]}x{0[1]} to {1}x{2}'.format(icon.shape, dy, dx))
    # print('icon orig size {0[0]}x{0[1]}'.format(icon.shape))
    icon = cv2.resize(icon, (dx,dy))
    # print('icon dest size {0[0]}x{0[1]}'.format(icon.shape))

    # calculate x position of icon
    if(xAlign == 'left'):
        x = rectangle[0][0] + marginSize
    elif(xAlign == 'right'):
        x = rectangle[1][0] - dx - marginSize
    elif (xAlign == 'center'):
        x = (rectangle[1][0]+rectangle[0][0]-dx) // 2
    else:
        # relative
        try:
            x = int( (1-xAlign)*rectangle[0][0] + xAlign*rectangle[1][0] - dx/2 )
        except:
            print('       icon x align bad format !!!!!!!')
            return
    
    # calculate y position of icon
    if(yAlign == 'top'):
        y = rectangle[0][1] + marginSize
    elif(yAlign == 'bottom'):
        y = rectangle[1][1] - dy - marginSize
    elif (yAlign == 'center'):
        y = (rectangle[1][1]+rectangle[0][1]-dy) // 2
    else:
        # relative
        try:
            pass
            y = int( (1-yAlign)*rectangle[0][1] + yAlign*rectangle[1][1] - dy/2 )
        except:
            print('       icon y align bad format !!!!!!!!')
            return

    return overlayImageOverImage(img, icon, (x,y))
    

            

