'''
Created on Jan 9, 2011

@author: Niriel
'''
import unittest
from pynguin.widget import windowwidget
from pynguin.widget.sizeablewidget import SizeableWidget
from mock import MockDisplayer

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.

class TestWindowWidget(unittest.TestCase):
    """Test the widget.windowwidget module."""
    def testInit(self):
        """WindowWidget.__init__ instantiates sprite and layout."""
        my_window = windowwidget.WindowWidget()
        self.assertTrue(my_window._sprite.__class__.__name__.\
                        endswith('WindowSprite'))
        self.assertTrue(my_window._layout.__class__.__name__.\
                        endswith('WindowLayout'))

    def testDispatchDisplayer(self):
        """WindowWidget.dispatchDisplayers transmits self to child."""
        widget = SizeableWidget()
        my_window = windowwidget.WindowWidget()
        my_window.addChild(widget, 'not', 'not')
        displayer = MockDisplayer()
        my_window.dispatchDisplayers(displayer)
        self.assertTrue(my_window.getDisplayer() is displayer)
        self.assertTrue(widget.getDisplayer() is my_window)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()