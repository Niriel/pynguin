'''
Created on Nov 4, 2010

@author: Bertrand

This module provides means to manage the size of widgets in a GUI.

'''


__all__ = ['Size', 'SizeRequisition', 'SizeAllocation'
           'Sizeable', 'Padding', 'Padded']


class SizeAllocationError(RuntimeError):
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
        nb_args = len(args)
        if nb_args == 1:
            arg = args[0]
            self.width = arg.width
            self.height = arg.height
        elif nb_args == 2:
            self.width = args[0]
            self.height = args[1]
        else:
            msg = "__init__() takes exactly 1 or 2 arguments " \
                  "(%i given)" % nb_args
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


class SizeAllocation(Size):
    def __init__(self, left, top, *args):
        """Create a SizeAllocation object.

        This constructor accepts different arguments:
        s = SizeAllocation(left, top, width, height)
        s = SizeAllocation(left, top, size_object)

        """
        Size.__init__(self, *args)
        self.left = left
        self.top = top
    def __repr__(self):
        return "%s(%i, %i, %i, %i)" % (self.__class__.__name__,
                                       self.left, self.top,
                                       self.width, self.height)
    def __eq__(self, other):
        """Sizes are equals if left, top, width and height are equal."""
        return self.width == other.width and self.height == other.height and \
               self.left == other.left and self.top == other.top
    def __ne__(self, other):
        """Sizes are different if left, top, width or height are different."""
        return self.width != other.width or self.height != other.height or \
               self.left != other.left or self.top != other.top

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
        return Size(self.width, self.height)

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


class Sizeable(object):
    def __init__(self):
        object.__init__(self)
        self.requested_size = None
        self.allocated_size = None

    def _computeRequestedSize(self):
        msg = "_computeRequestedSize not implemented for %s." % \
              self.__class__.__name__
        raise NotImplementedError(msg)

    def computeRequestedSize(self):
        self.requested_size = self._computeRequestedSize()

    def allocateSize(self, size):
        if not isinstance(size, SizeAllocation):
            msg = "Sizeable.allocateSize only accepts SizeAllocation " \
                  "instances (%r given)." % size
            raise TypeError(msg)


class Padded(Sizeable):
    """Holds a widget and a Padding object together.

    This is a useful things for containers: each widget comes with a padding
    but the padding is not an intrinsic property of the widget. So this class
    aims at binding the two.

    This class has the following attributes:
    
    - widget: the widget you are padding.
    
    - padding: the padding you surround the widget with.
    
    - requested_size: the result of the method computeRequestedSize.
    
    - allocated_size: the argument passed during the last call to the method
      allocateSize().
      
    - expand_width, expand_height: boolean set to True if the padded widget is
      allowed to occupy more space that its requested size in the given
      direction.
      
    - fill_width, fill_height: boolean set to True if the extra space when
      expand_*=True has to be given to the widget rather than its padding.

    Padded inherits from Sizable and implements a simple algorithm for
    computing the requested size.  It adds the size of the padding to the size
    of the widget.  This allows a Container to ask a Padded object the size it
    needs.

    Likewise, Padded objects come with a allocateSize method.

    """
    
    VALID_DIRS = ('', 'h', 'v', 'hv')
    
    def __init__(self, widget, expand_dirs, fill_dirs, *padding):
        """Create a new Padded object, binding a widget and a Padding object.

        The constructor takes a variable number of parameters.

        The first parameter the widget.

        >>> padded = Padded('a widget', '', '')
        >>> print padded.widget
        a widget

        Of course the string 'a widget' is hardly a widget, but it shows you
        that the first parameter is accessible later through the widget
        attribute.

        The second parameter is expand_dirs: the directions in which the padded
        widget is allowed to expand. Acceptable values are '', 'h', 'v' and
        'hv'. This controls whether or not the padding around the widget will
        inflate and make the container occupies as much space as it can in the
        horizontal (h) and vertical (v) directions.

        The third is fill_dirs.  Acceptable values are '', 'h', 'v' and
        'hv'. This controls whether or not the widget inflates beyond
        its requested size to fill all the available space inside the padding
        in the horizontal (h) and vertical (v) directions.

        The parameters expand_dirs and fill_dirs have no effect at all on the
        size requisition, they only influence the size allocation.
        
        It is forbidden to have expand=False and fill=True for one direction.
        >>> padded = Padded('a widget', '', 'h')
        Traceback (most recent call last):
        ...
        ValueError: It is forbidden to set expand=False and fill=True.

        The other parameters define the padding.  You can pass the 0 to 4
        parameters defining a padding, or directly one padding object.

        >>> print repr(Padded('widget', '', '').padding)
        Padding(0, 0, 0, 0)

        >>> print repr(Padded('widget', '', '', 42).padding)
        Padding(42, 42, 42, 42)

        >>> print repr(Padded('widget', '', '', 42, 666).padding)
        Padding(42, 42, 666, 666)

        >>> print repr(Padded('widget', '', '', 1, 2, 3, 4).padding)
        Padding(1, 2, 3, 4)

        >>> padding = Padding(1, 2, 3, 4)
        >>> padded = Padded('widget', '', '', padding)
        >>> print repr(padded.padding)
        Padding(1, 2, 3, 4)
        >>> print padded.padding is padding
        True

        """

        Sizeable.__init__(self)
        if expand_dirs not in self.VALID_DIRS:
            msg = "expand_dirs must be in %r (%r given)." % (self.VALID_DIRS, expand_dirs)
            raise ValueError(msg)
        if fill_dirs not in self.VALID_DIRS:
            msg = "fill_dirs must be in %r (%r given)." % (self.VALID_DIRS, fill_dirs)
            raise ValueError(msg)
        expand_width = 'h' in expand_dirs
        expand_height = 'v' in expand_dirs
        fill_width = 'h' in fill_dirs
        fill_height = 'v' in fill_dirs
        if (fill_width and not expand_width) or \
           (fill_height and not expand_height):
            msg = "It is forbidden to set expand=False and fill=True."
            raise ValueError(msg)
        if isinstance(widget, Padded):
            raise TypeError("You tried to put a Padded into a Padded, " \
                            "you're doing something wrong.")
        self.widget = widget
        self.expand_width = expand_width
        self.expand_height = expand_height
        self.fill_width = fill_width
        self.fill_height = fill_height
        if len(padding) == 1:
            if isinstance(padding[0], Padding):
                self.padding = padding[0]
            else:
                self.padding = Padding(*padding)
        else:
            self.padding = Padding(*padding)

    def __repr__(self):
        return "%s(%r, %r, %r, %r, %r, %r)" % (self.__class__.__name__,
                                               self.widget,
                                               self.expand_width,
                                               self.expand_height,
                                               self.fill_width,
                                               self.fill_height,
                                               self.padding)

    def __str__(self):
        lines = [self.__class__.__name__]
        lines.append("    padding      : %r" % self.padding)
        lines.append("    expand_width : %r" % self.expand_width)
        lines.append("    expand_height: %r" % self.expand_height)
        lines.append("    fill_width   : %r" % self.fill_width)
        lines.append("    fill_height  : %r" % self.fill_height)
        lines.append("    widget       : %r" % self.widget)
        return "\n".join(lines)

    def _computeRequestedSize(self):
        """Request the size of the padding + the size of the widget."""
        self.widget.computeRequestedSize()
        return self.widget.requested_size + self.padding.size

    def _shrink(self, allocated_length, padding_length, requested_length):
        """Return the widget width and extra padding when shrinking.

        When the allocated size for a Padded object is smaller than its
        requested size, the object needs to shrink.

        Since shrinking the width or the height uses the same logic, this
        function is general and does not care about the dimension on which you
        are working.  It just needs to be fed with lengths and coordinates.

        When shrinking, the padding tries to keep its size as much as it can.
        Therefore, the widget will be the first to shrink.

        When the widget shrinks, its length is simply the allocated length
        minus the padding length.  The minimum length being 0 of course,
        no negative value will ever be accepted for a length.

        If the allocated length is smaller than the padding length, it means
        that not only the widget length will be 0, but also the padding needs
        to be reduced.

        Reducing the padding has only one effect: instead of setting the
        widget coordinate (left or top) to the Padding value (left or top),
        the coordinate must be something smaller.  Since we do not modify the
        Padding object introduce an extra padding.  In this case, the extra
        padding will be negative.

        """
        # Remove the padding to have the length of the widget.
        widget_length = allocated_length - padding_length
        if widget_length < 0:
            widget_length = 0
        # The padding itself may be reduced.
        if allocated_length < padding_length:
            extra_padding = allocated_length - padding_length
        else:
            extra_padding = 0
        return widget_length, extra_padding

    def _inflate(self, expand, fill, allocated_length, padding_length, widget_length):
        """Return the widget width and extra padding when inflating.

        When the allocated size for a Padded object is smaller than its
        requested size, the object needs to inflate.

        Two possibilities then:
        - fill=False: the widget keeps its requested length and the padding
          inflates.
        - fill=True: the widget inflates and the padding keeps its length.

        An additional health checked is performed: it is forbidden to inflate
        when expand=False.  Attempting to do so will raise a
        SizeAllocationError.  The container should never order a Padded widget
        with expand=False to occupy more space than it requires.

        """
        if not expand:
            msg = "Size allocation (%r) tried to expand a padded (%r) that " \
                  "was added with expand=False." % (allocated_length, self)
            raise SizeAllocationError(msg)
        if fill:
            # Keep the padding as it is but inflate the widget.
            extra_padding = 0
            widget_length = allocated_length - padding_length
        else:
            # Keep the widget as it is but inflate the padding.
            extra_padding = allocated_length - widget_length - padding_length
        return widget_length, extra_padding

    def allocateSize(self, allocated_size):
        """Allocate the size of the widget, taking the padding into account.

        First case: shrink.
        -------------------

        The padding tries to maintain its size as much as it can.  The widget
        will shrink down to a size of zero first, and then the padding starts
        shrinking.

        However, once the allocated size is smaller than even the padding, one
        must be careful when setting the position of the widget.  Indeed, we do
        not want the widget to have a position outside of the allocated area.

        In that situation, the left or top of the widget can be smaller than
        the left or top attributes of the padding.


        Second case: inflate.
        ---------------------

        According to the values of expand and fill, the extra space goes either
        into an extra padding, or into the widget.

        * expand = False and fill = False

        Forbidden.  If you ask for a wider space than the requested size with
        these conditions, then you made a programming error.  Raises
        SizeAllocationError.

        * expand = False and fill = True

        Forbidden.  It is not even allowed to instantiate such a Padded object.
        expand has to be True if we want fill to be True as well.

        * expand = True and fill = False

        The padded inflates and put its extra space around the widget, as
        extra padding.

        * expand = True and fill = True

        The padded inflates and put its extra space inside the widget.


        Third case: neither shrink nor inflate.
        ---------------------------------------

        Happens when the allocated size is exactly the requested size.  In that
        case, both the padding and the widget get what they want.

        """
        self.allocated_size = allocated_size
        widget_size = SizeAllocation(0, 0, 0, 0)
        #
        for dimension_name, coord_name in (('width', 'left'), ('height', 'top')):
            allocated_length = getattr(allocated_size, dimension_name)
            requested_length = getattr(self.requested_size, dimension_name)
            padding_length = getattr(self.padding, dimension_name)
            padding_coord = getattr(self.padding, coord_name)
            if allocated_length < requested_length:
                # Shrink.
                widget_length, extra_padding = self._shrink(allocated_length,
                                                            padding_length,
                                                            requested_length)
            elif allocated_length > requested_length:
                # Inflate.
                expand = getattr(self, 'expand_%s' % dimension_name)
                fill = getattr(self, 'fill_%s' % dimension_name)
                widget_length = getattr(self.widget.requested_size,
                                        dimension_name)
                widget_length, extra_padding = self._inflate(expand, fill,
                                                             allocated_length,
                                                             padding_length,
                                                             widget_length)
            else:
                # Equal.
                widget_length = getattr(self.widget.requested_size,
                                        dimension_name)
                extra_padding = 0
            #
            # The extra padding must be shared, on both sides of the widget.
            # Let's just split it in two.
            # TODO: split it using the left/right or top/bottom as weights.
            extra_before = extra_padding // 2
            #extra_after = extra_padding - extra_before
            allocated_coord = getattr(allocated_size, coord_name)
            widget_coord = allocated_coord + padding_coord + extra_before
            #
            setattr(widget_size, dimension_name, widget_length)
            setattr(widget_size, coord_name, widget_coord)
        self.widget.allocateSize(widget_size)
