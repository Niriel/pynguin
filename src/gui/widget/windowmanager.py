'''
Created on Dec 5, 2010

@author: Niriel
'''

from gui.layout.size import SizeAllocation, Size, Pos

def ObtainAllocatedSize(widget):
    allo_size = widget.allocated_size
    if allo_size:
        return allo_size
    req_size = widget.requested_size
    if not req_size:
        widget.requestSize()
        req_size = widget.requested_size
    allo_size = SizeAllocation(Pos(0, 0), req_size)
    return allo_size

def ResizeToFitInto(window, container):
    win_size = ObtainAllocatedSize(window).size
    con_size = ObtainAllocatedSize(container).size
    win_size &= con_size
    window.forced_requested_size = win_size.copy()
    window.callForSizeNegotiation()

def MoveToFitInto(window, container):
    win_size = ObtainAllocatedSize(window)
    con_size = ObtainAllocatedSize(container)
    size_diff = 0
