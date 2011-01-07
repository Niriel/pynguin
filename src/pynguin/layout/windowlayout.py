#! /usr/bin/python
"""
Created on Dec 12, 2010

@author: delforge
"""

from size import SizeAllocation
from binlayout import BinLayout

__all__ = ['WindowLayout']

class WindowLayout(BinLayout):
    """A WindowLayout manages only one cell and sets its position to (0, 0).

    The idea of a window is that the children they contain have their position
    relative to that window and not the screen or anything else.

    The WindowLayout layout is made for Bin objects: objects that have only one
    cell.
    
    Therefore, the position of the child in the window is always (0, 0).

    """

    def allocateSize(self, allocated_size, requested_size, cell):
        """Windows subtract their position from the child's position.

        As a result, the position of the child is always (0, 0).

        """
        cell_size = SizeAllocation((0, 0), allocated_size.size)
        cell.allocateSize(cell_size)
