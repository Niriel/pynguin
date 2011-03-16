'''
Created on Jan 9, 2011

@author: Niriel
'''
import unittest
from pynguin.widget import widget
from mock import MockDisplayer

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.

class TestWidget(unittest.TestCase):
    """Test the widget.widget module."""

    def testInitNoSpriteClass(self):
        """Widget.__init__() does its job."""
        my_widget = widget.Widget()
        self.assertEquals(my_widget._sprite, None)
        self.assertEquals(my_widget._displayer, None)

    def testInitWithSpriteClass(self):
        """Widget.__init__() instanciate the sprite if SPRITE_CLS given."""
        class WidgetSprite(widget.Widget):
            """Just to have a SPRITE_CLS."""
            SPRITE_CLS = list # Anything instantiable, don't care.

        my_widget = WidgetSprite()
        self.assertEquals(my_widget._sprite.__class__, list)

    def testSetDisplayer(self):
        """Widget.setDisplayer sets the displayer."""
        my_widget = widget.Widget()
        displayer = MockDisplayer()
        my_widget.setDisplayer(displayer)
        self.assertTrue(my_widget._displayer() is displayer)
        #
        del displayer
        self.assertTrue(my_widget._displayer() is None)
        #
        displayer = MockDisplayer()
        my_widget.setDisplayer(displayer)
        my_widget.setDisplayer(None)
        self.assertTrue(my_widget._displayer is None)

    def testGetDisplayer(self):
        """Widget.getDisplayer retreives the displayer."""
        my_widget = widget.Widget()
        displayer = MockDisplayer()
        my_widget.setDisplayer(displayer)
        self.assertTrue(my_widget.getDisplayer() is displayer)
        del displayer
        self.assertTrue(my_widget.getDisplayer() is None)
        displayer = MockDisplayer()
        my_widget.setDisplayer(displayer)
        my_widget.setDisplayer(None)
        self.assertTrue(my_widget.getDisplayer() is None)

    def testSetDisplayerAddSprite(self):
        """Widget.setDisplayer adds the sprite to the displayer."""
        displayer = MockDisplayer()
        my_widget = widget.Widget()
        my_widget._sprite = 42
        my_widget.setDisplayer(displayer)
        self.assertEquals(displayer.sprites, [42])

    def testSetDisplayerRemoveSprite(self):
        """Widget.setDisplayer removes the sprite from the displayer."""
        displayer = MockDisplayer()
        my_widget = widget.Widget()
        my_widget._sprite = 42
        my_widget.setDisplayer(displayer)
        my_widget.setDisplayer(None)
        self.assertEquals(displayer.sprites, [])

    def testSetDisplayerChange(self):
        """Widget.setDisplayer moves the sprite when changing displayer."""
        displayer1 = MockDisplayer()
        displayer2 = MockDisplayer()
        my_widget = widget.Widget()
        my_widget._sprite = 42
        my_widget.setDisplayer(displayer1)
        self.assertEquals(displayer1.sprites, [42])
        self.assertEquals(displayer2.sprites, [])
        my_widget.setDisplayer(displayer2)
        self.assertEquals(displayer1.sprites, [])
        self.assertEquals(displayer2.sprites, [42])

    def testDispatchDisplayers(self):
        """Widget.dispatchDisplayers calls setDisplayer."""
        my_widget = widget.Widget()
        displayer = MockDisplayer()
        my_widget.dispatchDisplayers(displayer)
        self.assertTrue(my_widget.getDisplayer() is displayer)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
