#! /usr/bin/python
"""
Created on Jan 9, 2011

@author: Niriel
"""

import unittest
from pynguin.widget import labelwidget
from mock import MockFont

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.

class TestLabelWidget(unittest.TestCase):
    """Test the widget.LabelWidget module."""

    def testInit(self):
        """LabelWidget.__init__ passes font and text to its sprite."""
        font = MockFont(10)
        text = "Hello"
        label = labelwidget.LabelWidget(font, text)
        sprite = label._sprite
        self.assertEquals(sprite.text, text)
        self.assertEquals(sprite.font, font)

if __name__ == "__main__":
    unittest.main()
