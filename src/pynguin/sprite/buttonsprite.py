#! /usr/bin/python
"""
Created on Dec 2, 2010

@author: Niriel
"""

from guisprite import GuiSprite
import rectangle

__all__ = ['ButtonSprite']

class ButtonSprite(GuiSprite):
    """A ButtonSprite is a rectangular sprite that looks like it can be pressed.

    Its appearance is set by the setMode method.

    """
    BG_COLOR_NORMAL_TOP = (240, 240, 240)
    BG_COLOR_NORMAL_BOTTOM = (230, 230, 230)
    BG_COLOR_HIGHLIGHT_TOP = (250, 250, 250)
    BG_COLOR_HIGHLIGHT_BOTTOM = (240, 240, 240)
    BG_COLOR_PRESSED = (220, 220, 220)
    BG_COLOR_INACTIVE = (200, 200, 200)
    BD_COLOR = (100, 100, 100)

    def __init__(self):
        """Initialize a new button.
        
        The mode is set to 'normal'.
        
        """
        GuiSprite.__init__(self)
        self._draw_function = None
        self.setMode('normal')

    def _drawNormal(self):
        """Draw a normal button."""
        rectangle.RectangleVGrad(self.drawable_image,
                                 self.BG_COLOR_NORMAL_TOP,
                                 self.BG_COLOR_NORMAL_BOTTOM)
        rectangle.Border(self.drawable_image, self.BD_COLOR, 2)

    def _drawHighlighted(self):
        """Draw a highlighted button."""
        rectangle.RectangleVGrad(self.drawable_image,
                                 self.BG_COLOR_HIGHLIGHT_TOP,
                                 self.BG_COLOR_HIGHLIGHT_BOTTOM)
        rectangle.Border(self.drawable_image, self.BD_COLOR, 2)

    def _drawPressed(self):
        """Draw a pressed button."""
        self.drawable_image.fill(self.BG_COLOR_PRESSED)
        rectangle.Border(self.drawable_image, self.BD_COLOR, 2)

    def _drawInactive(self):
        """Draw an inactive button."""
        self.drawable_image.fill(self.BG_COLOR_INACTIVE)
        rectangle.Border(self.drawable_image, self.BD_COLOR, 2)

    def _draw(self):
        """Draw the button."""
        # There is no need to call GuiSprite._draw.
        self._draw_function()

    def setMode(self, mode):
        """Set a mode: 'normal', 'highlighted', 'pressed', 'inactive'."""
        self._draw_function = getattr('_draw%s' % mode.title())
