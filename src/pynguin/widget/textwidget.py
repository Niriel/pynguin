#! /usr/bin/python
"""
Created on Jan 7, 2011

@author: Niriel
"""

from sizeablewidget import SizeableWidget

__all__ = ['TextWidget']

class TextWidget(SizeableWidget):
    """An abstract class for widget having text."""

    def _requestSize(self):
        """Return the size needed by the widget to display itself.

        The sprite is responsible for calculating it for it is the sprite
        that possess the Font object able to render the text.

        """
        return self._sprite.getTextSize()

    def setText(self, text):
        """Set the text of the widget.

        The text string is contained in the sprite, not in the widget.  This
        method forwards the text to the sprite.

        If the text that is set is identical to the text of the sprite,
        then nothing is done. 

        """
        if text == self._sprite.text:
            return
        self._sprite.text = text
