'''
Created on Nov 17, 2010

@author: delforge
'''

import unittest
import container
import size

class TestContainer(unittest.TestCase):
    def testInit(self):
        """Container.__init__ does its job."""
        c = container.Container(42)
        self.assertEquals(c.spacing, 42)
        self.assertEquals(c.children, [])

    def testAddChild(self):
        """Container.addChild does its job."""
        child = ['whatever']
        c = container.Container(0)
        c.addChild(child, 'hv', 'h', 1, 2, 4, 8)
        padded = c.children[0]
        self.assertTrue(padded.widget is child)
        self.assertTrue(padded.expand_width)
        self.assertTrue(padded.expand_height)
        self.assertTrue(padded.fill_width)
        self.assertFalse(padded.fill_height)
        self.assertEquals(padded.padding, size.Padding(1, 2, 4, 8))

if __name__ == "__main__":
    unittest.main()
