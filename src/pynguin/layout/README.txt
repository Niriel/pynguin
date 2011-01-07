======
layout
======

`layout` is a package used to negotiate the sizes and positions of the elements
of a Graphical User Interface (GUI).

Notable modules.
================

Defining sizes and sizeable objects.
------------------------------------

All the elements of a GUI are sizeable objects.

* size: defines the notions of `size` and `position`.
* sizeable: base class for elements that have a size and a position.
  Implements the bases of `size negotiation` and `size requisition`.

Providing a mechanism to put elements into other elements.
----------------------------------------------------------

Containers are elements that can contain other elements.  An element in a
container is called `child` of that container, and the container is its
`parent`.

* parentable: base class for elements that can be placed in a container.
* container: base class for elements that can contain other elements.
* bin: a container that can contain only one element.
* padding: define the empty space around a child.
* cell: binds a child and its padding together.

Placing children inside containers.
-----------------------------------

Layouts are algorithms managing the size and position of children in a
container.

* boardlayout: the elements can go wherever they like.
* boxlayout: the elements are placed in a row or column.
* binlayout: only one element.
* windowlayout: the position of the element is relative to the window itself.
* scrolllayout: window that allows its content to take more space than itself.

Further readings.
=================

* doc/tutorial.txt : general principles of elements tree and size negotiation.
* Docstring of __init__.py : more technical approach on the layouts and
  the size negotiation mechanism.
