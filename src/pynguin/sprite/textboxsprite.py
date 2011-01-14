#! /usr/bin/python
"""
Created on Dec 2, 2010

@author: Niriel
"""

from textsprite import TextSprite

__all__ = ['TextBoxSprite']

class TextBoxSprite(TextSprite):
    """TextBoxSprite is a sprite used to represent a one-line text editor."""
    BG_COLOR = (255, 255, 255)
    TX_COLOR = (0, 0, 0)

    def __init__(self):
        """Initialize a new textbox with a font and a text."""
        TextSprite.__init__(self)
        self._draw_function = None
        self.setMode('normal')

    def _drawNormal(self):
        """Draw the text when not in edition mode.

        The text is left-justified.  If too long to fit, the end is cropped

        """
        self._drawBackground()
        text_image = self.font.render(self.text, True,
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

        Note that for simplicity, the cursor is ALWAYS at the end of the text.
        There is no way yet to edit the middle of the text.

        When editing the text we want to make sure we see its end.  That's why
        I match the right of the text on the right of the image.  But when the
        text is short there is no need for that, so in case of the resulting
        rectangle as a left>0 we bring it to 0.

        """
        self._drawBackground()
        text_image = self.font.render(self.text + self.CURSOR, True,
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
        self._draw_function = getattr(self, '_draw%s' % mode.title())
