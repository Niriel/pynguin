'''
Created on Nov 30, 2010

@author: Niriel
'''

import pygame

class Widget(object):
    def _allocateSize(self):
        self.adjustRect()

    def findGroup(self):
        obj = self
        while obj:
            if hasattr(obj, '_group'):
                return obj._group
            obj = obj.parent

    def addSprite(self, sprite, *args):
        if isinstance(sprite, pygame.sprite.Sprite):
            group = self.findGroup()
            group.add(sprite, *args)

    def adjustRect(self):
        """Make the rect property match the allocated_size property.
        
        The allocated_size property is created and maintained by a Sizeable
        object.
        
        """
        size = self.allocated_size
        self.rect.topleft = (size.left, size.top)
        self.rect.size = (size.width, size.height)
