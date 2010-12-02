'''
Created on Nov 25, 2010

@author: delforge
'''
import unittest
import guisprite
import gui.size
import pygame

class TestGuiSprite(unittest.TestCase):
    def testGuiSpriteInit(self):
        """GuiSprite.__init__ does its job."""
        s = guisprite.GuiSprite()
        self.assertEquals(s.rect, pygame.Rect(0,0,0,0))
        self.assertEquals(s.image, None)

    def testCreateImage(self):
        """GuiSprite._createImage allocates a Surface with the right size."""
        sp = guisprite.GuiSprite()
        sp.rect.size = (8, 16)
        sp._createImage()
        image = sp.image
        self.assertEquals(image.get_size(), (8, 16))

    def testAdjustRect(self):
        """GuiSprite.adjustRect adapts the rect to the allocated_size."""
        s = guisprite.GuiSprite()
        s.rect = pygame.Rect(0, 0, 0, 0)
        s.allocated_size = gui.size.SizeAllocation(10, 20, 30, 40)
        s.adjustRect()
        self.assertEquals(s.rect, pygame.Rect(10, 20, 30, 40))

    def testGetSpritesAt(self):
        """GuiSprite.getSpritesAt returns [self] if pos within, otherwise [].
        
        """
        sp = guisprite.GuiSprite()
        sp.rect = pygame.Rect(100, 200, 50, 50)
        self.assertEquals(sp.getSpritesAt((0, 0)), [])
        self.assertEquals(sp.getSpritesAt((125, 225)), [sp])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
