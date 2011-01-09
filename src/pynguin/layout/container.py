"""
Created on Nov 4, 2010

@author: Niriel
"""

import sizeable
import parentable
from cell import Cell


__all__ = ['Container', 'ContainerError']


class ContainerError(RuntimeError):
    """Base of all errors in the module container.

    >>> raise ContainerError('boom')
    Traceback (most recent call last):
    ...
    ContainerError: boom

    """


class NotAChildError(ContainerError):
    """Error raised when an element is used as a child but isn't really one.

    >>> raise NotAChildError('boom')
    Traceback (most recent call last):
    ...
    NotAChildError: boom

    """


class InconsistentParenthoodError(ContainerError):
    """Error raised when an the relation parent-child is confusing.

    >>> raise InconsistentParenthoodError('boom')
    Traceback (most recent call last):
    ...
    InconsistentParenthoodError: boom

    """


class InvalidWhereContstructError(ContainerError):
    """Error raised when the where-construct to insert a cell is insane.

    >>> raise InvalidWhereContstructError('boom')
    Traceback (most recent call last):
    ...
    InvalidWhereContstructError: boom

    """


class Container(sizeable.Sizeable, parentable.Parentable):
    """A GUI element that can contain other GUI elements.

    """
    def __init__(self):
        """Initialize a new Container object.

        Upon creation, the container initializes a list of cells::

            >>> container = Container()
            >>> print container.cells
            []

        """
        sizeable.Sizeable.__init__(self)
        parentable.Parentable.__init__(self)
        self._layout = None
        self.cells = []

    def __iter__(self):
        """Create an iterator over the children.

        Containers can create iterators over their children.

        Here is an example of a container used in a for loop::

            >>> from parentable import Parentable
            >>> container = Container()
            >>> children = [Parentable() for i in range(3)]
            >>> for child in children:
            ...     container.addChild(child, 'end', 'padding', 'padded', 8)
            >>> for child1, child2 in zip(children, container):
            ...     print child1 is child2
            True
            True
            True

        To iterate over the cells, use container.cells.

        As usual it is dangerous to modify the list of cells while iterating
        over it.

        """
        for cell in self.cells:
            yield cell.padded

    def __contains__(self, element):
        """Return True if element is a child of the container, False otherwise.

        There are two ways or determining whether or not an element is a child
        of a container:

        1. element.parent is container
        2. element in container.getChildren()

        If everything is consistent, then 1 and 2 are equivalent.  We want to
        check both so that we can detect inconsistencies.

        Three possibilities:
        1. the element is a child of the container => return True.
        2. the element is not a child of the container => return False.
        3. the situation is inconsistent => raise InconsistentParenthoodError.

        Possibility 1, the element is a child of the container::

            >>> from parentable import Parentable
            >>> container = Container()
            >>> element = Parentable()
            >>> container.addChild(element, 'end', 'not', 'not')
            >>> print element in container
            True

        Possibility 2, the element is not a child of the container::

            >>> container = Container()
            >>> element = Parentable()
            >>> print element in container
            False

        Possibility 3, the situation is inconsistent::

            >>> container = Container()
            >>> element = Parentable()
            >>> container.addChild(element, 'end', 'not', 'not')
            >>> element.parent = None  # Introduce inconsistency.
            >>> print element in container
            Traceback (most recent call last):
            ...
            InconsistentParenthoodError: Element is in the container but parent is not that container.

            >>> container = Container()
            >>> element = Parentable()
            >>> element.parent = container  # Introduce inconsistency.
            >>> print element in container
            Traceback (most recent call last):
            ...
            InconsistentParenthoodError: Element is not in the container but parent is that container.

        """
        is_parent_ok = element.parent is self
        is_child_ok = element in list(self)
        if is_parent_ok:
            if is_child_ok:
                return True
            else:
                msg = "Element is not in the container but parent is that " \
                      "container."
        else:
            if is_child_ok:
                msg = "Element is in the container but parent is not that " \
                      "container."
            else:
                return False
        raise InconsistentParenthoodError(msg)

    def _requestSize(self):
        """Defers the size requisition to the layout."""
        return self._layout.requestSize(self.cells)

    def requestSize(self, forward_request):
        """Compute the requested size and stores it.

        The size is computed is returned by the method _requestSize. Then it is
        stored by requestSize in the requested_size attribute. If the Sizeable
        object has a forced_requested_size that is not None, then this forced
        size overrides the requested size (_requestSize is still called).  The
        forced size is copied in order to avoid surprises.

        Parameter.
        ==========
        
        * `forward_request`: Boolean
          Some Sizeable contain other Sizeable objects: they are containers.
          The size requested by a container usually depends on the size
          requested by its content.  Setting `forward_request` to True will
          cause the container to call `requestSize` on its content before
          computing its own size.  Setting it to False will make the container
          re-use the `requested_size` of its content without recomputing this
          requested size first.  True is a safer value, but using False can
          be useful for optimizing.

        """
        for cell in self.cells:
            # Always call requestSize on cells.  That is because when a widget
            # is modified (Label becomes bigger because more text in it for
            # example), the cell containing the widget is not aware of the
            # modification.  But if you don't want the cell to recompute the
            # size of its padded then it won't.
            cell.requestSize(forward_request)
        sizeable.Sizeable.requestSize(self, forward_request)

    def _allocateSize(self):
        """Defers the size allocation to the layout."""
        self._layout.allocateSize(self.allocated_size,
                                  self.requested_size,
                                  self.cells)

    def _insertCellIndex(self, cell, index):
        """Insert cell into cells at the position index.

        Called by insertCell.

        If index is out of the list of cells, IndexError is raised.

        """
        if 0 <= index < len(self.cells):
            self.cells.insert(index, cell)
        else:
            raise IndexError('list index out of range')

    def _insertCellBeforeOrAfter(self, cell, child, offset):
        """Insert cell before or after the cell containing child.

        Called by insertCell.

        offset = 0 to insert before,
        offset = 1 to insert after.

        If the child is not in the container, NotAChildError is raised.

        """
        if child in self:
            index = list(self).index(child) + offset
            self.cells.insert(index, cell)
        else:
            msg = "Reference element is not a child of that container."
            raise NotAChildError(msg)

    def insertCell(self, cell, where):
        """Insert a cell in cells at the position described by where.

        Parameters:

        * `cell`: the cell to insert;
        * `where`: describes the position where the insertion must take place.

        `where` can have several values, either string or
        tuple(string, object):

        * 'beginning': the cell is inserted at the beginning of the list.
        * 'end': the cell is inserted at the end of the list.
        * ('index', int): the cell is inserted at the position indexed by the
          given integer.
        * ('before', child): the cell is inserted before the cell that contains
          the given child.
        * ('after', child): the cell is inserted after the cell that contains
          the given child.

        Insertion with where='beginning'::

            >>> from cell import Cell
            >>> from parentable import Parentable
            >>> container = Container()
            >>> cell1 = Cell(Parentable(), 'not', 'not')
            >>> cell2 = Cell(Parentable(), 'not', 'not')
            >>> container.insertCell(cell1, 'beginning')
            >>> container.insertCell(cell2, 'beginning')
            >>> print container.cells == [cell2, cell1]
            True

        Insertion with where='end'::

            >>> container = Container()
            >>> cell1 = Cell(Parentable(), 'not', 'not')
            >>> cell2 = Cell(Parentable(), 'not', 'not')
            >>> container.insertCell(cell1, 'end')
            >>> container.insertCell(cell2, 'end')
            >>> print container.cells == [cell1, cell2]
            True

        Insertion with where=('index', 1)::

            >>> container = Container()
            >>> cell1 = Cell(Parentable(), 'not', 'not')
            >>> cell2 = Cell(Parentable(), 'not', 'not')
            >>> cell3 = Cell(Parentable(), 'not', 'not')
            >>> container.insertCell(cell1, 'end')
            >>> container.insertCell(cell2, 'end')
            >>> container.insertCell(cell3, ('index', 1))
            >>> print container.cells == [cell1, cell3, cell2]
            True

        Insertion with where=('before', child)::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> child3 = Parentable()
            >>> child1.parent = container
            >>> child2.parent = container
            >>> child3.parent = container
            >>> cell1 = Cell(child1, 'not', 'not')
            >>> cell2 = Cell(child2, 'not', 'not')
            >>> cell3 = Cell(child3, 'not', 'not')
            >>> container.insertCell(cell1, 'end')
            >>> container.insertCell(cell2, 'end')
            >>> container.insertCell(cell3, ('before', child2))
            >>> print container.cells == [cell1, cell3, cell2]
            True

        Insertion with where=('after', child)::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> child3 = Parentable()
            >>> child1.parent = container
            >>> child2.parent = container
            >>> child3.parent = container
            >>> cell1 = Cell(child1, 'not', 'not')
            >>> cell2 = Cell(child2, 'not', 'not')
            >>> cell3 = Cell(child3, 'not', 'not')
            >>> container.insertCell(cell1, 'end')
            >>> container.insertCell(cell2, 'end')
            >>> container.insertCell(cell3, ('after', child1))
            >>> print container.cells == [cell1, cell3, cell2]
            True

        If the where construct is invalid, an InvalidWhereContstructError is
        raised::

            >>> container = Container()
            >>> cell1 = Cell(Parentable(), 'not', 'not')
            >>> container.insertCell(cell1, 'wrong')
            Traceback (most recent call last):
            ...
            InvalidWhereContstructError: Parameter where is invalid, please refer to the documentation of container.insertCell.
            >>> container.insertCell(cell1, ('wrong', 45))
            Traceback (most recent call last):
            ...
            InvalidWhereContstructError: Parameter where is invalid, please refer to the documentation of container.insertCell.

        If the integer given in the where=('index', integer) is out of bound,
        then IndexError is raised::

            >>> container = Container()
            >>> cell1 = Cell(Parentable(), 'not', 'not')
            >>> container.insertCell(cell1, ('index', 42))
            Traceback (most recent call last):
            ...
            IndexError: list index out of range

        If the object given in the where=('before'/'after', obj) is not a child
        of the container, NotAChildError is raised::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> cell2 = Cell(Parentable(), 'not', 'not')
            >>> container.insertCell(cell2, ('before', child1))
            Traceback (most recent call last):
            ...
            NotAChildError: Reference element is not a child of that container.

        """
        if where == 'end':
            self.cells.append(cell)
            return
        elif where == 'beginning':
            self.cells.insert(0, cell)
            return

        if not isinstance(where, tuple):
            msg = "Parameter where is invalid, please refer to the " \
                  "documentation of container.insertCell."
            raise InvalidWhereContstructError(msg)

        key, value = where
        if key == 'index':
            self._insertCellIndex(cell, value)
        elif key == 'before':
            self._insertCellBeforeOrAfter(cell, value, 0)
        elif key == 'after':
            self._insertCellBeforeOrAfter(cell, value, 1)
        else:
            msg = "Parameter where is invalid, please refer to the " \
                  "documentation of container.insertCell."
            raise InvalidWhereContstructError(msg)

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

        Examples.
        =========

        Adding a child to a container creates a cell for that child with
        the requested padding::

            >>> from parentable import Parentable
            >>> container = Container()
            >>> children = [Parentable() for i in range(3)]
            >>> for child in children:
            ...     container.addChild(child, 'end', 'padding', 'padded', 8)
            >>> len(container.cells)
            3
            >>> children[1] in container
            True
            >>> children[1].parent is container
            True
            >>> container.cells[0].padded is children[0]
            True
            >>> print repr(container.cells[1].padding)
            Padding(8, 8, 8, 8)
            >>> print container.cells[2].expand_width
            padding
            >>> print container.cells[1].expand_height
            padded

        Adding a child that has no `parent` attribute raises an exception::

            >>> container = Container()
            >>> container.addChild('whatever', 'end', 'not', 'not')
            Traceback (most recent call last):
            ...
            NoParentError: 'whatever' has no 'parent' attribute.  Make sure it inherits from Parentable.

        Adding a child that already has a parent raises an exception::

            >>> from parentable import Parentable
            >>> container1 = Container()
            >>> container2 = Container()
            >>> child = Parentable()
            >>> child.parent = container1  # Never do that, use addChild.
            >>> container2.addChild(child, 'end', 'not', 'not')
            Traceback (most recent call last):
            ...
            AlreadyParentError: Child already has a parent and cannot be added to this container.

        """
        if not hasattr(child, 'parent'):
            msg = "%r has no 'parent' attribute.  " \
                  "Make sure it inherits from Parentable." % child
            raise parentable.NoParentError(msg)
        if child.parent is not None:
            msg = "Child already has a parent and cannot be added to this " \
                  "container."
            raise parentable.AlreadyParentError(msg)

        cell = Cell(child, expand_width, expand_height, *padding)
        self.insertCell(cell, where)
        child.parent = self # Keep that for the end in case of failure above.

    def removeChild(self, child):
        """Remove child from the container.

        - child: the child to remove.

        If child is not a child of container, ContainerError is raised::

            >>> from parentable import Parentable
            >>> container = Container()
            >>> child = Parentable()
            >>> container.removeChild(child)
            Traceback (most recent call last):
            ...
            ContainerError: Element is not a child of that container and cannot be removed.

        The child disappears from the list of cells and loses its parent::

            >>> container = Container()
            >>> children = [Parentable() for i in range(3)]
            >>> for child in children:
            ...     container.addChild(child, 'end', 'not', 'not')
            >>> len(container.cells)
            3
            >>> children[1] in container
            True
            >>> children[1].parent is container
            True
            >>> container.removeChild(children[1])
            >>> len(container.cells)
            2
            >>> children[1] in container
            False
            >>> print children[1].parent
            None

        """
        if child in self:
            children = list(self)
            index = children.index(child)
            del self.cells[index]
            child.parent = None
        else:
            msg = "Element is not a child of that container and cannot be " \
                  "removed."
            raise ContainerError(msg)
