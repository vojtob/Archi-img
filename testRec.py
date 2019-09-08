import os
import cv2
import rectRecognition as rr

srcImagePath = os.path.join('C:\\', 'Projects_src', 'Work', 'CLK', 'temp', 'img_exported', 'landscape', 'AppLandscape.png')
img = cv2.imread(srcImagePath, cv2.IMREAD_UNCHANGED)
img = rr.identifyRectangles(img)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
destImagePath = os.path.join('C:\\', 'Projects_src', 'Work', 'CLK', 'release', 'img', 'landscape', 'AppLandscape.png')
cv2.imwrite(destImagePath, img)

print('DONE')