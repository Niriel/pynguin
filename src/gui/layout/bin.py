'''
Created on Nov 4, 2010

@author: Bertrand
'''

from gui.layout.size import Size
from container import Container


__all__ = ['BinError', 'BinHasAlreadyOneChildError', 'Bin']


class BinError(RuntimeError):
    pass


class BinHasAlreadyOneChildError(BinError):
    pass


class Bin(Container):
    """A Bin is a Container that contains only one child.

    Adding a second child to a Bin raises BinHasAlreadyOneChildError.

    """
    def __init__(self):
        Container.__init__(self)

    def _getCell(self):
        if self.cells:
            return self.cells[0]
        return None

    def _requestSize(self):
        cell = self.cell
        if not cell:
            return Size(0, 0)
        cell.requestSize()
        return cell.requested_size

    def _allocateSize(self):
        cell = self.cell
        if cell:
            cell.allocateSize(self.allocated_size)

    def addChild(self, child, *args):
        """Add a child to the Bin.

        If the Bin has already a child then BinHasAlreadyOneChildError is
        raised.

        """
        if self.cells:
            msg = "Cannot add a second child to a Bin."
            raise BinHasAlreadyOneChildError(msg)
        Container.addChild(self, child, *args)

    cell = property(_getCell)
