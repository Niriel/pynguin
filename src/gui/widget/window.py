'''
Created on Nov 25, 2010

@author: Niriel
'''

from container import Container
from gui.layout import Window as WindowLayout
from gui.sprite import Window as WindowSprite

__all__ = ['Window']

class Window(Container, WindowLayout, WindowSprite):
    def __init__(self):
        Container.__init__(self)
        WindowLayout.__init__(self)
        WindowSprite.__init__(self)

    def _allocateSize(self):
        WindowLayout._allocateSize(self)
        Container._allocateSize(self)

    def addChild(self, child, *args):
        Container.addChild(self, child)
        WindowLayout.addChild(self, child, *args)
