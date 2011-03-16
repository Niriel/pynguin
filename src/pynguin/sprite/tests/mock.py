#! /usr/bin/python
"""
Created on Jan 9, 2011

@author: Niriel
"""

class MockDisplayer(object):
    def __init__(self):
        object.__init__(self)
        self.sprites = []

    def addSprite(self, sprite, layer):
        self.sprites.append(sprite)

    def removeSprite(self, sprite):
        self.sprites.remove(sprite)

class MockSprite(object):
    pass

class MockTextSprite(object):
    def __init__(self):
        object.__init__(self)
        self.font = 0
        self.text = ''
    def getTextSize(self):
        return self.font.size(self.text)

class MockFont(object):
    def __init__(self, char_size):
        self.char_size = char_size
    def size(self, text):
        return self.char_size * len(text), self.char_size
