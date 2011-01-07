#! /usr/bin/python
"""
Created on Dec 2, 2010

@author: Niriel
"""

from guisprite import GuiSprite

__all__ = ['TextBox']

class TextBox(GuiSprite):
    """TextBox is a sprite used to represent a one-line text editor."""
    BG_COLOR = (255, 255, 255)
    TX_COLOR = (0, 0, 0)

    def __init__(self, font, text):
        """Initialize a new textbox with a font and a text."""
        GuiSprite.__init__(self)
        self._font = font
        self._text = text
        self._draw_function = None
        self.setMode('normal')

    def getTextSize(self):
        """Compute the size needed for rendering the text as (width, height).

        """
        return self._font.size(self._text)

    def _drawNormal(self):
        """Draw the text when not in edition mode."""
        self._drawBackground()
        text_image = self._font.render(self._text, True,
                                       self.TX_COLOR, self.BG_COLOR)
        self_left = self.drawable_image.get_rect().midleft
        dest_rect = text_image.get_rect(midleft=self_left)
        if dest_rect.left < 0:
            dest_rect.left = 0
        if dest_rect.top < 0:
            dest_rect.top = 0
        self.drawable_image.blit(text_image, dest_rect)

    def _drawEdit(self):
        """Draw the text when in edition mode.

        When editing the text we want to make sure we see its end.  That's why
        I match the right of the text on the right of the image.  But when the
        text is short there is no need for that, so in case of the resulting
        rectangle as a left>0 we bring it to 0.

        """
        self._drawBackground()
        text_image = self._font.render(self._text + "|", True,
                                       self.TX_COLOR, self.BG_COLOR)
        self_right = self.drawable_image.get_rect().midright
        dest_rect = text_image.get_rect(midright=self_right)
        if dest_rect.left > 0:
            dest_rect.left = 0
        if dest_rect.top < 0:
            dest_rect.top = 0
        self.drawable_image.blit(text_image, dest_rect)

    def _draw(self):
        """Draw the sprite."""
        self._draw_function()

    def setMode(self, mode):
        """Set the mode: 'normal' or 'edit'."""
        self._draw_function = getattr(self, 'draw%s' % mode.title())
