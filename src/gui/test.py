'''
Created on Nov 29, 2010

@author: delforge
'''

import pygame
from gui.layout import Cell
from gui.widget import Screen, Window, Label, HBox, VBox

EVENT_QUIT = pygame.QUIT

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 200

pygame.init()

pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 30)
font_big = pygame.font.Font(None, 50)

screen = Screen()
window = Window()
vbox = VBox(16, True)
hbox = HBox(16, True)
label0 = Label(font, "Hello")
label1 = Label(font_big, "super happy")
label2 = Label(font, "world!")
screen.addChild(window)
window.addChild(vbox, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING, 8)
vbox.addChild(label0, Cell.EXPAND_PADDING, Cell.EXPAND_PADDED )
vbox.addChild(hbox,   Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
hbox.addChild(label1, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
hbox.addChild(label2, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)

screen.negotiateSize()
screen.update()

print hbox.cells[1].requested_size
print hbox.cells[1].allocated_size
print label2.requested_size
print label2.allocated_size

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(30)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == EVENT_QUIT:
            running = False
print "Quitting..."
pygame.quit()
