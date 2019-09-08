import cv2
import numpy as np

def addIcon2Image(img, icon):
    icon = cv2.resize(icon, (150,150))
    x1, x2 = (img.shape[1] - icon.shape[1])//2, (img.shape[1] + icon.shape[1])//2
    y1, y2 = (img.shape[0] - icon.shape[0])//2, (img.shape[0] + icon.shape[0])//2
    alpha_icon = icon[:, :, 3] / 255.0
    alpha_img = 1.0 - alpha_icon

    for c in range(0, 3):
        img[y1:y2, x1:x2, c] = (alpha_icon * icon[:, :, c] + alpha_img * img[y1:y2, x1:x2, c])
    return img

def convertImage(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # edges = cv2.Canny(gray,100,200)
    # blur = cv2.blur(edges,(4,4))
    # cv2.imshow(cv2.namedWindow("addIcons"), gray)
    # cv2.waitKey()
    return thresh

def addPointToSegments(lineSegments, keyCoordinate, lenCoordinate, reallySmallGap, minSegmentLength):
    """ add a point to segments """
    if(lineSegments.get(keyCoordinate)):
        # there is a segment with key coordinate equal to keyCoordinate
        segments = lineSegments[keyCoordinate]
        # the last segment
        s = segments.pop()
        # check how close is the point to the last segment
        if( (lenCoordinate-s[1]) <= reallySmallGap ):
            # the point is too close to the last segment, we prolong this segment (poped element replaced with longer)
            segments.append((s[0],lenCoordinate))
        else:
            # the point is too far from previous segment
            # check, if the previous segment is long enough
            if( (s[1]-s[0]) > minSegmentLength ):
                # last segment is long enough, we should return it back to list (removed by pop)
                segments.append(s)
            # we should create a new segment, only one point long
            segments.append((lenCoordinate,lenCoordinate))
    else:
         # the very first segment for this key coordinate, create list of segments and a new segment       
         segments = []
         segments.append((lenCoordinate,lenCoordinate))
         lineSegments[keyCoordinate] = segments

def removeShortSegments(lineSegments, minSegmentLength):
    emptyList = []
    for keyCoordinate, segments in lineSegments.items():
        s = segments[-1]
        if( (s[1]-s[0]) < minSegmentLength ):
            segments.pop()
        if(len(segments) < 1):
            emptyList.append(keyCoordinate)
    for keyCoordinate in emptyList:
        lineSegments.pop(keyCoordinate)

def findLineSegments(img, reallySmallGap, minSegmentLength):
    """find line segments with minimal length"""

    # line segments are indexed by x or y coordinate and
    # for a particular x contain list of line segment
    # x : (y1,y2), (y3,y4)  - it means segments (x,y1, x,y2) and (x,y3, x,y4)
    lineSegmentsHorizontal = {}
    lineSegmentsVertical = {}

    # in this run we identify all line segments (even with length 1)
    # short segments could be only the last in list
    # opencv coordinate system is (row,col), therefore swith x-y
    maxY, maxX = img.shape[:2]
    for x in range(maxX):
        for y in range(maxY):
            # opencv coordinate system is (row,col), therefore swith x-y
            if(img[y,x]):
                # here is a point that should be added to segments
                addPointToSegments(lineSegmentsHorizontal, y, x, reallySmallGap, minSegmentLength)
                addPointToSegments(lineSegmentsVertical, x, y, reallySmallGap, minSegmentLength)

    # check segments for length
    removeShortSegments(lineSegmentsHorizontal, minSegmentLength)
    removeShortSegments(lineSegmentsVertical, minSegmentLength)

    return lineSegmentsHorizontal, lineSegmentsVertical

def findVerticalEdge(startX, startY, cornerGap, lineSegmentsVertical):
    xKeys = lineSegmentsVertical.keys()
    for x in sorted(xKeys):
        if(x < (startX-cornerGap)):
            # too small x
            continue
        if(x > (startX+cornerGap)):
            # too big
            return None
        # this x is in interval
        verticalEgdeCandidates = lineSegmentsVertical[x]
        for edge in verticalEgdeCandidates:
            if(edge[0] < (startY-cornerGap)):
                # too high
                continue
            if(edge[0] > (startY+cornerGap)):
                # too low
                # return None
                break
            return edge

def findBottomEdge(startX, endX, startY, cornerGap, lineSegmentsHorizontal):
    yKeys = lineSegmentsHorizontal.keys()
    for y in sorted(yKeys):
        if(y < (startY-cornerGap)):
            # too small
            continue
        if(y > (startY+cornerGap)):
            # too big
            return None
        # this y is in interval, find by left and right ends
        horizontalEgdeCandidates = lineSegmentsHorizontal[y]
        for edge in horizontalEgdeCandidates:
            if(edge[0] < (startX-cornerGap)):
                # too high
                continue
            if(edge[0] > (startX+cornerGap)):
                # too low
                # return None
                break
            # left corner OK, check right corner
            if(edge[1] < (endX-cornerGap)):
                # too small
                # return None
                break
            if(edge[1] > (endX+cornerGap)):
                # too big
                # return None
                break
            return edge

def findRectangles(lineSegmentsHorizontal, lineSegmentsVertical, cornerGap):
    rectangles = []

    # iterate over horizontal segments a consider them as horizontal top line of rectangle
    for y, topSegments in lineSegmentsHorizontal.items():
        # start with TOP edge
        for topEdge in topSegments:
            leftEdge = findVerticalEdge(topEdge[0], y, cornerGap, lineSegmentsVertical)
            if(not leftEdge):
                # left edge not found
                continue
            rightEdge = findVerticalEdge(topEdge[1], y, cornerGap, lineSegmentsVertical)
            if(not rightEdge):
                # right edge not found
                continue
            # try to find bottom edge
            bottomEdge = findBottomEdge(topEdge[0], topEdge[1], (leftEdge[1]+rightEdge[1])//2, cornerGap, lineSegmentsHorizontal)
            if(not bottomEdge):
                continue
            # we found a rectangle
            rectangles.append( ( (topEdge[0],leftEdge[0]), (bottomEdge[1],rightEdge[1]) )  ) 

    return rectangles

def identifyRectangles(img):
    # minSegmentLength = 30

    imgBW = convertImage(img)
    lineSegmentsHorizontal, lineSegmentsVertical = findLineSegments(imgBW, 6, 30)
    rectangles = findRectangles(lineSegmentsHorizontal, lineSegmentsVertical, 4)

    # for y, segments in lineSegmentsHorizontal.items():
    #     for s in segments:
    #         cv2.line(img, (s[0],y),(s[1],y), (0,255,0), thickness=2)
    # for x, segments in lineSegmentsVertical.items():
    #     for s in segments:
    #         cv2.line(img, (x,s[0]),(x,s[1]), (255,0,0), thickness=2)

    for r in rectangles:
        cv2.rectangle(img, r[0], r[1], (0,0,255), thickness=2)

    return img

