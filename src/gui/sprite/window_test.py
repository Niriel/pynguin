'''
Created on Nov 27, 2010

@author: Niriel
'''
import unittest
import pygame
import window
import guisprite

class windowTest(unittest.TestCase):
    def testInit(self):
        """window.__init__ does its job."""
        w = window.Window()
        self.assertEquals(w._group.__class__.__name__, 'LayeredUpdates')
    
    def testGetSpritesAt(self):
        """window.getSpritesAt return clicked children and itself."""
        w1 = window.Window()
        c1 = guisprite.GuiSprite()
        c2 = guisprite.GuiSprite()
        w2 = window.Window()
        c3 = guisprite.GuiSprite()
        #
        w1.rect = pygame.Rect((200, 100), (300, 150))
        c1.rect = pygame.Rect((10, 20), (50, 30))
        c2.rect = pygame.Rect((20, 30), (50, 30))
        w2.rect = pygame.Rect((240, 90), (50, 50))
        c3.rect = pygame.Rect((10, 10), (10, 10))
        # Notice that c1 and c2 overlap.
        w1._group.add([c1, c2, w2])
        w2._group.add(c3)
        #
        self.assertEquals(w1.getSpritesAt((0, 0)), [])
        self.assertEquals(w1.getSpritesAt((200, 100)), [w1])
        self.assertEquals(w1.getSpritesAt((215, 125)), [w1, c1])
        self.assertEquals(w1.getSpritesAt((225, 135)), [w1, c1, c2])
        self.assertEquals(w1.getSpritesAt((440, 190)), [w1, w2])
        self.assertEquals(w1.getSpritesAt((450, 200)), [w1, w2, c3])

if __name__ == '__main__':
    unittest.main()
