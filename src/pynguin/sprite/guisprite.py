"""
Created on Nov 25, 2010

@author: Niriel
"""

import pygame

__all__ = ['GuiSprite']

class GuiSprite(pygame.sprite.Sprite):
    """Ancestor of all sprite using the PYnGUIn system.

    This class is abstract.  Please use its descendants.

    """
    SURFACE_FLAGS = 0
    BG_COLOR = (32, 32, 32, 255)

    def __init__(self):
        """Initialize a new GuiSprite."""
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.drawable_image = self.image

    def _createImage(self):
        """Create a new pygame.Surface object for this sprite.

        The size of the image is taken from the rect.  Therefore the rect
        must be up-to-date.

        """
        # pylint: disable-msg=E1123,E1121
        self.image = pygame.Surface(self.rect.size, flags=self.SURFACE_FLAGS)
        self.drawable_image = self.image

    def _drawBackground(self):
        """Fill the drawable_image attribute with the solid color BG_COLOR."""
        self.drawable_image.fill(self.BG_COLOR)

    def _draw(self):
        """Draw this sprite.

        This method is likely to be overridden in subclasses.

        """
        self._drawBackground()

    def update(self):
        """(Re)create the sprite image from scratch.

        This method does two things:

        1. call _createImage if there is no image or if the size of the image
           does not match the size of the attribute rect.
        2. call _draw.

        Overload this method to suit your needs (for example containers should
        call update on their children first).  Do not forget to include a call
        to this method when you overload in order to take advantage of the
        point 1) explained above.  Note that you can also simply overload _draw
        if that's enough for you.

        Call this method only when you need it.  Not at every frame.

        """
        if not self.image or self.image.get_size() != self.rect.size:
            self._createImage()
        self._draw()

    def getSpritesAt(self, pos):
        """Return [itself] if the given position is within rect.  Otherwise [].

        This function returns a list in order to be compatible with drawer
        sprites: sprites that contain and draw other sprites onto themselves
        (like a window).  In that case, the window has to return itself and
        also return the button at the position pos.  We end up with a list of
        all the widgets, ordered by depth.

        """
        return [self] if self.rect.collidepoint(pos) else []
