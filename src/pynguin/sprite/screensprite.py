"""
Created on Nov 27, 2010

@author: Niriel
"""

import pygame
from windowsprite import WindowSprite

__all__ = ['ScreenSprite']

class ScreenSprite(WindowSprite):
    """A screen is a window that takes the display as drawing surface."""

    BG_COLOR = (255, 255, 255)

    def _createImage(self):
        """Set the display surface as its own surface."""
        self.image = pygame.display.get_surface()
        self.rect = self.image.get_rect()
        self.drawable_image = self.image

    def getDisplaySize(self):
        """Return the size of the display."""
        return pygame.display.get_surface().get_rect().size
