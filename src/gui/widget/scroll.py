'''
Created on Dec 1, 2010

@author: Niriel
'''

from container import Container
from gui.layout import Scroll as ScrollLayout
from gui.sprite import Scroll as ScrollSprite
from gui.layout.size import Pos

__all__ = ['Scroll']

class Scroll(Container, ScrollLayout, ScrollSprite):
    def __init__(self):
        Container.__init__(self)
        ScrollLayout.__init__(self)
        ScrollSprite.__init__(self)
        self.visible_pos = Pos(0, 0)

    def _allocateSize(self):
        # The order matters here.  You need to have finished all the allocation
        # before you can set the rects.
        ScrollLayout._allocateSize(self)
        Container._allocateSize(self) # Calls adjustRect.

    def adjustRect(self):
        """Update the three rects."""
        Container.adjustRect(self)
        self.adjustBigRect()
        self.adjustVisibleRect()

    def adjustBigRect(self):
        cell = self.cell
        if cell:
            size = cell.allocated_size
            zoom = self.ZOOM
            self.big_rect.size = (size.width * zoom, size.height * zoom)
        else:
            self.big_rect.size = (0, 0)

    def adjustVisibleRect(self):
        visible_pos = self.visible_pos
        zoom = self.ZOOM
        self.visible_rect.topleft = (visible_pos.x * zoom,
                                     visible_pos.y * zoom)
        self.visible_rect.size = self.rect.size

    def addChild(self, child, *args):
        Container.addChild(self, child)
        ScrollLayout.addChild(self, child, *args)

    def scrollTo(self, left, top):
        if left != self.visible_pos.x or top != self.visible_pos.y:
            self.visible_pos.x = left
            self.visible_pos.y = top
            self.adjustVisibleRect()
            if self.image:
                self._drawVisiblePart()
                self.callForRedraw()

    def tryScrollTo(self, left, top):
        if left < 0:
            left = 0
        if top < 0:
            top = 0
        cell = self.cell
        cell_size = cell.allocated_size.size
        self_size = self.allocated_size.size
        size_diff = cell_size - self_size
        max_x = size_diff.width
        max_y = size_diff.height
        if left > max_x:
            left = max_x
        if top > max_y:
            top = max_y
        self.scrollTo(left, top)
