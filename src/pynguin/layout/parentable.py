"""
Created on Nov 29, 2010

@author: Niriel
"""

import weakref

__all__ = ['ParentableError', 'NoParentError', 'AlreadyParentError',
           'Parentable']

class ParentableError(RuntimeError):
    """Base error for the parentable module."""

class NoParentError(ParentableError):
    """Parentable has no parent."""

class AlreadyParentError(ParentableError):
    """Parentable already has a parent."""

class Parentable(object):
    """Inherit from this class objects you want to put in a container."""
    def __init__(self):
        """Initialize a Parentable object.

        Parentable objects have a `parent` property set to None by default::

            >>> p = Parentable()
            >>> print p.parent
            None

        """
        object.__init__(self)
        self._parent = None
    def _getParent(self):
        """De-reference the weak reference to the parent, if any."""
        if self._parent is None:
            return None
        return self._parent()
    def _setParent(self, parent):
        """Create a weakref to the parent, or set _parent to None."""
        if parent is None:
            self._parent = None
        else:
            self._parent = weakref.ref(parent)
    parent = property(_getParent, _setParent)
