"""
Created on Nov 25, 2010

@author: Niriel
"""
import unittest
import pygame
from pynguin.sprite import guisprite

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Disabling the warning about calling a 'protected' member of the class (name
# starting with underscore).  I don't care, I'm allowed to do that in a test
# suite.

class TestGuiSprite(unittest.TestCase):
    """Test the guisprite module."""
    def testGuiSpriteInit(self):
        """GuiSprite.__init__ does its job."""
        sprite = guisprite.GuiSprite()
        self.assertEquals(sprite.rect, pygame.Rect(0, 0, 0, 0))
        self.assertEquals(sprite.image, None)
        self.assertTrue(sprite.drawable_image is sprite.image)
        self.assertEquals(sprite.SURFACE_FLAGS, 0)
        self.assertEquals(sprite.BG_COLOR, (32, 32, 32, 255))

    def testCreateImage(self):
        """GuiSprite._createImage allocates a Surface with the right size."""
        sprite = guisprite.GuiSprite()
        sprite.rect.size = (8, 16)

        sprite._createImage()
        self.assertTrue(sprite.drawable_image is sprite.image)
        image = sprite.image
        self.assertEquals(image.get_size(), (8, 16))

    def testGetSpritesAt(self):
        """GuiSprite.getSpritesAt returns [self] if pos within, otherwise [].

        """
        sprite = guisprite.GuiSprite()
        sprite.rect = pygame.Rect(100, 200, 50, 50)
        self.assertEquals(sprite.getSpritesAt((0, 0)), [])
        self.assertEquals(sprite.getSpritesAt((125, 225)), [sprite])

    def testDrawBackground(self):
        """GuiSprite._drawBackground fills the surface with the bg color."""
        sprite = guisprite.GuiSprite()
        sprite.rect = pygame.Rect(100, 200, 50, 50)
        sprite._createImage()
        self.assertEquals(sprite.image.get_at((25, 25)), (0, 0, 0))
        sprite._drawBackground()
        self.assertEquals(sprite.image.get_at((25, 25)), sprite.BG_COLOR)

    def testDraw(self):
        """GuiSprite._draw calls _drawBackground."""
        sprite = guisprite.GuiSprite()
        sprite.rect = pygame.Rect(100, 200, 50, 50)
        sprite._createImage()
        self.assertEquals(sprite.image.get_at((25, 25)), (0, 0, 0))
        sprite._draw()
        self.assertEquals(sprite.image.get_at((25, 25)), sprite.BG_COLOR)

    def testUpdateFromNone(self):
        """GuiSprite.update calls _createImage if image is None."""
        sprite = guisprite.GuiSprite()
        sprite.rect = pygame.Rect(100, 200, 50, 50)
        self.assertTrue(sprite.image is None)
        sprite.update()
        self.assertFalse(sprite.image is None)

    def testUpdateFromOtherSize(self):
        """GuiSprite.update calls _createImage if image has wrong size."""
        sprite = guisprite.GuiSprite()
        sprite.rect = pygame.Rect(100, 200, 50, 50)
        sprite._createImage()
        image_before = sprite.image
        sprite.rect = pygame.Rect(100, 200, 100, 50)
        sprite.update()
        image_after = sprite.image
        self.assertFalse(image_before is image_after)

    def testUpdateFromSameSize(self):
        """GuiSprite.update doesn't call _createImage if image has same size.

        """
        sprite = guisprite.GuiSprite()
        sprite.rect = pygame.Rect(100, 200, 50, 50)
        sprite._createImage()
        image_before = sprite.image
        sprite.update()
        image_after = sprite.image
        self.assertTrue(image_before is image_after)

    def testUpdateDraw(self):
        """GuiSprite.update calls _draw."""
        sprite = guisprite.GuiSprite()
        sprite.rect = pygame.Rect(100, 200, 50, 50)
        sprite.update()
        self.assertEquals(sprite.image.get_at((25, 25)), sprite.BG_COLOR)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
