#! /usr/bin/python
"""
Created on Nov 27, 2010

@author: Niriel
"""

from textwidget import TextWidget
from pynguin.sprite import LabelSprite

__all__ = ['LabelWidget']

# pylint: disable-msg=R0903
# To few public methods.  Labels don't do much.

class LabelWidget(TextWidget):
    """Widget displaying one line of text."""
    SPRITE_CLS = LabelSprite
