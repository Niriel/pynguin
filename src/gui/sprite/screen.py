'''
Created on Nov 27, 2010

@author: Niriel
'''

import pygame
from window import Window

__all__ = ['Screen']

class Screen(Window):
    BG_COLOR = (255, 255, 255)
    def _createImage(self):
        self.image = pygame.display.get_surface()
        self.rect = self.image.get_rect()
        print self.rect
        self.drawable_image = self.image
