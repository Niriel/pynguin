#! /usr/bin/python
"""
Created on Jan 9, 2011

@author: Niriel
"""

import unittest
from pynguin.widget import textwidget
from pynguin.layout import Size
from mock import MockTextSprite, MockFont

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.


class TestTextWidget(unittest.TestCase):
    """Test the textwidget module."""

    class TextWidgetWithSprite(textwidget.TextWidget):
        """Just to provide a SPRITE_CLS."""
        SPRITE_CLS = MockTextSprite

    def testInitWithSpriteClass(self):
        """TextWidget.__init__ instantiates sprite of SPRITE_CLS."""
        my_text_widget = self.TextWidgetWithSprite(42, 'Hello')
        self.assertTrue(my_text_widget._sprite.__class__ is MockTextSprite)
        self.assertEquals(my_text_widget.text, 'Hello')
        self.assertEquals(my_text_widget.font, 42)

    def testRequestSize(self):
        """TextWidget.requestSize calls getTextSize on its sprite."""
        my_text_widget = self.TextWidgetWithSprite(MockFont(10), 'Hello')
        my_text_widget.requestSize(True)
        # MockSprite considers that each character of the text is 10x10 because
        # its font=10.  Therefore size for "Hello" is 50x10.
        self.assertEquals(my_text_widget.requested_size, Size(50, 10))

if __name__ == "__main__":
    unittest.main()
