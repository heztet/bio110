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
    mitos = []
    currentHeights = []
    currentWidths = []
    container = Container(0, 0, 0, 0, 0)
    defaultDx = 0
    colors = ["aquamarine", "blue violet", "chartreuse", "dark cyan", "dark slate blue",
              "dark turquoise", "deep sky blue", "dark green", "forest green",
              "light blue", "medium sea green"]
    showCollisions = False

    def __init__(self, window):
        # Not drawn by default
        self.onRight = None
        self.p1 = None
        self.p2 = None
        self.mid = None
        self.color = Mito.colors[random.randrange(0, len(Mito.colors))]
        self.drawn = False
        self.oval = None
        self.window = window
        self.hasCollision = False
        self.dx = Mito.defaultDx

    # Create num amount of Mito objects in the mitos array
    @staticmethod
    def create(num, window):
        for i in range(0, num):
            Mito.mitos.append(Mito(window))

    # Check each mito object to see if it's near other mitos
    @staticmethod
    def checkCollisions():
        for curr_i, curr_m in enumerate(Mito.mitos):
            # Continue if we already know it's near other mitos
            if not curr_m.drawn:
                continue

            # Check if mito is near other mitos
            no_collisions = True
            for (check_i, check_m) in enumerate(Mito.mitos):
                if (check_i == curr_i) or (not check_m.drawn):
                    continue
                # X-coordinate check
                if abs(curr_m.mid.getX() - check_m.mid.getX()) <= Mito.mitoHeight * 2:
                    # Y-coordinate check
                    if abs(curr_m.mid.getY() - check_m.mid.getY()) <= Mito.mitoHeight * 2:
                        no_collisions = False
                        Mito.mitos[curr_i].hasCollision = True
                        Mito.mitos[check_i].hasCollision = True

            if no_collisions:
                Mito.mitos[curr_i].hasCollision = False

    # Mito has a 1/chance odds to be drawn
    def randDraw(self, chance):
        if random.randrange(0, chance) == 0:
            self.draw()
        return self.drawn

    def draw(self):
        # Randomly set whether Mito will be on the right or left side
        self.onRight = (False, True)[random.randrange(0, 2)]  # 1 = right, 0 = left

        self.hasCollision = False

        # Set x position
        if self.onRight:
            x = Mito.container.xMax
        else:
            x = Mito.container.x

        # Set y position
        y = -1
        valid_height = True
        minHeight = Mito.container.y + Mito.mitoHeight / 2
        max_height = Mito.container.yMax - Mito.mitoHeight / 2
        counter = 0  # Keep maximum iterations to 10
        while (not (minHeight <= y <= max_height) or not valid_height) and counter < 10:
            valid_height = True
            y = round(random.gauss(Mito.container.y + Mito.container.dy() / 2, 30), 2)
            # Check that height is valid
            for height in Mito.currentHeights:
                if (height - Mito.mitoHeight) <= y <= (height + Mito.mitoHeight):
                    valid_height = False
                    break
            counter += 1
        # Quit if maximum iterations was reached
        if counter >= 10:
            self.drawn = False
            return

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

    # Undraw a mito if it's out of bounds
    # Return whether the mito was undrawn
    def checkEnd(self):
        if not (Mito.container.x <= self.mid.getX() <= Mito.container.xMax):
            self.undraw()
            return True
        else:
            return False

    # Undraw mito oval and remove from current height/width
    def undraw(self):
        self.oval.undraw()
        height = self.mid.getY()
        width = self.mid.getX()
        if height in Mito.currentHeights:
            Mito.currentHeights.remove(height)
        if width in Mito.currentWidths:
            Mito.currentWidths.remove(width)

    # Always a positive velocity, since move() will handle the direction
    def updateVelocity(self):
        # Default randomly changed movement speed
        self.dx += random.gauss(0, 0.0005)

        # Decrease velocity if near other mito
        if self.hasCollision:
            self.dx -= abs(random.gauss(0, 0.01))

        if Mito.showCollisions:
            self.oval.setFill(["green", "red"][self.hasCollision])

        # Guarantee a positive velocity
        self.dx = abs(self.dx)
