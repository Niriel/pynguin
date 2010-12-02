'''
Created on Dec 2, 2010

@author: Niriel
'''

from widget import Widget

__all__ = ['Container']

class Container(Widget):
    def findGroup(self):
        obj = self
        while obj:
            if hasattr(obj, '_group'):
                return obj._group
            obj = obj.parent

    def addSprite(self, sprite, *args):
        if hasattr(sprite, 'image') and hasattr(sprite, 'rect'):
            group = self.findGroup()
            group.add(sprite, *args)

    def addChild(self, child):
        self.addSprite(child)