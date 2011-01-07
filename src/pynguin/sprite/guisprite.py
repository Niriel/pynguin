'''
Created on Nov 25, 2010

@author: Niriel
'''

import pygame

__all__ = ['GuiSprite']

class GuiSprite(pygame.sprite.Sprite):
    SURFACE_FLAGS = 0
    BG_COLOR = (32, 32, 32, 255)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.drawable_image = self.image

    def update(self):
        """Redraw the sprite.

        This method does two things:
        1) call _createImage if there is no image or if the size of the image
           does not match the size of the attribute rect.
        2) call drawBackgound.

        Overload this method to suit your need.  Do not forget to include a
        call to this method when you overload in order to take advantage of the
        point 1) explained above.  Note that you can also simply overload
        _drawBackground if that's enough for you.

        Call this method only when you need it.  Not at every frame.

        """
        if not self.image or self.image.get_size() != self.rect.size:
            self._createImage()
        self._draw()

    def _createImage(self):
        """Create a new pygame.Surface object for this sprite.

        The size of the image is taken from the rect.  Therefore the rect
        must be up-to-date.

        """
        self.image = pygame.Surface(self.rect.size, flags=self.SURFACE_FLAGS)
        self.drawable_image = self.image

    def _drawBackground(self):
        """Fill the image property with the solid color BG_COLOR."""
        self.drawable_image.fill(self.BG_COLOR)

    def _draw(self):
        self._drawBackground()

    def getSpritesAt(self, pos):
        return [self] if self.rect.collidepoint(pos) else []
