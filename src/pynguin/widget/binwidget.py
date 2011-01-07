"""
Created on Dec 2, 2010

@author: Niriel
"""

from pynguin.layout.container import Container
from widget import Widget

__all__ = ['BinWidget']

class BinWidget(Widget, Container):
    """Base class for widgets implementing a bin widget."""
    def __init__(self):
        """Initialize a new BinWidget object."""
        Container.__init__(self)
        Widget.__init__(self)
