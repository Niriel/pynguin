#! /usr/bin/python
"""
Created on Nov 29, 2010

@author: Niriel
"""

from size import Size
from size import SizeAllocation
from layout import Layout

__all__ = ['BoardLayout']

class BoardLayout(Layout):
    """A BoardLayout layout lets its content have the size and pos they want."""
    PREFERRED_SIZE = (64, 64)
    def __init__(self):
        """Initialize a new BoardLayout object.
        
        >>> my_board = BoardLayout()
        >>> print my_board.preferred_size
        Size(64, 64)
        
        """
        Layout.__init__(self)
        self.preferred_size = Size(*BoardLayout.PREFERRED_SIZE)

    def requestSize(self, cells):
        """Compute the requested size of a board: an arbitrary size.
        
        There is no reason for the board to have a size rather than another so
        we just make up something.

        """
        return self.preferred_size.copy()

    def allocateSize(self, allocated_size, requested_size, cells):
        """Allocate the size of the board and its children.

        The children get whatever they asked for.

        """
        for cell in cells:
            if cell.allocated_size:
                cell_size = cell.allocated_size
                cell_size.size = cell.requested_size.copy()
            else:
                cell_size = SizeAllocation((0, 0), cell.requested_size)
            cell.allocateSize(cell_size)
