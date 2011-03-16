"""
Created on Dec 2, 2010

@author: Niriel
"""

from pynguin.layout.bin import Bin
from widget import Widget

__all__ = ['BinWidget']

class BinWidget(Widget, Bin):
    """Base class for widgets implementing a bin widget."""
    LAYOUT_CLS = None
    def __init__(self):
        """Initialize a new BinWidget object.

        Note that the layout is not defined here.

        """
        Bin.__init__(self)
        Widget.__init__(self)
        # pylint: disable-msg=E1102
        # Because I know LAYOUT_CLS is not callable yet.
        self._layout = self.LAYOUT_CLS() if self.LAYOUT_CLS else None
        # pylint: enable-msg=E1102

    def dispatchDisplayers(self, displayer):
        """Recursively set the displayers of the widget tree.

        BinWidget.dispatchDisplayers calls setDisplayer on itself and
        dispatchDisplayers on its cell, if any.

        """
        self.setDisplayer(displayer)
        if self.cell:
            self.cell.padded.dispatchDisplayers(displayer)

    def addChild(self, child, expand_width, expand_height, *padding):
        """Add child to the container.

        Parameters.
        ===========

        - child: the child to add.
        - expand_width: 'not', 'padding' or 'padded'.
        - expand_height: 'not', 'padding' or 'padded'.
        - padding: a Padding object or 1, 2 or 4 integers.

        Parameters expand_* and padding.
        --------------------------------

        For expand_width, expand_height and padding, please refer to the
        documentation of Cell.

        This method overloads Bin.addChild.  It calls Bin.addChild and then
        assigns an altitude to the child: that of the bin + 1.

        """
        Bin.addChild(self, child, expand_width, expand_height, *padding)
        child.altitude = self.altitude + 1
