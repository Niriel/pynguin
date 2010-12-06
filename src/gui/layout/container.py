'''
Created on Nov 4, 2010

@author: Bertrand
'''

import sizeable
import parentable
from cell import Cell


__all__ = ['Container']


class Container(sizeable.Sizeable, parentable.Parentable):
    def __init__(self):
        sizeable.Sizeable.__init__(self)
        parentable.Parentable.__init__(self)
        self.cells = []

    def addChild(self, child, expand_width, expand_height, *padding):
        if not hasattr(child, 'parent'):
            msg = "%r has no 'parent' attribute.  " \
                  "Make sure it implements Parentable." % child
            raise parentable.NoParentError(msg)
        if child.parent is not None:
            msg = "%r already has a parent (%r), it cannot be added to %r." % \
                  (child, child.parent, self)
            raise parentable.AlreadyParentError(msg)
        child.parent = self
        cell = Cell(child, expand_width, expand_height, *padding)
        self.cells.append(cell)

    def getChildren(self):
        """Convenience method to get a list of the children in the cells.

        Container objects don't contain the children directly but within cells.
        This method provides the user with a convenient way to get a list of
        children from the list of cells.

        """
        return [cell.padded for cell in self.cells]
