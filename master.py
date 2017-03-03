from graphics import *
import random


def main():
    # Create window
    windowDimX = 500
    windowDimY = 200
    win = GraphWin("Neuron Mitochondria", windowDimX, windowDimY, autoflush=False)

    # Create neuron body
    distFromEdge = 50
    neuronLength = windowDimX - distFromEdge * 2
    neuronHeight = windowDimY - distFromEdge * 2
    neuronBody = Rectangle(Point(0 + distFromEdge, 0 + distFromEdge), Point(windowDimX - distFromEdge, windowDimY - distFromEdge))
    neuronBody.draw(win)

    # Create mitochondria objects
    mito = []
    numMito = 15
    heightBuffer = 10
    minHeight = distFromEdge + heightBuffer
    maxHeight = windowDimY - distFromEdge - heightBuffer
    leftSide = distFromEdge
    rightSide = windowDimX - distFromEdge
    mitoWidth = 50
    mitoHeight = 10
    for i in range(0, numMito):
        # Randomly choose right (1) or left (0) side
        side = random.randrange(0, 2)
        x = (leftSide, rightSide)[side]
        y = random.uniform(minHeight, maxHeight)
        p1 = Point(x - mitoWidth / 2, y - mitoHeight / 2)
        p2 = Point(x + mitoWidth / 2, y + mitoHeight / 2)
        drawn = False
        oval = 0
        mito.append([side, p1, p2, drawn, oval])

    # Run until mouse is clicked
    while (not win.checkMouse()):
        for i, m in enumerate(mito):
            # Randomly choose whether to draw new mito
            if ((not mito[i][3]) and (random.randrange(0, 10000) == 0)):
                mito[i][4] = Oval(mito[i][1], mito[i][2])
                mito[i][4].draw(win)
                mito[i][3] = True
            # Move mito if drawn
            if (mito[i][3]):
                dist = windowDimX / 50000
                # Reverse direction if moving left
                if (mito[i][0] == 1):
                    dist *= -1
                mito[i][4].move(dist, 0)
                mito[i][1] = mito[i][4].getP1()
                mito[i][2] = mito[i][4].getP2()
            # Reset mito if it's crossed the neuron body
            midPointX = Line(mito[i][1], mito[i][2]).getCenter().getX()
            if not (leftSide <= midPointX <= rightSide):
                mito[i][4].undraw()
                mito[i][3] = False

        # Refresh the window
        update()

def PointSubtract(p1, p2):
    return Point(p2.getX() - p1.getX(), p2.getY() - p1.getY())

    # Pause for click in window
    win.getMouse()
    win.close()

main()