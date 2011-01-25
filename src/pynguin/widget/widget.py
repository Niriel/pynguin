#! /usr/bin/python
"""
Created on Nov 30, 2010

@author: Niriel
"""

import weakref

__all__ = ['Widget']

# pylint: disable-msg=R0903
# To few public methods.  Don't care, it's abstract anyway. 

class Widget(object):
    """Base for all the widgets.

    This class is abstract: do not use it directly but use its descendants.

    """
    SPRITE_CLS = None
    def __init__(self):
        """Initializes a new widget."""
        object.__init__(self)
        # pylint: disable-msg=E1102
        # Because I know SPRITE_CLS is not callable yet.
        self._sprite = self.SPRITE_CLS() if self.SPRITE_CLS else None
        # pylint: enable-msg=E1102
        self._displayer = None
        self._altitude = -1

    def getDisplayer(self):
        """Retreives the widget responsible for displaying this widget."""
        if self._displayer is None:
            return None
        return self._displayer()

    def setDisplayer(self, displayer):
        """Assign the widget responsible for displaying this widget.

        Example: two buttons are displayed on the surface of a window and that
        window is drawn on the surface of the screen::

            button1.setDisplayer(window)
            window.setDisplayer(screen)
            button2.setDisplayer(window)

        The order of the calls to setDisplayer does not matter.

        The displayer must have a addSprite and a removeSprite method.

        When setting a new displayer, the sprite of the current widget (if not
        None) is removed from the current displayer of the current widget (if
        it has one) and added to the new displayer.

        `None` is a valid value for the displayer.  In that case the widget
        will not be displayed by any widget: it is invisible.  Although it is
        still taken into account during the size negotiation it will simply
        leave an empty space.

        Setting the same displayer twice to the same widget has no effect:
        setDisplayer returns immediately (no removal and addition of sprite
        happens).

        """
        old_displayer = self.getDisplayer()
        if displayer == old_displayer:
            return

        # Remove the sprite from the current (old) displayer.
        sprite = self._sprite
        if old_displayer and sprite:
            old_displayer.removeSprite(sprite)

        # Add the sprite to the new displayer.
        if displayer:
            if sprite:
                displayer.addSprite(sprite, 0) # 0 is the default sprite layer.
            self._displayer = weakref.ref(displayer)
        else:
            self._displayer = None

    def dispatchDisplayers(self, displayer):
        """Recursively set the displayers of the widget tree.

        Widget.dispatchDisplayers simply calls setDisplayer.  This method is
        overloaded on Containers to propagate it to the children.  Window
        widgets also overload this method because they are displayers, and
        they dispatch themselves to their children.

        """
        self.setDisplayer(displayer)

    def _getAltitude(self):
        """Return the altitude of the widget."""
        return self._altitude
    
    def _setAltitude(self, value):
        """Set the altitude of the widget."""
        self._altitude = value
    
    altitude = property(_getAltitude, _setAltitude, None, "Altitude")
