"""
Created on Nov 27, 2010

@author: Niriel
"""

from guisprite import GuiSprite

class TextSprite(GuiSprite):
    """Abstract class for sprites that display text."""

    CURSOR = '|'

    def __init__(self):
        """Initialize a new TextSprite."""
        GuiSprite.__init__(self)
        self.font = None
        self.text = ''

    def getTextSize(self):
        """Compute the size needed for rendering the text as (width, height).

        """
        return self.font.size(self.text)
