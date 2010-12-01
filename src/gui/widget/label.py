'''
Created on Nov 27, 2010

@author: Niriel
'''

from widget import Widget
from gui.layout import SizeRequisition, Sizeable, Parentable
from gui.sprite import Label as LabelSprite

class Label(Widget, Sizeable, Parentable, LabelSprite):
    def __init__(self, font, text):
        Widget.__init__(self)
        Sizeable.__init__(self)
        Parentable.__init__(self)
        LabelSprite.__init__(self, font, text)

    def _requestSize(self):
        return SizeRequisition(*self.getTextSize())
