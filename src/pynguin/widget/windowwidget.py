#! /usr/bin/python
"""
Created on Nov 25, 2010

@author: Niriel
"""

from binwidget import BinWidget
from pynguin.layout import WindowLayout
from pynguin.sprite import WindowSprite

__all__ = ['WindowWidget']

class WindowWidget(BinWidget):
    """Window widget."""
    SPRITE_CLS = WindowSprite
    LAYOUT_CLS = WindowLayout

    def dispatchDisplayers(self, displayer):
        """Recursively set the displayers of the widget tree.

        WindowWidget.dispatchDisplayers calls setDisplayer(displayer) on itself
        and dispatchDisplayers(self) on its cell, if any.  Indeed, window
        widgets are displayers.

        """
        self.setDisplayer(displayer)
        if self.cell:
            self.cell.padded.dispatchDisplayers(self)

    def addSprite(self, sprite, layer):
        """Add the given sprite to window sprite."""
        self._sprite.addSprite(sprite, layer)
