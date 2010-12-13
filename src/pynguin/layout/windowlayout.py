#! /usr/bin/python
"""
Created on Dec 12, 2010

@author: delforge
"""

from size import Size
from size import SizeAllocation
from layout import Layout

__all__ = ['WindowLayout', 'WindowError']

class WindowError(RuntimeError):
    """Base error for the window module."""

class WindowLayout(Layout):
    """A WindowLayout manages only one cell and sets its position to (0, 0).

    The idea of a window is that the children they contain have their position
    relative to that window and not the screen or anything else.

    The WindowLayout layout is made for Bin objects: objects that have only one
    cell.
    
    Therefore, the position of the child in the window is always (0, 0).

    """
    def _requestSize(self, cells):
        """Return the requested size of the cell."""
        if cells:
            return cells[0].requested_size
        return Size(0, 0)

    def requestSize(self, cells):
        """Request the size of the window.
        
        This method overrides Layout.requestSize in order to make sure that
        cells has only zero or one element, never more.  Indeed, this layout
        is for Bin containers.

        """
        if len(cells) > 1:
            raise WindowError("Too many cells, layout made for Bin containers")
        return Layout.requestSize(self, cells)

    def allocateSize(self, allocated_size, requested_size, cells):
        """Windows subtract their position from the child's position.

        As a result, the position of the child is always (0, 0).

        """
        cell_size = SizeAllocation((0, 0), allocated_size.size)
        cells[0].allocateSize(cell_size)
