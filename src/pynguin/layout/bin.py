"""
Created on Nov 4, 2010

@author: Niriel
"""

from container import Container

__all__ = ['BinError', 'BinHasAlreadyOneChildError', 'Bin']

class BinError(RuntimeError):
    """Base error for module bin."""


class BinHasAlreadyOneChildError(BinError):
    """Raised when trying to add a child to a bin that already has a child."""


class Bin(Container):
    """A Bin is a Container that contains only one child.

    Adding a second child to a Bin raises BinHasAlreadyOneChildError.

    """
    def __init__(self):
        Container.__init__(self)

    def _requestSize(self):
        """Defers the size requisition to the layout."""
        self._layout.requestSize(self.cell)
        return self._layout.requested_size

    def _allocateSize(self):
        """Defers the size allocation to the layout."""
        self._layout.allocateSize(self.allocated_size,
                                  self.requested_size,
                                  self.cell)

    def _getCell(self):
        """Return the first (and only) cell.

        Return the first cell if there is one, or None if there is none.

        >>> b = Bin()
        >>> print b._getCell()
        None
        >>> b.cells.append('something')
        >>> print b._getCell()
        something
        >>> b.cells.append('something else')
        >>> print b._getCell()
        something

        """
        if self.cells:
            return self.cells[0]
        return None

    def addChild(self, child, where, expand_width, expand_height, *padding):
        """Add a child to the Bin.

        If the Bin has already a child then BinHasAlreadyOneChildError is
        raised::
        
            >>> from parentable import Parentable
            >>> b = Bin()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> b.addChild(child1, 'end', 'not', 'not')
            >>> print b.cell.padded is child1
            True
            >>> b.addChild(child2, 'end', 'not', 'not')
            Traceback (most recent call last):
            ...
            BinHasAlreadyOneChildError: Cannot add a second child to a Bin.

        """
        if self.cells:
            msg = "Cannot add a second child to a Bin."
            raise BinHasAlreadyOneChildError(msg)
        Container.addChild(self, child, where, expand_width, expand_height,
                           *padding)

    cell = property(_getCell, None, None, "First and only cell.")
