"""
Created on Nov 4, 2010

@author: Niriel
"""

import sizeable
import parentable


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
    def __init__(self, max_children=-1):
        """Initialize a new Container object.

        Upon creation, the container initializes a list of children::

            >>> container = Container()
            >>> print container.children
            []

        """
        sizeable.Sizeable.__init__(self)
        parentable.Parentable.__init__(self)
        self._layout = None
        self.children = []
        self.max_children = max_children

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
            >>> container.addChild(element, 'end')
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
            >>> container.addChild(element, 'end')
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
        is_child_ok = element in self.children
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
        return self._layout.requestSize(self.children)

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
        if forward_request:
            for child in self.children:
                child.requestSize(forward_request)
        sizeable.Sizeable.requestSize(self, forward_request)

    def _allocateSize(self):
        """Defers the size allocation to the layout."""
        self._layout.allocateSize(self.allocated_size,
                                  self.requested_size,
                                  self.children)

    def _insertChildIndex(self, child, index):
        """Insert child into children at the position index.

        Called by _insertChild.

        If index is out of the list of children, IndexError is raised.

        """
        if 0 <= index < len(self.children):
            self.children.insert(index, child)
        else:
            raise IndexError('list index out of range')

    def _insertChildBeforeOrAfter(self, child, ref_child, offset):
        """Insert child before or after ref_child.

        Called by _insertChild.

        offset = 0 to insert before,
        offset = 1 to insert after.

        If the child is not in the container, NotAChildError is raised.

        """
        try:
            index = self.children.index(ref_child)
        except ValueError:
            msg = "Reference element is not a child of that container."
            raise NotAChildError(msg)
        self.children.insert(index + offset, child)
            

    def _insertChild(self, child, where):
        """Insert a child in children at the position described by where.

        Parameters:

        * `child`: the child to insert;
        * `where`: describes the position where the insertion must take place.

        `where` can have several values, either string or
        tuple(string, object):

        * 'beginning': the child is inserted at the beginning of the list.
        * 'end': the child is inserted at the end of the list.
        * ('index', int): the child is inserted at the position indexed by the
          given integer.
        * ('before', child): the child is inserted before the child that contains
          the given child.
        * ('after', child): the child is inserted after the child that contains
          the given child.

        Insertion with where='beginning'::

            >>> from parentable import Parentable
            >>> container = Container()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> container._insertChild(child1, 'beginning')
            >>> container._insertChild(child2, 'beginning')
            >>> print container.children == [child2, child1]
            True

        Insertion with where='end'::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> container._insertChild(child1, 'end')
            >>> container._insertChild(child2, 'end')
            >>> print container.children == [child1, child2]
            True

        Insertion with where=('index', 1)::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> child3 = Parentable()
            >>> container._insertChild(child1, 'end')
            >>> container._insertChild(child2, 'end')
            >>> container._insertChild(child3, ('index', 1))
            >>> print container.children == [child1, child3, child2]
            True

        Insertion with where=('before', child)::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> child3 = Parentable()
            >>> child1.parent = container
            >>> child2.parent = container
            >>> child3.parent = container
            >>> container._insertChild(child1, 'end')
            >>> container._insertChild(child2, 'end')
            >>> container._insertChild(child3, ('before', child2))
            >>> print container.children == [child1, child3, child2]
            True

        Insertion with where=('after', child)::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> child3 = Parentable()
            >>> child1.parent = container
            >>> child2.parent = container
            >>> child3.parent = container
            >>> container._insertChild(child1, 'end')
            >>> container._insertChild(child2, 'end')
            >>> container._insertChild(child3, ('after', child1))
            >>> print container.children == [child1, child3, child2]
            True

        If the where construct is invalid, an InvalidWhereContstructError is
        raised::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> container._insertChild(child1, 'wrong')
            Traceback (most recent call last):
            ...
            InvalidWhereContstructError: Parameter where is invalid, please refer to the documentation of container._insertChild.
            >>> container._insertChild(child1, ('wrong', 45))
            Traceback (most recent call last):
            ...
            InvalidWhereContstructError: Parameter where is invalid, please refer to the documentation of container._insertChild.

        If the integer given in the where=('index', integer) is out of bound,
        then IndexError is raised::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> container._insertChild(child1, ('index', 42))
            Traceback (most recent call last):
            ...
            IndexError: list index out of range

        If the object given in the where=('before'/'after', obj) is not a child
        of the container, NotAChildError is raised::

            >>> container = Container()
            >>> child1 = Parentable()
            >>> child2 = Parentable()
            >>> container._insertChild(child2, ('before', child1))
            Traceback (most recent call last):
            ...
            NotAChildError: Reference element is not a child of that container.

        """
        if where == 'end':
            self.children.append(child)
            return
        elif where == 'beginning':
            self.children.insert(0, child)
            return

        if not isinstance(where, tuple):
            msg = "Parameter where is invalid, please refer to the " \
                  "documentation of container._insertChild."
            raise InvalidWhereContstructError(msg)

        key, value = where
        if key == 'index':
            self._insertChildIndex(child, value)
        elif key == 'before':
            self._insertChildBeforeOrAfter(child, value, 0)
        elif key == 'after':
            self._insertChildBeforeOrAfter(child, value, 1)
        else:
            msg = "Parameter where is invalid, please refer to the " \
                  "documentation of container._insertChild."
            raise InvalidWhereContstructError(msg)

    def addChild(self, child, where):
        """Add child to the container.

        Parameters.
        ===========

        - child: the child to add.
        - where: a description of the position within the list of children where
          the cell for child must be inserted.

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

        Please read the documentation of the method _insertChild for more details
        on the `where` parameter.

        Examples.
        =========

        ::
        
            >>> from parentable import Parentable
            >>> container = Container()
            >>> children = [Parentable() for i in range(3)]
            >>> for child in children:
            ...     container.addChild(child, 'end')
            >>> len(container.children)
            3
            >>> children[1] in container
            True
            >>> children[1].parent is container
            True

        Adding a child that has no `parent` attribute raises an exception::

            >>> container = Container()
            >>> container.addChild('whatever', 'end')
            Traceback (most recent call last):
            ...
            NoParentError: 'whatever' has no 'parent' attribute.  Make sure it inherits from Parentable.

        Adding a child that already has a parent raises an exception::

            >>> from parentable import Parentable
            >>> container1 = Container()
            >>> container2 = Container()
            >>> child = Parentable()
            >>> child.parent = container1  # Never do that, use addChild.
            >>> container2.addChild(child, 'end')
            Traceback (most recent call last):
            ...
            AlreadyParentError: Child already has a parent and cannot be added to this container.

        """
        if self.max_children > -1:
            if len(self.children) >= self.max_children:
                msg = "Container capacity exceeded."
                raise ContainerError(msg)
        if not hasattr(child, 'parent'):
            msg = "%r has no 'parent' attribute.  " \
                  "Make sure it inherits from Parentable." % child
            raise parentable.NoParentError(msg)
        if child.parent is not None:
            msg = "Child already has a parent and cannot be added to this " \
                  "container."
            raise parentable.AlreadyParentError(msg)

        self._insertChild(child, where)
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

        The child disappears from the list of children and loses its parent::

            >>> container = Container()
            >>> children = [Parentable() for i in range(3)]
            >>> for child in children:
            ...     container.addChild(child, 'end')
            >>> len(container.children)
            3
            >>> children[1] in container
            True
            >>> children[1].parent is container
            True
            >>> container.removeChild(children[1])
            >>> len(container.children)
            2
            >>> children[1] in container
            False
            >>> print children[1].parent
            None

        """
        try:
            self.children.remove(child)
        except ValueError:
            msg = "Element is not a child of that container and cannot be " \
                  "removed."
            raise ContainerError(msg)
        else:
            child.parent = None
