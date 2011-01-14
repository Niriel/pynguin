"""
Created on Dec 2, 2010

@author: Niriel
"""

from pynguin.layout import BinLayout
from pynguin.sprite import ButtonSprite
from binwidget import BinWidget

__all__ = ['ButtonWidget']

class ButtonWidget(BinWidget):
    """Widget for a button that can be pressed."""
    def __init__(self):
        BinWidget.__init__(self)
        self._layout = BinLayout()
        self._sprite = ButtonSprite()

    def setMode(self, mode):
        """Set the mode of the button: normal, pressed, etc."""
        self._sprite.setMode(mode)
