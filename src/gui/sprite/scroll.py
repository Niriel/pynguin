'''Sprites that have a content bigger than what they display, and can scroll.

Created on Dec 1, 2010

@author: Niriel

A Scroll is a GuiSprite that has two separate images :
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

'''
import pygame
from window import Window

__all__ = ['Scroll']

class Scroll(Window):
    def __init__(self):
        Window.__init__(self)
        self.big_image = None
        self.big_rect = pygame.Rect(0, 0, 0, 0)
        self.visible_rect = pygame.Rect(0, 0, 0, 0)

    def _createImage(self):
        self.image = pygame.Surface(self.rect.size, flags=self.SURFACE_FLAGS)
        self.big_image = pygame.Surface(self.big_rect.size, flags=self.SURFACE_FLAGS)
        self.drawable_image = self.big_image

    def _draw(self):
        self._drawBackground()
        self._drawSprites()
        self._drawVisiblePart()

    def _drawVisiblePart(self):
        self.image.blit(self.big_image, (0, 0), self.visible_rect)
