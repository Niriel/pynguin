'''
Created on Jan 9, 2011

@author: Niriel
'''
import unittest
from pynguin.widget import binwidget
from pynguin.widget.sizeablewidget import SizeableWidget
from mock import MockDisplayer

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.

class TestBinWidget(unittest.TestCase):
    """Test the widget.binwidget module."""

    def testInitNoLayout(self):
        """BinWidget.__init__ does its job."""
        my_container = binwidget.BinWidget()
        self.assertTrue(my_container._layout is None)

    def testInitWithLayout(self):
        """BinWidget.__init__ instantiates a layout if LAYOUT_CLS given.

        """
        class BinWithLayout(binwidget.BinWidget):
            """Just to have a LAYOUT_CLS."""
            LAYOUT_CLS = list # Anything instantiable, don't care.

        my_container = BinWithLayout()
        self.assertEquals(my_container._layout.__class__, list)

    def testDispatchDisplayer(self):
        """BinWidget.dispatchDisplayers transmits displayer to child.

        """
        widget = SizeableWidget()
        my_container = binwidget.BinWidget()
        my_container.addChild(widget, 'end', 'not', 'not')
        displayer = MockDisplayer()
        my_container.dispatchDisplayers(displayer)
        self.assertTrue(my_container.getDisplayer() is displayer)
        self.assertTrue(widget.getDisplayer() is displayer)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
