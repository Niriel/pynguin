'''
Created on Nov 29, 2010

@author: Niriel
'''

from common.weakrefplus import WeakRef

class ParentableError(RuntimeError):
    pass

class NoParentError(ParentableError):
    pass

class AlreadyParentError(ParentableError):
    pass

class Parentable(object):
    """Inherit from this class objects you want to put in a container."""
    def __init__(self):
        object.__init__(self)
        self._parent = WeakRef(None)
    def _getParent(self):
        return self._parent()
    def _setParent(self, parent):
        self._parent.set(parent)
    parent = property(_getParent, _setParent)
