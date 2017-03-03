from graphics import *
import random


class Container(object):
    def __init__(self, x, xMax, y, yMax, buffer):
        self.x = x
        self.xMax = xMax
        self.y = y
        self.yMax = yMax
        self.buffer = buffer

    def draw(self, window):
        Rectangle(Point(self.x, self.y), Point(self.xMax, self.yMax)).draw(window)

    def printPoints(self):
        print("Point 1: (%f, %f)" % (self.x, self.y))
        print("Point 2: (%f, %f)" % (self.xMax, self.yMax))

    def dx(self):
        return self.xMax - self.x

    def dy(self):
        return self.yMax - self.y

class NeuronPoly(object):
    def __init__(self, model, avgHeight, numVertices, window):
        self.window = window
        self.color = "pale goldenrod"
        self.lineColor = "tan"
        self.poly = None
        self.avgHeight = avgHeight
        self.maxHeightDev = 0

        # Fill out random part of border
        self.points = []
        dx = (model.dx() - (2 * model.buffer)) / numVertices
        x = model.x
        while (x <= (model.xMax - model.buffer)):
            y = random.gauss(avgHeight, 5)

            # Update max height deviation
            heightDiff = abs(avgHeight - y)
            if (heightDiff> self.maxHeightDev):
                self.maxHeightDev = heightDiff

            self.points.append(Point(x, y))
            x += dx

        # Add points at the "base" of the shape (so that it's no longer a line
        #self.points.append

    def draw(self):
        self.poly = Polygon(self.points).draw(self.window)
        self.poly.setFill(self.color)
        self.poly.setOutline(self.lineColor)


class Mito(object):
    # Properties that all Mito objects will share
    mitoWidth  = 50
    mitoHeight = 10
    container = Container(0, 0, 0, 0, 0)

    #minHeight  = 0 #distFromEdge + mitoHeight
    #maxHeight  = 0 #windowDimY - distFromEdge - mitoHeight
    #leftSide   = 0 #distFromEdge
    #rightSide  = 0 #windowDimX - distFromEdge
    defaultDx  = 0
    colors = ["aquamarine", "blue violet", "chartreuse", "dark cyan", "dark slate blue",
              "dark turquoise", "deep sky blue", "dark green", "forest green", "light blue", "medium sea green"]

    def __init__(self, window):
        # Randomly set whether Mito will be on the right or left side
        self.onRight = (False, True)[random.randrange(0, 2)] # 1 = right, 0 = left
        if self.onRight:
            x = Mito.container.x
        else:
            x = Mito.container.xMax
        y = random.uniform(Mito.container.y, Mito.container.yMax)

        # Initial two points for Mito oval
        self.p1 = Point(x - Mito.mitoWidth / 2, y - Mito.mitoHeight / 2)
        self.p2 = Point(x + Mito.mitoWidth / 2, y + Mito.mitoHeight / 2)
        self.mid = Line(self.p1, self.p2).getCenter()

        # Initial dx
        self.dx = Mito.defaultDx

        # Not drawn by default
        self.color = Mito.colors[random.randrange(0, len(Mito.colors))]
        self.drawn = False
        self.oval = None
        self.window = window

    # Mito has a 1/chance odds to be drawn
    def randDraw(self, chance):
        if (random.randrange(0, chance) == 0):
            self.draw()

    def draw(self):
        self.oval = Oval(self.p1, self.p2)
        self.oval.draw(self.window)
        self.oval.setFill(self.color)
        self.drawn = True

    # Move mito oval and update its points
    def move(self):
        dist = self.dx
        if (self.onRight):
            dist *= -1
        self.oval.move(dist, 0)
        self.p1 = self.oval.getP1()
        self.p2 = self.oval.getP2()
        self.mid = Line(self.p1, self.p2).getCenter()

    def checkEnd(self):
        if not (Mito.container.x <= self.mid.getX() <= Mito.container.xMax):
            self.undraw()
            return True
        else:
            return False

    def undraw(self):
        self.oval.undraw()