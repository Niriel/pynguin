'''
Created on Nov 29, 2010

@author: Niriel
'''

from cell import Cell
from size import Size, SizeAllocation, Pos
from container import Container

__all__ = ['Board']

class Board(Container):
    PREFERRED_SIZE = (64, 64)
    def __init__(self):
        Container.__init__(self)
        self.preferred_size = Size(*Board.PREFERRED_SIZE)

    def _requestSize(self):
        # There is no reason for the board to have a size rather than another
        # so we just make up something. We still have to ask the children what
        # they request.
        for cell in self.cells:
            cell.requestSize()
        return self.preferred_size

    def _allocateSize(self):
        # Just give all the children what they want.
        for cell in self.cells:
            if cell.allocated_size:
                sa = cell.allocated_size
                sa.size = Size(cell.requested_size)
            else:
                sa = SizeAllocation(Pos(0, 0), cell.requested_size)
            cell.allocateSize(sa)

    def negotiateSize(self):
        self.requestSize()
        allocated_size = self.allocated_size
        if allocated_size:
            allocated_size.size = self.requested_size.copy()
        else:
            allocated_size = SizeAllocation((0, 0), self.requested_size)
        self.allocateSize(allocated_size)

    def addChild(self, child):
        Container.addChild(self, child, Cell.EXPAND_NOT, Cell.EXPAND_NOT)
