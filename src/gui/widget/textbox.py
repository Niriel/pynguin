'''
Created on Dec 2, 2010

@author: Niriel
'''

import string
from widget import Widget
from gui.layout import Sizeable, Parentable, SizeRequisition
from gui.sprite import TextBox as TextBoxSprite

__all__ = ['TextBox']

class TextBox(Widget, Sizeable, Parentable, TextBoxSprite):
    VALID_CHARACTERS = string.letters + \
                       string.digits + \
                       string.punctuation + \
                       ' '
    def __init__(self, font):
        Widget.__init__(self)
        Sizeable.__init__(self)
        Parentable.__init__(self)
        TextBoxSprite.__init__(self, font)
        self._text = ""
    
    def _requestSize(self):
        return SizeRequisition(*self.getTextSize())
