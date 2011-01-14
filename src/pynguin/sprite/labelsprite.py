"""
Created on Nov 27, 2010

@author: Niriel
"""

import pygame
from textsprite import TextSprite

class LabelSprite(TextSprite):
    """LabelSprite is a sprite that displays one line of text."""
    SURFACE_FLAGS = pygame.SRCALPHA
    BG_COLOR = (255, 0, 0, 255) # Fully transparent.
    TX_COLOR = (0, 0, 0, 255) # Pure black.

    def _drawText(self):
        """Centers the text on the sprite image.

        If the text is too big to be centered, then you will only see the top-
        left.

        Be careful, this method uses pygame.Font.render with anti-aliasing and
        alpha layers, which is time consuming.  You don't want to call that too
        often.

        """
        text_image = self.font.render(self.text, True, self.TX_COLOR)
        self_center = self.drawable_image.get_rect().center
        dest_rect = text_image.get_rect(center = self_center)
        if dest_rect.left < 0:
            dest_rect.left = 0
        if dest_rect.top < 0:
            dest_rect.top = 0
        self.drawable_image.blit(text_image, dest_rect)

    def _draw(self):
        """Draw the label onto its own drawable image."""
        self._drawBackground()
        self._drawText()
