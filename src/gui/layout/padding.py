'''Padding represents the space inside the Cell and around a Child.

The space around a child is represented by a Padding object.  The four
attributes of a Padding object are left, right, top and bottom.  Their values
are positive integers representing the distance between the border of the child
and the border of the cell on each side.

The Padding object also provides three convenient read-only properties: width,
height and size ; returning left+right, top+bottom and Size(width, height).

Created on Nov 27, 2010

@author: delforge
'''

import size

__all__ = ['Padding']

class Padding(object):
    """The padding is the space around a widget. 

    Do not mistake it for the spacing, which is the space between widgets.
    
    A padding is not Sizable.  It means that its size cannot be negotiated.

    A padding object has four primary attributes:
        - left
        - right
        - top
        - bottom

    Each represent the empty space in one direction around the widget.  They
    must be positive integers.

    >>> p = Padding(1, 2, 3, 4)
    >>> print p.left, p.right, p.top, p.bottom
    1 2 3 4
    >>> p.top = 42
    >>> print p.left, p.right, p.top, p.bottom
    1 2 42 4

    It also has three derived attributes:
        - width
        - height
        - size
    width = left + right, and height = top + bottom.
    These are read-only (implemented as properties without setters).

    >>> print Padding(1, 2, 4, 8).width
    3
    >>> print Padding(1, 2, 4, 8).height
    12

    The size attribute creates a Size object using the width and height of the
    Padding object as parameters.
    >>> print Padding(1, 2, 4, 8).size
    Size(3, 12)

    """
    def __init__(self, *args):
        """Create a new Padding object and specify its size.

        The number of arguments is variable:
        
        >>> print Padding()
        Padding
            left   = 0
            right  = 0
            top    = 0
            bottom = 0
        
        >>> print Padding(42)
        Padding
            left   = 42
            right  = 42
            top    = 42
            bottom = 42
        
        >>> print Padding(42, 666)
        Padding
            left   = 42
            right  = 42
            top    = 666
            bottom = 666
        
        >>> print Padding(1, 2, 3, 4)
        Padding
            left   = 1
            right  = 2
            top    = 3
            bottom = 4
        
        No other number of parameters is valid.  TypeError is raised if an
        invalid number of parameters is used.
        
        >>> print Padding(1, 2, 3)
        Traceback (most recent call last):
        ...
        TypeError: __init__() takes exactly 0, 1, 2 or 4 arguments (3 given)
        
        """
        object.__init__(self)
        len_args = len(args)
        if len_args == 0:
            left = right = top = bottom = 0
        elif len_args == 1:
            left = right = top = bottom = args[0]
        elif len_args == 2:
            left = right = args[0]
            top = bottom = args[1]
        elif len_args == 4:
            left, right, top, bottom = args
        else:
            msg = "__init__() takes exactly 0, 1, 2 or 4 arguments " \
                  "(%i given)" % len_args
            raise TypeError(msg)
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%i, %i, %i, %i)" % (self.__class__.__name__,
                                       self.left, self.right,
                                       self.top, self.bottom)

    def __str__(self):
        lines = [self.__class__.__name__]
        lines.append("    left   = %i" % self.left)
        lines.append("    right  = %i" % self.right)
        lines.append("    top    = %i" % self.top)
        lines.append("    bottom = %i" % self.bottom)
        return "\n".join(lines)

    def _getWidth(self):
        """Return the sum of the left and right attributes.

        >>> print Padding(1, 2, 4, 8)._getWidth()
        3

        """
        return self.left + self.right

    def _getHeight(self):
        """Return the sum of the top and bottom attributes.

        >>> print Padding(1, 2, 4, 8)._getHeight()
        12

        """
        return self.top + self.bottom

    def _getSize(self):
        """Return a Size object with the width and height of the Padding.

        >>> print Padding(1, 2, 4, 8)._getSize()
        Size(3, 12)

        """
        return size.Size(self.width, self.height)

    width = property(_getWidth)
    height = property(_getHeight)
    size = property(_getSize)

    def __eq__(self, other):
        """Paddings are equals if their attributes are equal."""
        return self.left == other.left and \
               self.right == other.right and \
               self.top == other.top and \
               self.bottom == other.bottom

    def __ne__(self, other):
        """Paddings are different if some attributes are different."""
        return self.left != other.left or \
               self.right != other.right or \
               self.top != other.top or \
               self.bottom != other.bottom

    # // Beginning of block to remove in production.
    # This is handy to debug but it's slow.
    def _getLeft(self):
        """Return the left attribute value.

        >>> print Padding(1, 2, 4, 8)._getLeft()
        1

        """
        return self._left

    def _getRight(self):
        """Return the right attribute value.

        >>> print Padding(1, 2, 4, 8)._getRight()
        2

        """
        return self._right

    def _getTop(self):
        """Return the top attribute value.

        >>> print Padding(1, 2, 4, 8)._getTop()
        4

        """
        return self._top

    def _getBottom(self):
        """Return the bottom attribute value.

        >>> print Padding(1, 2, 4, 8)._getBottom()
        8

        """
        return self._bottom

    def _isPositiveInteger(self, value):
        return isinstance(value, int) and value >= 0

    def _setLeft(self, value):
        if self._isPositiveInteger(value):
            self._left = value
        else:
            msg = "Padding().left must be a positive integer, not %r." % value
            raise ValueError(msg)

    def _setRight(self, value):
        if self._isPositiveInteger(value):
            self._right = value
        else:
            msg = "Padding().right must be a positive integer, not %r." % value
            raise ValueError(msg)

    def _setTop(self, value):
        if self._isPositiveInteger(value):
            self._top = value
        else:
            msg = "Padding().top must be a positive integer, not %r." % value
            raise ValueError(msg)

    def _setBottom(self, value):
        if self._isPositiveInteger(value):
            self._bottom = value
        else:
            msg = "Padding().bottom must be a positive integer, not %r." % value
            raise ValueError(msg)

    left = property(_getLeft, _setLeft)
    right = property(_getRight, _setRight)
    top = property(_getTop, _setTop)
    bottom = property(_getBottom, _setBottom)
    # \\ Beginning of block to remove in production.
