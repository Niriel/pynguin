#! /usr/bin/python
"""
Created on Nov 29, 2010

@author: Niriel
"""

from size import SizeAllocation

class SizeableError(RuntimeError):
    """Base error raised by the sizeable module."""

class Sizeable(object):
    """Object that can have its size negociated."""
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
        """Compute the requested size and returns it.

        Users should not call this method.  They should call requestSize
        instead.  However, developers should override this method and leave
        requestSize untouched.

        """
        msg = "_requestSize not implemented for %s." % \
              self.__class__.__name__
        raise NotImplementedError(msg)

    def requestSize(self):
        """Compute the requested size and stores it.

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
        """Proceed to the size allocation.

        Users should not call this method.  They should call allocateSize
        instead.  However, developers should override this method and leave
        allocateSize untouched.

        """
        msg = "allocateSize not implemented for %s." % \
              self.__class__.__name__
        raise NotImplementedError(msg)

    def allocateSize(self, allocated_size):
        """Store the allocated size and proceed to the size allocation.

        Parameters.
        ===========

        * allocated_size: a SizeAllocation object.

        Action.
        =======

        1. `allocateSize` performs a deep copy of the parameter
           `allocated_size` and stores it in the `allocated_size` attribute of
           the object.  Copying prevents a lot of bad surprises and
           hard-to-find bugs.
        2. calls the method `_allocateSize` (notice the underscore) which
           does the real work of size allocation.  Each layout has its own
           implementation of `_allocateSize`.

        Usage.
        ======

        * The developer should never override `allocateSize` but should
          override `_allocateSize` instead.  That way we ensure that whatever
          happens, the allocated size is properly stored.
        * The user should never call `_allocateSize` and should only call
          `allocateSize`.

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

    def moveTo(self, pos_x, pos_y):
        """Change allocated_size to the given position, then allocate.

        """
        allocated_size = self.allocated_size
        if allocated_size:
            allocated_size.pos.x = pos_x
            allocated_size.pos.y = pos_y
            self.allocateSize(allocated_size)
        else:
            raise SizeableError("No allocated size yet, call allocateSize.")

    def resize(self, width, height):
        """Change allocated_size to the given width and height, then allocate.

        """
        allocated_size = self.allocated_size
        if allocated_size:
            allocated_size.width = width
            allocated_size.height = height
            self.allocateSize(allocated_size)
        else:
            raise SizeableError("No allocated size yet, call allocateSize.")

    def moveAndResize(self, pos_x, pos_y, width, height):
        """Change allocated_size to the given position and size, then allocate.

        """
        allocated_size = self.allocated_size
        if self.allocated_size:
            allocated_size.pos.x = pos_x
            allocated_size.pos.y = pos_y
            allocated_size.width = width
            allocated_size.height = height
            self.allocateSize(allocated_size)
        else:
            raise SizeableError("No allocated size yet, call allocateSize.")
