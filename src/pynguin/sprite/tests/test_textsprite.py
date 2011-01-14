#! /usr/bin/python
"""
Created on Jan 10, 2011

@author: Niriel
"""

import unittest
from pynguin.sprite import textsprite
from mock import MockFont

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.


class TestTextSprite(unittest.TestCase):
    """Test the sprite.textsprite module."""

    def testInit(self):
        """TextSprite.__init__ sets `font` at None and `text` at ""."""
        my_sprite = textsprite.TextSprite()
        self.assertEquals(my_sprite.text, "")
        self.assertTrue(my_sprite.font is None)

    def testGetTextSize(self):
        """TextSprite.getTextSize asks font to render the text."""
        my_sprite = textsprite.TextSprite()
        my_sprite.font = MockFont(10)
        my_sprite.text = "Hello"
        size = my_sprite.getTextSize()
        self.assertEquals(size, (50, 10))

if __name__ == "__main__":
    unittest.main()
