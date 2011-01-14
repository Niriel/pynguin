#! /usr/bin/python
"""
Created on Jan 10, 2011

@author: Niriel
"""

import unittest
import pygame
from pynguin.sprite import labelsprite

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.


class Test(unittest.TestCase):
    """Test the sprite.labelsprite module."""
    def setUp(self):
        """Prepare pygame so that we can use fonts."""
        pygame.init()

    def tearDown(self):
        """Shut down pygame."""
        pygame.quit()

    # pylint: disable-msg=R0201
    # No references to 'self' in the next tests.
    def testDraw(self):
        """LabelSprite._draw doesn't crash."""
        font = pygame.font.Font(None, 16)
        my_sprite = labelsprite.LabelSprite()
        my_sprite.font = font
        my_sprite.text = "Hello"
        my_sprite.rect.size = my_sprite.getTextSize()
        my_sprite._createImage()
        my_sprite._draw()
    # pylint: enable-msg=R0201

if __name__ == "__main__":
    unittest.main()
