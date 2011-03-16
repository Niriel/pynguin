"""
Created on Nov 27, 2010

@author: Niriel
"""
import unittest
import pygame
from pynguin.sprite import guisprite, windowsprite

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Disabling the warning about calling a 'protected' member of the class (name
# starting with underscore).  I don't care, I'm allowed to do that in a test
# suite.

class WindowTest(unittest.TestCase):
    """Test the sprite.window module."""
    def testInit(self):
        """WindowSprite.__init__ does its job."""
        win = windowsprite.WindowSprite()
        self.assertEquals(win._sprites_group.__class__.__name__,
                          'LayeredUpdates')

    def testGetSpritesAt(self):
        """WindowSprite.getSpritesAt return clicked children and itself."""
        win1 = windowsprite.WindowSprite()
        spr1 = guisprite.GuiSprite()
        spr2 = guisprite.GuiSprite()
        win2 = windowsprite.WindowSprite()
        spr3 = guisprite.GuiSprite()
        #
        win1.rect = pygame.Rect((200, 100), (300, 150))
        spr1.rect = pygame.Rect((10, 20), (50, 30))
        spr2.rect = pygame.Rect((20, 30), (50, 30))
        win2.rect = pygame.Rect((240, 90), (50, 50))
        spr3.rect = pygame.Rect((10, 10), (10, 10))
        # Notice that spr1 and spr2 overlap.
        win1._sprites_group.add([spr1, spr2, win2])
        win2._sprites_group.add(spr3)
        #
        self.assertEquals(win1.getSpritesAt((0, 0)), [])
        self.assertEquals(win1.getSpritesAt((200, 100)), [win1])
        self.assertEquals(win1.getSpritesAt((215, 125)), [win1, spr1])
        self.assertEquals(win1.getSpritesAt((225, 135)), [win1, spr1, spr2])
        self.assertEquals(win1.getSpritesAt((440, 190)), [win1, win2])
        self.assertEquals(win1.getSpritesAt((450, 200)), [win1, win2, spr3])

if __name__ == '__main__':
    unittest.main()
