import unittest
import imagefocus as imgf

def addpoint(p1, p2):
    return (p1[0]+p2[0], p1[1]+p2[1])

class TestImageFocus(unittest.TestCase):
    r1 = ((10, 10), (90, 80))
    r2 = ((10, 90), (90, 160))
    r3 = ((100, 50), (150, 120))
    rectangles = [r1, r2, r3]

    def test_opposite(self):
        self.assertEqual(imgf.DOWN, imgf.getopposite(imgf.UP))

    def test_start(self):
        self.assertEqual(imgf.find_start_rect(self.rectangles), self.r1)


    def test_edge(self):
        r = ((10, 20), (90, 110))
        edger = (90, 20, 110)
        edgel = (10, 20, 110)
        edgeu = (20, 10, 90)
        edged = (110, 10, 90)
        self.assertEqual(imgf.get_edge(r, imgf.UP), edgeu)
        self.assertEqual(imgf.get_edge(r, imgf.RIGHT), edger)
        self.assertEqual(imgf.get_edge(r, imgf.DOWN), edged)
        self.assertEqual(imgf.get_edge(r, imgf.LEFT), edgel)

    def test_collision_edge(self):
        e = imgf.get_edge(self.r1, imgf.RIGHT)
        ce = imgf.get_collision_edge(e, imgf.RIGHT, imgf.DOWN)
        self.assertEqual((e[0]+imgf.AREA_GAP, e[1], e[2]+imgf.AREA_GAP), ce)

        e = imgf.get_edge(self.r3, imgf.DOWN)
        ce = imgf.get_collision_edge(e, imgf.DOWN, imgf.LEFT)
        self.assertEqual((e[0]+imgf.AREA_GAP, e[1]-imgf.AREA_GAP, e[2]), ce)

        cp = imgf.get_collision_point(imgf.get_edge(self.r1, imgf.RIGHT), imgf.RIGHT, imgf.DOWN, imgf.get_edge(self.r3, imgf.UP))
        self.assertEqual(cp, (self.r1[1][0]+imgf.AREA_BORDER, self.r3[0][1]-imgf.AREA_BORDER))

    def test_collision(self):
        rectangles = [self.r1, self.r2, self.r3]
        self.assertEqual(imgf.turn_after_collision(rectangles, imgf.get_edge(self.r1, imgf.UP), imgf.UP, imgf.RIGHT), None)

        collision = imgf.turn_after_collision(rectangles, imgf.get_edge(self.r1, imgf.RIGHT), imgf.RIGHT, imgf.DOWN)
        self.assertEqual(collision[0], (self.r1[1][0]+imgf.AREA_BORDER, self.r3[0][1]-imgf.AREA_BORDER), msg='collision point')
        self.assertEqual(collision[1], imgf.get_edge(self.r3, imgf.UP), msg='collision next edge')
        self.assertEqual(collision[2], (imgf.UP, imgf.RIGHT), msg='collision next edge name-direction')
        
        collision = imgf.turn_after_collision(rectangles, imgf.get_edge(self.r3, imgf.DOWN), imgf.DOWN, imgf.LEFT)
        self.assertEqual(collision[0], (self.r1[1][0]+imgf.AREA_BORDER, self.r3[1][1]+imgf.AREA_BORDER), msg='collision point')
        self.assertEqual(collision[1], imgf.get_edge(self.r2, imgf.RIGHT), msg='collision next edge')
        self.assertEqual(collision[2], (imgf.RIGHT, imgf.DOWN), msg='collision next edge name-direction')

    def test_continue_on(self):
        rectangles = [self.r1, self.r2, self.r3]

        nextedge = imgf.continue_on(rectangles, imgf.get_edge(self.r1, imgf.UP), imgf.UP, imgf.RIGHT)
        self.assertEqual(nextedge, None)

        nextedge = imgf.continue_on(rectangles, imgf.get_edge(self.r2, imgf.LEFT), imgf.LEFT, imgf.UP)
        self.assertEqual(nextedge, (imgf.get_edge(self.r1, imgf.LEFT), imgf.LEFT, imgf.UP))

    def test_points(self):
        b = imgf.AREA_BORDER
        points = imgf.find_traverse_points(self.rectangles)
        mypoints = [addpoint(self.r1[0],(-b,-b)), 
            addpoint((self.r1[1][0],self.r1[0][1]),(b,-b)), 
            addpoint((self.r1[1][0],self.r3[0][1]),(b,-b)), 
            addpoint((self.r3[1][0],self.r3[0][1]),(b,-b)), 
            addpoint((self.r3[1][0],self.r3[1][1]),(b,b)),
            addpoint((self.r2[1][0],self.r3[1][1]),(b,b)),
            addpoint(self.r2[1],(b,b)), 
            addpoint((self.r2[0][0],self.r2[1][1]),(-b,b))]
        self.assertEqual(points, mypoints)


if __name__ == '__main__':
    unittest.main()
