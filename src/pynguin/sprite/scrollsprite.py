#! /usr/bin/python
"""Sprites that have a content bigger than what they display, and can scroll.

Created on Dec 1, 2010

@author: Niriel

A ScrollSprite is a GuiSprite that has two separate images :
  - the image it displays on the screen ;
  - the image it draws its widgets on.
The first is a subset of the second.

The idea behind this is to implement the usual scrollable windows/panels.

The 'real' image is bigger than the displayed image, and by scrolling we can
select which portion of the big image is displayed on the screen.

Along with the two images, two rectangles are needed:
  - the rectangle setting the position and space occupied by the visible image,
  - the rectangle defining the visible portion of the big image.


Naming the images.
------------------

Because of the way sprites work, the image that will be shown on the screen
has to be called "image".  The other image, bigger, will be called big_image.

big_image can never be smaller than image, in any direction.


Naming the rects.
-----------------

The rect determining the position of the sprite has to be called "rect".  The
rect defining the shape of big_image is called "big_rect".  The rect delimiting
the portion of big_image to blit onto image is called "visible_rect".

"""

import pygame
from windowsprite import WindowSprite

__all__ = ['ScrollSprite']

class ScrollSprite(WindowSprite):
    """ScrollSprite is a window that only displays a part of itself."""
    def __init__(self):
        """Initialize a new ScrollSprite."""
        WindowSprite.__init__(self)
        self.big_image = None
        self.big_rect = pygame.Rect(0, 0, 0, 0)
        self.visible_rect = pygame.Rect(0, 0, 0, 0)

    def _createImage(self):
        """Create two images: the visible one and the drawable one."""
        # pylint: disable-msg=E1123,E1121

        self.image = pygame.Surface(self.rect.size, flags=self.SURFACE_FLAGS)
        self.big_image = pygame.Surface(self.big_rect.size,
                                        flags=self.SURFACE_FLAGS)
        self.drawable_image = self.big_image

    def _drawVisiblePart(self):
        """Draw the visible part of the big image onto the visible image.

        Note that NO check is done to make sure that the position of the
        visible part of the big image is within the boundaries of the big
        image.  Anything that is outside the boundaries will appear background-
        colored.

        """
        self.visible_rect.size = self.rect.size # Just to make sure.
        self.image.blit(self.big_image, (0, 0), self.visible_rect)

    def _draw(self):
        """Draw the scroll.

        1. Draw the background and the sprites on the drawable image.  That's
           what Window._draw() does.
        2. Draw a part of the drawable image on the visible one.

        """
        WindowSprite._draw(self)
        self._drawVisiblePart()

    def scrollTo(self, pos_x, pos_y):
        """Select the position of the portion of the big image to display.

        Note that NO check is done to make sure that the position is within
        the boundaries of the big image.  Anything that is outside the
        boundaries will appear background-colored.

        """
        self.visible_rect.topleft = (pos_x, pos_y)
