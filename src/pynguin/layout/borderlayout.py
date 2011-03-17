#! /usr/bin/python
"""
Created on Mar 17, 2011

@author: Niriel
"""

from layout import Layout
from size import SizeAllocation
import tools

__all__ = ['BorderLayout']

class BorderLayout(Layout):
    """Put a margin around a widget."""
    def __init__(self, margins=0):
        """margins can be an int or a tuple/list of 1, 2 or 4 int."""
        Layout.__init__(self)
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.parseMargins(margins)

    def parseMargins(self, margins):
        """Set the left, top, right and bottom margins."""
        try:
            len_padding = len(margins)
        except TypeError:
            # No len, so we assume it's an int.
            self.left = margins
            self.top = margins
            self.right = margins
            self.bottom = margins
            return
        if len_padding == 1:
            self.left = margins[0]
            self.top = margins[0]
            self.right = margins[0]
            self.bottom = margins[0]
        elif len_padding == 2:
            self.left = margins[0]
            self.top = margins[1]
            self.right = margins[0]
            self.bottom = margins[1]
        elif len_padding == 4:
            self.left = margins[0]
            self.top = margins[1]
            self.right = margins[2]
            self.bottom = margins[3]
        else:
            raise ValueError("Invalid margins.")
            
    def requestSize(self, children):
        """Return child size + margins size."""
        assert len(children) == 1
        child = children[0]
        requested_size = child.requested_size.copy()
        requested_size.width += self.left + self.right
        requested_size.height += self.top + self.bottom
        return requested_size

    def allocateSize(self, allocated_size, requested_size, children):
        """Share the space between the margins and the child."""
        assert len(children) == 1
        child = children[0]

        # Share the width between the border and the child.
        border_width = self.left + self.right
        child_width = allocated_size.width - border_width
        if child_width < 0:
            # Not enough space to store the child.
            child_width = 0
            border_width = allocated_size.width
        elif child_width <= child.requested_size.width:
            # Everything's healthy, border and child get what they want.
            pass
        else:
            # allocated_size too big.  Give extra to the border or the child.
            if child.can_expand_width:
                # Then the child expands, border gets what it wants.
                pass
            else:
                # The child must not expand so we expand the border instead.
                child_width = child.requested_size.width
                border_width = allocated_size.width - child_width

        # Share the height between the border and the child.
        border_height = self.top + self.bottom
        child_height = allocated_size.height - border_height
        if child_height < 0:
            # Not enough space to store the child.
            child_height = 0
            border_height = allocated_size.height
        elif child_height <= child.requested_size.height:
            # Everything's healthy, border and child get what they want.
            pass
        else:
            # allocated_size too big.  Give extra to the border or the child.
            if child.can_expand_height:
                # Then the child expands, border gets what it wants.
                pass
            else:
                # The child must not expand so we expand the border instead.
                child_height = child.requested_size.height
                border_height = allocated_size.height - child_height

        # Position of child is position of border + thickness of border.
        unused, lengths = tools.Homothecy([self.left, self.right],
                                          border_width)
        child_left = lengths[0]
        unused, lengths = tools.Homothecy([self.top, self.bottom],
                                          border_height)
        child_top = lengths[0]
        child_size = SizeAllocation((allocated_size.left + child_left,
                                     allocated_size.top + child_top),
                                     (child_width, child_height))
        child.allocateSize(child_size)
