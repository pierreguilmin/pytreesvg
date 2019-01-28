import unittest
import sys, os
sys.path.insert(0, os.path.abspath('pytreesvg'))

from pytreesvg.node_svg import NodeStyle, NodeSVG
import random

class TestClassNodeStyle(unittest.TestCase):
    """Unit test for the ``NodeStyle`` class."""

    def setUp(self):
        self.style_1 = NodeStyle('green@12')
        self.style_2 = NodeStyle('#aa8ef7@3')
        self.style_3 = NodeStyle('#f00@38')
        self.style_4 = NodeStyle('rgb(122,17,234)@7')
        self.style_5 = NodeStyle('rgb(23%,5%,100%)@10')

    def test_init(self):
        with self.assertRaises(ValueError): NodeStyle('')
        with self.assertRaises(ValueError): NodeStyle('@')
        with self.assertRaises(ValueError): NodeStyle('#@')
        with self.assertRaises(ValueError): NodeStyle('#green')
        with self.assertRaises(ValueError): NodeStyle('@12')
        with self.assertRaises(ValueError): NodeStyle('12')

    def test_get_valid_color(self):
        with self.assertRaises(ValueError): NodeStyle._get_valid_color('lol')
        with self.assertRaises(ValueError): NodeStyle._get_valid_color('12')
        with self.assertRaises(ValueError): NodeStyle._get_valid_color('fff')
        with self.assertRaises(ValueError): NodeStyle._get_valid_color('#FF87')
        with self.assertRaises(ValueError): NodeStyle._get_valid_color('#rgb(122,17,234)')

        NodeStyle._get_valid_color('#F7AA9E')
        NodeStyle._get_valid_color('#FFF')
        NodeStyle._get_valid_color('rGb(122,17,234)')
        NodeStyle._get_valid_color('rgb( 122, 17, 234 )')
        NodeStyle._get_valid_color('rGb(23%,5%,100%)')
        NodeStyle._get_valid_color('rgb( 23%, 5 %, 100% )')

    def test_get_valid_size(self):
        with self.assertRaises(ValueError): NodeStyle._get_valid_size('125')
        with self.assertRaises(ValueError): NodeStyle._get_valid_size('-2')

    def test_repr(self):
        self.assertEqual(repr(self.style_1), "<NodeStyle: color='green', size=12>")
        self.assertEqual(repr(self.style_2), "<NodeStyle: color='#aa8ef7', size=3>")
        self.assertEqual(repr(self.style_3), "<NodeStyle: color='#f00', size=38>")
        self.assertEqual(repr(self.style_4), "<NodeStyle: color='rgb(122,17,234)', size=7>")
        self.assertEqual(repr(self.style_5), "<NodeStyle: color='rgb(23%,5%,100%)', size=10>")

    def test_str(self):
        self.assertEqual(str(self.style_1), 'green@12')
        self.assertEqual(str(self.style_2), '#aa8ef7@3')
        self.assertEqual(str(self.style_3), '#f00@38')
        self.assertEqual(str(self.style_4), 'rgb(122,17,234)@7')
        self.assertEqual(str(self.style_5), 'rgb(23%,5%,100%)@10')

    def test_get_color_id(self):
        self.assertEqual(self.style_1.get_color_id(), 'green')
        self.assertEqual(self.style_2.get_color_id(), 'aa8ef7')
        self.assertEqual(self.style_3.get_color_id(), 'f00')
        self.assertEqual(self.style_4.get_color_id(), 'rgb.122.17.234')
        self.assertEqual(self.style_5.get_color_id(), 'rgb.23p.5p.100p')

        self.assertEqual(NodeStyle('rgb( 122, 17, 234 )@7').get_color_id(), 'rgb.122.17.234')
        self.assertEqual(NodeStyle('rgb( 23%, 5 %, 100% )@7').get_color_id(), 'rgb.23p.5p.100p')


class TestClassNodeSVG(unittest.TestCase):
    """Unit test for the ``NodeSVG`` class."""

    def setUp(self):
        self.basic_tree   = NodeSVG('+', children=[NodeSVG(1), NodeSVG(2), NodeSVG(3)])
        self.complex_tree = NodeSVG('-', children=[NodeSVG(1), NodeSVG('*', children=[NodeSVG(5), NodeSVG(4)])])

    def test_repr(self):
        self.assertEqual(repr(self.basic_tree), "'+' (blue@12, x: 0.00, y: 0.00)\n"
                                                "└── 1 (blue@12, x: 0.00, y: 0.00)\n"
                                                "└── 2 (blue@12, x: 0.00, y: 0.00)\n"
                                                "└── 3 (blue@12, x: 0.00, y: 0.00)")

        self.assertEqual(repr(self.complex_tree), "'-' (blue@12, x: 0.00, y: 0.00)\n"
                                                  "└── 1 (blue@12, x: 0.00, y: 0.00)\n"
                                                  "└── '*' (blue@12, x: 0.00, y: 0.00)\n"
                                                  "    └── 5 (blue@12, x: 0.00, y: 0.00)\n"
                                                  "    └── 4 (blue@12, x: 0.00, y: 0.00)")

    def test_str(self):
        self.assertEqual(str(self.basic_tree), '+\n'
                                               '└── 1\n'
                                               '└── 2\n'
                                               '└── 3')

        self.assertEqual(str(self.complex_tree), '-\n'
                                                 '└── 1\n'
                                                 '└── *\n'
                                                 '    └── 5\n'
                                                 '    └── 4')

    def test_is_leaf(self):
        self.assertEqual(self.basic_tree.is_leaf(), False)
        self.assertEqual(self.basic_tree.children[0].is_leaf(), True)

    def test_get_depth(self):
        self.assertEqual(self.basic_tree.get_depth(), 1)
        self.assertEqual(self.complex_tree.get_depth(), 2)

    def test_get_random_node(self):
        random.seed(42)

        self.assertEqual(repr(NodeSVG.get_random_node()), '3 (rgb(57,12,140)@12, x: 0.00, y: 0.00)')

        random_node = NodeSVG.get_random_node(values=['Michel', 'Julia', 'Robert'],
                                              sizes=[18, 1, 2],
                                              colors=['aqua', 'salmon', '#ff8', 'rgb(10%, 22%, 13%)'])
        self.assertEqual(repr(random_node), "'Robert' (salmon@18, x: 0.00, y: 0.00)")

        with self.assertRaises(TypeError): NodeSVG.get_random_node(values=1)
        with self.assertRaises(TypeError): NodeSVG.get_random_node(sizes=1)
        with self.assertRaises(Exception): NodeSVG.get_random_node(colors='aqua')


# shell command to run the tests:
# $ python -m unittest -v test.test_node_svg
if __name__ == '__main__':
    unittest.main()
