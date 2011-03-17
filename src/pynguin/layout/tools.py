#! /usr/bin/python
"""
Created on Mar 17, 2011

@author: delforge
"""

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