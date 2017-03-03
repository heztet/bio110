from graphics import *
import random

random.seed()
windowDimX = 500
windowDimY = 200
distFromEdge = 50

def main():
    # Create window
    win = GraphWin("Neuron Mitochondria", windowDimX, windowDimY, autoflush=False)

    # Create neuron body
    neuronBody = Rectangle(Point(0 + distFromEdge, 0 + distFromEdge), Point(windowDimX - distFromEdge, windowDimY - distFromEdge))
    neuronBody.draw(win)

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
                m.randDraw(10000)
            # Move mito if drawn
            else:
                m.move()
            # Reset mito if it's crossed the neuron body
            if (m.checkEnd()):
                mitos.remove(m)
                mitos.append(Mito(win))
        # Refresh the window
        update()
        print(len(mitos))
    # Pause for click in window
    win.getMouse()
    win.close()

class Mito(object):
    heightBuffer = 10
    minHeight = distFromEdge + heightBuffer
    maxHeight = windowDimY - distFromEdge - heightBuffer
    leftSide = distFromEdge
    rightSide = windowDimX - distFromEdge
    mitoWidth = 50
    mitoHeight = 10
    dx = windowDimX / 50000

    def __init__(self, window):
        self.onRight = (False, True)[random.randrange(0, 2)] # 1 = right, 0 = left
        if self.onRight:
            x = Mito.rightSide
        else:
            x = Mito.leftSide
        y = random.uniform(Mito.minHeight, Mito.maxHeight)
        self.p1 = Point(x - Mito.mitoWidth / 2, y - Mito.mitoHeight / 2)
        self.p2 = Point(x + Mito.mitoWidth / 2, y + Mito.mitoHeight / 2)
        self.mid = Line(self.p1, self.p2).getCenter()
        self.drawn = False
        self.oval = None
        self.window = window

    def randDraw(self, chance):
        if (random.randrange(0, 10000) == 0):
            self.draw()

    def draw(self):
        self.oval = Oval(self.p1, self.p2)
        self.oval.draw(self.window)
        self.drawn = True

    def move(self):
        dist = Mito.dx
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

main()