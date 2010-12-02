'''
Created on Dec 1, 2010

@author: delforge
'''

from widget import Widget
from gui.layout import Scroll as ScrollLayout
from gui.sprite import Scroll as ScrollSprite
from gui.layout.size import Pos

__all__ = ['Scroll']

class Scroll(Widget, ScrollLayout, ScrollSprite):
    def __init__(self):
        Widget.__init__(self)
        ScrollLayout.__init__(self)
        ScrollSprite.__init__(self)
        self.visible_pos = Pos(0, 0)

    def _allocateSize(self):
        # The order matters here.  You need to have finished all the allocation
        # before you can set the rects.
        ScrollLayout._allocateSize(self)
        Widget._allocateSize(self)

    def adjustRect(self):
        """Update the three rects."""
        Widget.adjustRect(self)
        self.adjustBigRect()
        self.adjustVisibleRect()

    def adjustBigRect(self):
        if self.cells:
            size = self.cells[0].allocated_size
            self.big_rect.size = (size.width, size.height)
        else:
            self.big_rect.size = (0, 0)

    def adjustVisibleRect(self):
        visible_pos = self.visible_pos
        self.visible_rect.topleft = (visible_pos.x, visible_pos.y)
        self.visible_rect.size = self.rect.size

    def addChild(self, child, *args):
        self.addSprite(child)
        ScrollLayout.addChild(self, child, *args)

    def scrollTo(self, left, top):
        self.visible_pos.x = left
        self.visible_pos.y = top
        self.adjustVisibleRect()
        if self.image:
            self.drawVisiblePart()

    def tryScrollTo(self, left, top):
        if left < 0:
            left = 0
        if top < 0:
            top = 0
        max_x = self.big_rect.width - self.rect.width
        max_y = self.big_rect.height - self.rect.height
        if left > max_x:
            left = max_x
        if top > max_y:
            top = max_y
        self.scrollTo(left, top)
