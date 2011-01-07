======
widget
======

`widget` is a package used to create and manipulate Graphical User Interfaces
(GUI's).  It relies on PyGame_

Notable modules.
================

These modules are likely to be useful to many users of the package.

* window: a widget that can draw other widgets onto itself ; useful to force
  boundaries and ensure an easy layering.
* scroll: a widget similar to window but that can have a content bigger than
  itself, visible by means of scrolling.
* screen: a widget that covers the entire screen and serves as root to the
  widget tree.
* box: an invisible widget that can organize widgets in a row or a column.
* label: a widget representing a line of text.
* button: a widget that can be pressed to trigger an action.
* textbox: a widget that allows the user to enter a line of text.

Other modules.
==============

These modules are more useful to developers who wish to create their own
widgets. 

* widget: defines properties common to all widgets.
* container: defines properties common to all the widgets that can contain
  other widgets.
* windowmanager: highly experimental, will probably disappear soon.

Further readings.
=================

* doc/tutorial.txt : general principles widget creation and manipulation.
* Docstring of __init__.py : more technical approach on the widgets.

References and footnotes.
=========================

.. _PyGame: http://www.pygame.org/
