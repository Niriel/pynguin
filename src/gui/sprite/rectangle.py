'''
Created on Nov 27, 2010

@author: Niriel
'''

import pygame

def Rectangle(surface, bg_color, bd_color, bd_thickness):
    surface.fill(bg_color)
    if not bd_thickness:
        return
    width = bd_thickness * 2 - 1
    pygame.draw.rect(surface, bd_color, surface.get_rect(), width)
