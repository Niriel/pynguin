'''
Created on Nov 30, 2010

@author: delforge
'''

from gui.layout import HBox as HBoxLayout
from gui.layout import VBox as VBoxLayout
from widget import Widget

__all__ = ['HBox', 'VBox']

class HBox(Widget, HBoxLayout):
    def __init__(self, homogeneous, spacing):
        Widget.__init__(self)
        HBoxLayout.__init__(self, homogeneous, spacing)
    
    def _allocateSize(self):
        Widget._allocateSize(self)
        HBoxLayout._allocateSize(self)
    
    def addChild(self, child, expand_width, expand_height, *padding):
        self.addSprite(child)
        HBoxLayout.addChild(self, child, expand_width, expand_height, *padding)


class VBox(Widget, VBoxLayout):
    def __init__(self, homogeneous, spacing):
        Widget.__init__(self)
        VBoxLayout.__init__(self, homogeneous, spacing)
    
    def _allocateSize(self):
        Widget._allocateSize(self)
        VBoxLayout._allocateSize(self)
    
    def addChild(self, child, expand_width, expand_height, *padding):
        self.addSprite(child)
        VBoxLayout.addChild(self, child, expand_width, expand_height, *padding)
