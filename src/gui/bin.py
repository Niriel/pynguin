'''
Created on Nov 4, 2010

@author: Bertrand
'''

from container import Container


class BinError(RuntimeError):
    pass


class BinHasAlreadyOneChildError(BinError):
    pass


class Bin(Container):
    """A Bin is a Container that contains only one child.

    Because a Bin has only one child, the notion of spacing between children
    has no meaning.  Therefore the constructor of Bin does not ask for a
    spacing.

    """
    def __init__(self):
        Container.__init__(self, 0)

    def addChild(self, child):
        """Add a child to the Bin.

        If the Bin has already a child, then BinHasAlreadyOneChildError is
        raised.

        """
        if self.children:
            raise BinHasAlreadyOneChildError()
        else:
            Container.addChild(self, child)
