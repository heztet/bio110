from graphics import *
import random


class Container(object):
    def __init__(self, x, x_max, y, y_max, buffer):
        self.x = x
        self.xMax = x_max
        self.y = y
        self.yMax = y_max
        self.buffer = buffer
        self.mid = Line(Point(x, y), Point(x_max, y_max)).getCenter()

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
    def __init__(self, model, avg_height, num_vertices, window):
        self.window = window
        self.color = "pale goldenrod"
        self.lineColor = "tan"
        self.poly = None
        self.avgHeight = avg_height
        self.maxHeightDev = 0

        # Fill out random part of border
        self.points = []
        dx = (model.dx() - (2 * model.buffer)) / num_vertices
        x = model.x
        while x <= (model.xMax - model.buffer):
            y = random.gauss(avg_height, 5)

            # Update max height deviation
            height_diff = abs(avg_height - y)
            if height_diff > self.maxHeightDev:
                self.maxHeightDev = height_diff

            self.points.append(Point(x, y))
            x += dx

            # Add points at the "base" of the shape (so that it's no longer a line
            # self.points.append

    def draw(self):
        self.poly = Polygon(self.points).draw(self.window)
        self.poly.setFill(self.color)
        self.poly.setOutline(self.lineColor)


class Mito(object):
    # Properties that all Mito objects will share
    mitoWidth = 50
    mitoHeight = 10
    currentHeights = []
    currentWidths = []
    container = Container(0, 0, 0, 0, 0)
    defaultDx = 0
    colors = ["aquamarine", "blue violet", "chartreuse", "dark cyan", "dark slate blue",
              "dark turquoise", "deep sky blue", "dark green", "forest green",
              "light blue", "medium sea green"]

    def __init__(self, window):
        # Randomly set whether Mito will be on the right or left side
        self.onRight = (False, True)[random.randrange(0, 2)]  # 1 = right, 0 = left

        # Not drawn by default
        self.color = Mito.colors[random.randrange(0, len(Mito.colors))]
        self.drawn = False
        self.oval = None
        self.window = window

    # Mito has a 1/chance odds to be drawn
    def randDraw(self, chance):
        if random.randrange(0, chance) == 0:
            self.draw()
        return self.drawn

    def draw(self):
        # Set x position
        if self.onRight:
            x = Mito.container.xMax
        else:
            x = Mito.container.x

        # Set y position
        y = -1
        validHeight = True
        minHeight = Mito.container.y + Mito.mitoHeight / 2
        maxHeight = Mito.container.yMax - Mito.mitoHeight / 2
        counter = 0 # Keep maximum iterations to 10
        while ((not (minHeight <= y <= maxHeight)) or (not validHeight)) and counter < 10:
            validHeight = True
            y = round(random.gauss(Mito.container.y + Mito.container.dy() / 2, 30), 2)
            # Check that height is valid
            for height in Mito.currentHeights:
                if (height - Mito.mitoHeight) <= y <= (height + Mito.mitoHeight):
                    validHeight = False
                    break
            counter += 1
        # Quit if maximum iterations was reached
        if counter >= 10:
            self.drawn = False
            return
        #Mito.currentHeights.append(y)

        # Initial two points for Mito oval
        self.p1 = Point(x - Mito.mitoWidth / 2, y - Mito.mitoHeight / 2)
        self.p2 = Point(x + Mito.mitoWidth / 2, y + Mito.mitoHeight / 2)
        self.mid = Line(self.p1, self.p2).getCenter()

        Mito.currentHeights.append(self.mid.getY())
        Mito.currentWidths.append(self.mid.getX())

        # Initial dx
        # Mito closer to the center will move faster
        mid_height = Mito.container.mid.getY()
        if mid_height == self.mid.getY():
            ratio = 0
        else:
            ratio = abs(Mito.container.mid.getY() - self.mid.getY()) / Mito.container.mid.getY()
        self.dx = Mito.defaultDx * (1 - ratio)

        self.oval = Oval(self.p1, self.p2)
        self.oval.draw(self.window)
        self.oval.setFill(self.color)
        self.drawn = True

    # Move mito oval and update its points
    def move(self):
        self.updateVelocity()

        dist = self.dx
        if self.onRight:
            dist = -1 * self.dx

        width = self.mid.getX()
        if width in Mito.currentWidths:
            Mito.currentHeights.remove(self.mid.getY())
            Mito.currentWidths.remove(width)

        self.oval.move(dist, 0)
        self.p1 = self.oval.getP1()
        self.p2 = self.oval.getP2()
        self.mid = Line(self.p1, self.p2).getCenter()

        Mito.currentWidths.append(self.mid.getX())
        Mito.currentHeights.append(self.mid.getY())

    def checkEnd(self):
        if not (Mito.container.x <= self.mid.getX() <= Mito.container.xMax):
            self.undraw()
            return True
        else:
            return False

    def undraw(self):
        self.oval.undraw()
        height = self.mid.getY()
        if height in Mito.currentHeights:
            Mito.currentHeights.remove(height)
            Mito.currentWidths.remove(self.mid.getX())

    def updateVelocity(self):
        # Default randomly changed movement speed
        self.dx += random.gauss(0, 0.0005)

        current_width = self.mid.getX()
        min_width = current_width - Mito.mitoWidth
        max_width = current_width + Mito.mitoWidth

        # Check if mito is near other mitos
        for (idx, width) in enumerate(Mito.currentWidths):
            if (width != current_width) and (min_width <= width <= max_width):
                print("Close")
                current_height = self.mid.getY()
                other_height = Mito.currentHeights[idx]
                if abs(current_height - other_height) <= Mito.mitoHeight * 2:
                    print("Slowing")
                    self.dx -= random.gauss(0, 0.01)




