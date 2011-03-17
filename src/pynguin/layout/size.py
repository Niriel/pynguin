"""
Created on Nov 4, 2010

@author: Niriel

This module provides means to manage the size and position of widgets in a GUI.

The elements of a GUI (Graphical User Interface) are most of time rectangles.
As such, they can be characterized by a position (left, top) and a size (width,
height).  Even non-rectangular GUI elements can be localized within a
rectangular region.

The present module defines
    - a Vector class, for managing couple of coordinates c1, c2.
    - a Pos class, extending Vector for positions.
    - a Size class, extending Vector for sizes.
    - a SizeAllocation class, binding a Pos and a Size together.

"""


__all__ = ['Size', 'Pos', 'SizeAllocation']

# pylint: disable-msg=C0103
# Because I like c1 and c2 as variable names. 

class Vector(object):
    """A two-dimensional vector of coordinates c1 and c2, with maths.

    A Vector object has two coordinates: c1 and c2.

    The class Vector provides a way of storing couple of coordinates such as
    sizes, positions, speeds, etc.  It also provide methods to manipulate them.
    Many methods are of mathematical nature and will add, subtract, etc..  Some
    methods are handy for performing deep copies.

    """
    def __init__(self, c1, c2):
        """Initialize a Vector object with coordinates c1 and c2.

        >>> v = Vector(1, 2)
        >>> print v.c1
        1
        >>> print v.c2
        2

        """
        self._c1 = c1
        self._c2 = c2

    def __repr__(self):
        """Return a string that Python can evaluate to create a similar object.

        >>> v = Vector(1, 2)
        >>> print repr(v)
        Vector(1, 2)

        """
        return "%s(%r, %r)" % (self.__class__.__name__, self.c1, self.c2)

    def __eq__(self, other):
        """Return True if c1 and c2 are equal, False otherwise.

        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(1, 2)
        >>> v3 = Vector(1, 9)
        >>> v4 = Vector(9, 2)
        >>> v5 = Vector(9, 9)
        >>> print v1 == v2
        True
        >>> print v1 == v3
        False
        >>> print v1 == v4
        False
        >>> print v1 == v5
        False

        """
        return self.c1 == other.c1 and self.c2 == other.c2

    def __ne__(self, other):
        """Return True if c1 or c2 differ, False otherwise.

        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(1, 2)
        >>> v3 = Vector(1, 9)
        >>> v4 = Vector(9, 2)
        >>> v5 = Vector(9, 9)
        >>> print v1 != v2
        False
        >>> print v1 != v3
        True
        >>> print v1 != v4
        True
        >>> print v1 != v5
        True

        """
        return self.c1 != other.c1 or self.c2 != other.c2

    def __add__(self, other):
        """Return a new Vector with added coordinates.

        Return a new object of the same class than the one on the left of the +
        sign.

        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(3, 4)
        >>> v3 = v1 + v2
        >>> print v1
        Vector(1, 2)
        >>> print v2
        Vector(3, 4)
        >>> print v3
        Vector(4, 6)

        """
        return self.__class__(self.c1 + other.c1, self.c2 + other.c2)

    def __sub__(self, other):
        """Return a new Vector with subtracted coordinates.

        Return a new object of the same class than the one on the left of the -
        sign.

        >>> v1 = Vector(4, 6)
        >>> v2 = Vector(3, 4)
        >>> v3 = v1 - v2
        >>> print v1
        Vector(4, 6)
        >>> print v2
        Vector(3, 4)
        >>> print v3
        Vector(1, 2)

        """
        return self.__class__(self.c1 - other.c1, self.c2 - other.c2)

    def __mul__(self, other):
        """Return a new Vector with coordinates multiplied by a scalar.

        Return a new object of the same class than the one on the left of the *
        sign.

        >>> v1 = Vector(5, 6)
        >>> v2 = v1 * 2
        >>> print v1
        Vector(5, 6)
        >>> print v2
        Vector(10, 12)

        """
        return self.__class__(self.c1 * other, self.c2 * other)

    def __rmul__(self, other):
        """Return a new Vector with coordinates multiplied by a scalar.

        Return a new object of the same class than the one on the right of the
        * sign.

        >>> v1 = Vector(5, 6)
        >>> v2 = 2 * v1
        >>> print v1
        Vector(5, 6)
        >>> print v2
        Vector(10, 12)

        """
        return self.__class__(self.c1 * other, self.c2 * other)

    def __div__(self, other):
        """Return a new Vector with coordinates divided by a scalar.

        Return a new object of the same class than the one on the left of the /
        sign.

        >>> v1 = Vector(5, 6)
        >>> v2 = v1 / 2
        >>> print v1
        Vector(5, 6)
        >>> print v2
        Vector(2, 3)

        """
        return self.__class__(self.c1 / other, self.c2 / other)

    def __and__(self, other):
        """Return a new Vector with the smallest coordinates.

        Think of 'and' to work like an intersection.  You end up with the
        smallest of both c1 and the smallest of both ys.

        Return a new object of the same class than the one on the left
        of the & sign.

        >>> v1 = Vector(1, 5)
        >>> v2 = Vector(3, 4)
        >>> v3 = v1 & v2
        >>> print v1
        Vector(1, 5)
        >>> print v2
        Vector(3, 4)
        >>> print v3
        Vector(1, 4)

        """
        return self.__class__(min([self.c1, other.c1]),
                              min([self.c2, other.c2]))

    def __or__(self, other):
        """Return a new Vector with the biggest coordinates.

        Think of 'or' to work like an union.  You end up with the
        greatest of both c1 and the smallest of both ys.

        Return a new object of the same class than the one on the left
        of the | sign.

        >>> v1 = Vector(1, 5)
        >>> v2 = Vector(3, 4)
        >>> v3 = v1 | v2
        >>> print v1
        Vector(1, 5)
        >>> print v2
        Vector(3, 4)
        >>> print v3
        Vector(3, 5)

        """
        return self.__class__(max([self.c1, other.c1]),
                              max([self.c2, other.c2]))

    def __iadd__(self, other):
        """Add the coordinates in place.

        >>> s = Vector(5, 6)
        >>> s += Vector(1, 2)
        >>> print s
        Vector(6, 8)

        """
        self.c1 += other.c1
        self.c2 += other.c2
        return self

    def __isub__(self, other):
        """Subtract the coordinates in place.

        >>> s = Vector(5, 7)
        >>> s -= Vector(1, 2)
        >>> print s
        Vector(4, 5)

        """
        self.c1 -= other.c1
        self.c2 -= other.c2
        return self

    def __imul__(self, other):
        """Multiply the coordinates in place.

        >>> s = Vector(5, 7)
        >>> s *= 2
        >>> print s
        Vector(10, 14)

        """
        self.c1 *= other
        self.c2 *= other
        return self

    def __idiv__(self, other):
        """Divide the coordinates in place.

        >>> s = Vector(5, 6)
        >>> s /= 2
        >>> print s
        Vector(2, 3)

        """
        self.c1 /= other
        self.c2 /= other
        return self

    def __iand__(self, other):
        """Assign the smallest coordinates in place.

        Think of 'and' to work like an intersection.  You end up with the
        smallest of both c1 and the smallest of both ys.

        >>> s = Vector(1, 5)
        >>> s &= Vector(3, 4)
        >>> print s
        Vector(1, 4)

        """
        self.c1 = min([self.c1, other.c1])
        self.c2 = min([self.c2, other.c2])
        return self

    def __ior__(self, other):
        """Assign the biggest coordinates in place.

        Think of 'or' to work like an union.  You end up with the
        greatest of both c1 and the smallest of both ys.

        >>> s = Vector(1, 5)
        >>> s |= Vector(3, 4)
        >>> print s
        Vector(3, 5)

        """
        self.c1 = max([self.c1, other.c1])
        self.c2 = max([self.c2, other.c2])
        return self

    def subZero(self, other):
        """Subtract the coordinates with a minimum of 0.

        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(0, 2)
        >>> v3 = v1.subZero(v2)
        >>> print v1
        Vector(1, 2)
        >>> print v2
        Vector(0, 2)
        >>> print v3
        Vector(1, 0)

        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(9, 1)
        >>> v3 = v1.subZero(v2)
        >>> print v1
        Vector(1, 2)
        >>> print v2
        Vector(9, 1)
        >>> print v3
        Vector(0, 1)

        """
        other_x, other_y = other.c1, other.c2
        #
        x = self.c1 - other_x if other_x < self.c1 else 0
        y = self.c2 - other_y if other_y < self.c2 else 0
        return self.__class__(x, y)

    def isubZero(self, other):
        """Subtract the coordinates in place with a minimum of 0.

        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(0, 2)
        >>> v1.isubZero(v2)
        Vector(1, 0)

        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(9, 1)
        >>> v1.isubZero(v2)
        Vector(0, 1)

        """
        other_x, other_y = other.c1, other.c2
        #
        x = self.c1 - other_x if other_x < self.c1 else 0
        y = self.c2 - other_y if other_y < self.c2 else 0
        self.c1 = x
        self.c2 = y
        return self

    def copy(self):
        """Create a new instance of Vector with the same c1 and c2.

        >>> v1 = Vector(1, 2)
        >>> v2 = v1.copy()
        >>> print v1 == v2
        True
        >>> print v1 is v2
        False

        """
        return self.__class__(self.c1, self.c2)

    def icopy(self, other):
        """Copy the coordinates of other into itself, in place.

        >>> v1 = Vector(1, 2)
        >>> v2 = Vector(3, 4)
        >>> v1.icopy(v2)
        >>> print v1
        Vector(3, 4)
        >>> print v1 == v2
        True
        >>> print v1 is v2
        False

        """
        self.c1 = other.c1
        self.c2 = other.c2

    def asTuple(self):
        """Return a tuple (c1, c2).

        >>> v1 = Vector(1, 2)
        >>> print v1.asTuple()
        (1, 2)

        """
        return self.c1, self.c2

    def _getC1(self):
        """Return _c1.

        >>> v1 = Vector(1, 2)
        >>> print v1._c1
        1
        >>> print v1._getC1()
        1

        """
        return self._c1

    def _getC2(self):
        """Return _c2.

        >>> v1 = Vector(1, 2)
        >>> print v1._c2
        2
        >>> print v1._getC2()
        2

        """
        return self._c2

    def _setC1(self, value):
        """Set _c1.

        >>> v1 = Vector(0, 0)
        >>> v1._setC1(1)
        >>> print v1._c1
        1

        """
        self._c1 = value

    def _setC2(self, value):
        """Set _c2.

        >>> v1 = Vector(0, 0)
        >>> v1._setC2(1)
        >>> print v1._c2
        1

        """
        self._c2 = value

    c1 = property(_getC1, _setC1, None, "c1 coordinate.")
    c2 = property(_getC2, _setC2, None, "c2 coordinate.")


class Size(Vector):
    """Process a Vector as a Size.

    A Size is a Vector with an additional constraint: c1 and c2 can never be
    smaller than 0.

    >>> s = Size(1, 2)
    >>> print s
    Size(1, 2)

    >>> s = Size(-42, 0)
    Traceback (most recent call last):
     ...
    ValueError: Size.width must be positive, not -42.

    Size objects come with two properties, width and height, that are
    equivalent to c1 and c2.

    >>> s = Size(1, 2)
    >>> print s.c1, s.width
    1 1
    >>> print s.c2, s.height
    2 2

    """
    def __init__(self, width, height):
        """Create a Size object from a width and a height.

        The constructor takes two parameters: the width and the height.

        >>> s1 = Size(1, 2)
        >>> print s1
        Size(1, 2)
        >>> print s1.c1
        1
        >>> print s1.width
        1
        >>> print s1.c2
        2
        >>> print s1.height
        2

        """
        # I MUST overload Vector's init because I want to use c1 and c2 from
        # the current class, not Vector's.
        Vector.__init__(self, 0, 0)
        self.c1 = width
        self.c2 = height

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

    def _setC1(self, value):
        """Set the width of a Size object and perform health checks.

        >>> s = Size(0, 0)
        >>> s._setC1(1)
        >>> print s._c1
        1

        Only positive integers are accepted.

        If the value is not an integer, TypeError is raised:

        >>> s = Size(0, 0)
        >>> s._setC1(3.1415)
        Traceback (most recent call last):
        ...
        TypeError: Size.width must be an integer, not 3.1415000000000002.

        If the value is not positive, ValueError is raised:

        >>> s = Size(0, 0)
        >>> s._setC1(-42)
        Traceback (most recent call last):
        ...
        ValueError: Size.width must be positive, not -42.

        """
        if not isinstance(value, int):
            raise TypeError("Size.width must be an integer, not %r." % value)
        if value < 0:
            raise ValueError("Size.width must be positive, not %i." % value)
        self._c1 = value

    def _setC2(self, value):
        """Set the height of a Size object and perform health checks.

        >>> s = Size(0, 0)
        >>> s._setC2(1)
        >>> print s._c2
        1

        Only positive integers are accepted.

        If the value is not an integer, TypeError is raised:

        >>> s = Size(0, 0)
        >>> s._setC2(3.1415)
        Traceback (most recent call last):
        ...
        TypeError: Size.height must be an integer, not 3.1415000000000002.

        If the value is not positive, ValueError is raised:

        >>> s = Size(0, 0)
        >>> s._setC2(-42)
        Traceback (most recent call last):
        ...
        ValueError: Size.height must be positive, not -42.

        """
        if not isinstance(value, int):
            raise TypeError("Size.height must be an integer, not %r." % value)
        if value < 0:
            raise ValueError("Size.height must be positive, not %i." % value)
        self._c2 = value

    c1 = width = property(Vector._getC1, _setC1, None,
                          "Secured access to the width (c1).")
    c2 = height = property(Vector._getC2, _setC2, None,
                           "Secured access to the height (c2).")


class Pos(Vector):
    """A position.
    
    Two properties: x and y.
    
    """
    x = Vector.c1
    y = Vector.c2


class SizeAllocation(Vector):
    """SizeAllocation contains a position and a size.

    SizeAllocation is also a Vector.  The first coordinate is the position,
    the second coordinate is the size.  It makes mathematics easier:

    >>> s1 = SizeAllocation(Pos(1, 2), Size(3, 4))
    >>> s2 = SizeAllocation(Pos(5, 6), Size(7, 8))
    >>> s3 = s1 + s2
    >>> print s3
    SizeAllocation(Pos(6, 8), Size(10, 12))
    >>> print s3 * 10 # Handy for zooming the GUI !
    SizeAllocation(Pos(60, 80), Size(100, 120))

    For convenience, SizeAllocation can also be instantiated with tuple
    parameters.  See SizeAllocation.__init__.

    """
    def __init__(self, pos, size):
        """Create a SizeAllocation object.

        Arguments:
        - pos: the position where the Sizeable object must be placed.
        - size: the size that the Sizeable object must adopt.

        pos can be a Pos object or a tuple.
        size can be a Size object or a tuple.

        >>> sa = SizeAllocation((1, 2), (3, 4))
        >>> print sa.pos
        Pos(1, 2)
        >>> print sa.size
        Size(3, 4)

        >>> pos = Pos(1, 2)
        >>> size = Size(3, 4)
        >>> sa = SizeAllocation(pos, size)
        >>> print sa.pos
        Pos(1, 2)
        >>> print sa.size
        Size(3, 4)
        >>> print sa.pos is pos
        False
        >>> print sa.size is size
        False

        As you see, pos and size are copied.  This prevents a lot of surprises
        and usually corresponds to the desired behavior.

        """
        Vector.__init__(self, None, None)
        # pylint: disable-msg=W0142
        # Because using *pos and *size here is not that dirty.
        self.pos = Pos(*pos) if isinstance(pos, tuple) else pos.copy()
        self.size = Size(*size) if isinstance(size, tuple) else size.copy()

    def ideepCopy(self, other):
        """Store copies of other.pos and other.size into itself.

        >>> sa1 = SizeAllocation((1, 2), (3, 4))
        >>> sa2 = SizeAllocation((5, 6), (7, 8))
        >>> sa1.icopy(sa2) # Shallow copy, pos and size are the same.
        >>> print sa1 == sa2
        True
        >>> print sa1.pos is sa2.pos
        True
        >>> print sa1.size is sa2.size
        True
        >>> sa1.ideepCopy(sa2) # Deep copy, pos and size differ.
        >>> print sa1 == sa2
        True
        >>> print sa1.pos is sa2.pos
        False
        >>> print sa1.size is sa2.size
        False

        """
        self.pos = other.pos.copy()
        self.size = other.size.copy()

    def asDeepTuple(self):
        """Return a tuple of tuples.

        >>> sa = SizeAllocation(Pos(1, 2), Size(3, 4))
        >>> print sa.asTuple()
        (Pos(1, 2), Size(3, 4))
        >>> print sa.asDeepTuple()
        ((1, 2), (3, 4))

        """
        return (self.pos.asTuple(), self.size.asTuple())

    def _getLeft(self):
        """Return the x of pos.

        >>> sa = SizeAllocation(Pos(1, 2), Size(3, 4))
        >>> print sa.left
        1

        """
        return self.pos.x

    def _getTop(self):
        """Return the y of pos.

        >>> sa = SizeAllocation(Pos(1, 2), Size(3, 4))
        >>> print sa.top
        2

        """
        return self.pos.y

    def _getWidth(self):
        """Return the width of size.

        >>> sa = SizeAllocation(Pos(1, 2), Size(3, 4))
        >>> print sa.width
        3

        """
        return self.size.width

    def _getHeight(self):
        """Return the height of size.

        >>> sa = SizeAllocation(Pos(1, 2), Size(3, 4))
        >>> print sa.height
        4

        """
        return self.size.height

    def _setLeft(self, value):
        """Set the c1 of pos.

        >>> sa = SizeAllocation(Pos(0, 0), Size(0, 0))
        >>> sa.left = 1
        >>> print sa.pos.c1
        1

        """
        self.pos.c1 = value

    def _setTop(self, value):
        """Set the c2 of pos.

        >>> sa = SizeAllocation(Pos(0, 0), Size(0, 0))
        >>> sa.top = 1
        >>> print sa.pos.c2
        1

        """
        self.pos.c2 = value

    def _setWidth(self, value):
        """Set the width of size.

        >>> sa = SizeAllocation(Pos(0, 0), Size(0, 0))
        >>> sa.width = 1
        >>> print sa.size.width
        1

        """
        self.size.width = value

    def _setHeight(self, value):
        """Set the height of size.

        >>> sa = SizeAllocation(Pos(0, 0), Size(0, 0))
        >>> sa.height = 1
        >>> print sa.size.height
        1

        """
        self.size.height = value

    pos = Vector.c1
    size = Vector.c2

    left = property(_getLeft, _setLeft, None, "Convenient access to pos.x.")
    top = property(_getTop, _setTop, None, "Convenient access to pos.y.")
    width = property(_getWidth, _setWidth, None,
                     "Convenient access to size.width.")
    height = property(_getHeight, _setHeight, None,
                      "Convenient access to size.height.")

if __name__ == '__main__':
    help(__name__)
