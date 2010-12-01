'''
Created on Nov 29, 2010

@author: Niriel
'''

from cell import Cell
from size import SizeRequisition, SizeAllocation, Pos
from container import Container

__all__ = ['Board']

class Board(Container):
    PREFERRED_SIZE = SizeRequisition(64, 64)
    def __init__(self):
        Container.__init__(self)
    
    def _requestSize(self):
        # There is no reason for the board to have a size rather than another
        # so we just make up something. We still have to ask the children what
        # they request.
        for cell in self.cells:
            cell.requestSize()
        return self.PREFERRED_SIZE
    
    def _allocateSize(self):
        # Just give all the children what they want.
        for cell in self.cells:
            if not cell.allocated_size:
                sa = SizeAllocation(Pos(0, 0), cell.requested_size)
                cell.allocateSize(sa)

    def negotiateSize(self):
        self.requestSize()
        sa = SizeAllocation(Pos(0, 0), self.requested_size)
        self.allocateSize(sa)

    def addChild(self, child):
        Container.addChild(self, child, Cell.EXPAND_NOT, Cell.EXPAND_NOT)
