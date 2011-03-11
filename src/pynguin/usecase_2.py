"""
Created on Feb 07, 2011.

@author: Niriel

This use case shows how I can plug the PYnGUIn into my own event manager.

The event manager used here is extremely primitive and ad-hoc, and the event
processing is too simple to be used, but the principle holds.

"""

import pygame
import pynguin

EVENT_QUIT = pygame.QUIT

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MAX_FPS = 100

class EventManager(object):
    def __init__(self):
        object.__init__(self)
        self.listeners = []
    def register(self, listener):
        self.listeners.append(listener)
        listener.event_manager = self
    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)

class Event(object):
    def __init__(self, name, what):
        self.name = name
        self.what = what
    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.name, self.what)

class MyDisplayWidget(pynguin.DisplayWidget):
    def notify(self, event):
        if event.name == 'mouse click':
            pos = event.what
            widgets = pynguin.findWidgetsAtPosition(self, pos)
            if widgets:
                # Click the topmost widget that's under the mouse.
                new_event = Event('widget click', widgets[-1])
                self.event_manager.post(new_event)

class MyButtonWidget(pynguin.ButtonWidget):
    def __init__(self):
        pynguin.ButtonWidget.__init__(self)
        event_manager = None
        self.on_click_event = None
    def notify(self, event):
        if event.name == 'widget click':
            if event.what is self:
                self.mode = 'pressed'
                self.event_manager.post(self.on_click_event)
        elif event.name == 'mouse release':
            self.mode = 'normal'



def CreateGui(event_manager):
    font = pygame.font.Font(None, 30)
    font_big = pygame.font.Font(None, 50)

    # The order in which I declare does not matter.
    display = MyDisplayWidget()
    event_manager.register(display)
    # Note that having several displays is technichally allowed, even if I
    # don't know what to do with that.  They're all going to write stuff on the
    # same pygame display, resulting in overlapping things.  I accept that it
    # can fuck up things.
    vbox = pynguin.VBoxWidget(0, False)
    label_help = pynguin.LabelWidget(font_big, "Click on the buttons.")
    hbox = pynguin.HBoxWidget(8, True)
    button_left = MyButtonWidget()
    button_right = MyButtonWidget()
    label_left = pynguin.LabelWidget(font, "Left.")
    label_right = pynguin.LabelWidget(font, "Right.")

    button_left.on_click_event = Event('clicked', 'left')
    button_right.on_click_event = Event('clicked', 'right')


    # The order in which we add widgets to parents does not matter.
    # Except in the vbox of course since this one has an intrinsic order.
    display.addChild(vbox, 'widget', 'widget')
    vbox.addChild(label_help, 'end', 'padding', 'padding')
    vbox.addChild(hbox, 'end', 'padded', 'padded')
    hbox.addChild(button_left, 'end', 'widget', 'widget')
    hbox.addChild(button_right, 'end', 'widget', 'widget')
    button_left.addChild(label_left, 'padding', 'padding')
    button_right.addChild(label_right, 'padding', 'padding')


class ConsoleViewer(object):
    def notify(self, event):
        print event


def main():
    pygame.init()

    # Note : the DisplayWidget does NOT take care of the creation of the
    # display area.  I do not want the GUI to force me to change anything to
    # my code.

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    event_manager = EventManager()

    CreateGui(event_manager)

    console_viewer = ConsoleViewer()
    event_manager.register(console_viewer)

    running = True
    clock = pygame.time.Clock()
    while running:
        # I expect the GUI to have to update itself once per frame at max.
        # If `pynguin.update` has nothing to do then it returns immediately.
        pynguin.update()
        pygame.display.flip()
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == EVENT_QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Left button.
                    event_manager.post(Event("mouse click", event.pos))

    print "Quitting..."
    pygame.quit()

if __name__ == '__main__':
    main()
