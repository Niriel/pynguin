'''
Created on Nov 17, 2010

@author: delforge
'''

import unittest
from gui.layout import container
from gui.layout.cell import Cell
from gui.layout.parentable import Parentable
from gui.layout.padding import Padding

class TestContainer(unittest.TestCase):
    def testInit(self):
        """Container.__init__ does its job."""
        c = container.Container()
        self.assertEquals(c.cells, [])

    def testAddChild(self):
        """Container.addChild does its job."""
        child = Parentable()
        c = container.Container()
        c.addChild(child, Cell.EXPAND_PADDED, Cell.EXPAND_PADDING, 1, 2, 4, 8)
        cell = c.cells[0]
        self.assertTrue(cell.padded is child)
        self.assertTrue(child.parent is c)
        self.assertEquals(cell.expand_width, Cell.EXPAND_PADDED)
        self.assertEquals(cell.expand_height, Cell.EXPAND_PADDING)
        self.assertEquals(cell.padding, Padding(1, 2, 4, 8))

if __name__ == "__main__":
    unittest.main()
