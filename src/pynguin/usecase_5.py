#! /usr/bin/python
"""
Created on Mar 9, 2011

@author: delforge

This usecase is about drag and drop.

Drag and drop is an obvious way of putting cards in decks, slots and all.

The problem with it is that it is very mouse-centric.  Something similar should
be achievable with the joypad.  Maybe even the keyboard.

When starting dragging something, the places where the dragged object can go
should become obviously visible.  Brighter and glowing for example.

Drag and drop should be cancelable.  Dropping in an illegal place cancels the
drag and drop.

When approaching a valid place for the object, the object should snap
immediately.

When canceling, the object should go back to its original place.  Probably
with an animation to show what's going on.

When using drag and drop with the keyboard or the joypad, one should be able
to quickly select the dock we're going to drop the object to.

I have no need of complex things.  I do not wish to dock parts of windows
together in the way Eclipse does.  All I want is to be able to build a deck
out of cards.  That's my only usecase so far.  Moving cards around.

"""
