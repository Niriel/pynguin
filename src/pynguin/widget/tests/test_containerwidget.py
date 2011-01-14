'''
Created on Jan 9, 2011

@author: Niriel
'''
import unittest
from pynguin.widget import containerwidget
from pynguin.widget.sizeablewidget import SizeableWidget
from mock import MockDisplayer

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.

class TestContainerWidget(unittest.TestCase):
    """Test the widget.containerwidget module."""
    def testInitNoLayout(self):
        """ContainerWidget.__init__ does its job."""
        my_container = containerwidget.ContainerWidget()
        self.assertTrue(my_container._layout is None)

    def testInitWithLayout(self):
        """ContainerWidget.__init__ instantiates a layout if LAYOUT_CLS given.

        """
        class ContainerWithLayout(containerwidget.ContainerWidget):
            """Just to have a LAYOUT_CLS."""
            LAYOUT_CLS = list # Anything instantiable, don't care.

        my_container = ContainerWithLayout()
        self.assertEquals(my_container._layout.__class__, list)

    def testDispatchDisplayer(self):
        """ContainerWidget.dispatchDisplayers transmits displayers to children.

        """
        widget1 = SizeableWidget()
        widget2 = SizeableWidget()
        my_container = containerwidget.ContainerWidget()
        my_container.addChild(widget1, 'end', 'not', 'not')
        my_container.addChild(widget2, 'end', 'not', 'not')
        displayer = MockDisplayer()
        my_container.dispatchDisplayers(displayer)
        self.assertTrue(my_container.getDisplayer() is displayer)
        self.assertTrue(widget1.getDisplayer() is displayer)
        self.assertTrue(widget2.getDisplayer() is displayer)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
