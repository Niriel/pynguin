'''
Created on Nov 9, 2010

@author: delforge
'''


import size
import container


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
        container.Container.__init__(self, spacing)
        self.homogeneous = homogeneous

    def addChild(self, child, expand_dirs, fill_dirs, *padding):
        """Adds a child to the Box.

        child: a widget.
        
        expand_dirs, fill_dirs, *padding: please refer to the documentation
        of size.Padded.

        It is mandatory to set at least one of the directions of expand_dirs
        ('h', 'v' or 'hv'). If none is set, container.ContainerError is raised.
        This is due to the fact that even if you do not want your widgets to
        expand in the main direction of your box (Horizontal or Vertical, see
        HBox and VBox classes), you still want the widgets to all have the same
        height for a horizontal Box and the same width for a vertical Box.  So
        for a Horizontal box, always set the 'v' of expand_dirs.

        If the box is homogeneous then expand_dirs is set to 'hv' whatever the
        programmer asks.  The previous check is still done though, forcing the
        programmer to write a clean code anyway.

        """
        if not expand_dirs:
            msg = "When adding a child to a Box, at least one of the " \
                  "directions of expand_dirs must be set."
            raise container.ContainerError(msg)
        container.Container.addChild(self, child,
                                     expand_dirs, fill_dirs,
                                     *padding)

    def _computeRequestedSizeHomogeneous(self):
        """Compute the size needed by a homogeneous Box.

        In a homogeneous box, the space allocated to the widgets is the same
        for all.

        The algorithm looks at all the widgets and finds the size of the
        biggest one.  This size is used for all the widgets.

        Be careful: when the Box is homogeneous, then make sure that all the
        padded widgets inside have expand=True.  It will not be a problem
        during the size requisition, but it will break during the size
        allocation, raising AllocationSizeError.

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
        max_size = size.SizeRequisition(0, 0)
        for child in self.children:
            child.computeRequestedSize()
            max_size |= child.requested_size
        children_nb = len(self.children)
        length = children_nb * getattr(max_size, PRIMARY_LENGTH)
        thickness = getattr(max_size, SECONDARY_LENGTH)
        if children_nb >= 2:
            length += (children_nb - 1) * self.spacing
        result = size.SizeRequisition(0, 0)
        setattr(result, PRIMARY_LENGTH, length)
        setattr(result, SECONDARY_LENGTH, thickness)
        return result

    def _computeRequestedSizeHeterogeneous(self):
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
        for child in self.children:
            child.computeRequestedSize()
            child_size = child.requested_size
            box_long += getattr(child_size, long_name)
            child_short = getattr(child_size, short_name)
            if child_short > box_short:
                box_short = child_short
        children_nb = len(self.children)
        # Add the spacing between the widgets.
        if children_nb >= 2:
            box_long += (children_nb - 1) * self.spacing
        result = size.SizeRequisition(0, 0)
        setattr(result, long_name, box_long)
        setattr(result, short_name, box_short)
        return result

    def _computeRequestedSize(self):
        """Compute the requested size of the Box."""
        if self.homogeneous:
            return self._computeRequestedSizeHomogeneous()
        else:
            return self._computeRequestedSizeHeterogeneous()

    def _shrink(self):
        if not self.children:
            return
        long_name = self.PRIMARY_LENGTH
        short_name = self.SECONDARY_LENGTH
        allocated_size = self.allocated_size
        requested_size = self.requested_size
        allocated_long = getattr(allocated_size, long_name)
        allocated_short = getattr(allocated_size, short_name)
        requested_long = getattr(requested_size, long_name)
        if long_name == 'width':
            long_coord_name = 'left'
            short_coord_name = 'top'
        else:
            long_coord_name = 'top'
            short_coord_name = 'left'

        # We're going to deal with floating point numbers here.  This is risky
        # because we're gonna loose precision. It means that we might be off by
        # a pixel or two at the end. It is of course unacceptable, therefore I
        # need to make sure that everything adds up. The easy way I am thinking
        # about to do that is to keep the last child out of the loop, and give
        # it the remaining space.

        # We need to think about the spacing too.  The Box tries to maintain
        # its spacing as long as it can, but if we run out, we need to start
        # shrinking it too.
        children_nb = len(self.children) # Minimum 1 at this point.
        total_spacing = (children_nb - 1) * self.spacing
        if requested_long > total_spacing:
            # We can keep the spacing intact.
            spacing = self.spacing
            # There is still room for the children. Measure it.
            children_request = 0
            for child in self.children:
                children_request += getattr(child.requested_size, long_name)
            factor = float(allocated_long - total_spacing) / children_request
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
        for child in self.children[:-1]:
            child_request = child.requested_size
            child_long = int(round(getattr(child_request, long_name) * factor))
            child_size = size.SizeAllocation(0, 0, 0, 0)
            setattr(child_size, long_name, child_long)
            setattr(child_size, short_name, allocated_short)
            setattr(child_size, long_coord_name, cumul_long)
            setattr(child_size, short_coord_name, 0)
            child.allocateSize(child_size)
            cumul_long += child_long + spacing
        child = self.children[-1]
        child_size = size.SizeAllocation(0, 0, 0, 0)
        setattr(child_size, long_name, allocated_long - cumul_long)
        setattr(child_size, short_name, allocated_short)
        setattr(child_size, long_coord_name, cumul_long)
        setattr(child_size, short_coord_name, 0)
        child.allocateSize(child_size)

    def _getExpandableIds(self, direction):
        result = []
        attribute = 'expand_%s' % direction
        children = self.children
        for child_id, child in enumerate(children):
            expandable = getattr(child, attribute)
            if expandable:
                result.append(child_id)
        return result

    def _inflate(self):
        if not self.children:
            return

        allocated_size = self.allocated_size
        children = self.children
        PRIMARY_LENGTH = self.PRIMARY_LENGTH
        SECONDARY_LENGTH = self.SECONDARY_LENGTH

        #children_allo_size = map(size.SizeAllocation, children)
        children_allo_size = []
        for child_id in range(len(children)):
            children_allo_size.append(size.SizeAllocation(0, 0, 0, 0))

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

        # What is the space we can give to the expandable children ? It's the
        # total allocated space, minus the spacing, minus the length of the
        # non-expandable children.  Meanwhile, the non-expandable children just
        # get what they ask for.        
        expandable_children_length = getattr(allocated_size, PRIMARY_LENGTH)
        expandable_children_length -= self.spacing * (len(children) - 1)
        for child_id, child in enumerate(children):
            if child_id not in expandable_ids:
                child_length = getattr(child.requested_size, PRIMARY_LENGTH)
                expandable_children_length -= child_length
                setattr(children_allo_size[child_id], PRIMARY_LENGTH, child_length)

        # Apply the homothecy on the expandable children.
        # The original lengths are the requested lengths.
        # The destination length is the length calculated above.
        ori_lengths = []
        for child_id in expandable_ids:
            child_length = getattr(self.children[child_id].requested_size, PRIMARY_LENGTH)
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
        for child, child_allo_size in zip(children, children_allo_size):
            child.allocateSize(child_allo_size)


    def allocateSize(self, allocated_size):
        """Allocate the size of the box.
        
        Child widgets inflate or shrink by a factor proportional to their
        requested size.

        There is a difference between inflating and shrinking: not all widgets
        can inflate (expand=False) but all can shrink.

        The ideal case, where all widgets get what they want, is no different
        from shrinking or inflating by a factor 1.

        Note first that if no child widget was added with expand=True, then
        trying to allocate more size than what the Box requests is forbidden.
        Doing so raises a size.SizeAllocationError.
        
        """
        self.allocated_size = allocated_size
        requested_size = self.requested_size
        allocated_long = getattr(allocated_size, self.PRIMARY_LENGTH)
        allocated_short = getattr(allocated_size, self.SECONDARY_LENGTH)
        requested_long = getattr(requested_size, self.PRIMARY_LENGTH)
        requested_short = getattr(requested_size, self.SECONDARY_LENGTH)
        #
        # Not allowed to inflate if no widget can expand.
        #
        expand_primary_name = 'expand_%s' % self.PRIMARY_LENGTH
        expand_secondary_name = 'expand_%s' % self.SECONDARY_LENGTH

        if allocated_long > requested_long:
            can_expand_primary = False
            for child in self.children:
                if getattr(child, expand_primary_name):
                    can_expand_primary = True
                    break
            if not can_expand_primary:
                msg = "Cannot inflate a Box if no widget can expand.  " \
                      "You can avoid that by preventing your Box to expand."
                raise size.SizeAllocationError(msg)

        if allocated_short > requested_short:
            can_expand_secondary = False
            for child in self.children:
                if getattr(child, expand_secondary_name):
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

        if allocated_long > requested_long:
            self._inflate()
        elif allocated_long < requested_long:
            self._shrink()
        else:
            # Ideal.
            pass


class HBox(Box):
    """HBox is the horizontal version of Box."""
    PRIMARY_LENGTH = 'width'
    SECONDARY_LENGTH = 'height'
    def addChild(self, widget, expand, fill, *padding):
        if self.homogeneous and not expand:
            msg = "Homogeneous HBox objects do not accept widgets with " \
                  "expand=False."
            raise container.ContainerError(msg)
        expand_width = expand
        expand_height = True
        Box.addWidget(self, widget, expand_width, expand_height, fill, fill,
                      *padding)

class VBox(Box):
    """HBox is the vertical version of Box."""
    PRIMARY_LENGTH = 'height'
    SECONDARY_LENGTH = 'width'
    def addChild(self, widget, expand, fill, *padding):
        if self.homogeneous and not expand:
            msg = "Homogeneous VBox objects do not accept widgets with " \
                  "expand=False."
            raise container.ContainerError(msg)
        expand_width = True
        expand_height = expand
        Box.addWidget(self, widget, expand_width, expand_height, fill, fill,
                      *padding)
