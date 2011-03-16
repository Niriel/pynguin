#! /usr/bin/python
"""
Created on Jan 7, 2011

@author: Niriel
"""

from sizeablewidget import SizeableWidget
from pynguin.layout.size import Size

__all__ = ['TextWidget']

class TextWidget(SizeableWidget):
    """An abstract class for widget having text."""

    SPRITE_CLS = None

    def __init__(self, font, text):
        """Initialize a new TextWidget."""
        SizeableWidget.__init__(self)
        self.font = font
        self.text = text

    def _getText(self):
        """Get the text of the sprite."""
        return self._sprite.text

    def _setText(self, text):
        """Set the text of the sprite.

        The text string is contained in the sprite, not in the widget.  This
        method forwards the text to the sprite.

        If the text that is set is identical to the text of the sprite, then
        nothing is done.

        """

        if text == self.text:
            return
        self._sprite.text = text

    def _getFont(self):
        """Get the font of the sprite."""
        return self._sprite.font

    def _setFont(self, font):
        """Set the font of the sprite.

        The font string is contained in the sprite, not in the widget.  This
        method forwards the font to the sprite.

        If the font that is set is identical to the font of the sprite, then
        nothing is done.

        """

        if font == self.font:
            return
        self._sprite.font = font

    def _requestSize(self):
        """Return the size needed by the widget to display itself.

        The sprite is responsible for calculating it for it is the sprite
        that possess the Font object able to render the text.

        """
        return Size(*self._sprite.getTextSize())

    text = property(_getText, _setText, None, "Text of the sprite.")
    font = property(_getFont, _setFont, None, "Font of the sprite.")
