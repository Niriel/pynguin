'''
Created on Dec 1, 2010

@author: delforge
'''

from size import SizeAllocation, Pos
from window import Window

__all__ = ['Scroll']

class Scroll(Window):
    def __init__(self):
        Window.__init__(self)

    def _allocateSize(self):
        """The child of a scroll cannot be smaller than its requested size."""
        if self.cells:
            allocated_size = self.allocated_size
            max_size = allocated_size.size | self.requested_size
            sa = SizeAllocation(Pos(0, 0), max_size)
            self.cells[0].allocateSize(sa)
