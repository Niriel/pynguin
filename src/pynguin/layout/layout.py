#! /usr/bin/python
"""
Created on Dec 12, 2010

@author: delforge
"""

__all__ = ['Layout']

class Layout(object):
    """Base class for layouts.

    A Layout organizes the position and size of several cells belonging to a
    container.

    This class is abstract.

    """
    def _requestSize(self, cells):
        """Does the actual computation of the requested size.

        Parameters.
        -----------

        * cells: list of Cell objects.  Their size must have already been
          requested.

        The method requestSize calls this method after having requested
        the size of all the cells.
        
        """
        raise NotImplementedError("Class is abstract")

    def requestSize(self, cells):
        """Compute and request the size necessary for displaying all the cells.

        Parameters.
        -----------

        * cells: list of Cell objects.  Their size do not need to have been
          requested, this method will do the request on them first.

        Return.
        -------
        
        A Size object: the size needed by the layout to display its content.
        
        Warning.
        --------
        
        Note that requestSize on a layout returns a value, unlike requestSize
        on a Sizeable.  A layout is not a Sizeable object.
        
        """
        for cell in cells:
            cell.requestSize()
        return self._requestSize(cells)

    def allocateSize(self, allocated_size, requested_size, cells):
        """Allocate the cells size to match allocated_size.

        Parameters.
        -----------

        * allocated_size: SizeAllocation object, defines the size and position
          that the widget will have.
        * requested_size: Size object, defines the size that the widget
          requested.
        * cells: list of Cell objects.

        The requested size is important for the size allocation because it is
        used for computing proportionality coefficients.

        """
        raise NotImplementedError("Class is abstract.")
