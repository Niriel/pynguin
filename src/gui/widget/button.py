'''
Created on Dec 2, 2010

@author: Niriel
'''

from gui.layout import Bin as BinLayout
from gui.sprite import Button as ButtonSprite
from container import Container

__all__ = ['Button']

class Button(Container, BinLayout, ButtonSprite):
    MODE_NORMAL = 0
    MODE_PRESSED = 1
    MODE_HIGHLIGHT = 2
    MODE_INACTIVE = 3
    def __init__(self):
        Container.__init__(self)
        BinLayout.__init__(self)
        ButtonSprite.__init__(self)
        self.mode = self.MODE_NORMAL

    def _allocateSize(self):
        BinLayout._allocateSize(self)
        Container._allocateSize(self)

    def addChild(self, child, *args):
        Container.addChild(self, child)
        BinLayout.addChild(self, child, *args)

    def setMode(self, mode):
        VALID = (Button.MODE_NORMAL,
                 Button.MODE_PRESSED,
                 Button.MODE_HIGHLIGHT,
                 Button.MODE_INACTIVE)
        if mode not in VALID:
            msg = "Valid values for mode are Button.MODE_NORMAL, " \
                  "Button.MODE_PRESSED, Button.MODE_HIGHLIGHT and " \
                  "Button.MODE_INACTIVE."
            raise ValueError(msg)
        self.mode = mode
        self._draw = (self._drawNormal,
                     self._drawPressed,
                     self._drawHighlight,
                     self._drawInactive)[mode]
        if self.drawable_image:
            self._draw()
            self.callForUpdate()
