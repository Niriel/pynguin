'''
Created on Nov 29, 2010

@author: Niriel
'''

from gui.widget import Container
from gui.layout import Board as BoardLayout
from gui.layout import SizeRequisition
from gui.sprite import Screen as ScreenSprite

__all__ = ['Screen']

class Screen(Container, BoardLayout, ScreenSprite):
    def __init__(self):
        Container.__init__(self)
        BoardLayout.__init__(self)
        ScreenSprite.__init__(self)
        self._batch_update = False
        self._updates_nb = 0

    def update(self):
        self._updates_nb = 0
        ScreenSprite.update(self)
        ScreenSprite.PREFERRED_SIZE = SizeRequisition(*self.rect.size)

    def addChild(self, child):
        Container.addChild(self, child)
        BoardLayout.addChild(self, child)

    def _allocateSize(self):
        BoardLayout._allocateSize(self)
        Container._allocateSize(self)

    def callForUpdate(self):
        if self._batch_update:
            self._updates_nb += 1
        else:
            self.update()

    def batchUpdate(self, value):
        self._batch_update = value
        if not value and self._updates_nb:
            self.update()

    def callForRedraw(self):
        self._draw()