#! /usr/bin/python
"""
Created on Jan 7, 2011

@author: Niriel
"""

from size import Size
from layout import Layout

__all__ = ['BinLayout']

class BinLayout(Layout):
    """Simplest layout for a Bin.
    
    This layout is not abstract, you can use it.
    
    """
    def _requestSize(self, cell):
        """Return the requested size of the cell."""
        return cell.requested_size

    def requestSize(self, cell):
        cell.requestSize()
        return self._requestSize(cell)

    def allocateSize(self, allocated_size, requested_size, cell):
        """Pass the allocated size to the cell."""
        cell.allocateSize(allocated_size)
