'''
Created on Nov 27, 2010

@author: Niriel
'''

import pygame

def Border(surface, bd_color, bd_thickness):
    if not bd_thickness:
        return
    width = bd_thickness * 2 - 1
    pygame.draw.rect(surface, bd_color, surface.get_rect(), width)

def Rectangle(surface, bg_color):
    surface.fill(bg_color)

def InterpoloateComponent(comp_from, comp_to, progress, progress_max):
    return int(round((comp_to - comp_from) * float(progress) / progress_max + comp_from))

def InterpolateColor(color_from, color_to, progress, progress_max):
    return (InterpoloateComponent(color_from[0], color_to[0], progress, progress_max),
            InterpoloateComponent(color_from[1], color_to[1], progress, progress_max),
            InterpoloateComponent(color_from[2], color_to[2], progress, progress_max))

def RectangleVGrad(surface, bg_color_top, bg_color_bottom):
    x_max, y_max = surface.get_size()
    for y in range(y_max):
        color = InterpolateColor(bg_color_top, bg_color_bottom, y, y_max)
        pygame.draw.line(surface, color, (0, y), (x_max, y))
