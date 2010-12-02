'''
Created on Dec 2, 2010

@author: Niriel
'''

from guisprite import GuiSprite
import rectangle

__all__ = ['Button']

class Button(GuiSprite):
    BG_COLOR_NORMAL_TOP = (240, 240, 240)
    BG_COLOR_NORMAL_BOTTOM = (230, 230, 230)
    BG_COLOR_HIGHLIGHT_TOP = (250, 250, 250)
    BG_COLOR_HIGHLIGHT_BOTTOM = (240, 240, 240)
    BG_COLOR_PRESSED = (220, 220, 220)
    BG_COLOR_INACTIVE = (200, 200, 200)
    BD_COLOR = (100, 100, 100)
    def __init__(self):
        GuiSprite.__init__(self)
        self._draw = self._drawNormal

    def update(self):
        GuiSprite.update(self)
        self._draw()
        rectangle.Border(self.drawable_image, self.BD_COLOR, 1)

    def _drawNormal(self):
        rectangle.RectangleVGrad(self.drawable_image,
                                 self.BG_COLOR_NORMAL_TOP,
                                 self.BG_COLOR_NORMAL_BOTTOM)

    def _drawHighlight(self):
        rectangle.RectangleVGrad(self.drawable_image,
                                 self.BG_COLOR_HIGHLIGHT_TOP,
                                 self.BG_COLOR_HIGHLIGHT_BOTTOM)

    def _drawPressed(self):
        self.drawable_image.fill(self.BG_COLOR_PRESSED)
 
    def _drawInactive(self):
        self.drawable_image.fill(self.BG_COLOR_INACTIVE)
