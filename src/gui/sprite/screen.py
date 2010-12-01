'''
Created on Nov 27, 2010

@author: Niriel
'''

import pygame
from window import Window

__all__ = ['Screen']

class Screen(Window):
    BG_COLOR = (237, 236, 235)
    def __init__(self):
        Window.__init__(self)
        self.update()

    def update(self):
        self.image = pygame.display.get_surface()
        self.rect = self.image.get_rect()
        Window.update(self)

