#! /usr/bin/python
"""
Created on Dec 14, 2010

@author: Niriel
"""

from pynguin.layout.sizeable import Sizeable
from pynguin.layout.parentable import Parentable
from widget import Widget

__all__ = ['SizeableWidget']

class SizeableWidget(Widget, Parentable, Sizeable):
    """Base for all the widgets that are not containers.

    This class is abstract: do not use it directly but use its descendants.

    """
    def __init__(self):
        """Initializes a new widget."""
        Sizeable.__init__(self)
        Parentable.__init__(self)
        Widget.__init__(self)
