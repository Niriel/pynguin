'''
Created on Nov 25, 2010

@author: Niriel
'''

from gui.widget import Widget
from gui.layout import Window as WindowLayout
from gui.sprite import Window as WindowSprite

class Window(Widget, WindowLayout, WindowSprite):
    def __init__(self):
        Widget.__init__(self)
        WindowLayout.__init__(self)
        WindowSprite.__init__(self)

    def _allocateSize(self):
        WindowLayout._allocateSize(self)
        Widget._allocateSize(self)

    def addChild(self, child, *args):
        self.addSprite(child)
        WindowLayout.addChild(self, child, *args)
