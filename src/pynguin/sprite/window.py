#! /usr/bin/python
"""
Created on Nov 26, 2010

@author: Niriel
"""

import pygame
from guisprite import GuiSprite

__all__ = ['Window']

class WindowError(RuntimeError):
    """Base class for exceptions in the window module."""

class SpriteNotInGroupError(WindowError):
    """Raised when removing a sprite that is not part of the group."""

class SpriteAlreadyInGroupError(WindowError):
    """Raised when adding a sprite that was already added."""

class Window(GuiSprite):
    """A Window is a Sprite that draws other sprites onto itself.

    The Window has a pygame sprite group that it uses to display widgets
    on its surface.

    This is handy:

    * since the window has its own surface we make sure we never draw outside
      of the window ;
    * when a LayeredUpdate group is needed, there is no layer competition
      between the windows anymore: each windows has its own.
    * the coordinates of the widgets contained in the windows are relative to
      the window itself, not the screen.  It makes things easier by reducing
      maintenance when a window is moved.

    """

    BG_COLOR = (235, 235, 235)

    def __init__(self):
        GuiSprite.__init__(self)
        self._sprites_group = pygame.sprite.LayeredUpdates()

    def _drawSprites(self):
        """Draw the contained sprites onto itself.

        Warning: this DOES NOT call the method _draw of the sprites of the
        _sprites_group.  It draws them as they are.

        """

        self._sprites_group.draw(self.drawable_image)

    def _draw(self):
        """Draw the window onto its own surface: background and sprites.

        Warning: this DOES NOT call the method _draw of the sprites of the
        _sprites_group.  It draws them as they are.

        """
        GuiSprite._draw(self)
        self._drawSprites()

    def update(self):
        """(Re)create the sprite image from scratch.

        Starts by calling update() on all the sprites of _sprites_group.

        Call this method only when you need it.  Not at every frame.

        """
        self._sprites_group.update()
        GuiSprite.update(self)

    def getSpritesAt(self, pos):
        """Return a list of all the contained sprites at pos, including self.

        The sprites are returned from bottom to top.

        """
        if not self.rect.collidepoint(pos):
            return []
        result = [self]
        rel_pos = (pos[0] - self.rect.left, pos[1] - self.rect.top)
        sprites = self._sprites_group.get_sprites_at(rel_pos)
        for sprite in sprites:
            result += sprite.getSpritesAt(rel_pos)
        return result

    def moveToFront(self, sprite):
        """Bring the provided sprite to the top of the top layer."""
        self._sprites_group.move_to_front(sprite)

    def moveToBack(self, sprite):
        """Bring the provided sprite to the bottom of the bottom layer."""
        self._sprites_group.move_to_back(sprite)

    def addSprite(self, sprite, layer):
        """Add the given sprite to the given layer of sprite group."""
        if self._sprites_group.has(sprite):
            msg = "Sprite already in group, cannot add twice."
            raise SpriteAlreadyInGroupError(msg)
        self._sprites_group.add(sprite, layer=layer)

    def removeSprite(self, sprite):
        """Remove the given sprite from the window sprite group."""
        if not self._sprites_group.has(sprite):
            msg = "Cannot remove a sprite that is not in the group."
            raise SpriteNotInGroupError(msg)
