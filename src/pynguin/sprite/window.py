'''
Created on Nov 26, 2010

@author: Niriel
'''

import pygame
from guisprite import GuiSprite

__all__ = ['Window']

class Window(GuiSprite):
    """A Window is a Sprite that draws other sprites onto itself.

    The Window has a pygame sprite group that it uses to display widgets
    on its surface.

    This is handy:

    - since the window has its own surface we make sure we never draw outside
    of the window ;

    - when a LayeredUpdate group is needed, there is no layer competition
    between the windows anymore, each windows has its own.

    - the coordinates of the widgets contained in the windows are relative to
    the window itself, not the screen.  It just makes things easier by reducing
    maintenance when a window is moved.

    """

    BG_COLOR = (235, 235, 235)
    SPRITES_GROUP_CLS = pygame.sprite.LayeredUpdates

    def __init__(self):
        GuiSprite.__init__(self)
        self.sprites_group = self.SPRITES_GROUP_CLS()

    def update(self):
        """Refreshes the image of the window by redrawing all the sprites.

        Call this method only when you need it.  Not at every frame.

        """
        self.sprites_group.update()
        GuiSprite.update(self)

    def _draw(self):
        self._drawBackground()
        self._drawSprites()

    def _drawSprites(self):
        self.sprites_group.draw(self.drawable_image)

    def getSpritesAt(self, pos):
        if not self.rect.collidepoint(pos):
            return []
        result = [self]
        rel_pos = (pos[0] - self.rect.left, pos[1] - self.rect.top)
        sprites = self.sprites_group.get_sprites_at(rel_pos)
        for sprite in sprites:
            result += sprite.getSpritesAt(rel_pos)
        return result

    def _findDrawerOld(self):
        return self
