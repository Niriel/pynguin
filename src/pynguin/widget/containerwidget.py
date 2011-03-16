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

    def _setAltitude(self, value):
        """Set the altitude of the widget and its children.

        If you assign to this container an altitude of `n`, then its children
        will be assigned the altitude `n+1`.

        """
        Widget._setAltitude(self, value)
        children_altitude = self.altitude + 1
        for child in self:
            child.altitude = children_altitude

    def addChild(self, child, where, expand_width, expand_height, *padding):
        """Add child to the container.

        Parameters.
        ===========

        - child: the child to add.
        - where: a description of the position within the list of cells where
          the cell for child must be inserted.
        - expand_width: 'not', 'padding' or 'padded'.
        - expand_height: 'not', 'padding' or 'padded'.
        - padding: a Padding object or 1, 2 or 4 integers.

        Parameter `where`.
        ------------------

        `where` can have several values, either string or
        tuple(string, object):

        * 'beginning': the child is inserted at the beginning of the list.
        * 'end': the child is inserted at the end of the list.
        * ('index', int): the child is inserted at the position indexed by the
          given integer.
        * ('before', ref_child): the child is inserted before the given
          reference child.
        * ('after', ref_child): the child is inserted after the given reference
          child.

        An incorrect `where` construct can raise:

        * IndexError: the given index is out of bound.
        * NotAChildError: the given reference child is not in the container.
        * InvalidWhereContstructError: incorrect tuple or string.

        Please read the documentation of the method insertCell for more details
        on the `where` parameter.

        Parameters expand_* and padding.
        --------------------------------

        For expand_width, expand_height and padding, please refer to the
        documentation of Cell.

        This method overloads Container.addChild.  It calls Container.addChild
        and then assigns an altitude to the child: that of the container + 1.

        """
        Container.addChild(self, child, where, expand_width, expand_height,
                           *padding)
        child.altitude = self.altitude + 1
