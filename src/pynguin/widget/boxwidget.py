"""
Created on Nov 30, 2010

@author: Niriel
"""

from pynguin.layout import HBoxLayout
from pynguin.layout import VBoxLayout
from containerwidget import ContainerWidget


__all__ = ['HBoxWidget', 'VBoxWidget']


_common_doc = """

    This widget does not have a sprite (the sprite is left at None).  Therefore
    this widget cannot be displayed.  However, its content can.

    """

class HBoxWidget(ContainerWidget):
    """ContainerWidget with a HBoxLayout."""
    __doc__ += _common_doc
    def __init__(self, spacing, homogeneous):
        ContainerWidget.__init__(self)
        self._layout = HBoxLayout(spacing, homogeneous)

class VBoxWidget(ContainerWidget):
    """ContainerWidget with a VBoxLayout."""
    __doc__ += _common_doc
    def __init__(self, spacing, homogeneous):
        ContainerWidget.__init__(self)
        self._layout = VBoxLayout(spacing, homogeneous)
