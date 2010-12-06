'''
Created on Nov 25, 2010

@author: Niriel
'''

from sizeable import Sizeable
from padding import Padding
import size


__all__ = ['CellError', 'Cell']


class CellError(RuntimeError):
    pass


class Cell(Sizeable):
    """Holds a Sizeable object and a Padding object together.

    This is a useful things for containers: each Sizeable object comes with a
    padding but the padding is not an intrinsic property of the Sizeable
    object.  This class aims at binding the two.

    This class has the following attributes:

    - padded: the Sizeable object you are padding.

    - padding: the padding you surround the padded with.

    - requested_size: the result of the method requestSize.

    - allocated_size: the argument passed during the last call to the method
      allocateSize().

    - expand_width, expand_height: boolean set to True if the cell is
      allowed to occupy more space that its requested size in the given
      direction.

    - fill_width, fill_height: boolean set to True if the extra space when
      expand_*=True has to be given to the padded rather than its padding.

    Cell inherits from Sizable and implements a simple algorithm for
    computing the requested size.  It adds the size of the padding to the size
    of the padded.  This allows a Container to ask a Cell object the size it
    needs.

    Likewise, Cell objects come with a allocateSize method.

    """

    # I felt like putting shitty numbers there because I don't want developers
    # starting to do smartass things with simples values like 0, 1 and 2.  Like
    # using the truth value, or doing bitwise operations, whatever.  Just use
    # the fucking constants.  Gosh I'd like an enumerated type in Python.

    EXPAND_NOT = 42
    EXPAND_PADDING = 666
    EXPAND_PADDED = 1984

    def __init__(self, padded, expand_width, expand_height, *padding):
        """Create a new Cell object, binding a Sizeable and a Padding object.

        The constructor takes a variable number of parameters.

        The first parameter is the Sizeable object you wish to surround with
        the padding.  We call this object "the padded".

        >>> cell = Cell('a padded', Cell.EXPAND_NOT, Cell.EXPAND_NOT)
        >>> print cell.padded
        a padded

        Of course the string 'a padded' is hardly a Sizeable, but it shows you
        that the first parameter is accessible later through the padded
        attribute.

        The second and thirds parameters are expand_width and expand_height.
        The valid values for these parameters are Cell.EXPAND_NOT,
        Cell.EXPAND_PADDING and Cell.EXPAND_PADDED.
        
        EXPAND_NOT: the cell cannot expand.  Trying to allocate a size bigger
        than its requested size will raise an exception.

        EXPAND_PADDING: the cell can expand, and the extra space is given to
        the padding.  The padded keeps its requested size.

        EXPAND_PADDED: the cell can expand, and the extra space is given to the
        padded. The padding remains intact.

        The other parameters define the padding.  You can pass the 0 to 4
        parameters defining a padding, or directly one padding object.

        >>> print repr(Cell('padded', Cell.EXPAND_NOT, Cell.EXPAND_NOT).padding)
        Padding(0, 0, 0, 0)

        >>> print repr(Cell('padded', Cell.EXPAND_NOT, Cell.EXPAND_NOT, 42).padding)
        Padding(42, 42, 42, 42)

        >>> print repr(Cell('padded', Cell.EXPAND_NOT, Cell.EXPAND_NOT, 42, 666).padding)
        Padding(42, 42, 666, 666)

        >>> print repr(Cell('padded', Cell.EXPAND_NOT, Cell.EXPAND_NOT, 1, 2, 3, 4).padding)
        Padding(1, 2, 3, 4)

        >>> padding = Padding(1, 2, 3, 4)
        >>> cell = Cell('padded', Cell.EXPAND_NOT, Cell.EXPAND_NOT, padding)
        >>> print repr(cell.padding)
        Padding(1, 2, 3, 4)
        >>> print cell.padding is padding
        True

        """
        Sizeable.__init__(self)

        VALID = (Cell.EXPAND_NOT, Cell.EXPAND_PADDED, Cell.EXPAND_PADDING)
        VALIDSTR = "(Cell.EXPAND_NOT, Cell.EXPAND_PADDED, Cell.EXPAND_PADDING)"
        if expand_width not in VALID:
            msg = "expand_width must be in %s (%r given)." % (VALIDSTR, expand_width)
            raise ValueError(msg)
        if expand_height not in VALID:
            msg = "expand_height must be in %s (%r given)." % (VALIDSTR, expand_height)
            raise ValueError(msg)

        if isinstance(padded, Cell):
            # This is how much I trust myself.
            raise TypeError("You tried to put a Cell into a Cell, " \
                            "you're doing something wrong.")

        self.padded = padded
        self.expand_width = expand_width
        self.expand_height = expand_height

        if len(padding) == 1:
            if isinstance(padding[0], Padding):
                self.padding = padding[0]
            else:
                self.padding = Padding(*padding)
        else:
            self.padding = Padding(*padding)

    def __getConstName(self, value):
        d = {Cell.EXPAND_NOT: 'Cell.EXPAND_NOT',
             Cell.EXPAND_PADDED: 'Cell.EXPAND_PADDED',
             Cell.EXPAND_PADDING: 'Cell.EXPAND_PADDING'}
        return d[value]

    def __repr__(self):
        expand_width = self.__getConstName(self.expand_width)
        expand_height = self.__getConstName(self.expand_height)
        return "%s(%r, %s, %s, %r)" % (self.__class__.__name__, self.padded,
                                       expand_width, expand_height,
                                       self.padding)

    def __str__(self):
        expand_width = self.__getConstName(self.expand_width)
        expand_height = self.__getConstName(self.expand_height)
        lines = [self.__class__.__name__]
        lines.append("    padding      : %r" % self.padding)
        lines.append("    expand_width : %s" % expand_width)
        lines.append("    expand_height: %s" % expand_height)
        lines.append("    padded       : %r" % self.padded)
        return "\n".join(lines)

    def isExpandable(self, direction):
        attribute_name = 'expand_' + direction
        return getattr(self, attribute_name) != Cell.EXPAND_NOT

    def _requestSize(self):
        """Request the size of the padding + the size of the padded."""
        self.padded.requestSize()
        return self.padded.requested_size + self.padding.size

    def _shrink(self, length_name):
        """Return the padded width and extra padding when shrinking.

        When the allocated length for a Cell object is smaller than its
        requested size, the Cell object needs to shrink.

        The input parameter length_name (valid values are 'width' and 'length')
        determine the direction that is considered.

        When shrinking, the padding tries to keep its size as long as it can.
        Therefore, the padded will be the first to shrink.

        When the padded shrinks, its allocated length equals the allocated
        length of the Cell object minus the padding length.  If the allocated
        length for the padded object is negative, it is brought back to 0: no
        negative value will ever be accepted for a length.

        If the allocated length for the Cell object is smaller than the padding
        length, then not only the padded has a length of 0 but the padding
        needs to shrink as well.  The extra_padding resulting from this
        function will then be negative.

        """
        # Remove the padding to have the length of the padded.
        allocated_length = getattr(self.allocated_size, length_name)
        padding_length = getattr(self.padding, length_name)
        padded_length = allocated_length - padding_length
        if padded_length < 0:
            padded_length = 0
        # The padding itself may be reduced.
        if allocated_length < padding_length:
            extra_padding = allocated_length - padding_length # Negative.
        else:
            extra_padding = 0
        return padded_length, extra_padding

    def _inflate(self, length_name):
        """Return the padded length and extra padding when inflating.

        This works for one direction specified by the input parameter
        length_name: 'width' or 'height'.

        When the allocated length for a Cell object is bigger than its
        requested length, the object needs to inflate.

        Two possibilities then:

        - expand = EXPAND_PADDING : the padded keeps its requested length and
          the padding inflates.

        - expand = EXPAND_PADDED : the padded inflates and the padding keeps
          its length.

        An additional health checked is performed: it is forbidden to inflate
        when expand = EXPAND_NOT.  Attempting to do so will raise a
        SizeAllocationError.  The container should never order a Cell padded
        with expand = EXPAND_NOT to occupy more length than it requires.

        """
        expand_name = 'expand_' + length_name
        expand = getattr(self, expand_name)
        if expand == Cell.EXPAND_NOT:
            msg = "A cell with %s=Cell.EXPAND_NOT was asked to expand its %s" \
                  " beyond the requested size." % (expand_name, length_name)
            raise CellError(msg)
        elif expand == Cell.EXPAND_PADDED:
            # Inflate the padded and keep the padding.
            padded_length = getattr(self.allocated_size, length_name) - \
                            getattr(self.padding, length_name)
            extra_padding = 0
        elif expand == Cell.EXPAND_PADDING:
            # Keep the padded and inflate the padding.
            padded_length = getattr(self.padded.requested_size, length_name)
            extra_padding = getattr(self.allocated_size, length_name) - \
                            getattr(self.padding, length_name) - \
                            padded_length
        else:
            raise ValueError("Invalid value for %s: %r." % expand_name, expand)
        return padded_length, extra_padding

    def _allocateSize(self):
        """Allocate the size of the padded, taking the padding into account.

        First case: shrink.
        -------------------

        The padding tries to maintain its size as long as it can.  The padded
        will shrink down to a size of zero first, and then the padding starts
        shrinking.


        Second case: inflate.
        ---------------------

        According to the values of expand_width and expand_height, the extra
        space goes either into an extra padding, or into the padded.

        * expand = Cell.EXPAND_NOT

        Forbidden.  If you ask for a wider space than the requested size with
        these conditions, then you made a programming error.  Raises
        SizeAllocationError.

        * expand = Cell.EXPAND_PADDING

        The cell inflates and put its extra space around the padded, as
        extra padding.

        * expand = Cell.EXPAND_PADDED

        The cell inflates and put its extra space inside the padded.


        Third case: neither shrink nor inflate.
        ---------------------------------------

        Happens when the allocated size is exactly the requested size.  In that
        case, both the padding and the padded get what they want.

        """
        allocated_size = self.allocated_size
        padded_size = size.SizeAllocation(size.Pos(0, 0),
                                          size.Size(0, 0))
        #
        for length_name, coord_name in (('width', 'left'), ('height', 'top')):
            # Here we are computing two things:
            # - the length to allocate to the object: padded_length;
            # - how much padding we need to add or remove: extra_padding.
            # And this, for each direction (horizontal and vertical).
            allocated_length = getattr(allocated_size, length_name)
            requested_length = getattr(self.requested_size, length_name)
            if allocated_length < requested_length:
                # Shrink.
                padded_length, extra_padding = self._shrink(length_name)
            elif allocated_length > requested_length:
                # Inflate.
                padded_length, extra_padding = self._inflate(length_name)
            else:
                # Ideal case.  The padded gets the length it wants.
                padded_length = getattr(self.padded.requested_size, length_name)
                extra_padding = 0

            # The extra padding must be shared, on both sides of the widget.
            # Let's just split it in two.
            # TODO: split it using the left/right or top/bottom as weights.
            extra_before = extra_padding // 2
            allocated_coord = getattr(allocated_size, coord_name)
            padding_coord = getattr(self.padding, coord_name)
            padded_coord = allocated_coord + padding_coord + extra_before

            setattr(padded_size, length_name, padded_length)
            setattr(padded_size, coord_name, padded_coord)
        self.padded.allocateSize(padded_size)
