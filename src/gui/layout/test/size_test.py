'''
Created on Nov 4, 2010

@author: Niriel
'''


import unittest
from gui.layout import size


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


if __name__ == "__main__":
    unittest.main()
