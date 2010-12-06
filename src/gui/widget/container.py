'''
Created on Dec 2, 2010

@author: Niriel
'''

from widget import Widget

__all__ = ['Container']

class Container(Widget):
    def addSprite(self, sprite, *args):
        if hasattr(sprite, 'image') and hasattr(sprite, 'rect'):
            drawer = self._findDrawers()[-1]
            drawer.sprites_group.add(sprite, *args)

    def addChild(self, child):
        self.addSprite(child)
