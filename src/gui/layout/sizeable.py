'''
Created on Nov 29, 2010

@author: Niriel
'''

from size import SizeAllocation

class Sizeable(object):
    def __init__(self):
        """Create a new sizeable object.
        
        >>> s = Sizeable()
        >>> print s.requested_size
        None
        >>> print s.allocated_size
        None
        >>> print s.forced_requested_size
        None

        """
        object.__init__(self)
        self.requested_size = None
        self.allocated_size = None
        self.forced_requested_size = None

    def _requestSize(self):
        msg = "_requestSize not implemented for %s." % \
              self.__class__.__name__
        raise NotImplementedError(msg)

    def requestSize(self):
        """Compute the requested size.

        The size is computed is returned by the method _requestSize. Then it is
        stored by requestSize in the requested_size attribute. If the Sizeable
        object has a forced_requested_size that is not None, then this forced
        size overrides the requested size (_requestSize is still called).  The
        forced size is copied in order to avoid surprises.

        >>> import size
        >>> def giveASize():return size.Size(1, 2)
        >>> s = Sizeable()
        >>> s._requestSize = giveASize # Remove the NotImplementedError.
        >>> s.requestSize()
        >>> print s.requested_size
        Size(1, 2)
        >>> s.forced_requested_size = size.Size(10, 20)
        >>> s.requestSize()
        >>> print s.requested_size
        Size(10, 20)
        >>> print s.requested_size == s.forced_requested_size
        True
        >>> print s.requested_size is s.forced_requested_size
        False

        """
        self.requested_size = self._requestSize()
        if self.forced_requested_size:
            self.requested_size = self.forced_requested_size.copy()

    def _allocateSize(self):
        msg = "allocateSize not implemented for %s." % \
              self.__class__.__name__
        raise NotImplementedError(msg)

    def allocateSize(self, allocated_size):
        """Set the allocated size and does any relevant processing.
        
        allocated_size is a SizeAllocation object.  A deep copy is performed
        in order to avoid surprises.
        
        After the allocated size is set, _allocateSize is called.
        
        The developer should never override allocateSize but override
        _allocateSize instead.  That way we ensure that whatever happens,
        the allocated_size is properly stored.

        >>> def doNothing():print "_allocateSize called."
        >>> import size
        >>> s = Sizeable()
        >>> s._allocateSize = doNothing # Remove the NotImplementedError.
        >>> sa = size.SizeAllocation((1, 2), (3, 4))
        >>> s.allocateSize(sa)
        _allocateSize called.
        >>> print s.allocated_size == sa
        True
        >>> print s.allocated_size is sa
        False
        >>> print s.allocated_size.pos is sa.pos
        False
        >>> print s.allocated_size.size is sa.size
        False

        """
        self.allocated_size = allocated_size.copy()
        self._allocateSize()

    def negotiateSize(self):
        """Run the full cycle of size negotiation: request and allocation.

        WARNING: call this method only when you wish your Sizeable object
        to have the size it requests.  If you wish to impose a size which
        differs from the requested size, please use requestSize first
        and then allocateSize.  But read further.

        The position part of the allocation is not modified.  If the size had
        never been allocated before, then the position (0, 0) is used.

        Important note: The behavior described above is merely a default
        behavior.  You may very well decide to override this method in a child
        class in order to allocate a fixed size for example.  For example, the
        widget representing the entire screen should always impose its own size
        since the screen has a fixed resolution.  You MUST still call
        requestSize even though you don't use the requested size: the result of
        requestSize is used during the size allocation phase.

        """
        self.requestSize()
        pos = self.allocated_size.pos if self.allocated_size else (0, 0)
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

    def moveAndResize(self, x, y, width, height):
        self.allocated_size.pos.x = x
        self.allocated_size.pos.y = y
        self.allocated_size.width = width
        self.allocated_size.height = height
        self.allocateSize(self.allocated_size)
