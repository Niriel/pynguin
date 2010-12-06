'''
Created on Dec 1, 2010

@author: Niriel
'''

from size import SizeAllocation, Pos
from bin import Bin

__all__ = ['Window']

class Window(Bin):
    def _allocateSize(self):
        """Windows subtract their position from the child's position.

        As a result, the position of the child is always (0, 0).

        """
        cell = self.cell
        if cell:
            allocated_size = self.allocated_size
            sa = SizeAllocation(Pos(0, 0), allocated_size.size)
            cell.allocateSize(sa)
