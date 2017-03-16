from shapes import *
import random


def main():
    random.seed()

    # Create window
    main_window = Container(0, 600, 0, 250, 25)
    win = GraphWin("Neuron Mitochondria", main_window.xMax, main_window.yMax, autoflush=False)

    # Create label container
    label_width = 100
    labels = Container(main_window.xMax - main_window.buffer - label_width,
                       main_window.xMax - main_window.buffer,
                       main_window.y + main_window.buffer,
                       main_window.yMax - main_window.buffer,
                       10)

    # Mitochondria counter
    counter_label = Text(Point(labels.mid.getX(), labels.mid.getY() - labels.buffer), "Mitochondria")
    counter_num = Text(Point(labels.mid.getX(), labels.mid.getY() + labels.buffer), "Count: 0")
    mito_count = 0
    counter_label.draw(win)
    counter_num.draw(win)

    # Buffer values for model, label, and arrow containers
    model_label_buffer = 30
    model_arrows_buffer = 10

    # Arrows container
    arrows_height = 30
    arrows = Container(main_window.x + main_window.buffer,
                       main_window.xMax - main_window.buffer - labels.dx() - model_label_buffer,
                       main_window.yMax - main_window.buffer - arrows_height,
                       main_window.yMax - main_window.buffer,
                       10)

    # Draw arrows
    arrow_text_buffer = 15
    arrow_length = 50
    ante_text = Text(Point(arrows.x + arrows.dx() / 6, arrows.mid.getY()), "Anterograde")
    ante_text.setFill("blue")
    ante_text.draw(win)
    ante_arrow = Line(Point(ante_text.getAnchor().getX() - arrow_length / 2,
                            ante_text.getAnchor().getY() + arrow_text_buffer),
                      Point(ante_text.getAnchor().getX() + arrow_length / 2,
                            ante_text.getAnchor().getY() + arrow_text_buffer))
    ante_arrow.setArrow("last")
    ante_arrow.setWidth(4)
    ante_arrow.setFill("blue")
    ante_arrow.draw(win)

    retro_text = Text(Point(arrows.xMax - arrows.dx() / 6, arrows.mid.getY()), "Retrograde")
    retro_text.setFill("red")
    retro_text.draw(win)
    retro_arrow = Line(Point(retro_text.getAnchor().getX() + arrow_length / 2,
                             retro_text.getAnchor().getY() + arrow_text_buffer),
                       Point(retro_text.getAnchor().getX() - arrow_length / 2,
                             retro_text.getAnchor().getY() + arrow_text_buffer))
    retro_arrow.setArrow("last")
    retro_arrow.setWidth(4)
    retro_arrow.setFill("red")
    retro_arrow.draw(win)

    # Create model
    model = Container(main_window.x + main_window.buffer,
                      main_window.xMax - main_window.buffer - labels.dx() - model_label_buffer,
                      main_window.y + main_window.buffer,
                      main_window.yMax - arrows.dy() - main_window.buffer - model_arrows_buffer,
                      0)

    # Arbitrary height of both halves of neuron body
    neuron_height = model.dy() / 6

    # Draw upper part of neuron
    top_neuron = NeuronPoly(model, model.y + neuron_height, 50, win)
    top_neuron.points.append(Point(model.xMax - model.buffer, model.y))
    top_neuron.points.append(Point(model.x + model.buffer, model.y))
    top_neuron.draw()

    # Draw bottom part of neuron
    bottom_neuron = NeuronPoly(model, model.yMax - model.buffer - neuron_height, 50, win)
    bottom_neuron.points.append(Point(model.xMax - model.buffer, model.yMax))
    bottom_neuron.points.append(Point(model.x + model.buffer, model.yMax))
    bottom_neuron.draw()

    # Set up area for mito to be placed
    # Only allow mito to be within neuron edges
    Mito.container = Container(model.x + model.buffer,
                               model.xMax - model.buffer,
                               top_neuron.avgHeight + top_neuron.maxHeightDev,
                               bottom_neuron.avgHeight - bottom_neuron.maxHeightDev,
                               Mito.mitoHeight)
    Mito.defaultDx = model.dx() / 10000

    # Create mitochondria objects
    Mito.create(15, win)
    Mito.showCollisions = False

    # Run until mouse is clicked
    try:
        while not win.checkMouse():
            Mito.checkCollisions()
            for m in Mito.mitos:
                # Auto draw a mito if none are currently on screen
                if mito_count == 0:
                    if m.randDraw(1):
                        mito_count += 1
                        counter_num.setText("Count: {0}".format(mito_count))
                # Randomly choose whether to draw new mito
                elif not m.drawn:
                    if m.randDraw(10000):
                        mito_count += 1
                        counter_num.setText("Count: {0}".format(mito_count))
                # Move mito if drawn
                else:
                    m.move()
                    # Reset mito if it's crossed the neuron body
                    if m.checkEnd():
                        Mito.mitos.remove(m)
                        Mito.mitos.append(Mito(win))
                        mito_count -= 1
                        counter_num.setText("Count: {0}".format(mito_count))
            # Limit the window refresh so that adding more mito won't slow the simulation down
            update(1000)
        # Pause for click in window
        win.getMouse()
        win.close()
    except GraphicsError as err:
        if "{0}".format(err) != "checkMouse in closed window":
            print("GraphicsError: {0}".format(err))

# Run
if __name__ == "__main__":
    random.seed()
    main()
