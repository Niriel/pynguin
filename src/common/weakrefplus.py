"""
Created on Nov 27, 2010

@author: Niriel
"""
import weakref

class WeakRef(object):
    def __init__(self, target):
        object.__init__(self)
        self.set(target)
    def set(self, target):
        if target is None:
            self._target = None
        else:
            self._target = weakref.ref(target)
    def __call__(self):
        if self._target is None:
            return None
        return self._target()
