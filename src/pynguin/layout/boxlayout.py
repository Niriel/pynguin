#! /usr/bin/python
"""
Created on Nov 9, 2010

@author: Niriel
"""


from size import Size
from size import SizeAllocation
from layout import Layout


__all__ = ['HBoxLayout', 'VBoxLayout', 'BoxError']


class BoxError(RuntimeError):
    """Base error for the box module."""
    pass


def Homothecy(ori_lengths, dest_length):
    """Return a list of pos and lengths zoomed in or out to fit a length.

    This is used to shrink or inflate widgets in boxes during the size
    allocation phase.

    The word "length" is used here to mean either width or height.  It has
    nothing to do with the number of elements in the lists.

    ori_length is an array of integer: the original length of the widgets.

    dest_length is an integer: the length you in which you want to fit all the
    widgets.

    The result is a tuple containing two elements:
     - a list of positions,
     - a list of lengths.
    You can find the positions by accumulating the lenghts.

    >>> print Homothecy([50, 100, 33], 183) # No change in zoom.
    ([0, 50, 150], [50, 100, 33])

    >>> print Homothecy([50, 100, 33], 366) # Zoom in times 2.
    ([0, 100, 300], [100, 200, 66])

    >>> print Homothecy([50, 100, 33], 91) # Zoom out times 2.
    ([0, 25, 75], [25, 50, 16])

    >>> print Homothecy([50, 100, 33], 0)
    ([0, 0, 0], [0, 0, 0])

    That the sum of the resulting list of lengths is of course always equal to
    the destination length you pass as a parameter.  That's what this function
    is made for.

    """
    ori_positions = [0]
    for length in ori_lengths:
        ori_positions.append(ori_positions[-1] + length)
    ori_end = ori_positions[-1]
    if ori_end == dest_length:
        # No need to do any math here.
        dest_lengths = list(ori_lengths) # Safer to return a new object.
        dest_positions = [0]
        for length in dest_lengths[:-1]:
            dest_positions.append(dest_positions[-1] + length)
        return dest_positions, dest_lengths
    #
    factor = float(dest_length) / ori_end # Integer divisions create problems.
    dest_positions = [int(round(ori_position * factor)) \
                      for ori_position in ori_positions]
    #
    dest_lengths = []
    for i in xrange(len(dest_positions) - 1):
        dest_length = dest_positions[i + 1] - dest_positions[i]
        dest_lengths.append(dest_length)
    #
    return dest_positions[:-1], dest_lengths


def GetExpandableIds(cells, length_name):
    """Return a list of indexes of the cells that can expand in given dir.

    Parameters.
    -----------

    * cells: a list of cells.
    * length_name: a string "width" or "height".

    Return.
    -------

    A list of integers.  Each integer is an index for a cell in cells that can
    expand in the direction given by length_name.

    """
    result = []
    for cell_id, cell in enumerate(cells):
        if cell.isExpandable(length_name):
            result.append(cell_id)
    return result


class BoxLayout(Layout):
    """A BoxLayout organizes widgets in a row or a column.

    BoxLayout is an abstract class.  Use HBoxLayout and VBoxLayout.

    BoxLayout objects have a spacing attribute.  This positive integer commands
    the space that the BoxLayout requests and allocates BETWEEN the cells.  Do
    not mistake the spacing and the padding.

    A BoxLayout can be homogeneous or not.  A homogeneous box allocates the
    same space for all the cells.  A non-homogeneous (heterogeneous) box does
    not do that.  Define whether or not your BoxLayout is homogeneous by
    setting the appropriate parameter to True or False in the constructor.

    """

    # To overload in the subclasses.
    PRIMARY_LENGTH = 'undefined'
    SECONDARY_LENGTH = 'undefined'
    PRIMARY_COORD = 'undefined'
    SECONDARY_COORD = 'undefined'

    def __init__(self, spacing, is_homogeneous):
        """Initialize a new BoxLayout object.

        BoxLayout is abstract.

        Parameters.
        -----------

        * spacing: positive integer.

          The space that the BoxLayout allocates BETWEEN the cells, not
          around them.  Do not confuse with the padding of the cells.

        * is_homogeneous: boolean.

          True for a homogeneous BoxLayout (all the cells get the same size),
          False for a heterogeneous BoxLayout.

        >>> box = BoxLayout(8, True)
        >>> print box.spacing
        8
        >>> print box.is_homogeneous
        True

        Note that modifying spacing and is_homogeneous after the creation is
        not guaranteed to work.

        """
        Layout.__init__(self)
        self.spacing = spacing
        self.is_homogeneous = is_homogeneous

    def _requestSizeHomogeneous(self, cells):
        """Compute the size needed by a homogeneous BoxLayout.

        In a homogeneous box, the size allocated to the cells is the same
        for all.

        The algorithm looks at all the cells and finds the size of the
        biggest one.  This size is used for all the cells.

        This method is generic in the sense that it doesn't know whether the
        BoxLayout is horizontal (HBoxLayout) or vertical (VBoxLayout).  See the
        classes HBoxLayout and VBoxLayout.  The only difference between those
        two is that in one case, the primary dimension will be the width and
        the secondary will be the height, and in the other case it will be
        reversed.

        So for a horizontal box, have the following attribute values:
            PRIMARY_LENGTH = 'width'
            SECONDARY_LENGTH = 'height'
        and for a vertical box, have these
            PRIMARY_LENGTH = 'height'
            SECONDARY_LENGTH = 'width'

        """
        primary_length_name = self.PRIMARY_LENGTH
        secondary_length_name = self.SECONDARY_LENGTH
        max_size = Size(0, 0)
        try:
            for cell in cells:
                max_size |= cell.requested_size
        except AttributeError as ex:
            # I want to modify the text that's in the first arg.  But strings
            # as well as tuples are immutable.  So I just make a list for
            # a little while.
            args = list(ex.args)
            args[0] += ", did you forget to request the size of the padded?"
            ex.args = tuple(args)
            raise
        children_nb = len(cells)
        primary_length = children_nb * getattr(max_size, primary_length_name)
        secondary_length = getattr(max_size, secondary_length_name)

        primary_length += (children_nb - 1) * self.spacing

        result = Size(0, 0)
        setattr(result, primary_length_name, primary_length)
        setattr(result, secondary_length_name, secondary_length)
        return result

    def _requestSizeHeterogeneous(self, cells):
        """Compute the size needed by a heterogeneous BoxLayout.

        In a heterogeneous box, the size requested is just enough to hold
        the widgets with their requested size.

        The algorithm looks through all the widgets, summing their width or
        height (depends on the direction of the box), and taking the max of
        their height or width in the other direction.

        This method is generic in the sense that it doesn't know whether the
        BoxLayout is horizontal (HBoxLayout) or vertical (VBoxLayout).  See the classes HBoxLayout and
        VBoxLayout.  The only difference between those two is that in one case, the
        primary dimension will be the width and the secondary one will be the
        height, and in the other case it will be reversed.

        So for a horizontal box, have the following attribute values:
            PRIMARY_LENGTH = 'width'
            SECONDARY_LENGTH = 'height'
            PRIMARY_COORD = 'left'
            SECONDARY_COORD = 'top'
        and for a vertical box, have these
            PRIMARY_LENGTH = 'height'
            SECONDARY_LENGTH = 'width'
            PRIMARY_COORD = 'top'
            SECONDARY_COORD = 'left'

        """
        primary_length_name = self.PRIMARY_LENGTH
        secondary_length_name = self.SECONDARY_LENGTH
        primary_length = secondary_length = 0
        for cell in cells:
            cell_size = cell.requested_size
            primary_length += getattr(cell_size, primary_length_name)
            cell_secondary_length = getattr(cell_size, secondary_length_name)
            if cell_secondary_length > secondary_length:
                secondary_length = cell_secondary_length

        children_nb = len(cells)
        primary_length += (children_nb - 1) * self.spacing

        result = Size(0, 0)
        setattr(result, primary_length_name, primary_length)
        setattr(result, secondary_length_name, secondary_length)
        return result

    def requestSize(self, cells):
        """Compute the requested size of the BoxLayout."""
        if not cells:
            return Size(0, 0)
        if self.is_homogeneous:
            return self._requestSizeHomogeneous(cells)
        else:
            return self._requestSizeHeterogeneous(cells)

    def _allocatedSizeShrink(self, allocated_size, cells):
        """Performs the size allocation."""
        # What is the length we can give to the cells ? It's the total
        # allocated length minus the spacing.
        alloc_primary_len = getattr(allocated_size, self.PRIMARY_LENGTH)
        total_cell_length = alloc_primary_len - self.spacing * (len(cells) - 1)

        if total_cell_length > 0:
            # Apply the Homothecy on the cells. For the heterogeneous case, the
            # original lengths are the requested lengths.  For the homogeneous
            # case, the original lengths are all equals to the biggest
            # requested length. The destination length is the length calculated
            # above. We obtain the position and length of every widget.
            primary_lengths = [getattr(cell.requested_size,
                                       self.PRIMARY_LENGTH)
                               for cell in cells]
            if self.is_homogeneous:
                primary_lengths = [max(primary_lengths)] * len(cells)
            primary_coords, primary_lengths = Homothecy(primary_lengths,
                                                        total_cell_length)
            # The position needs to take the spacing into account.  Plus the
            # position of the BoxLayout itself.
            box_primary_coord = getattr(allocated_size, self.PRIMARY_COORD)
            for i in xrange(len(primary_coords)):
                primary_coords[i] += box_primary_coord + i * self.spacing
        else:
            # We shrink so much that there is no room for the cells at all
            # anymore.  Not even enough room for the spacing.
            #
            # But because we want to do things well, we are going to apply an
            # homothecy on the spacing itself in order to shrink it properly.
            # The coordinates resulting from the homothecy will give us the
            # coordinates of our cells.
            primary_lengths = [self.spacing] * (len(cells) - 1)
            primary_coords, primary_lengths = Homothecy(primary_lengths,
                                                        alloc_primary_len)
            # The last cell starts after the last spacing.
            primary_coords += [primary_coords[-1] + primary_lengths[-1]]
            box_primary_coord = getattr(allocated_size, self.PRIMARY_COORD)
            for i in xrange(len(primary_coords)):
                primary_coords[i] += box_primary_coord
            # No room for cells at all.
            primary_lengths = [0] * len(cells)

        secondary_coord = getattr(allocated_size, self.SECONDARY_COORD)
        secondary_length = getattr(allocated_size, self.SECONDARY_LENGTH)

        for cell_id in xrange(len(cells)):
            cell_size = SizeAllocation((0, 0), (0, 0))
            setattr(cell_size, self.PRIMARY_COORD, primary_coords[cell_id])
            setattr(cell_size, self.SECONDARY_COORD, secondary_coord)
            setattr(cell_size, self.PRIMARY_LENGTH, primary_lengths[cell_id])
            setattr(cell_size, self.SECONDARY_LENGTH, secondary_length)
            cells[cell_id].allocateSize(cell_size)

    def _allocateSizeInflate(self, allocated_size, cells):
        """Performs the size allocation."""
        # What is the length we can give to the cells ?  It's the allocated
        # length minus the spacing.
        total_cell_length = getattr(allocated_size, self.PRIMARY_LENGTH)
        total_cell_length -= self.spacing * (len(cells) - 1)

        # Compute an list of lengths, one length per cell: `lengths`.
        if self.is_homogeneous:
            # The homogeneous case is easy: pretend that all the cells have
            # requested the same length: the length of the longest cell. Then
            # apply an homothecy to make it fit the allocated size.
            max_length = 0
            for cell in cells:
                length = getattr(cell.requested_size, self.PRIMARY_LENGTH)
                if length > max_length:
                    max_length = length
                lengths = [max_length] * len(cells)
            unused, lengths = Homothecy(lengths, total_cell_length)
            del unused, max_length
        else:
            # Heterogeneous case.  Some cells can expand, some cannot.  The
            # extra space is only for the cells that can expand.  We will apply
            # an homothecy on the expandable cells.  For that, we need to
            # identify them.  We also need to compute the available space for
            # the expandable cells by removing the space claimed by the fixed
            # cells.
            lengths = [0] * len(cells)
            exp_ids = []
            exp_lengths = []
            for cell_id, cell in enumerate(cells):
                length = getattr(cell.requested_size, self.PRIMARY_LENGTH)
                if cell.isExpandable(self.PRIMARY_LENGTH):
                    # Take note of expandable cells for homothecy.
                    exp_ids.append(cell_id)
                    exp_lengths.append(length)
                else:
                    # Non-expandable cells need no homothecy.
                    lengths[cell_id] = length
            # Compute allocated length available for expandable cells.
            total_exp_length = total_cell_length - sum(lengths)
            # Perform the homothecy on the expandable cells.
            unused, exp_lengths = Homothecy(exp_lengths, total_exp_length)
            # Inject the result of the homothecy into the `lengths` list.
            for cell_id, length in zip(exp_ids, exp_lengths):
                lengths[cell_id] = length
            # Make sure we don't reuse this stuff later.
            del exp_ids, exp_lengths, total_exp_length, unused, cell_id

        # Compute the positions from the lengths.
        coords = [getattr(allocated_size, self.PRIMARY_COORD)]
        for length in lengths:
            coords.append(coords[-1] + length + self.spacing)

        # For the secondary (transverse) dimension, easy:
        secondary_coord = getattr(allocated_size, self.SECONDARY_COORD)
        secondary_length = getattr(allocated_size, self.SECONDARY_LENGTH)

        # Finally, allocate the size of each cell.
        for cell, primary_coord, primary_length in zip(cells, coords, lengths):
            cell_size = SizeAllocation((0, 0), (0, 0))
            setattr(cell_size, self.PRIMARY_COORD, primary_coord)
            setattr(cell_size, self.SECONDARY_COORD, secondary_coord)
            setattr(cell_size, self.PRIMARY_LENGTH, primary_length)
            setattr(cell_size, self.SECONDARY_LENGTH, secondary_length)
            cell.allocateSize(cell_size)

    def _allocateSizeIdeal(self, allocated_size, cells):
        """Performs the size allocation."""
        # Secondary dimension is the same for everybody.
        secondary_length = getattr(allocated_size, self.SECONDARY_LENGTH)
        secondary_coord = getattr(allocated_size, self.SECONDARY_COORD)

        # Homogeneous box: every cell gets the max primary.
        # Heterogeneous box: every cell gets the primary it asked for.
        if self.is_homogeneous:
            primary_length = 0
            for cell in cells:
                cell_prim = getattr(cell.requested_size,
                                    self.PRIMARY_LENGTH)
                if cell_prim > primary_length:
                    primary_length = cell_prim
        heterogeneous = not self.is_homogeneous
        primary_coord = getattr(allocated_size, self.PRIMARY_COORD)
        for cell in cells:
            if heterogeneous:
                primary_length = getattr(cell.requested_size,
                                         self.PRIMARY_LENGTH)
            size_a = SizeAllocation((0, 0), (0, 0))
            setattr(size_a, self.PRIMARY_LENGTH, primary_length)
            setattr(size_a, self.SECONDARY_LENGTH, secondary_length)
            setattr(size_a, self.PRIMARY_COORD, primary_coord)
            setattr(size_a, self.SECONDARY_COORD, secondary_coord)
            cell.allocateSize(size_a)
            primary_coord += primary_length + self.spacing

    def allocateSize(self, allocated_size, requested_size, cells):
        """Allocate the size of the box.

        Child widgets inflate or shrink by a factor proportional to their
        requested size.

        There is a difference between inflating and shrinking: not all widgets
        can inflate (expand=False) but all can shrink.

        The ideal case, where all widgets get what they want, is no different
        from shrinking or inflating by a factor 1.

        Note first that if no cell widget was added with expand=True, then
        trying to allocate more size than what the BoxLayout requests is forbidden.
        Doing so raises a size.SizeAllocationError.

        """
        if not cells:
            return
        allocated_primary = getattr(allocated_size, self.PRIMARY_LENGTH)
        allocated_secondary = getattr(allocated_size, self.SECONDARY_LENGTH)
        requested_primary = getattr(requested_size, self.PRIMARY_LENGTH)
        requested_secondary = getattr(requested_size, self.SECONDARY_LENGTH)
        #
        # Not allowed to inflate if no widget can expand.
        #
        if allocated_primary > requested_primary:
            can_expand_primary = False
            for cell in cells:
                if cell.isExpandable(self.PRIMARY_LENGTH):
                    can_expand_primary = True
                    break
            if not can_expand_primary:
                msg = "Cannot inflate a BoxLayout if no widget can expand."
                raise BoxError(msg)

        if allocated_secondary > requested_secondary:
            can_expand_secondary = False
            for cell in cells:
                if cell.isExpandable(self.SECONDARY_LENGTH):
                    can_expand_secondary = True
                    break
            if not can_expand_secondary:
                msg = "Cannot inflate a BoxLayout if no widget can expand."
                raise BoxError(msg)

        if allocated_primary > requested_primary:
            self._allocateSizeInflate(allocated_size, cells)
        elif allocated_primary < requested_primary:
            self._allocatedSizeShrink(allocated_size, cells)
        else:
            self._allocateSizeIdeal(allocated_size, cells)

class HBoxLayout(BoxLayout):
    """HBoxLayout layout places its children in a row."""
    PRIMARY_LENGTH = 'width'
    SECONDARY_LENGTH = 'height'
    PRIMARY_COORD = 'left'
    SECONDARY_COORD = 'top'

class VBoxLayout(BoxLayout):
    """VBoxLayout layout places its children in a column."""
    PRIMARY_LENGTH = 'height'
    SECONDARY_LENGTH = 'width'
    PRIMARY_COORD = 'top'
    SECONDARY_COORD = 'left'
