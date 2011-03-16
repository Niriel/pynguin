===================================
PYnGUIn branch padding_as_container
===================================

Rationale
=========

I don't like any more the way the padding is handled.

I don't like:

    * That padding have sizes but are not Sizeable objects.
    * That all containers work on cells and that we end up hiding cells from
      the user.
    * That some containers should not be using cells and therefore any padding
      because the padding doesn't make any sense for the layout. See a
      BoardLayout: padding windows on a desktop doesn't make sense since they
      can be placed wherever they want.
    * Stop instantiating tons of useless Padding objects, and therefore tons of
      useless Cell objects.
    * Programming some layouts is weird because you have to actually care about
      the padding. See HBoxLayout. Why does it have to wonder whether there is
      enough space for the padding?

Proposal
========

Make the padding a real container. A Bin actually, since a padding will only
contain one child.

The Cell should totally disappear. The API of containers will be clearer
because there won't be any subtleties about cells vs children.

Side-effects
------------

Padding a widget was done by passing a Padding object or some parameters to the
addChild method of a container.  We don't want to do that anymore.

We will end-up with a more verbose GUI creation. Is is desirable ? It's more
text to type, which is a pity. But providing a shortcut would break the "one
way only to do something" rule.

From now on, padding an object is exactly like using a Bin. The only difference
between the Bin and the Padding (for now) would be that the padding has a few
other properties, for the four directions.

I am thinking of allowing to give Widgets to a container's __init__, avoiding
repeated calls to addChild and making the code shorter. That's an idea for a
later improvement.

Another side effect: who will take care of whether or not a widget should
expand?  This was done by the cell.  Maybe it should just be stored on the
widget itself.  After all, the widget already contains its own size, I don't
see why it couldn't also contain the limitations on this size.

This gives Sizeable a couple of more properties/attributes: expand_width
and expand_height.  Yay !
