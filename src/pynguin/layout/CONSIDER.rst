========
CONSIDER
========

Why not make padding a container ?
==================================

Some containers do not need a padding.  For example a Board container.
Indeed, the padding only makes sense when the widgets have to be layed
out on a surface with some distance between them.  In a board container,
the widgets can go wherever they want (think of the board like the desktop
of your computer: windows can happily overlap each other there).

So maybe some containers should not need a padding.

Also, I do not like the fact that I am having a weird inheritance diagram for
Bin and Container.

In the layout package::

    class Container(sizeable.Sizeable, parentable.Parentable)
    class Bin(Container)

But in the widget package, the Bin widget does not inherit from the Container
widget.  It's weirdish.

Also, why would Bin inherit from Container in the first place ?  Is containing
only one child a particular case of containing many ?

I think I should make Padding a Bin.  Or inherit padding from it.  I can't see
any reason for introducing this cell thing anymore.  In the end, I get rid of
all the Cells, and I even stop creating Padding objects when no padding is
needed.
