'''
Created on Nov 30, 2010

@author: Niriel
'''

import weakref
from common.weakrefplus import WeakRef

__all__ = ['Widget']

class Widget(object):
    ZOOM = 1
    def __init__(self):
        object.__init__(self)
        self._size_negotiator = WeakRef(None)
        self._drawers = None

    def _allocateSize(self):
        self.adjustRect()

    def adjustRect(self):
        """Make the rect property match the allocated_size property.

        The allocated_size property is created and maintained by a Sizeable
        object.

        The rect property is created by the Sprite object.

        """
        size = self.allocated_size
        zoom = self.ZOOM
        self.rect.topleft = (size.left * zoom, size.top * zoom)
        self.rect.size = (size.width * zoom, size.height * zoom)

    def _findDrawers(self, drawers=None):
        if self._drawers is not None:
            return self._drawers
        #print "Finding drawers for %r." % self
        if drawers is None:
            drawers = []
            #print "  No drawers provided, set to []."
        else:
            #print "  Drawers provided: %r." % drawers
            pass
        if self.parent:
            #print "  self has a parent: %r." % self.parent
            drawers = self.parent._findDrawers(drawers)
        self._drawers = list(drawers)
        #print "  Assigning drawers to %r: %r (%x)." % (self, self._drawers, id(self._drawers))
        if hasattr(self, 'sprites_group'):
            drawers.append(weakref.proxy(self))
            #print "  self is a drawer, appending to the list: %r." % drawers
        #print "  Returning %r." % drawers
        return drawers

    def callForRedraw(self):
        drawers = self._findDrawers()
        for drawer in drawers:
            # drawer may be None since drawers is a list of weakrefs. Let's not
            # secure the code, I want it to break asap just to explore the
            # possibilities.
            drawer._draw()

    def _findSizeNegotiator(self, caller):
        negotiator = self._size_negotiator()
        if negotiator:
            return negotiator
        parent = self.parent
        if parent:
            negotiator = parent._findSizeNegotiator(self)
        self._size_negotiator.set(negotiator)
        return negotiator

    def callForSizeNegotiation(self):
        negotiator = self._findSizeNegotiator(self)
        negotiator.negotiateSize()

    def callForUpdate(self):
        parent = self.parent
        if parent:
            parent.callForUpdate()
