'''
Created on Dec 2, 2010

@author: Niriel
'''

from guisprite import GuiSprite

__all__ = ['TextBox']

class TextBox(GuiSprite):
    BG_COLOR = (255, 255, 255)
    TX_COLOR = (0, 0, 0)

    def __init__(self, font):
        GuiSprite.__init__(self)
        self._font = font
        self._drawText = self._drawTextNormal

    def getTextSize(self):
        return self._font.size(self._text)

    def _drawTextNormal(self):
        """Draw the text when not in edition mode."""
        text_image = self._font.render(self._text, True, self.TX_COLOR, self.BG_COLOR)
        dest_rect = text_image.get_rect(midleft=self.drawable_image.get_rect().midleft)
        if dest_rect.left < 0:
            dest_rect.left = 0
        if dest_rect.top < 0:
            dest_rect.top = 0
        self.drawable_image.blit(text_image, dest_rect)

    def _drawTextEdit(self):
        """Draw the text when in edition mode.
        
        When editing the text we want to make sure we see its end.  That's why
        I match the right of the text on the right of the image.  But when the
        text is short there is no need for that, so in case of the resulting
        rectangle as a left>0 we bring it to 0.

        """
        text_image = self._font.render(self._text + "|", True, self.TX_COLOR, self.BG_COLOR)
        dest_rect = text_image.get_rect(midright=self.drawable_image.get_rect().midright)
        if dest_rect.left > 0:
            dest_rect.left = 0
        if dest_rect.top < 0:
            dest_rect.top = 0
        self.drawable_image.blit(text_image, dest_rect)

    def _draw(self):
        self._drawBackground()
        self._drawText()


