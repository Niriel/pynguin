#! /usr/bin/python
"""
Created on Mar 17, 2011

@author: delforge
"""

from containerwidget import ContainerWidget
from pynguin.layout.borderlayout import BorderLayout

__all__ = ['BorderWidget']

class BorderWidget(ContainerWidget):
    LAYOUT_CLS = BorderLayout
    def __init__(self, padding):
        ContainerWidget.__init__(self)
        self._layout.parseMargins(padding)
        self.max_children = 1
