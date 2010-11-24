'''
Created on Nov 4, 2010

@author: Bertrand
'''

import size

class ContainerError(RuntimeError):
    pass

class Container(size.Sizeable):
    def __init__(self, spacing):
        size.Sizeable.__init__(self)
        self.spacing = spacing
        self.children = []

    def addChild(self, child, expand_dirs, fill_dirs, *padding):
        padded = size.Padded(child, expand_dirs, fill_dirs, *padding)
        self.children.append(padded)
