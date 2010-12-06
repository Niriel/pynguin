'''
Created on Nov 29, 2010

@author: Niriel
'''

from gui.widget import Container
from gui.layout import Board as BoardLayout
from gui.layout import Size
from gui.sprite import Screen as ScreenSprite

__all__ = ['Screen']

class Screen(Container, BoardLayout, ScreenSprite):
    def __init__(self):
        Container.__init__(self)
        BoardLayout.__init__(self)
        ScreenSprite.__init__(self)
        self._batch_update = False
        self._updates_nb = 0
        self._createImage()
        self.preferred_size = Size(*self.rect.size)

    def update(self):
        self._updates_nb = 0
        ScreenSprite.update(self)
        self.preferred_size = Size(*self.rect.size)

    def addChild(self, child):
        Container.addChild(self, child)
        BoardLayout.addChild(self, child)

    def _allocateSize(self):
        BoardLayout._allocateSize(self)
        Container._allocateSize(self)

    def batchUpdate(self, value):
        self._batch_update = value
        if not value and self._updates_nb:
            self.update()

    def callForUpdate(self):
        if self._batch_update:
            self._updates_nb += 1
        else:
            self.update()

    def _findSizeNegotiator(self, caller):
        return caller if caller else self
