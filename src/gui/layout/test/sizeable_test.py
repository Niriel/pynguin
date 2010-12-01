'''
Created on Nov 4, 2010

@author: Niriel
'''


import unittest
from gui.layout import sizeable, size


class TestDocTest(unittest.TestCase):
    def testDocTest(self):
        """module sizeable passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=sizeable)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)


class TestSizeable(unittest.TestCase):
    class MockSizeable(sizeable.Sizeable):
        def _requestSize(self):
            return size.SizeRequisition(32, 16)
        def allocateSize(self, size):
            self.allocated_size = size

    def testInit(self):
        """Sizeable.__init__ does its job."""
        s = sizeable.Sizeable()
        self.assertTrue(s.requested_size is None)
        self.assertTrue(s.allocated_size is None)

    def testNegotiateSize(self):
        """Sizeable.negotiateSize allocates what it requests."""
        s = self.MockSizeable()
        self.assertFalse(s.requested_size)
        self.assertFalse(s.allocated_size)
        s.negotiateSize()
        self.assertTrue(s.requested_size)
        self.assertTrue(s.allocated_size)
        self.assertEquals(s.allocated_size.size, s.requested_size)
        self.assertEquals(s.allocated_size.pos, size.Pos(0, 0))
        # Check that the position is maintained.
        s.allocated_size.width = 0
        s.allocated_size.height = 0
        s.allocated_size.left = 100
        s.allocated_size.top = 200
        s.negotiateSize()
        self.assertEquals(s.allocated_size.size, s.requested_size)
        self.assertEquals(s.allocated_size.pos, size.Pos(100, 200))

#if __name__ == "__main__":
#    unittest.main()
