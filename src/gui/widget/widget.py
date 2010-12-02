'''
Created on Nov 30, 2010

@author: Niriel
'''

__all__ = ['Widget']

class Widget(object):
    def _allocateSize(self):
        self.adjustRect()

    def adjustRect(self):
        """Make the rect property match the allocated_size property.
        
        The allocated_size property is created and maintained by a Sizeable
        object.
        
        """
        size = self.allocated_size
        self.rect.topleft = (size.left, size.top)
        self.rect.size = (size.width, size.height)

    def callForUpdate(self):
        parent = self.parent
        if parent:
            parent.callForUpdate()
