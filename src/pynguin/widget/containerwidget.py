"""
Created on Dec 2, 2010

@author: Niriel
"""

from pynguin.layout.container import Container
from widget import Widget

__all__ = ['ContainerWidget']

class ContainerWidget(Widget, Container):
    """Base class for widgets implementing a container widget."""
    LAYOUT_CLS = None
    def __init__(self):
        """Initialize a new ContainerWidget object.
        
        Note that the layout is not specified here.

        """
        Container.__init__(self)
        Widget.__init__(self)
        # pylint: disable-msg=E1102
        # Because I know LAYOUT_CLS is not callable yet.
        self._layout = self.LAYOUT_CLS() if self.LAYOUT_CLS else None
        # pylint: enable-msg=E1102

    def dispatchDisplayers(self, displayer):
        """Recursively set the displayers of the widget tree.

        ContainerWidget.dispatchDisplayers calls setDisplayer on itself and
        dispatchDisplayers on its cells, if any.

        """
        self.setDisplayer(displayer)
        for cell in self.cells:
            cell.padded.dispatchDisplayers(displayer)
