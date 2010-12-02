'''
Created on Nov 29, 2010

@author: Niriel
'''

from gui.sprite.board import Board as BoardSprite
from gui.layout.board import Board as BoardLayout

__all__ = ['Board']

class Board(BoardLayout, BoardSprite):
    pass
