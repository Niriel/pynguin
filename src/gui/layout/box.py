'''
Created on Nov 9, 2010

@author: Niriel
'''


import size
import container
from cell import Cell


__all__ = ['HBox', 'VBox']


def Homothecy(ori_lengths, dest_length):
    """Returns a list of lengths zoomed in or out to fit the destination.

    This is used to shrink or inflate widgets in boxes during the size
    allocation phase.
    
    The word "length" is used here to mean either width or height.  It has
    nothing to do with the number of elements in the lists.

    ori_length is an array of integer: the original length of the widgets.

    dest_length is an integer: the length you in which you want to fit all the
    widgets.

    >>> Homothecy([50, 100, 33], 183) # No change in zoom.
    [50, 100, 33]

    >>> Homothecy([50, 100, 33], 366) # Zoom in times 2.
    [100, 200, 66]

    >>> Homothecy([50, 100, 33], 91) # Zoom out times 2.
    [25, 50, 16]

    >>> Homothecy([50, 100, 33], 0)
    [0, 0, 0]

    That the sum of the resulting vector is of course always equal to the
    destination length you pass as a parameter.  That's what this function is
    made for.

    """
    ori_positions = [0]
    for length in ori_lengths:
        ori_positions.append(ori_positions[-1] + length)
    ori_end = ori_positions[-1]
    if ori_end == dest_length:
        # No need to do any math here.
        return [] + ori_lengths # Probably safer to return a different object.
    #
    factor = float(dest_length) / ori_end # Integer divisions create problems.
    dest_positions = []
    for ori_position in ori_positions:
        dest_position = int(round(ori_position * factor))
        dest_positions.append(dest_position)
    #
    dest_lengths = []
    for i in range(len(dest_positions) - 1):
        dest_length = dest_positions[i + 1] - dest_positions[i]
        dest_lengths.append(dest_length)
    #
    return dest_lengths


class Box(container.Container):
    """A Box is a container that organizes child widgets in a row or a column.

    Box is an abstract class.  Use HBox and VBox.

    Box objects have a spacing attribute.  This positive integer commands the
    space that the Box requests and allocates BETWEEN the child widgets.  Do
    not mistake the spacing and the padding.

    A Box can be homogeneous or not.  A homogeneous box allocates the same
    space for all the child widgets it contains.  A non-homogeneous
    (heterogeneous) box does not do that.  Define whether or not your Box is
    homogeneous by setting the appropriate parameter to True or False in the
    constructor.  There is NO GUARANTEE that changing the parameter after the
    box is constructed will work as you expect.

    """

    PRIMARY_LENGTH = 'undefined'
    SECONDARY_LENGTH = 'undefined'
    PRIMARY_COORD = 'undefined'
    SECONDARY_COORD = 'undefined'


    def __init__(self, spacing, homogeneous):
        """Create a new Box object.

        Note that Box is 'abstract', do not use it for your production code.
        Use it for testing purposes only.

        Parameter spacing: positive integer.  The space that the Box allocates
        BETWEEN widgets.  Not around them.  Do not confuse with the padding.

        Parameter homogeneous: boolean.  True for a homogeneous Box, False for
        a non-homogeneous Box.

        """
        container.Container.__init__(self)
        self.spacing = spacing
        self.homogeneous = homogeneous

    def addChild(self, child, expand_width, expand_height, *padding):
        """Adds a child to the Box.

        child: a widget.
        
        expand_width, expand_height, *padding: please refer to the
        documentation of cell.Cell.

        It is mandatory to set at least one of the directions of expand to
        Cell.EXPAND_PADDING or Cell.EXPAND_PADDED.  For a horizontal box (see
        class HBox), the vertical direction must be able to expand.  And for a
        vertical box, it is the horizontal dimension that should be able to
        expand.  Box being common to HBox and VBox, it simply ensures that one
        is set.  The rest is to be checked by HBox and VBox themselves.

        """
        if (expand_width, expand_height) == (Cell.EXPAND_NOT, Cell.EXPAND_NOT):
            msg = "When adding a child to a Box, at least one of the " \
                  "directions of expand_dirs must be set."
            raise container.ContainerError(msg)
        container.Container.addChild(self, child, expand_width, expand_height,
                                     *padding)

    def _requestSizeHomogeneous(self):
        """Compute the size needed by a homogeneous Box.

        In a homogeneous box, the space allocated to the widgets is the same
        for all.

        The algorithm looks at all the widgets and finds the size of the
        biggest one.  This size is used for all the widgets.

        Be careful: when the Box is homogeneous, then make sure that all the
        cells inside have expand=True.  It will not be a problem during the
        size requisition, but it will break during the size allocation, raising
        AllocationSizeError.

        This method is generic in the sense that it doesn't know whether the
        Box is horizontal (HBox) or vertical (VBox).  See the classes HBox and
        VBox.  The only difference between those two is that in one case, the
        length dimension will be the width and the thickness will be the height, and
        in the other case it will be reversed.

        So for a horizontal box, have the following attribute values:
            PRIMARY_LENGTH = 'width'
            SECONDARY_LENGTH = 'height'
        and for a vertical box, have these
            PRIMARY_LENGTH = 'height'
            SECONDARY_LENGTH = 'width'

        """
        PRIMARY_LENGTH = self.PRIMARY_LENGTH
        SECONDARY_LENGTH = self.SECONDARY_LENGTH
        max_size = size.Size(0, 0)
        for child in self.cells:
            child.requestSize()
            max_size |= child.requested_size
        children_nb = len(self.cells)
        length = children_nb * getattr(max_size, PRIMARY_LENGTH)
        thickness = getattr(max_size, SECONDARY_LENGTH)
        if children_nb >= 2:
            length += (children_nb - 1) * self.spacing
        result = size.Size(0, 0)
        setattr(result, PRIMARY_LENGTH, length)
        setattr(result, SECONDARY_LENGTH, thickness)
        return result

    def _requestSizeHeterogeneous(self):
        """Compute the size needed by a non-homogeneous Box.

        In a non-homogeneous box, the size requested is just enough to hold
        the widgets with their preferred size.

        The algorithm looks through all the widgets, summing their width or
        height (depends on the direction of the box), and taking the max of
        their height or width in the other direction.

        This method is generic in the sense that it doesn't know whether the
        Box is horizontal (HBox) or vertical (VBox).  See the classes HBox and
        VBox.  The only difference between those two is that in one case, the
        long dimension will be the width and the short will be the height, and
        in the other case it will be reversed.

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
        long_name = self.PRIMARY_LENGTH
        short_name = self.SECONDARY_LENGTH
        box_long = box_short = 0
        for child in self.cells:
            child.requestSize()
            child_size = child.requested_size
            box_long += getattr(child_size, long_name)
            child_short = getattr(child_size, short_name)
            if child_short > box_short:
                box_short = child_short
        children_nb = len(self.cells)
        # Add the spacing between the widgets.
        if children_nb >= 2:
            box_long += (children_nb - 1) * self.spacing
        result = size.Size(0, 0)
        setattr(result, long_name, box_long)
        setattr(result, short_name, box_short)
        return result

    def _requestSize(self):
        """Compute the requested size of the Box."""
        if self.homogeneous:
            return self._requestSizeHomogeneous()
        else:
            return self._requestSizeHeterogeneous()

    def _shrink(self):
        if not self.cells:
            return
        PRIMARY_LENGTH = self.PRIMARY_LENGTH
        SECONDARY_LENGTH = self.SECONDARY_LENGTH
        PRIMARY_COORD = self.PRIMARY_COORD
        SECONDARY_COORD = self.SECONDARY_COORD
        allocated_primary = getattr(self.allocated_size, PRIMARY_LENGTH)
        allocated_secondary = getattr(self.allocated_size, SECONDARY_LENGTH)
        requested_primary = getattr(self.requested_size, PRIMARY_LENGTH)

        # We're going to deal with floating point numbers here.  This is risky
        # because we're gonna loose precision. It means that we might be off by
        # a pixel or two at the end. It is of course unacceptable, therefore I
        # need to make sure that everything adds up. The easy way I am thinking
        # about to do that is to keep the last child out of the loop, and give
        # it the remaining space.

        # We need to think about the spacing too.  The Box tries to maintain
        # its spacing as long as it can, but if we run out, we need to start
        # shrinking it too.
        children_nb = len(self.cells) # Minimum 1 at this point.
        total_spacing = (children_nb - 1) * self.spacing
        if requested_primary > total_spacing:
            # We can keep the spacing intact.
            spacing = self.spacing
            # There is still room for the cells. Measure it.
            children_request = 0
            for child in self.cells:
                children_request += getattr(child.requested_size, PRIMARY_LENGTH)
            factor = float(allocated_primary - total_spacing) / children_request
        else:
            # Here the children are reduced to size zero. It means that there
            # is NOTHING to display but empty space. Therefore we do not have
            # to worry at all about the spacing.
            spacing = 0
            total_spacing = 0
            factor = 0
        # No need to define spacing if 0 or 1 child: won't enter the loop
        # in which spacing is used.

        # TODO: re-think the following piece of code.  I should round the
        # accumulated size and not accumulate the rounded size.  Not only can
        # it lead me to under-estimate all the children until the last one
        # which will become too big; but it can also lead me to over-estimate
        # all the child and have to force the last one to a negative size !
        # The difficulty comes from the spacing which is not scaled down.

        # I'm thinking about keeping two cursors, one in the requested scale,
        # one in the allocated scale.  And they move together...  But wouldn't
        # that make me do the same mistake ?

        # Maybe I need to keep two accumulated sizes:
        # - The accumulated sizes of the widgets in the requested scale
        # - and in the allocated scale.
        # Comes a new widget.  I add its size to the accumulated requested
        # scale.  Now I apply the zoom factor and get a new allocated value. If
        # I subtract the accumulated allocated size from this value I get the
        # allocated width for that widget !

        cumul_long = 0
        for child in self.cells[:-1]:
            child_request = child.requested_size
            child_long = int(round(getattr(child_request, PRIMARY_LENGTH) * factor))
            child_size = size.SizeAllocation(size.Pos(0, 0),
                                             size.Size(0, 0))
            setattr(child_size, PRIMARY_LENGTH, child_long)
            setattr(child_size, SECONDARY_LENGTH, allocated_secondary)
            setattr(child_size, PRIMARY_COORD, cumul_long)
            setattr(child_size, SECONDARY_COORD, 0)
            child.allocateSize(child_size)
            cumul_long += child_long + spacing
        child = self.cells[-1]
        child_size = size.SizeAllocation(size.Pos(0, 0), size.Size(0, 0))
        setattr(child_size, PRIMARY_LENGTH, allocated_primary - cumul_long)
        setattr(child_size, SECONDARY_LENGTH, allocated_secondary)
        setattr(child_size, PRIMARY_COORD, cumul_long)
        setattr(child_size, SECONDARY_COORD, 0)
        child.allocateSize(child_size)

    def _getExpandableIds(self, length_name):
        result = []
        for cell_id, cell in enumerate(self.cells):
            if cell.isExpandable(length_name):
                result.append(cell_id)
        return result

    def _inflate(self):
        if not self.cells:
            return

        allocated_size = self.allocated_size
        cells = self.cells
        PRIMARY_LENGTH = self.PRIMARY_LENGTH
        SECONDARY_LENGTH = self.SECONDARY_LENGTH

        #children_allo_size = map(size.SizeAllocation, cells)
        children_allo_size = []
        for child_id in range(len(cells)):
            children_allo_size.append(size.SizeAllocation(size.Pos(0, 0),
                                                          size.Size(0, 0)))

        # The secondary direction is easy, just apply it to every child.
        secondary_length = getattr(allocated_size, SECONDARY_LENGTH)
        for child_allo_size in children_allo_size:
            setattr(child_allo_size, SECONDARY_LENGTH, secondary_length)

        # Not every child can inflate.  Only those with the expand property
        # can.
        expandable_ids = self._getExpandableIds(PRIMARY_LENGTH)
        if not expandable_ids:
            msg = "No child can expand, the box cannot inflate."
            raise RuntimeError(msg)

        # What is the space we can give to the expandable cells ? It's the
        # total allocated space, minus the spacing, minus the length of the
        # non-expandable cells.  Meanwhile, the non-expandable cells just
        # get what they ask for.        
        expandable_children_length = getattr(allocated_size, PRIMARY_LENGTH)
        expandable_children_length -= self.spacing * (len(cells) - 1)
        for child_id, child in enumerate(cells):
            if child_id not in expandable_ids:
                child_length = getattr(child.requested_size, PRIMARY_LENGTH)
                expandable_children_length -= child_length
                setattr(children_allo_size[child_id], PRIMARY_LENGTH, child_length)

        # Apply the homothecy on the expandable cells.
        # The original lengths are the requested lengths.
        # The destination length is the length calculated above.
        ori_lengths = []
        for child_id in expandable_ids:
            child_length = getattr(self.cells[child_id].requested_size, PRIMARY_LENGTH)
            ori_lengths.append(child_length)
        dest_lengths = Homothecy(ori_lengths, expandable_children_length)
        for child_id, child_length in zip(expandable_ids, dest_lengths):
            setattr(children_allo_size[child_id], PRIMARY_LENGTH, child_length)
        del ori_lengths, dest_lengths # Remove temptation to use them.

        # We took care of all the heights and widths.  Time to look at the
        # positions now.
        PRIMARY_COORD = self.PRIMARY_COORD
        SECONDARY_COORD = self.SECONDARY_COORD
        allo_primary = getattr(allocated_size, PRIMARY_COORD)
        allo_secondary = getattr(allocated_size, SECONDARY_COORD)
        spacing = self.spacing
        for child_allo_size in children_allo_size:
            setattr(child_allo_size, PRIMARY_COORD, allo_primary)
            setattr(child_allo_size, SECONDARY_COORD, allo_secondary)
            allo_primary += getattr(child_allo_size, PRIMARY_LENGTH)
            allo_primary += spacing

        # Finally allocated all the calculated sizes.
        for child, child_allo_size in zip(cells, children_allo_size):
            child.allocateSize(child_allo_size)

    
    def _ideal(self):
        if not self.cells:
            return
        # Secondary dimension is the same for everybody.
        secondary_length = getattr(self.allocated_size, self.SECONDARY_LENGTH)
        secondary_coord = getattr(self.allocated_size, self.SECONDARY_COORD)
        
        # Homogeneous box: every cell gets the max primary possible.
        # Heterogeneous box: every cell gets the primary it asked for.
        if self.homogeneous:
            primary_length = 0
            for cell in self.cells:
                cell_prim = getattr(cell.requested_size, self.PRIMARY_LENGTH)
                if cell_prim > primary_length:
                    primary_length = cell_prim
        heterogeneous = not self.homogeneous
        primary_coord = getattr(self.allocated_size, self.PRIMARY_COORD)
        for cell in self.cells:
            if heterogeneous: 
                primary_length = getattr(cell.requested_size, self.PRIMARY_LENGTH)
            sa = size.SizeAllocation(size.Pos(0, 0), size.Size(0, 0))
            setattr(sa, self.PRIMARY_LENGTH, primary_length)
            setattr(sa, self.SECONDARY_LENGTH, secondary_length)
            setattr(sa, self.PRIMARY_COORD, primary_coord)
            setattr(sa, self.SECONDARY_COORD, secondary_coord)
            cell.allocateSize(sa)
            primary_coord += primary_length + self.spacing


    def _allocateSize(self):
        """Allocate the size of the box.
        
        Child widgets inflate or shrink by a factor proportional to their
        requested size.

        There is a difference between inflating and shrinking: not all widgets
        can inflate (expand=False) but all can shrink.

        The ideal case, where all widgets get what they want, is no different
        from shrinking or inflating by a factor 1.

        Note first that if no cell widget was added with expand=True, then
        trying to allocate more size than what the Box requests is forbidden.
        Doing so raises a size.SizeAllocationError.
        
        """
        allocated_size = self.allocated_size
        requested_size = self.requested_size
        allocated_primary = getattr(allocated_size, self.PRIMARY_LENGTH)
        allocated_secondary = getattr(allocated_size, self.SECONDARY_LENGTH)
        requested_primary = getattr(requested_size, self.PRIMARY_LENGTH)
        requested_secondary = getattr(requested_size, self.SECONDARY_LENGTH)
        #
        # Not allowed to inflate if no widget can expand.
        #

        if allocated_primary > requested_primary:
            can_expand_primary = False
            for cell in self.cells:
                if cell.isExpandable(self.PRIMARY_LENGTH):
                    can_expand_primary = True
                    break
            if not can_expand_primary:
                msg = "Cannot inflate a Box if no widget can expand.  " \
                      "You can avoid that by preventing your Box to expand."
                raise size.SizeAllocationError(msg)

        if allocated_secondary > requested_secondary:
            can_expand_secondary = False
            for cell in self.cells:
                if cell.isExpandable(self.SECONDARY_LENGTH):
                    can_expand_secondary = True
                    break
            if not can_expand_secondary:
                msg = "Cannot inflate a Box if no widget can expand.  " \
                      "You can avoid that by preventing your Box to expand."
                raise size.SizeAllocationError(msg)

        # Managing the short side is easy, there is nothing special to do at
        # all.  Just order the widget to take it.

        # The long side is where the fun begins. First we need to know whether
        # we have to inflate or shrink.  It's not the same because some widgets
        # are not allowed to inflate, but all widgets are allowed to shrink.

        if allocated_primary > requested_primary:
            self._inflate()
        elif allocated_primary < requested_primary:
            self._shrink()
        else:
            self._ideal()


class HBox(Box):
    """HBox is the horizontal version of Box."""
    PRIMARY_LENGTH = 'width'
    SECONDARY_LENGTH = 'height'
    PRIMARY_COORD = 'left'
    SECONDARY_COORD = 'top'

    def addChild(self, child, expand_width, expand_height, *padding):
        expandable_width = expand_width != Cell.EXPAND_NOT
        expandable_height = expand_height != Cell.EXPAND_NOT 
        if self.homogeneous and not expandable_width:
            msg = "Homogeneous HBox objects do not accept children with " \
                  "expand_width=Cell.EXPAND_NOT."
            raise container.ContainerError(msg)
        if not expandable_height:
            msg = "HBox objects do not accept children with " \
                  "expand_height=Cell.EXPAND_NOT."
            raise container.ContainerError(msg)
        Box.addChild(self, child, expand_width, expand_height, *padding)


class VBox(Box):
    """VBox is the vertical version of Box."""
    PRIMARY_LENGTH = 'height'
    SECONDARY_LENGTH = 'width'
    PRIMARY_COORD = 'top'
    SECONDARY_COORD = 'left'
    def addChild(self, child, expand_width, expand_height, *padding):
        expandable_width = expand_width != Cell.EXPAND_NOT
        expandable_height = expand_height != Cell.EXPAND_NOT 
        if self.homogeneous and not expandable_height:
            msg = "Homogeneous VBox objects do not accept children with " \
                  "expand_height=Cell.EXPAND_NOT."
            raise container.ContainerError(msg)
        if not expandable_width:
            msg = "VBox objects do not accept children with " \
                  "expand_width=Cell.EXPAND_NOT."
            raise container.ContainerError(msg)
        Box.addChild(self, child, expand_width, expand_height, *padding)
