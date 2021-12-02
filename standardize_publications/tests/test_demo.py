import unittest

from lw_pub_statistics import MyModel

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_modelError(self):
        m = MyModel()
        self.assertAlmostEqual(m.my_method(10), 0.01) # when comapring floats one shoudl allow for some margin
        with self.assertRaises(AssertionError):       # to trigger and test for intended failure
            m.my_method(200)

if __name__ == '__main__':
    unittest.main()