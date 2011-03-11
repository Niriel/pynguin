"""
Created on Feb 07, 2011.

@author: Niriel

This use case shows how I wish to have the GUI able to animate itself.

Sometimes I do not want the GUI to react instantly to a click.  For example,
when I display a deck of cards, I want that the card on which I click come to
the front with a pretty animation.  Or when the character in the game picks
up an object, I may want to see it moving from the floor to an inventory icon.
Stuff like that: widgets that move on their own in an automatic way.

The animation duration is fixed in time and must not depend on the number of
frames per second.  I could also have fixed speed animation but I can't think
of any use for it, and the difference with fixed duration is tiny.

Some animations can loop forever, or a given nb of times.  And can be stopped.

The GUI must always respond immediately to the user.  That means that any
animation can be interrupted at any time.  Example: the user selects a card.
That card 'slowly' moves to the center.  The user selects the next card (by
pushing the Right key again for example).  The user should not wait for the
first card to have finished moving before he can access the second card.

Another way of saying that is that the animation is just decorative, it must
have no effect whatsoever on the rest of the GUI.  Once an animation showing
something has started, that something has already happened.

Animations can be anything really.  A widget moving, changing size, changing
appearance.  There is no enforced limit.  An animation could also post events.
Not only at the beginning or at the end, but at any moment.  However, it is not
PYnGUIn's job to manage events.  And since animations can be interrupted, there
may be no guarantee that all the desired event are posted.

Just to be on the safe side, animations should have a 'final state'.  This
would be a method/function that is called whenever the animation is finished
for whatever reason: natural end of the animation, exception, whatever.

"""

# Thinking as I'm writing.  Maybe the animations could be generators.  Each
# frame on the animation is computed, and then a yield gives the control back
# to the application.  Coroutines is the word I'm looking for.  But that's
# an implementation detail isn't it ?  It'll be hidden to the user anyway.
# The user should just write a function that takes the progress (for example)
# as a parameter.

# How is an animation different from the update method on a sprite?  Couldn't I
# use update on a widget ?  Well, one reason is that I keep a list of
# animations, which avoids calling a ton of update for nothing all the time.
# But that's an early optimization.  The idea of having animations decoupled
# from the widget class is that it would allow an animation to be applied to
# objects of different classes.  But do I have a usecase for that ?  Maybe.
# For example, a Fade-in animation ?  Something playing sounds ?

# Do I allow several animations to play at once on a single object ?  I should.
# But not when animations conflict.  For example a widget could fade in while
# scrolling from the side of the screen.  The duration of the fade-in does not
# have to match that of the scrolling.  They're like transitions in video-
# editing software or power-point presentations.  Only one animation of a given
# type is allowed on an object at any time.  That means that the object knows
# which animations are applied to it.  They're probably in a dictionary.
# The key of the dictionary can be a class: the class of the animation.
# But that would pose problems when an animation is inherited from another.
# So the registration of animations should be explicit.

# But as I am thinking about it, I DO NOT need several animations per widget
# yet.  I really just need one: a deck of card scrolling.  Therefore I should
# not over-design and should just have one animation per widget.  A new anim
# immediately replaces a previous one.  I think.  Which could actually be a
# problem if I want to force posting an event at the end of the animation...

# So for that I must think.  What kind of animation do I have ?  I have the
# scrolling deck, where the selected card moves to the front of the deck card
# widget.  I have cards moving from a deck to another (that means they get
# out of their container !).  For that second one I'm not even sure.  Maybe
# I just need drag and drop for it.

# By the way, is drag and drop an animation ?  Sort of.  The widget follows the
# mouse instead of following an algorithm.  That makes animations sentitive
# to events.  It would not be a bad thing as it could help synchronizing them.

# So here I am.  Animations are event listeners.  But the event-listener part
# is not to be included into PYnGUIn.  I must provide the barebones.

# NO ! If animations are listeners then they actually act as some kind of
# controllers.  This is getting confusing.  A power of the animations is: keep
# it simple.  They do not listen to events.


# Still, that makes the animation a full fledged class, otherwise it's hard to
# subclass it as an event listener.

# I'm thinking about this interruptible nature of animations.  That could lead
# to some serious mess.  For example, the deck of cards.  The player presses
# the [left] key to scroll the deck.  What if he fires many animations by
# pressing super fast ?  It's kind of stupid to replace a scroll-left animation
# by another one, isn't it ?  Unless each time a key is pressed, a new card is
# selected.  Starting a new animation for this new card makes it go faster
# and faster.

# That is the thing: the animation is sugar coating.  While the widget is
# animated, the effect has ALREADY taken place.  So we have already selected
# the fifth card on the left, even if it's still moving.  It also saves us in
# case of aborted animation.

# I wonder if I should make animation have a fixed duration or a fixed speed.
# For example, the deck of card.  Whether I want to scroll 1 or 1000 cards, it
# should not matter.  I do not want to have to wait 1000 times longer.  It
# should be always done in half a second or so.  But what of other animations ?
# Could I need some that have a fixed speed, and the faster they are finished
# the better ?  Nah, I do not want to worry about that.

# So, fixed duration.  Variable FPS, so interpolation.

import pygame
import pynguin

EVENT_QUIT = pygame.QUIT
EVENT_KEYDOWN = pygame.KEYDOWN
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MAX_FPS = 100


def AnimMoveRight(widget, progress):
    "Goes from x=100 to x=400"
    pos = 100 + 300 * progress
    widget.position.x = pos
    widget.text = str(pos)

def AnimBounce(widget, progress):
    if progress < .5:
        pos = 400 + 100 * progress
    else:
        pos = 500 - 100 * (progress - .5)
    widget.position.y = pos

def AnimShowFPS(widget, progress, clock):
    # Here Progress isn't used.  I could probably have a caller that doesn't
    # give Progress.
    #
    # Also, this looks like a simple update of the sprite.  Do I need an
    # animation for that ?  Maybe.  Could I imagine periodic modifications of
    # widgets for which the animation mechanism would not be suitable ?
    fps = int(round(clock.get_fps()))
    widget.text = "%i FPS" % fps

def AnimFollowMouse(widget, progress):
    # Example. doesn't mean I want to do it like that, I'd rather use events.
    # Once again, the progress here is useless.
    widget.position = pygame.mouse.get_pos()

# Both AnimShowFPS and AnimFollowMouse don't use the `progress` parameter.
# That's because they're one-frame animations.  Does this concept of one-franme
# animation has any interest ?  Should we forbid them since they're
# degerenated?  Where would be a 'good' place to implement the FPS widget?
# Perhaps a OnNewFrame event to which the widget would react.


def CreateGui():
    font = pygame.font.Font(None, 30)

    display = pynguin.DisplayWidget()
    board = pynguin.BoardWidget()
    label_move = pynguin.LabelWidget(font, "move on command")
    label_fps = pynguin.LabelWidget(font, "fps")
    label_follow = pynguin.LabelWidget(font, "follow")
    label_bounce = pynguin.LabelWidget(font, "bounce")

    label_move.position = (200, 100)
    label_fps.position = (8, 8)
    label_follow.position = (320, 240)
    label_bounce.position = (500, 400)
    
    display.addChild(board, 'widget', 'widget')
    board.addChild(label_move)
    board.addChild(label_fps)
    return label_move, label_fps, label_follow, label_bounce


def main():
    print "[SPACE]: show animation object."
    print "[RETURN]: start animation."

    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    label_move, label_fps, label_follow, label_bounce = CreateGui()

    running = True
    clock = pygame.time.Clock()

    label_follow.startAnimation(AnimFollowMouse, -1) # Negative duration: loop.
    label_fps.startAnimation(AnimShowFPS, -1, clock) # Can pass extra params.
    label_bounce.startAnimation(AnimBounce, -500) # 500 ms, loop.

    while running:
        clock.tick(MAX_FPS)
        gui_time = pygame.time.get_ticks() # I can use any time I want.-
        #
        # NOTE:
        #
        # In this usecase I provide a time to the update function.  I didn't
        # do it before.  Looks like the time is necessary.  Question is: should
        # I allow the user to call update without parameter, and if yes what
        # should be the default value, and what should it mean ?  Since without
        # time it is impossible to use animations, it would be natural to just
        # don't animate anything if the time is not provided.
        pynguin.update(gui_time)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == EVENT_QUIT:
                running = False
            elif event.type == EVENT_KEYDOWN:
                if event.key == ' ':
                    print label_move.animation
                elif event.key == pygame.K_RETURN:
                    if label_move.animation is None:
                        label_move.startAnimation(AnimMoveRight, 2000) # In ms.
                    else:
                        print "Animation already running."
    print "Quitting..."
    pygame.quit()

if __name__ == '__main__':
    main()
