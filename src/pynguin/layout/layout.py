#! /usr/bin/python
"""
Created on Dec 12, 2010

@author: delforge
"""

__all__ = ['Layout']

class Layout(object):
    """Base class for layouts.

    A layout organizes the position and size of several cells belonging to a
    container.

    This class is abstract.

    """
    def requestSize(self, cells):
        """Does the actual computation of the requested size.

        Parameters.
        ===========

        * `cells`: list of Cell objects.  Their size must have already been
          requested.

        """
        raise NotImplementedError("Class is abstract.")

    def allocateSize(self, allocated_size, requested_size, cells):
        """Allocate the cells size to match allocated_size.

        Parameters.
        ===========

        * `allocated_size`: SizeAllocation object, defines the size and
          position that the widget will have.
        * `requested_size`: Size object, defines the size that the widget
          requested.
        * `cells`: list of Cell objects.

        The requested size is important for the size allocation because it is
        used for computing proportionality coefficients.

        """
        raise NotImplementedError("Class is abstract.")
