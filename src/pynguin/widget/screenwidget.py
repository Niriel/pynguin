#! /usr/bin/python
"""
Created on Nov 29, 2010

@author: Niriel
"""

from windowwidget import WindowWidget
from pynguin.sprite import ScreenSprite
from pynguin.layout.size import Size

__all__ = ['ScreenWidget']

class ScreenWidgetError(RuntimeError):
    """Base exception for errors of the screenwidget module."""

class DisplayerError(ScreenWidgetError):
    """Exception raised when set a non-None displayer to a screen widget."""

class ScreenWidget(WindowWidget):
    """ScreenWidget is a widget that takes the display as drawing surface.

    Anything drawn on the drawable_image of a screen object will be displayed
    at the next refresh (pygame.display.flip() for example).

    """

    SPRITE_CLS = ScreenSprite

    def __init__(self):
        WindowWidget.__init__(self)
        self._size_negotiation_askers = []

    def _requestSize(self):
        return Size(*self._sprite.getDisplaySize())

    def setDisplayer(self, displayer):
        """Raise DisplayerError if displayer parameter is not None.

        Indeed, no widget can be the displayer of a screen widget.  Screen
        widgets are at the root of the widget tree.  The displayer of a
        screen widget is always None.

        This method is written to help the developer making sure he's not doing
        anything weird.

        """
        if displayer is not None:
            msg = "Only None is a valid displayer for ScreenWidget " \
                  "(%r) given" % displayer
            raise DisplayerError(msg)

    def dispatchDisplayers(self, displayer=None):
        """Recursively set the displayers of the widget tree.

        ScreenWidget.dispatchDisplayers calls dispatchDisplayers(self) on its
        cell, if any.  Indeed, screen widgets are displayers, and nothing
        displays screen widgets: they are the ultimate displayers, the root of
        all.

        Note that the input parameter `displayer` here is present for
        consistency with the other widgets but it is never used.  This is why
        this parameter `displayer` has a default value of None.  Just call
        screen.dispatchDisplayers() once your tree is built.

        """
        for cell in self.cells:
            cell.padded.dispatchDisplayers(self)
