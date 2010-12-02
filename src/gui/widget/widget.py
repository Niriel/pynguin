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

    def _findDrawer(self):
        obj = self
        while obj:
            if hasattr(obj, 'sprites_group'):
                return obj
            obj = obj.parent

    def callForUpdate(self):
        parent = self.parent
        if parent:
            parent.callForUpdate()

    def callForRedraw(self):
        drawer = self._findDrawer()
        if drawer:
            drawer.callForRedraw()
