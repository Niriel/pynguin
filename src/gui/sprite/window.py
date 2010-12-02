'''
Created on Nov 26, 2010

@author: delforge
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

    BG_COLOR = (255, 255, 255)
    SPRITE_GROUP_CLS = pygame.sprite.LayeredUpdates

    def __init__(self):
        GuiSprite.__init__(self)
        self._group = self.SPRITE_GROUP_CLS()

    def update(self):
        """Refreshes the image of the window by redrawing all the sprites.

        Call this method only when you need it.  Not at every frame.

        """
        GuiSprite.update(self)
        self._group.update()
        self.drawSprites()

    def drawSprites(self):
        self._group.draw(self.drawable_image)

    def getSpritesAt(self, pos):
        if not self.rect.collidepoint(pos):
            return []
        result = [self]
        rel_pos = (pos[0] - self.rect.left, pos[1] - self.rect.top)
        sprites = self._group.get_sprites_at(rel_pos)
        for sprite in sprites:
            result += sprite.getSpritesAt(rel_pos)
        return result
