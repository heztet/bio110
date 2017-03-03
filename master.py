#from graphics import *
from shapes import *
import random

def main():
    random.seed()

    # Create window
    mainWindow = Container(0, 600, 0, 200, 25)
    win = GraphWin("Neuron Mitochondria", mainWindow.xMax, mainWindow.yMax, autoflush=False)
    mainWindow.draw(win)

    # Create model
    model = Container(mainWindow.x + mainWindow.buffer,
                      mainWindow.xMax - mainWindow.buffer - 100,
                      mainWindow.y + mainWindow.buffer,
                      mainWindow.yMax - mainWindow.buffer,
                      0)
    #model.draw(win)

    neuronHeight = model.dy() / 6 # arbitrary height of both halves of neuron body

    # Draw upper part of neuron
    topNeuron = NeuronPoly(model, model.y + neuronHeight, 50, win)
    topNeuron.points.append(Point(model.xMax - model.buffer, model.y))
    topNeuron.points.append(Point(model.x + model.buffer, model.y))
    topNeuron.draw()

    # Draw bottom part of neuron
    bottomNeuron = NeuronPoly(model, model.yMax - model.buffer - neuronHeight, 50, win)
    bottomNeuron.points.append(Point(model.xMax - model.buffer, model.yMax))
    bottomNeuron.points.append(Point(model.x + model.buffer, model.yMax))
    bottomNeuron.draw()

    # Create mitochondria objects
    Mito.container = Container(model.x + model.buffer,
                               model.xMax - model.buffer,
                               topNeuron.avgHeight + topNeuron.maxHeightDev,
                               bottomNeuron.avgHeight - bottomNeuron.maxHeightDev,
                               Mito.mitoHeight)
    Mito.defaultDx = model.dx() / 50000

    mitos = []
    mitosNum = 10

    for i in range(0, mitosNum):
        # Randomly choose right (1) or left (0) side
        mitos.append(Mito(win))

    # Run until mouse is clicked
    try:
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
    except GraphicsError as err:
        if "{0}".format(err) != "checkMouse in closed window":
            print("GraphicsError: {0}".format(err))



# Run
if __name__ == "__main__":
    main()