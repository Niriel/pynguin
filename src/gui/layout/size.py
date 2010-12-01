'''
Created on Nov 4, 2010

@author: Niriel

This module provides means to manage the size of widgets in a GUI.

'''

__all__ = ['SizeError', 'SizeAllocationError',
           'Size', 'SizeRequisition', 'Pos', 'SizeAllocation']


class SizeError(RuntimeError):
    pass


class SizeAllocationError(SizeError):
    pass


class Size(object):
    def __init__(self, *args):
        """Create a Size object from a width and a height or another size.

        The constructor takes 1 or two parameters.

        - If only one parameter, then the constructor assumes that that
          parameter has a height and a width attribute, and uses them as
          inputs.

        - If two parameters, they are the width and the height, in that
          order.

        >>> s1 = Size(1, 2)
        >>> print s1
        Size(1, 2)
        >>> print s1.width
        1
        >>> print s1.height
        2
        >>> s2 = Size(s1)
        >>> print s2
        Size(1, 2)
        >>> print s1 is s2
        False

        """
        object.__init__(self)
        args_nb = len(args)
        if args_nb == 1:
            arg = args[0]
            self.width = arg.width
            self.height = arg.height
        elif args_nb == 2:
            self.width = args[0]
            self.height = args[1]
        else:
            msg = "__init__() takes exactly 1 or 2 arguments " \
                  "(%i given)" % args_nb
            raise TypeError(msg)

    def __repr__(self):
        return "%s(%i, %i)" % (self.__class__.__name__, self.width, self.height)

    def __eq__(self, other):
        """Sizes are equals if both their width and heights are equal."""
        return self.width == other.width and self.height == other.height

    def __ne__(self, other):
        """Sizes are different if their width or height are different."""
        return self.width != other.width or self.height != other.height

    def __add__(self, other):
        """Adding sizes adds the widths and the heights.

        Return a new object of the same class than the one on the left of the +
        sign.
        
        >>> print Size(5, 6) + Size(1, 2)
        Size(6, 8)

        """
        return self.__class__(self.width + other.width, self.height + other.height)

    def __sub__(self, other):
        """Subtracting sizes subtracts the widths and the heights.

        Return a new object of the same class than the one on the left of the -
        sign.

        >>> print Size(5, 7) - Size(1, 2)
        Size(4, 5)

        """
        return self.__class__(self.width - other.width, self.height - other.height)

    def __mul__(self, other):
        """Multiplying a size by a scalar multiplies width and height by it.

        Return a new object of the same class than the one on the left of the *
        sign.

        >>> print Size(5, 6) * 2
        Size(10, 12)

        """
        return self.__class__(self.width * other, self.height * other)

    def __rmul__(self, other):
        """Multiplying a size by a scalar multiplies width and height by it.

        Return a new object of the same class than the one on the right of the
        * sign.

        >>> print 2 * Size(5, 6)
        Size(10, 12)

        """
        return self.__class__(self.width * other, self.height * other)

    def __div__(self, other):
        """Dividing a size by a scalar divides width and height by it.

        Return a new object of the same class than the one on the left of the /
        sign.

        >>> print Size(5, 6) / 2
        Size(2, 3)

        """
        return self.__class__(self.width / other, self.height / other)

    def __and__(self, other):
        """Applying and on sizes return the smallest heights and width.
        
        Think of 'and' to work like an intersection.  You end up with the
        smallest of both width and the smallest of both heights.

        Return a new object of the same class than the one on the left
        of the & sign.

        >>> print Size(1, 5) & Size(3, 4)
        Size(1, 4)

        """
        return self.__class__(min([self.width, other.width]),
                              min([self.height, other.height]))

    def __or__(self, other):
        """Applying or on sizes return the greatest heights and width.
        
        Think of 'or' to work like an union.  You end up with the
        greatest of both width and the smallest of both heights.

        Return a new object of the same class than the one on the left
        of the | sign.

        >>> print Size(1, 5) | Size(3, 4)
        Size(3, 5)

        """
        return self.__class__(max([self.width, other.width]),
                              max([self.height, other.height]))

    def __iadd__(self, other):
        """Adding sizes adds the widths and the heights.

        Does the operation in place.
        
        >>> s = Size(5, 6)
        >>> s += Size(1, 2)
        >>> print s
        Size(6, 8)

        """
        self.width += other.width
        self.height += other.height
        return self

    def __isub__(self, other):
        """Subtracting sizes subtracts the widths and the heights.

        Does the operation in place.
        
        >>> s = Size(5, 7)
        >>> s -= Size(1, 2)
        >>> print s
        Size(4, 5)

        """
        self.width -= other.width
        self.height -= other.height
        return self

    def __imul__(self, other):
        """Multiplying a size by a scalar multiplies width and height by it.

        Does the operation in place.

        >>> s = Size(5, 7)
        >>> s *= 2
        >>> print s
        Size(10, 14)

        """
        self.width *= other
        self.height *= other
        return self

    def __idiv__(self, other):
        """Dividing a size by a scalar divides width and height by it.

        Does the operation in place.

        >>> s = Size(5, 6)
        >>> s /= 2
        >>> print s
        Size(2, 3)

        """
        self.width /= other
        self.height /= other
        return self

    def __iand__(self, other):
        """Applying and on sizes return the smallest heights and width.
        
        Think of 'and' to work like an intersection.  You end up with the
        smallest of both width and the smallest of both heights.

        Does the operation in place.

        >>> s = Size(1, 5)
        >>> s &= Size(3, 4)
        >>> print s
        Size(1, 4)

        """
        if other.width < self.width:
            self.width = other.width
        if other.height < self.height:
            self.height = other.height
        return self

    def __ior__(self, other):
        """Applying or on sizes return the greatest heights and width.
        
        Think of 'or' to work like an union.  You end up with the
        greatest of both width and the smallest of both heights.

        Does the operation in place.

        >>> s = Size(1, 5)
        >>> s |= Size(3, 4)
        >>> print s
        Size(3, 5)

        """
        if other.width > self.width:
            self.width = other.width
        if other.height > self.height:
            self.height = other.height
        return self

    def subZero(self, other):
        """A version of the subtraction that has a minimum of zero.

        >>> s1 = Size(1, 2)
        >>> s2 = Size(0, 2)
        >>> print s1.subZero(s2)
        Size(1, 0)

        >>> s1 = Size(1, 2)
        >>> s2 = Size(6, 1)
        >>> print s1.subZero(s2)
        Size(0, 1)

        """
        other_width, other_height = other.width, other.height
        #
        width = self.width - other_width if other_width < self.width else 0
        height = self.height - other_height if other_height < self.height else 0
        return self.__class__(width, height)

    def isubZero(self, other):
        """A version of the subtraction that has a minimum of zero, in-place.
        
        >>> s1 = Size(1, 2)
        >>> s2 = Size(0, 2)
        >>> s1.isubZero(s2)
        Size(1, 0)
        
        >>> s1 = Size(1, 2)
        >>> s2 = Size(6, 1)
        >>> s1.isubZero(s2)
        Size(0, 1)

        """
        other_width, other_height = other.width, other.height
        #
        width = self.width - other_width if other_width < self.width else 0
        height = self.height - other_height if other_height < self.height else 0
        self.width = width
        self.height = height
        return self

    def occupiesSurface(self):
        """Tells whether or not the Size object has a non-null area.

        Return True if both the width and the height are strictly greater than
        0.

        This is useful because there is no need to spend time trying to draw a
        widget if it covers 0 pixels on screen.

        >>> print Size(1, 2).occupiesSurface()
        True
        >>> print Size(0, 2).occupiesSurface()
        False
        >>> print Size(1, 0).occupiesSurface()
        False
        >>> print Size(0, 0).occupiesSurface()
        False

        """
        return self.width > 0 and self.height > 0

    # // Beginning of block to remove in production.
    # This is handy to debug but it may be slow.
    # TODO: put all that in a class and mixin it only when __debug__ == True.
    def _getWidth(self):
        """Return the width of a Size object.

        >>> s = Size(1, 2)
        >>> print s._getWidth()
        1

        """
        return self._width

    def _getHeight(self):
        """Return the height of a Size object.

        >>> s = Size(1, 2)
        >>> print s._getHeight()
        2

        """
        return self._height

    def _setWidth(self, width):
        """Set the width of a Size object and perform health checks.

        >>> s = Size(0, 0)
        >>> s._setWidth(1)
        >>> print s.width
        1

        Only positive integers are accepted.

        If the value is not an integer, TypeError is raised:

        >>> s = Size(0, 0)
        >>> s._setWidth(3.1415)
        Traceback (most recent call last):
        ...
        TypeError: Size.width must be an integer, not 3.1415000000000002.

        If the value is not positive, ValueError is raised:

        >>> s = Size(0, 0)
        >>> s._setWidth(-42)
        Traceback (most recent call last):
        ...
        ValueError: Size.width must be positive, not -42.

        """
        if not isinstance(width, int):
            raise TypeError("Size.width must be an integer, not %r." % width)
        if width < 0:
            raise ValueError("Size.width must be positive, not %i." % width)
        self._width = width

    def _setHeight(self, height):
        """Set the height of a Size object and perform health checks.

        >>> s = Size(0, 0)
        >>> s._setHeight(1)
        >>> print s.height
        1

        Only positive integers are accepted.

        If the value is not an integer, TypeError is raised:

        >>> s = Size(0, 0)
        >>> s._setHeight(3.1415)
        Traceback (most recent call last):
        ...
        TypeError: Size.height must be an integer, not 3.1415000000000002.

        If the value is not positive, ValueError is raised:

        >>> s = Size(0, 0)
        >>> s._setHeight(-42)
        Traceback (most recent call last):
        ...
        ValueError: Size.height must be positive, not -42.

        """
        if not isinstance(height, int):
            raise TypeError("Size.height must be an integer, not %r." % height)
        if height < 0:
            raise ValueError("Size.height must be positive, not %i." % height)
        self._height = height

    width = property(_getWidth, _setWidth)
    height = property(_getHeight, _setHeight)
    # \\ End of block to remove in production.


class SizeRequisition(Size):
    pass


class Pos(object):
    def __init__(self, *args):
        args_nb = len(args)
        if args_nb == 1:
            arg = args[0]
            self.x = arg.x
            self.y = arg.y
        elif args_nb == 2:
            self.x, self.y = args
        else:
            msg = "__init__() takes exactly 1 or 2 arguments " \
                  "(%i given)" % args_nb
            raise TypeError(msg)                
    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y


class SizeAllocation(object):
    def __init__(self, pos, size):
        """Create a SizeAllocation object.

        Arguments:
        - pos: a Pos object;
        - size: a Size object.
        
        These arguments are copied:

        >>> p = Pos(1, 2)
        >>> s = Size(3, 4)
        >>> sa = SizeAllocation(p, s)
        >>> print sa.pos == p
        True
        >>> print sa.pos is p
        False
        >>> print sa.size == s
        True
        >>> print sa.size is s
        False

        This was made necessary in order to avoid surprising behaviors.  When
        doing something like
            sa = SizeAllocation(position, requested_size)
        you can imagine what crazy things would happen once the requested and
        the allocated size start sharing the same width and height.
        
        If you really need to set a specific size or position, you can always
        assign it yourself :
        >>> p = Pos(1, 2)
        >>> s = Size(3, 4)
        >>> sa = SizeAllocation(p, Size(0, 0))
        >>> sa.size = s
        >>> print sa.size is s
        True
        

        """
        object.__init__(self)
        self.pos = Pos(pos)
        self.size = Size(size)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,
                               self.pos, self.size)
    def __eq__(self, other):
        """Sizes are equals if left, top, width and height are equal."""
        return self.pos == other.pos and \
               self.size == other.size
    def __ne__(self, other):
        """Sizes are different if left, top, width or height are different."""
        return self.pos != other.pos or \
               self.size != other.size
    
    def _getLeft(self):
        return self.pos.x
    def _getTop(self):
        return self.pos.y
    def _getWidth(self):
        return self.size.width
    def _getHeight(self):
        return self.size.height
    def _setLeft(self, value):
        self.pos.x = value
    def _setTop(self, value):
        self.pos.y = value
    def _setWidth(self, value):
        self.size.width = value
    def _setHeight(self, value):
        self.size.height = value
    left = property(_getLeft, _setLeft)
    top = property(_getTop, _setTop)
    width = property(_getWidth, _setWidth)
    height = property(_getHeight, _setHeight)
