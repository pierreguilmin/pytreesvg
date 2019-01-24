import unittest
import sys, os
sys.path.insert(0, os.path.abspath('pytreesvg'))

from pytreesvg.tools import map

import math

class TestModuleTools(unittest.TestCase):
    """Unit test for the ``tools`` module."""

    def test_map(self):
        self.assertEqual(map(1, 0, 2, 0, 10), 5.0)
        self.assertEqual(map(30, 0, 180, 0, math.pi), 0.5235987755982988)

        with self.assertRaises(ValueError): map(1, 1, 1, 0, 10)


# shell command to run the tests:
# $ python -m unittest -v test.test_tools
if __name__ == '__main__':
    unittest.main()
