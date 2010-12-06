'''
Created on Nov 27, 2010

@author: Niriel
'''

import math
from widget import Widget
from gui.layout import Size, Sizeable, Parentable
from gui.sprite import Label as LabelSprite

__all__ = ['Label']

class Label(Widget, Sizeable, Parentable, LabelSprite):
    def __init__(self, font, text):
        Widget.__init__(self)
        Sizeable.__init__(self)
        Parentable.__init__(self)
        LabelSprite.__init__(self, font)
        self._text = text

    def _requestSize(self):
        width, height = self.getTextSize()
        zoom = self.ZOOM
        width = int(math.ceil(float(width) / zoom))
        height = int(math.ceil(float(height) / zoom))
        return Size(width, height)

    def setText(self, text):
        if text == self._text:
            return
        self._text = text
        self._refreshGui()

    def _refreshGui(self):
        if self._requestSize() != self.requested_size:
            self.callForSizeNegotiation()
            self.callForUpdate()
        else:
            self.callForRedraw()
