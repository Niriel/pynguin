'''
Created on Nov 29, 2010

@author: Niriel
'''

import pygame
from gui.layout import Cell
from gui.widget import Screen, Label, HBox, VBox, Scroll, Button, TextBox
from gui.widget import windowmanager

EVENT_QUIT = pygame.QUIT

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    pygame.init()

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 30)
    font_big = pygame.font.Font(None, 50)

    screen = Screen()
    window = Scroll()
    vbox = VBox(16, True)
    hbox = HBox(16, True)
    label0 = Label(font, "Hello")
    label1 = Label(font_big, "super happy")
    button = Button()
    label2 = Label(font, "world!")
    textbox = TextBox(font)
    screen.addChild(window)
    window.addChild(vbox, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING, 8)
    vbox.addChild(label0, Cell.EXPAND_PADDING, Cell.EXPAND_PADDED)
    vbox.addChild(hbox, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
    hbox.addChild(label1, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
    hbox.addChild(button, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
    button.addChild(label2, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING, 8)
    vbox.addChild(textbox, Cell.EXPAND_PADDED, Cell.EXPAND_PADDING, 8)

    textbox._text = "sadjlpfADF"
    textbox._drawText = textbox._drawTextEdit

    screen.negotiateSize()
    print window.allocated_size
    windowmanager.ResizeToFitInto(window, screen)

    button.setMode(Button.MODE_INACTIVE)
    screen.update()
    import random

    running = True
    clock = pygame.time.Clock()
    x, dx = 1, 1
    while running:
        screen.batchUpdate(False)
        pygame.display.flip()
        screen.batchUpdate(True)
        clock.tick()
        button.setMode(random.randrange(4))
        label1.setText("%i FPS" % int(round(clock.get_fps())))
        window.tryScrollTo(x, 0)
        x += dx
        if x >= 300 or x <= 0:
            dx = -dx
        for event in pygame.event.get():
            if event.type == EVENT_QUIT:
                running = False
    print "Quitting..."
    pygame.quit()

if __name__ == '__main__':
    import cProfile as profile
    if False:
        profile.run('main()')
    else:
        main()