#! /usr/bin/python
"""
Created on Jan 7, 2011

@author: Niriel
"""

from layout import Layout

__all__ = ['BinLayout']

class BinLayout(Layout):
    """Simplest layout for a Bin.
    
    This layout is not abstract, you can use it.
    
    """
    def requestSize(self, cell):
        """Return the requested size of the cell."""
        return cell.requested_size

    def allocateSize(self, allocated_size, requested_size, cell):
        """Pass the allocated size to the cell."""
        cell.allocateSize(allocated_size)
