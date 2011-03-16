"""
Created on Nov 29, 2010

@author: Niriel
"""

import pygame
from pynguin.widget import *

EVENT_QUIT = pygame.QUIT

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def main():
    pygame.init()

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.Font(None, 30)
    #font_big = pygame.font.Font(None, 50)

    screen = ScreenWidget()
    screen.altitude = 0
    box = VBoxWidget(0, True)
    label_hello = LabelWidget(font, "Hello,")
    label_world = LabelWidget(font,  "world !")
    screen.addChild(box, 'padded', 'padded')
    box.addChild(label_hello, 'end', 'padding', 'padding')
    box.addChild(label_world, 'end', 'padded', 'padded')
    screen.dispatchDisplayers()
    screen.negotiateSize(True)
    screen._sprite.update()
    print label_hello.altitude
    running = True
    clock = pygame.time.Clock()
    while running:
        pygame.display.flip()
        clock.tick(100)
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
