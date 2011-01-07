#! /usr/bin/python
"""
Created on Dec 2, 2010

@author: Niriel
"""

from textwidget import TextWidget
from pynguin.sprite import TextBoxSprite

__all__ = ['TextBoxWidget']

class TextBoxWidget(TextWidget):
    """A widget for entering a line of text."""
    def __init__(self, font, text):
        """Initialize a new TextBoxWidget object.

        Parameters:

        * font: a Pygame.Font object.
        * text: a string.

        """
        TextWidget.__init__(self)
        self._sprite = TextBoxSprite(font, text)
