'''
Created on Nov 29, 2010

@author: Niriel
'''

import pygame
from gui.widget import Widget
from gui.layout import Board as BoardLayout
from gui.layout import SizeRequisition
from gui.sprite import Screen as ScreenSprite

class Screen(Widget, BoardLayout, ScreenSprite):
    def __init__(self):
        Widget.__init__(self)
        BoardLayout.__init__(self)
        ScreenSprite.__init__(self)

    def update(self):
        ScreenSprite.update(self)
        ScreenSprite.PREFERRED_SIZE = SizeRequisition(*self.rect.size)

    def addChild(self, child):
        self.addSprite(child)
        BoardLayout.addChild(self, child)

    def _allocateSize(self):
        Widget._allocateSize(self)
        BoardLayout._allocateSize(self)
