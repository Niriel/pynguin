'''
Created on Nov 27, 2010

@author: delforge
'''

import pygame
from guisprite import GuiSprite

class Label(GuiSprite):
    SURFACE_FLAGS = pygame.SRCALPHA
    BG_COLOR = (0, 0, 0, 0) # Fully transparent.
    TX_COLOR = (0, 0, 0, 255) # Pure black.

    def __init__(self, font, text):
        GuiSprite.__init__(self)
        self._font = font
        self._text = text

    def update(self):
        GuiSprite.update(self)
        self.drawText()
    
    def getTextSize(self):
        return self._font.size(self._text)
    
    def drawText(self):
        """Centers the text on the sprite image.

        If the text is too big to be centered, then you will only see the top-
        left.

        Be careful, this method uses pygame.Font.render with anti-aliasing and
        alpha layers, which is time consuming.  You don't want to call that too
        often.

        """
        text_image = self._font.render(self._text, True, self.TX_COLOR)
        dest_rect = text_image.get_rect(center = self.image.get_rect().center)
        if dest_rect.left < 0:
            dest_rect.left = 0
        if dest_rect.top < 0:
            dest_rect.top = 0
        self.drawable_image.blit(text_image, dest_rect)

    def setText(self, text):
        if text == self._text:
            return
        self.text = text
        self.callForSizeNegotiation()
