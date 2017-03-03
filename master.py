from graphics import *
import random

random.seed()
windowDimX = 500
windowDimY = 200
distFromEdge = 50

def main():
    # Create window
    win = GraphWin("Neuron Mitochondria", windowDimX, windowDimY, autoflush=False)

    # Draw upper part of neuron
    topLine = NeuronPoly(distFromEdge, 50, win)
    topLine.points.append(Point(windowDimX - distFromEdge, 0))
    topLine.points.append(Point(distFromEdge, 0))
    topLine.draw()

    # Draw bottom part of neuron
    bottomLine = NeuronPoly(windowDimY - distFromEdge, 50, win)
    bottomLine.points.append(Point(windowDimX - distFromEdge, windowDimY - 1))
    bottomLine.points.append(Point(distFromEdge, windowDimY - 1))
    bottomLine.draw()

    #neuronBody = Rectangle(Point(0 + distFromEdge, 0 + distFromEdge), Point(windowDimX - distFromEdge, windowDimY - distFromEdge))
    #neuronBody.draw(win)

    # Create mitochondria objects
    mitos = []
    mitosNum = 10

    for i in range(0, mitosNum):
        # Randomly choose right (1) or left (0) side
        mitos.append(Mito(win))

    # Run until mouse is clicked
    while (not win.checkMouse()):
        for m in mitos:
            # Randomly choose whether to draw new mito
            if (not m.drawn):
                m.randDraw(15000)
            # Move mito if drawn
            else:
                m.move()
            # Reset mito if it's crossed the neuron body
            if (m.checkEnd()):
                mitos.remove(m)
                mitos.append(Mito(win))
        # Refresh the window
        update()
    # Pause for click in window
    win.getMouse()
    win.close()

class NeuronPoly(object):
    def __init__(self, avgHeight, numVertices, window):
        self.window = window
        self.color = "pale goldenrod"
        self.poly = None
        self.avgHeight = avgHeight
        self.maxHeightDev = 0

        # Fill out random part of border
        self.points = []
        dx = (windowDimX - (2 * distFromEdge)) / numVertices
        x = distFromEdge
        while (x <= (windowDimX - distFromEdge)):
            y = random.gauss(avgHeight, 5)

            # Update max height deviation
            heightDiff = abs(avgHeight - y)
            if (heightDiff> self.maxHeightDev):
                self.maxHeightDev = heightDiff

            self.points.append(Point(x, y))
            x += dx

    def draw(self):
        self.poly = Polygon(self.points).draw(self.window)
        self.poly.setFill(self.color)


class Mito(object):
    # Properties that all Mito objects will share
    heightBuffer = 10
    minHeight = distFromEdge + heightBuffer
    maxHeight = windowDimY - distFromEdge - heightBuffer
    leftSide = distFromEdge
    rightSide = windowDimX - distFromEdge
    mitoWidth = 50
    mitoHeight = 10
    colors = ["aquamarine", "blue violet", "chartreuse", "dark cyan", "dark slate blue",
              "dark turquoise", "deep sky blue", "dark green", "forest green", "light blue", "medium sea green"]
    defaultDx = windowDimX / 50000

    def __init__(self, window):
        # Randomly set whether Mito will be on the right or left side
        self.onRight = (False, True)[random.randrange(0, 2)] # 1 = right, 0 = left
        if self.onRight:
            x = Mito.rightSide
        else:
            x = Mito.leftSide
        y = random.uniform(Mito.minHeight, Mito.maxHeight)

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
        if not (Mito.leftSide <= self.mid.getX() <= Mito.rightSide):
            self.undraw()
            return True
        else:
            return False

    def undraw(self):
        self.oval.undraw()

# Run
if __name__ == "__main__":
    main()