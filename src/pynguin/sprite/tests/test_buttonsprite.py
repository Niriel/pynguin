#! /usr/bin/python
"""
Created on Jan 10, 2011

@author: Niriel
"""

import unittest
from pynguin.sprite import buttonsprite

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.


class TestButtonSprite(unittest.TestCase):
    """Test the sprite.buttonsprite module."""
    def testInit(self):
        """ButtonSprite.__init__ sets the mode to 'normal'."""
        my_button = buttonsprite.ButtonSprite()
        self.assertEquals(my_button._draw_function, my_button._drawNormal)

    def testSetMode(self):
        """ButtonSprite.setMode accepts 'normal', 'inactive', ..."""
        my_button = buttonsprite.ButtonSprite()
        my_button.setMode('inactive')
        self.assertEquals(my_button._draw_function, my_button._drawInactive)
        my_button.setMode('highlighted')
        self.assertEquals(my_button._draw_function, my_button._drawHighlighted)
        my_button.setMode('pressed')
        self.assertEquals(my_button._draw_function, my_button._drawPressed)
        my_button.setMode('normal')
        self.assertEquals(my_button._draw_function, my_button._drawNormal)

    # pylint: disable-msg=R0201
    # No references to 'self' in the next tests.
    def testDrawDoesNotCrash(self):
        """ButtonSprite._draw crashes on no mode."""
        my_button = buttonsprite.ButtonSprite()
        my_button.rect.size = (64, 24)
        my_button._createImage()
        my_button.setMode('inactive')
        my_button._draw()
        my_button.setMode('highlighted')
        my_button._draw()
        my_button.setMode('pressed')
        my_button._draw()
        my_button.setMode('normal')
        my_button._draw()
    # pylint: enable-msg=R0201

if __name__ == "__main__":
    unittest.main()
