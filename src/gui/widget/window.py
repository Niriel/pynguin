'''
Created on Nov 25, 2010

@author: Niriel
'''

from gui.widget import Widget
from gui.layout import Bin as BinLayout
from gui.sprite import Window as WindowSprite

class Window(Widget, BinLayout, WindowSprite):
    def __init__(self):
        Widget.__init__(self)
        BinLayout.__init__(self)
        WindowSprite.__init__(self)

    def _allocateSize(self):
        Widget._allocateSize(self)
        BinLayout._allocateSize(self)

    def addChild(self, child, *args):
        self.addSprite(child)
        BinLayout.addChild(self, child, *args)

    def setPos(self, x, y):
        self.rect.topleft = (x, y)
