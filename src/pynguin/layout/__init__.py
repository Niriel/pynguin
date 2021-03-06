"""Manages the sizes and positions of elements in containers.

This package is intended for being used within a graphical user interface
(GUI).

Although designed with pygame in mind, no reference to pygame is ever made in
this package.  This is supposed to increase the re-usability of the code, as
well as the clarity of the different concepts used in a GUI.

The goal of this package is to manage the sizes and positions of elements in
containers, where the containers are also elements that can be inserted into
containers.


I] Sizeable.
============

Any element or container that needs a size should inherit from Sizeable. To put
a button in a window, you will want to create a Button and a Window class, both
inheriting from Sizeable.

A Sizeable object has three sizes:
- a requested size ;
- an allocated size ;
- a forced requested size.

1) The requested size.
----------------------

The Sizeable object is responsible for calculating its own requested size.  For
example, the button requests the size needed to display its text and some
margin around.  The window requests the size needed to display all its content.

The requested size is calculated in the method _requestSize.  Its
default behavior is to raise a NotImplementedError, since Sizeable is not
supposed to be used as is. Each class subclassing Sizeable should have its own
_requestSize.

The method _requestSize returns a size.Size object.  This
object has two properties: width and height.

The user should never call _requestSize but should call requestSize instead.
requestSize does not return anything. It calls _requestSize and stores the
result in the attribute requested_size of the Sizeable object.

2) The allocated size.
----------------------

In an ideal case, each element of your GUI would receive the size it asks for.
But the screen is not infinitely big or the user may want to change the size of
the windows.  The allocated size is the size that you force onto your element.
Any Sizeable object must be designed and implemented in order to accept any
possible size.  It does not need to be pretty or to make sense, but it needs to
not crash.  If the user reduces the window to a few pixels, or even 0, the code
should still work and do its best.

The user allocates the size of the Sizeable object by calling its allocateSize
method. This method stores the allocated size in the allocated_size property of
the Sizeable object, and then calls _allocateSize.  This second method is the
one that the developer should override to suit his need.  The default behavior
is to raise NotImplementedError.

The allocated size should be a size.SizeAllocation object. These contain not
only a size but also a position.

IMPORTANT: always remember to call requestSize before calling
allocateSize, even if you do not allocate the requested size.  This is because
requestSize will give allocateSize a first guess to start with.

3) The forced requested size.
-----------------------------

Sizeable objects have a forced_requested_size attribute.  Its value is None by
default and often remains None.

The method requestSize calls _requestSize.  Then, if forced_requested_size is
not None, then requested_size takes the value of forced_requested_size.  It is
important to call _requestSize even though we do not use requested_size
because _requestSize often calls requestSize of children (see the part on
Container objects).

This is useful in some situations.  For example, the user has placed a window
somewhere on the screen, with a specific size and position.  This window
contains a large widget for entering some text (think of a notepad
application).  A lot of text is inserted.  The window would like to grow bigger
and bigger with each letter inserted in order to display it all, to the point
of growing bigger than the screen.  Such a behavior would be strange and
annoying.  It can be overridden by setting a forced requested size.

4) Size negotiation.
--------------------

The size negotiation takes two steps:

- size requisition;
- size allocation.

Sizeable objects are provided with a method called negotiateSize.  The default
behavior is to call requestSize, and then call allocatedSize with the obtained
requested size.  That gives the Sizeable object the size it wants.  If you do
not wish to let the objects get the size they want, then you may want to call
requestSize and allocateSize yourself instead of calling negotiateSize.

You will need to override this behavior sometimes.  For example, you can see
the entire screen of your application as a Container.  Therefore it is also a
Sizeable.  But this Sizeable should always have one size: the size of the
screen (for example 800x600).  Remember to always compute the requested size
before allocating.


II] Container.
==============

The Container class inherits from Sizeable.  Container objects contain Sizeable
objects. That means that a Container object can contain another Container
object.  For example, a window contains a button, and the button contains a
label (or an image).

The objects that are added into a container are called "children".  You add an
object to a container with the method Container.addChild.

However, the container does not directly store the children in a list.  Each
child is wrapped in a Cell object.  Cell objects are Sizeable but are not
Container themselves.  Cells are used to provide some padding around a child
and define if and how the child is allowed to inflate beyond its requested
size.

Containers have a _layout attribute, set to None by default.  Subclass
Container to instantiate a real layout.  When the methods requestSize and
allocateSize are called on the container, the container defers them to its
layout which does the real computations.

The Bin is a special container that can only containe one cell.


III] Cell.
==========

Each time you add a child to a container, you create a cell for that child.

With the Cell we do the first step toward building a layout manager for our
GUI.  A Cell object binds two objects together:

- a Sizeable object called "padded";
- a Padding object called "padding".

1) A short note on padding.
---------------------------

When putting buttons next to each other in a window, you may want to insert
some space between them.  You can either to that by setting the spacing
attribute of Container objects, or by specifying a padding.

The spacing is the space BETWEEN the children, while the padding is the space
AROUND them.  You can have both.  The spacing is the same for all the children
but each child has its own padding.  Read further for more information on
padding.

2) How cells expand.
--------------------

Sizeable objects should accept any size, gigantic or microscopic.  But some
size don't really make sense. For example: a window containing an area for
entering some text and a OK button.  When making the window bigger, it makes
sense to make the text area bigger but the button doesn't need (and shouldn't)
expand beyond necessary: it would become an ugly waste of space. This is why
cells come with attributes to control their expansion.

Cells can shrink down to 0 in both directions.

The two properties used by the cells to control their expansion are similar,
but one is for the horizontal dimension and one for the vertical one.  They are
called "expand_width" and "expand_height".  Since they work in the same way,
let's group them under the name "expand" for the rest of the explanation.

expand can take three values: EXPAND_NOT, EXPAND_PADDING and EXPAND_PADDED.  In
order to make the code easier to write, these constants have string values that
you can use:
 * EXPAND_NOT: 'not'
 * EXPAND_PADDING: 'padding'
 * EXPAND_PADDED: 'padded'

EXPAND_NOT: the cell cannot expand.  Trying to allocate a size bigger than its
requested size will raise an exception.

EXPAND_PADDING: the cell can expand, and the extra space is given to the
padding.  The Child keeps its requested size.

EXPAND_PADDED: the cell can expand, and the extra space is given to the child.
The padding around the child remains intact.

When a cell is shrunk below its desired size, the padding is kept intact as
long as it can and it is the child that shrinks.  Once the child reaches a size
of 0, the padding starts to shrink too.

Note that the two directions, horizontal and vertical, are processed
separately. It is perfectly valid to double the height of a cell while halving
its width for example.  expand_width and expaned_height are totally independent
from each other.

Note also that some containers may impose some values on expand_width or
expand_height.  This is described in their documentation.


IV] Padding.
============

The space around a child is represented by a Padding object.  The four
attributes of a Padding object are left, right, top and bottom.  Their values
are positive integers representing the distance between the border of the child
and the border of the cell on each side.

The Padding object also provides three convenient read-only properties: width,
height and size ; returning left+right, top+bottom and Size(width, height).


V] Parentable.
==============

Any Sizeable object that is supposed to be added to a Container should subclass
Parentable.

We have established that Containers contain children and have pointers to all
of them.  But it is also often useful for children to have a pointer to their
container.  Parentable provides the object with a property named "parent" which
is set by Container.addChild.

Because introducing this property creates circular references which can easily
cause troubles, the "parent" property uses a weak reference to point to its
container.  Once the container disappears, all its children automatically
receive None for parent.

Since not all Sizeable Object should be Parentable (exemple: Cell objects),
the two functionalities are kept separately.

Note that Container implements Parentable.  This is because in many situations
you will add containers to other containers, so generalizing it from the
beginning helps a bit.


VI] Layouts.
============

Layout objects provide algorithms for the size negotiation.  All the containers
have a layout.  When requestSize or allocateSize are called on the container,
the container passes it to its layout which will do the computations.

Some layouts can manage several children (BoxLayout, BoardLayout), and some
can only manage one (WindowLayout, ScrollLayout).  When giving a layout to
a container, make sure they are compatible.  For example, WindowLayout and
ScrollLayout should only be given to Bin containers.

VII] For more information.
==========================

Please refer to the documentation of the individual modules for a more detailed
description of the classes.

"""
from size import Size
from size import Pos
from size import SizeAllocation
from sizeable import Sizeable
from sizeable import SizeableError
from sizeable import SizeAllocationError
from sizeable import ExpandError
from parentable import Parentable
from parentable import ParentableError
from parentable import NoParentError
from parentable import AlreadyParentError
from container import Container
from container import ContainerError
from container import NotAChildError
from container import InconsistentParenthoodError
from container import InvalidWhereConstructError

from layout import Layout
from boardlayout import BoardLayout
from borderlayout import BorderLayout
from boxlayout import HBoxLayout
from boxlayout import VBoxLayout
from windowlayout import WindowLayout
from scrolllayout import ScrollLayout
