'''
Created on Nov 29, 2010

@author: Niriel
'''

from gui.sprite.board import Board as BoardSprite
from gui.layout.board import Board as BoardLayout
from container import Container

__all__ = ['Board']

class Board(Container, BoardLayout, BoardSprite):
    def __init__(self):
        raise NotImplementedError()
