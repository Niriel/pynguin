'''
Created on Dec 1, 2010

@author: Niriel
'''

from size import SizeAllocation, Pos
from window import Window

__all__ = ['Scroll']

class Scroll(Window):
    def _allocateSize(self):
        """The child of a scroll cannot be smaller than its requested size.

        Like any Sizeable object, the Scroll object does obey to allocateSize
        and sets its size to the allocated size.  However, in the specific case
        of a Scroll object, the allocated size only affects what will be
        visible on the screen once the GUI is drawn.  The content of the Scroll
        object may very well be wider or higher than that, and that is
        perfectly valid: that is the very purpose of the Scroll object: instead
        of shrinking the content to fit the allocated size, provide the user
        with a mean of scrolling to see all the content.

        In short, the content of a Scroll is always at least as big as the
        scroll itself.

        """
        cell = self.cell
        if cell:
            allocated_size = self.allocated_size
            max_size = allocated_size.size | self.requested_size
            sa = SizeAllocation(Pos(0, 0), max_size)
            cell.allocateSize(sa)
