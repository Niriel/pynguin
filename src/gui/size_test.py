'''
Created on Nov 4, 2010

@author: Bertrand
'''


import unittest
import size


class TestDocTest(unittest.TestCase):
    def testDocTest(self):
        """module size passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=size)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)


class TestSize(unittest.TestCase):
    def testInitTwoParams(self):
        """Size.__init__(width, height) does not crash."""
        s = size.Size(0, 0)
        del s # Just to remove the eclipse warning about the unused variable.

    def testInitOneParam(self):
        """Size.__init__(size) does not crash."""
        s1 = size.Size(1, 2)
        s2 = size.Size(s1)
        self.assertEquals(s1, s2)
        self.assertFalse(s1 is s2)

    def testRepr(self):
        """Size.__repr__ returns code to create itself."""
        s = size.Size(1, 2)
        r = repr(s)
        self.assertEquals(r, 'Size(1, 2)')

    def testGetWidth(self):
        """Size._getWidth returns the width."""
        s = size.Size(1, 2)
        self.assertEquals(s._getWidth(), 1)

    def testGetHeight(self):
        """Size._getHeight returns the width."""
        s = size.Size(1, 2)
        self.assertEquals(s._getHeight(), 2)

    def testSetWidthPositive(self):
        """Size._setWidth accepts positive integers."""
        s = size.Size(0, 0)
        s._setWidth(1)
        self.assertEquals(s.width, 1)
        s._setWidth(0) # 0 is also a legal value.

    def testSetWidthNegative(self):
        """Size._setWidth raises ValueError on negative integers."""
        s = size.Size(0, 0)
        self.assertRaises(ValueError, s._setWidth, -1)

    def testSetWidthNonInteger(self):
        """Size._setWidth raises TypeError on non-integer values."""
        s = size.Size(0, 0)
        self.assertRaises(TypeError, s._setWidth, "spam")

    def testSetHeightPositive(self):
        """Size._setHeight accepts positive integers."""
        s = size.Size(0, 0)
        s._setHeight(1)
        self.assertEquals(s.height, 1)
        s._setHeight(0) # 0 is also a legal value.

    def testSetHeightNegative(self):
        """Size._setHeight raises ValueError on negative integers."""
        s = size.Size(0, 0)
        self.assertRaises(ValueError, s._setHeight, -1)

    def testSetHeightNonInteger(self):
        """Size._setHeight raises TypeError on non-integer values."""
        s = size.Size(0, 0)
        self.assertRaises(TypeError, s._setHeight, "spam")

    def testPropertyWidth(self):
        """Size.width can be read and written."""
        s = size.Size(0, 0)
        s.width = 1
        self.assertEquals(s.width, 1)

    def testPropertyHeight(self):
        """Size.height can be read and written."""
        s = size.Size(0, 0)
        s.height = 1
        self.assertEquals(s.height, 1)

    def testEquals(self):
        """Size.__eq__ returns True iif widths and heights are equal."""
        s0 = size.Size(1, 2)
        s1 = size.Size(1, 3)
        self.assertFalse(s0 == s1)
        s0 = size.Size(1, 2)
        s1 = size.Size(0, 2)
        self.assertFalse(s0 == s1)
        s0 = size.Size(1, 2)
        s1 = size.Size(0, 3)
        self.assertFalse(s0 == s1)
        s0 = size.Size(1, 2)
        s1 = size.Size(1, 2)
        self.assertTrue(s0 == s1)

    def testNotEquals(self):
        """Size.__ne__ returns True iif widths or heights are differ."""
        s0 = size.Size(1, 2)
        s1 = size.Size(1, 3)
        self.assertTrue(s0 != s1)
        s0 = size.Size(1, 2)
        s1 = size.Size(0, 2)
        self.assertTrue(s0 != s1)
        s0 = size.Size(1, 2)
        s1 = size.Size(0, 3)
        self.assertTrue(s0 != s1)
        s0 = size.Size(1, 2)
        s1 = size.Size(1, 2)
        self.assertFalse(s0 != s1)

    def testAdd(self):
        """Size.__add__ adds the coords of two sizes."""
        s1 = size.Size(1, 2)
        s2 = size.Size(3, 4)
        s3 = s1 + s2
        self.assertEquals(s1, size.Size(1, 2))
        self.assertEquals(s2, size.Size(3, 4))
        self.assertEquals(s3, size.Size(4, 6))

    def testSub(self):
        """Size.__sub__ subtracts the coords of two sizes."""
        s1 = size.Size(3, 4)
        s2 = size.Size(2, 1)
        s3 = s1 - s2
        self.assertEquals(s1, size.Size(3, 4))
        self.assertEquals(s2, size.Size(2, 1))
        self.assertEquals(s3, size.Size(1, 3))

    def testMul(self):
        """Size.__mul__ multiplies the coords by a scalar."""
        s1 = size.Size(2, 3)
        s2 = s1 * 10
        self.assertEquals(s1, size.Size(2, 3))
        self.assertEquals(s2, size.Size(20, 30))

    def testRmul(self):
        """Size.__rmul__ multiplies the coords by a scalar."""
        s1 = size.Size(2, 3)
        s2 = 10 * s1
        self.assertEquals(s1, size.Size(2, 3))
        self.assertEquals(s2, size.Size(20, 30))

    def testDiv(self):
        """Size.__div__ divides the coords by a scalar."""
        s1 = size.Size(20, 30)
        s2 = s1 / 10
        self.assertEquals(s1, size.Size(20, 30))
        self.assertEquals(s2, size.Size(2, 3))

    def testAnd(self):
        """Size.__and__ returns the mins of each coords of two sizes."""
        s1 = size.Size(1, 2)
        s2 = size.Size(4, 5)
        s3 = s1 & s2
        self.assertEquals(s1, size.Size(1, 2))
        self.assertEquals(s2, size.Size(4, 5))
        self.assertEquals(s3, size.Size(1, 2))
        #
        s1 = size.Size(4, 2)
        s2 = size.Size(1, 5)
        s3 = s1 & s2
        self.assertEquals(s1, size.Size(4, 2))
        self.assertEquals(s2, size.Size(1, 5))
        self.assertEquals(s3, size.Size(1, 2))
        #
        s1 = size.Size(1, 5)
        s2 = size.Size(4, 2)
        s3 = s1 & s2
        self.assertEquals(s1, size.Size(1, 5))
        self.assertEquals(s2, size.Size(4, 2))
        self.assertEquals(s3, size.Size(1, 2))
        #
        s1 = size.Size(4, 5)
        s2 = size.Size(1, 2)
        s3 = s1 & s2
        self.assertEquals(s1, size.Size(4, 5))
        self.assertEquals(s2, size.Size(1, 2))
        self.assertEquals(s3, size.Size(1, 2))

    def testOr(self):
        """Size.__or__ returns the max of each coords of two sizes."""
        s1 = size.Size(1, 2)
        s2 = size.Size(4, 5)
        s3 = s1 | s2
        self.assertEquals(s1, size.Size(1, 2))
        self.assertEquals(s2, size.Size(4, 5))
        self.assertEquals(s3, size.Size(4, 5))
        #
        s1 = size.Size(4, 2)
        s2 = size.Size(1, 5)
        s3 = s1 | s2
        self.assertEquals(s1, size.Size(4, 2))
        self.assertEquals(s2, size.Size(1, 5))
        self.assertEquals(s3, size.Size(4, 5))
        #
        s1 = size.Size(1, 5)
        s2 = size.Size(4, 2)
        s3 = s1 | s2
        self.assertEquals(s1, size.Size(1, 5))
        self.assertEquals(s2, size.Size(4, 2))
        self.assertEquals(s3, size.Size(4, 5))
        #
        s1 = size.Size(4, 5)
        s2 = size.Size(1, 2)
        s3 = s1 | s2
        self.assertEquals(s1, size.Size(4, 5))
        self.assertEquals(s2, size.Size(1, 2))
        self.assertEquals(s3, size.Size(4, 5))

    def testAddClass(self):
        """Size.__add__ returns an object of the same class."""
        class MySize(size.Size):
            pass
        s1 = MySize(1, 2)
        s2 = size.Size(3, 4)
        s3 = s1 + s2
        self.assertTrue(type(s3) is MySize)

    def testSubClass(self):
        """Size.__sub__ returns an object of the same class."""
        class MySize(size.Size):
            pass
        s1 = MySize(3, 4)
        s2 = size.Size(1, 2)
        s3 = s1 - s2
        self.assertTrue(type(s3) is MySize)

    def testMulClass(self):
        """Size.__mul__ returns an object of the same class."""
        class MySize(size.Size):
            pass
        s1 = MySize(1, 2)
        s2 = s1 * 10
        self.assertTrue(type(s2) is MySize)

    def testDivClass(self):
        """Size.__div__ returns an object of the same class."""
        class MySize(size.Size):
            pass
        s1 = MySize(1, 2)
        s2 = s1 / 10
        self.assertTrue(type(s2) is MySize)

    def testAndClass(self):
        """Size.__and__ returns an object of the same class."""
        class MySize(size.Size):
            pass
        s1 = MySize(1, 2)
        s2 = size.Size(1, 2)
        s3 = s1 & s2
        self.assertTrue(type(s3) is MySize)

    def testOrClass(self):
        """Size.__or__ returns an object of the same class."""
        class MySize(size.Size):
            pass
        s1 = MySize(1, 2)
        s2 = size.Size(1, 2)
        s3 = s1 | s2
        self.assertTrue(type(s3) is MySize)

    def testIadd(self):
        """Size.__iadd__ adds coords in place."""
        s1 = size.Size(3, 4)
        s2 = size.Size(1, 2)
        s1 += s2
        self.assertEquals(s1, size.Size(4, 6))

    def testIsub(self):
        """Size.__isub__ subtracts coords in place."""
        s1 = size.Size(3, 4)
        s2 = size.Size(1, 2)
        s1 -= s2
        self.assertEquals(s1, size.Size(2, 2))

    def testImul(self):
        """Size.__imul__ multiplies coords in place."""
        s1 = size.Size(3, 4)
        s1 *= 2
        self.assertEquals(s1, size.Size(6, 8))

    def testIdiv(self):
        """Size.__idiv__ divides coords in place."""
        s1 = size.Size(20, 30)
        s1 /= 10
        self.assertEquals(s1, size.Size(2, 3))

    def testIand(self):
        """Size.__iand__ applies and on coords in place."""
        s1 = size.Size(3, 4)
        s2 = size.Size(1, 2)
        s1 &= s2
        self.assertEquals(s1, size.Size(1, 2))

    def testIor(self):
        """Size.__ior__ applies or on coords in place."""
        s1 = size.Size(3, 4)
        s2 = size.Size(1, 5)
        s1 |= s2
        self.assertEquals(s1, size.Size(3, 5))


class TestSizeRequisition(unittest.TestCase):
    def testRepr(self):
        """SizeRequisition.__repr__ returns code to create itself."""
        s = size.SizeRequisition(1, 2)
        r = repr(s)
        self.assertEquals(r, 'SizeRequisition(1, 2)')


class TestPadded(unittest.TestCase):
    class MockWidget(object):
        """A pseudo widget implementing only what I need for this test."""
        def computeRequestedSize(self):
            self.requested_size = size.SizeRequisition(10, 20)
        def allocateSize(self, allocated_size):
            self.allocated_size = allocated_size

    def testInitWidget(self):
        """Padded.__init__ properly assigns the widget."""
        widget = TestPadded.MockWidget()
        p = size.Padded(widget, '', '')
        self.assertTrue(p.widget is widget)

    def testInitExpandFill(self):
        """Padded.__init__ raises ValueError iif expand=False and fill=True."""
        size.Padded(None, '', '')
        size.Padded(None, 'hv', '')
        size.Padded(None, 'hv', 'hv')
        self.assertRaises(ValueError, size.Padded, None, '', 'hv')

    def testInitPadding(self):
        """Padded.__init__ assigns the proper padding values."""
        #
        p = size.Padded(None, '', '')
        self.assertEquals(p.padding, size.Padding())
        #
        p = size.Padded(None, '', '', 42)
        self.assertEquals(p.padding, size.Padding(42))
        #
        p = size.Padded(None, '', '', 42, 666)
        self.assertEquals(p.padding, size.Padding(42, 666))
        #
        p = size.Padded(None, '', '', 1, 2, 3, 4)
        self.assertEquals(p.padding, size.Padding(1, 2, 3, 4))
        # When a Padding object is used as a parameter, then the padding
        # attribute of the Padded object is not a copy but is the Padding
        # object itself.
        padding = size.Padding(1, 2, 3, 4)
        p = size.Padded(None, '', '', padding)
        self.assertTrue(p.padding is padding)

    def testcomputeRequestedSize(self):
        """Padded._computeRequestedSize adds padding size to widget size.""" 
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, '', '', 1, 2, 4, 8)
        rs = padded._computeRequestedSize()
        self.assertEquals(rs, size.Size(13, 32))
        self.assertTrue(isinstance(rs, size.SizeRequisition))

    def testGetRequestedSize(self):
        """Padded._getRequestedSize adds padding size to widget size.""" 
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, '', '', 1, 2, 4, 8)
        padded.computeRequestedSize()
        rs = padded.requested_size
        self.assertEquals(rs, size.Size(13, 32))
        self.assertTrue(isinstance(rs, size.SizeRequisition))

    def testAllocateSizeEqual(self):
        """Padded.allocateSize gives the widget what it wants when ideal.

        We give a padded object exactly the size it requests.  Therefore
        its widget should also have the size it requests.  We also check
        that the coordinates of the widget are properly set.

        """
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, '', '', 1, 2, 4, 8)
        padded.computeRequestedSize()
        requested_size = padded.requested_size        
        allocated_size = size.SizeAllocation(100, 200, requested_size)
        padded.allocateSize(allocated_size)
        widget_size = widget.allocated_size
        self.assertEquals(widget_size.width, 10)
        self.assertEquals(widget_size.height, 20)
        self.assertEquals(widget_size.left, 101)
        self.assertEquals(widget_size.top, 204)

    def testAllocateSizeShrinkABit(self):
        """Padded.allocateSize shrinks the widget when needed."""
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, '', '', 1, 2, 4, 8)
        padded.computeRequestedSize()
        requested_size = padded.requested_size
        allocated_size = size.SizeAllocation(100, 200, requested_size)
        allocated_size.height -= 15 # Widget height is 20, remove 15 leaves 5.
        padded.allocateSize(allocated_size)
        widget_size = widget.allocated_size
        self.assertEquals(widget_size.width, 10)
        self.assertEquals(widget_size.height, 5) # Only difference with ideal.
        self.assertEquals(widget_size.left, 101)
        self.assertEquals(widget_size.top, 204)

    def testAllocateSizeShrinkWidgetAtMax(self):
        """Padded.allocateSize shrinks the widget down to 0."""
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, '', '', 1, 2, 4, 8)
        padded.computeRequestedSize()
        requested_size = padded.requested_size
        allocated_size = size.SizeAllocation(100, 200, requested_size)
        allocated_size.height -= 20 # Widget height is 20, remove 20 leaves 0.
        padded.allocateSize(allocated_size)
        widget_size = widget.allocated_size
        self.assertEquals(widget_size.width, 10)
        self.assertEquals(widget_size.height, 0) # Only difference with ideal.
        self.assertEquals(widget_size.left, 101)
        self.assertEquals(widget_size.top, 204)

    def testAllocateSizeShrinkALot(self):
        """Padded.allocateSize shrinks the widget and padding when needed."""
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, '', '', 1, 2, 4, 8)
        padded.computeRequestedSize()
        requested_size = padded.requested_size
        allocated_size = size.SizeAllocation(100, 200, requested_size)
        allocated_size.height = 7 # Instead of 4+8=12.
        # The padding is 7 instead of 12.  That's a difference of 5. Divided by
        # two, it gives a reduction of -5//2=-3 on the top position of the
        # widget.
        padded.allocateSize(allocated_size)
        widget_size = widget.allocated_size
        self.assertEquals(widget_size.width, 10)
        self.assertEquals(widget_size.height, 0)
        self.assertEquals(widget_size.left, 101)
        self.assertEquals(widget_size.top, 201)

    def testAllocateSizeInflateNoExpand(self):
        """Padded.allocateSize breaks if too large and expand=False."""
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, '', '', 1, 2, 4, 8)
        padded.computeRequestedSize()
        requested_size = padded.requested_size
        allocated_size = size.SizeAllocation(0, 0, requested_size)
        allocated_size.height = 50
        self.assertRaises(size.SizeAllocationError,
                          padded.allocateSize, allocated_size)

    def testAllocatedSizeInflateNoFill(self):
        """Padded.allocatedSize inflates the padding when needed."""
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, 'hv', '', 1, 2, 4, 8)
        padded.computeRequestedSize()
        requested_size = padded.requested_size
        allocated_size = size.SizeAllocation(100, 200, requested_size)
        allocated_size.height += 50
        # Adding 50 adds 50//2=25 to the top position.
        padded.allocateSize(allocated_size)
        widget_size = widget.allocated_size
        self.assertEquals(widget_size.width, 10)
        self.assertEquals(widget_size.height, 20)
        self.assertEquals(widget_size.left, 101)
        self.assertEquals(widget_size.top, 204 + 25)

    def testAllocatedSizeInflateFill(self):
        """Padded.allocatedSize inflates the widget when needed."""
        widget = TestPadded.MockWidget()
        padded = size.Padded(widget, 'hv', 'hv', 1, 2, 4, 8)
        padded.computeRequestedSize()
        requested_size = padded.requested_size
        allocated_size = size.SizeAllocation(100, 200, requested_size)
        allocated_size.height += 50
        padded.allocateSize(allocated_size)
        widget_size = widget.allocated_size
        self.assertEquals(widget_size.width, 10)
        self.assertEquals(widget_size.height, 20 + 50)
        self.assertEquals(widget_size.left, 101)
        self.assertEquals(widget_size.top, 204)

#if __name__ == "__main__":
#    unittest.main()
