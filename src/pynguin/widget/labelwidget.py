"""
Created on Nov 27, 2010

@author: Niriel
"""

from sizeablewidget import SizeableWidget
from pynguin.sprite import LabelSprite

__all__ = ['LabelWidget']

# pylint: disable-msg=R0903
# To few public methods.  Labels don't do much.

class LabelWidget(SizeableWidget):
    """Widget displaying one line of text."""

    def __init__(self, font, text):
        """Initialize a new LabelWidget object.

        Parameters:

        * font: a Pygame.Font object.
        * text: a string.

        """
        SizeableWidget.__init__(self)
        self._sprite = LabelSprite(font, text)

    def _requestSize(self):
        """Return the size needed by the label to display itself.

        The sprite is responsible for calculating it for it is the sprite
        that possess the Font object able to render the text.

        """
        return self._sprite.getTextSize()

    def setText(self, text):
        """Set the text of the label.

        The text string is contained in the sprite, not in the widget.  This
        method forwards the text to the sprite.

        If the text that is set is identical to the text of the sprite,
        then nothing is done. 

        """
        if text == self._sprite.text:
            return
        self._sprite.text = text
