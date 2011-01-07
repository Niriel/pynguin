"""
Created on Nov 27, 2010

@author: Niriel
"""

import pygame
from window import Window

__all__ = ['Screen']

class Screen(Window):
    """A screen is a window that takes the display as drawing surface."""

    BG_COLOR = (255, 255, 255)

    def _createImage(self):
        """Set the display surface as its own surface."""
        self.image = pygame.display.get_surface()
        self.rect = self.image.get_rect()
        self.drawable_image = self.image
