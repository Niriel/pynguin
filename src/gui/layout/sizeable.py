'''
Created on Nov 29, 2010

@author: Niriel
'''

from size import SizeAllocation, Pos

class Sizeable(object):
    def __init__(self):
        object.__init__(self)
        self.requested_size = None
        self.allocated_size = None

    def _requestSize(self):
        msg = "_requestSize not implemented for %s." % \
              self.__class__.__name__
        raise NotImplementedError(msg)

    def requestSize(self):
        self.requested_size = self._requestSize()

    def _allocateSize(self):
        msg = "allocateSize not implemented for %s." % \
              self.__class__.__name__
        raise NotImplementedError(msg)
    
    def allocateSize(self, size):
        self.allocated_size = SizeAllocation(size.pos, size.size)
        self._allocateSize()

    def callForSizeNegociation(self, caller):
        current_size = self.requested_size
        new_size = self._requestSize()
        if current_size == new_size:
            if caller:
                caller.negotiateSize()
        elif self.parent:
            self.parent.callForSizeNegotiation(self)
        else:
            self.negotiateSize()

    def negotiateSize(self):
        """Run the full cycle of size negotiation: request and allocation.

        WARNING: call this method only when you wish your Sizeable object
        to have the size it requests.  If you wish to impose a size which
        differs from the requested size, please use requestSize first
        and then allocateSize.  But read further.

        The position part of the allocation isn't modified.  If the size had
        never been allocated before, then the position (0, 0) is used.

        Important note: The behavior described above is merely a default
        behavior.  You may very well decide to override this method in a child
        class in order to allocate a fixed size.  For example, the widget
        representing the entire screen should always impose its own size since
        the screen has a fixed resolution.  You MUST still call
        requestSize even though you don't use the requested size: the
        result of requestSize is used during the size allocation
        phase.

        """
        self.requestSize()
        if self.allocated_size:
            pos = self.allocated_size.pos
        else:
            pos = Pos(0, 0)
        new_allo_size = SizeAllocation(pos, self.requested_size)
        self.allocateSize(new_allo_size)

    def moveTo(self, x, y):
        self.allocated_size.pos.x = x
        self.allocated_size.pos.y = y
        self.allocateSize(self.allocated_size)

    def resize(self, width, height):
        self.allocated_size.width = width
        self.allocated_size.height = height
        self.allocateSize(self.allocated_size)
