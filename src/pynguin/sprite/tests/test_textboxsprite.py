#! /usr/bin/python
"""
Created on Jan 10, 2011

@author: Niriel
"""

import unittest
import pygame
from pynguin.sprite import textboxsprite

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.


class Test(unittest.TestCase):
    """Test the sprite.textboxsprite module."""
    def setUp(self):
        """Prepare pygame so that we can use fonts."""
        pygame.init()

    def tearDown(self):
        """Shut down pygame."""
        pygame.quit()

    def testInit(self):
        """TextBoxSprite.__init__ sets mode to 'normal'."""
        my_sprite = textboxsprite.TextBoxSprite()
        # Cannot test on identity here because of wrapper for bound methods. Or
        # so I think.
        self.assertEquals(my_sprite._draw_function, my_sprite._drawNormal)

    def testSetMode(self):
        """TextBoxSprite.setMode accepts 'normal' and 'edit'."""
        my_sprite = textboxsprite.TextBoxSprite()
        my_sprite.setMode('edit')
        self.assertEquals(my_sprite._draw_function, my_sprite._drawEdit)
        my_sprite.setMode('normal')
        self.assertEquals(my_sprite._draw_function, my_sprite._drawNormal)
    
    # pylint: disable-msg=R0201
    # No references to 'self' in the next tests.
    def testDrawNormal(self):
        """TextBoxSprite._drawNormal doesn't crash."""
        font = pygame.font.Font(None, 16)
        my_sprite = textboxsprite.TextBoxSprite()
        my_sprite.font = font
        my_sprite.text = "Hello"
        my_sprite.rect.size = my_sprite.getTextSize()
        my_sprite._createImage()
        my_sprite._drawNormal()

    def testDrawEdit(self):
        """TextBoxSprite._drawEdit doesn't crash."""
        font = pygame.font.Font(None, 16)
        my_sprite = textboxsprite.TextBoxSprite()
        my_sprite.font = font
        my_sprite.text = "Hello"
        my_sprite.rect.size = my_sprite.getTextSize()
        my_sprite._createImage()
        my_sprite._drawEdit()
    # pylint: enable-msg=R0201

if __name__ == "__main__":
    unittest.main()
