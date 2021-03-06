=======
PYnGUIn
=======

`PYnGUIn` is a package used to create Graphical User Interfaces containing
windows, buttons, etc.

This package is itself divided into several packages:

* layout: manages the sizes and positions of the GUI elements.
* sprite: renders the GUI elements on screen using `PyGame`_.
* widget: binds layouts and sprites together in high-level objects.

Users of 'PYnGUIn' should only need to use the 'widget' package and let the
packages 'layout' and 'sprite' take care of the low-level functionalities.

Although `PYnGUIn` was designed with PyGame in mind, `layout` does not use
PyGame at all and can be re-used in other projects.  Likewise, `widget` never
directly uses PyGame and instead uses `sprite`.  `sprite` is the only package
that imports PyGame.  That should increase the portability of the
code.

.. _`PyGame`:
    http://www.pygame.org
