"""Widgets bind a layout and a sprite together.

"""
import layout
import sprite
import widget

__all__ = ['layout', 'sprite', 'widget']

_to_resize = {}
_to_redraw = {}

def _AddToAltitude(dico, wid):
    altitude = wid.altitude
    if altitude not in dico:
        dico[altitude] = set()
    dico[altitude].add(wid)

def AskForSizeNegotiation(wid):
    _AddToAltitude(_to_resize, wid)

def AskForRedrawing(wid):
    _AddToAltitude(_to_redraw, wid)

def ProceedToSizeNegotiation():
    altitudes = _to_resize.keys()
    altitudes.sort(reverse=True)

    # Add all the parents of all the widgets.
    # We need to only add the first parent of each widget.  At the next
    # iteration of altitude, these parents will be dealt with and their own
    # parents will be added.
    for altitude in altitudes:
        for wid in _to_resize[altitude]:
            parent = wid.parent
            if parent:
                AskForSizeNegotiation(parent)
                # TODO: Additional check here ?  Only Display objects should
                # not have parents.

    # Negotiate the sizes.
    for altitude in altitudes:
        widgets = _to_resize[altitude]
        while widgets:
            wid = widgets.pop()
            wid.requestSize(False) # False means no recursion.
    # Following line works because the loop ends with widget being the root.
    # We assume here that there is only one root: the Display.
    allocated_size = layout.SizeAllocation((0, 0), wid.requested_size)
    wid.allocateSize(allocated_size)
    _to_resize.clear()

def ProceedToRedrawing():
    altitudes = _to_redraw.keys()
    altitudes.sort(reverse=True)

    # Add all the parents of all the widgets.
    # Redrawing is a bit different from resizing: only the widgets that
    # have a sprite can be redrawn.  So only widgets with sprites are added
    # to the list.  BUT we do not want to break the chain: in the case
    # of a window-hbox-button, window and button have sprites and hbox
    # doesn't.  Even though hbox should not appear in to_redraw, window
    # should.  So we go up until we find a parent with a sprite.
    # We don't go up more than that because we don't want to process the same
    # widget twice.
    for altitude in altitudes:
        for wid in _to_redraw[altitude]:
            parent = wid.parent
            while parent:
                if parent.sprite:
                    AskForRedrawing(parent)
                    break
                parent = parent.parent

    # Redraws.
    for altitude in altitudes:
        widgets = _to_resize[altitude]
        while widgets:
            wid = widgets.pop()
            wid.draw()
    _to_redraw.clear()
