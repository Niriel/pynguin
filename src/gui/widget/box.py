'''
Created on Nov 30, 2010

@author: Niriel
'''

from gui.layout import HBox as HBoxLayout
from gui.layout import VBox as VBoxLayout
from container import Container

__all__ = ['HBox', 'VBox']

class HBox(Container, HBoxLayout):
    def __init__(self, homogeneous, spacing):
        Container.__init__(self)
        HBoxLayout.__init__(self, homogeneous, spacing)
    
    def _allocateSize(self):
        Container._allocateSize(self)
        HBoxLayout._allocateSize(self)
    
    def addChild(self, child, expand_width, expand_height, *padding):
        Container.addChild(self, child)
        HBoxLayout.addChild(self, child, expand_width, expand_height, *padding)
    
    def adjustRect(self):
        pass


class VBox(Container, VBoxLayout):
    def __init__(self, homogeneous, spacing):
        Container.__init__(self)
        VBoxLayout.__init__(self, homogeneous, spacing)
    
    def _allocateSize(self):
        Container._allocateSize(self)
        VBoxLayout._allocateSize(self)
    
    def addChild(self, child, expand_width, expand_height, *padding):
        Container.addChild(self, child)
        VBoxLayout.addChild(self, child, expand_width, expand_height, *padding)

    def adjustRect(self):
        pass