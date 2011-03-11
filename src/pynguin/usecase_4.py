"""
Created on Feb 07, 2011.

@author: Niriel

This use case shows how I wish to manipulate the GUI with the mouse and the
keyboard.  Joypad ?

Joypad could be a possibility but since the game is also online and therefore
requires typing, we should stick to the combo keyboard+mouse. However I intend
my game to also run on Pandora which has a pad...  Not everyone wants to play
online, in which case the keyboard becomes kinda distracting and cumbersome.
It's always going to be faster to click with a mouse than with a pad.  Just try
to help both.  See it like in Animal crossings.

In animal crossing, it's better than tab and shift/tab to navigate between
widgets.  It is possible in that game to click left/up/right/down to the
closest widgets that's in that direction.  The GUI should provide something
to easily do that: .moveFocusLeft().

We must use the same keys to navigate between widgets and to move your
character. It means we need a button to toggle between the two modes ?

Following the principle of least surprise, all the usual keyboard shortcuts
should apply.  Including copy-paste !  This is of importance when you start
entering IP addresses or things like that.

However, reacting to keys is not the role of this GUI since it would make it
process events.  What the GUI should provide is not a reaction to the fact that
the TAB key was pressed.  It should provide a .focusNextWidget method.  What
about a text area?  Well, it should have methods like .moveCursorLeft (notice
how I totally ignore right-to-left writing languages ? :D), .cancelLastInput
(ctrl-Z), .insertTextAtCursor, .selectOneMoreCharacterOnTheLeft, etc..  And
somewhere, something converts the pygame key events and calls these functions.
I do not care for now if each widget is gonna be a view, or if the whole screen
will react to events.

So this is going to end up in many requirements for many widgets.  Each widget
will come with its list of methods.  It is therefore a bit tough to implement
it here right now.  Usecase for each widget !
 
"""
