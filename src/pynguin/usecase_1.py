"""
Created on Feb 07, 2011.

@author: Niriel

This use case shows how to modify the appearance and sizes of widgets.  The GUI
must adapt itself automatically.

"""

import random
import pygame
import pynguin

EVENT_QUIT = pygame.QUIT

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MAX_FPS = 100

def CreateGui():
    font = pygame.font.Font(None, 30)
    font_big = pygame.font.Font(None, 50)

    # The order in which I declare does not matter.
    display = pynguin.DisplayWidget()
    # Note that having several displays is technichally allowed, even if I
    # don't know what to do with that.  They're all going to write stuff on the
    # same pygame display, resulting in overlapping things.  I accept that it
    # can fuck up things.
    board = pynguin.BoardWidget()
    window = pynguin.WindowWidget()
    vbox = pynguin.VBoxWidget(0, False)
    hbox = pynguin.HBoxWidget(8, True)
    label_hello = pynguin.LabelWidget(font_big, "Hello.")
    window.position = (200, 100)
    window.max_requested_size = (400, 200)
    button = pynguin.ButtonWidget()
    button_label = pynguin.LabelWidget(font, "Click me.")
    text_input = pynguin.TextInputWidget(font, "Type here.")

    # The order in which we add widgets to parents does not matter.
    # Except in the vbox of course since this one has an intrinsic order.
    display.addChild(board, 'widget', 'widget')
    vbox.addChild(label_hello, 'end', 'not', 'not')
    board.addChild(window) # Padding has no meaning in a board.
    window.addChild(vbox, 'widget', 'widget')
    button.addChild(button_label)
    hbox.addChild(button, 'end', 'not', 'widget', (16, 8))
    vbox.addChild(hbox, 'end', 'not', 'not')
    hbox.addChild(text_input, 'beginning', 'widget', 'padding')
    # I expect that all this adding and removal of widgets is properly
    # registered so that the call to `pynguin.update()` (see below) does all
    # the drawing and registering for me.

    return button, text_input

def main():
    pygame.init()

    # Note : the DisplayWidget does NOT take care of the creation of the
    # display area.  I do not want the GUI to force me to change anything to
    # my code.

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    button, text_input = CreateGui()

    running = True
    clock = pygame.time.Clock()
    while running:
        # I expect the GUI to have to update itself once per frame at max.
        # If `pynguin.update` has nothing to do then it return immediately.
        # In this usecase, the GUI is not modified after the initial creation
        # so `pynguin.update` will do something only the first time.
        pynguin.update()
        pygame.display.flip()
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == EVENT_QUIT:
                running = False
        # Modify the appearance of the GUI.
        if random.randrange == 0:
            # Modify the appearance.
            button.mode = random.choice(['normal', 'clicked'])
        if random.randrange == 0:
            # Modify the size.
            # That should also change the size of the window.
            text_input.text = str(random.randrange(9999999)) * random.randrange(10)
        text_input

    print "Quitting..."
    pygame.quit()


if __name__ == '__main__':
    main()
