"""
Created on Dec 1, 2010

@author: Niriel
"""

from windowwidget import WindowWidget
from pynguin.layout import ScrollLayout
from pynguin.sprite import ScrollSprite
from pynguin.layout.size import Pos

__all__ = ['ScrollWidget']

class ScrollWidget(WindowWidget):
    LAYOUT_CLS = ScrollLayout
    SPRITE_CLS = ScrollSprite

    def __init__(self):
        WindowWidget.__init__(self)
        self.visible_pos = Pos(0, 0)

    def adjustRect(self):
        """Update the three rects."""
        self.adjustBigRect()
        self.adjustVisibleRect()

    def adjustBigRect(self):
        cell = self.cell
        if cell:
            size = cell.allocated_size
            self._sprite.big_rect.size = (size.width, size.height)
        else:
            self._sprite.big_rect.size = (0, 0)

    def adjustVisibleRect(self):
        visible_pos = self.visible_pos
        self._sprite.visible_rect.topleft = (visible_pos.x, visible_pos.y)
        self._sprite.visible_rect.size = self._sprite.rect.size

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
