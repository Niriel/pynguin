"""
Created on Dec 2, 2010

@author: Niriel
"""

from pynguin.layout import Layout
from pynguin.sprite import ButtonSprite
from containerwidget import ContainerWidget

__all__ = ['ButtonWidget']

class ButtonWidget(ContainerWidget):
    """Widget for a button that can be pressed."""
    def __init__(self):
        ContainerWidget.__init__(self)
        self._layout = Layout()
        self._sprite = ButtonSprite()

    def setMode(self, mode):
        """Set the mode of the button: normal, pressed, etc."""
        self._sprite.setMode(mode)
