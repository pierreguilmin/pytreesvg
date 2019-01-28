"""This module implements a set of classes to draw a SVG tree.

.. testsetup::

    from pytreesvg.node_svg import NodeStyle, NodeSVG
"""

import re
from pytreesvg.tools import map

class NodeStyle:
    """This class defines a node style by detailing its SVG characteristics.
    
    Each node SVG style is defined by a short string representation of the form ``'<node color>@<node size>'`` like 
    ``'green@12'``, ``'#aa8ef7@3'``, ``'#f00@38'``, ``'rgb(122,17,234)@7'``, ``'rgb(23%,5%,100%)@10'``, ...

    Attributes
    ----------
    color: str
        Background color of the node circle, see **Notes** under.
    size: int
        Radius of the node circle in pixel, has to be an integer in [0, 100].
    
    Notes
    -----
    To respect the `W3C SVG 1.1 (Second Edition) Recommendation - Section 4.2 
    <https://www.w3.org/TR/2011/REC-SVG11-20110816/types.html#BasicDataTypes>`_, the following color notations 
    are allowed:

    - base color: ``aliceblue``, ``darkturquoise``, ``lightcoral``, ... (see `W3C SVG 1.1 (Second Edition) 
      Recommendation - Section 4.4 <https://www.w3.org/TR/2011/REC-SVG11-20110816/types.html#ColorKeywords>`_)
    - hexadecimal notation (short or long): ``#aa8ef7``, ``#F7AA9E``, ``#f00``, ``#FFF``, ...
    - rgb notation (value or percentage): ``rgb(122,17,234)``, ``rGb(13, 0, 137)``, ``rgb(23%,5%,100%)``, 
      ``RGB(23 %, 5 %, 100 %)``, ...
    """

    def __init__(self, representation='blue@12'):
        """Create a ``NodeStyle`` object.

        Parameters
        ----------
        representation: str, optional
            Short representation of the node style (`default='blue@12'`).

        Raises
        ------
        ValueError
            If the given representation is incorrect (i.e. the representation syntax is invalid or the color or the size
             don't respect the requirements described above).

        Examples
        --------
        .. doctest::

            >>> NodeStyle('green@12')
            <NodeStyle: color='green', size=12>
            >>> NodeStyle('#aa8ef7@3')
            <NodeStyle: color='#aa8ef7', size=3>
            >>> NodeStyle('rgb(122,17,234)@62')
            <NodeStyle: color='rgb(122,17,234)', size=62>
            >>> NodeStyle('bug_color@62')
            Traceback (most recent call last):
            ...
            ValueError: incorrect color (ex: 'green', '#aa8ef7', '#f00', 'rgb(122,17,234)', 'rgb(23%,5%,100%)', ...)
        """
        if not re.search(r'^.+@[0-9]+$', representation):
            raise ValueError("incorrect SVG node style representation (ex: 'green@12', '#aa8ef7@3', '#f00@38', "
                             "'rgb(122,17,234)@7', 'rgb(23%,5%,100%)@10', ...")

        # we need to remove extra '', see https://docs.python.org/2/library/re.html#re.split
        chuncks = [s for s in re.split(r'@', representation) if s != '']

        self.color = NodeStyle._get_valid_color(chuncks[0])
        self.size  = NodeStyle._get_valid_size(chuncks[1])

    @staticmethod
    def _get_valid_color(color):
        """Return a valid SVG color or raise an error.

        Parameters
        ----------
        color: str
            Color string.

        Raises
        ------
        ValueError
            If the given color doesn't match the SVG colors requirements described above.
        """
        # see https://www.w3.org/TR/2011/REC-SVG11-20110816/types.html#ColorKeywords
        base_color_list = [
            'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond',
            'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral',
            'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray',
            'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid',
            'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise',
            'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite',
            'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green',
            'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush',
            'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray',
            'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray',
            'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon',
            'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue',
            'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose',
            'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid',
            'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
            'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
            'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
            'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white',
            'whitesmoke', 'yellow', 'yellowgreen'
        ]

        # match one or two groups of 3 alphanumeric characters ('#aa8ef7', '#F7AA9E', '#f00', '#FFF', ...)
        hexadec_notation_regex = re.compile(r'^#([a-f0-9]{3}){1,2}$', re.IGNORECASE)

        # match colors like 'rgb(122,17,234)', 'rGb(122,17,234)', 'rgb( 122, 17, 234 )', ...
        rgb_notation_val_regex = re.compile(r'^rgb\(\s?[0-9]{1,3}\s?(,\s?[0-9]{1,3}\s?){2}\)', re.IGNORECASE)

        # match colors like 'rgb(23%,5%,100%)', 'rGb(23%,5%,100%)', 'rgb( 23%, 5 %, 100% )', ...
        rgb_notation_per_regex = re.compile(r'^rgb\(\s?[0-9]{1,3}\s?%\s?(,\s?[0-9]{1,3}\s?%\s?){2}\)$', re.IGNORECASE)

        if (color not in base_color_list and
                not hexadec_notation_regex.search(color) and
                not rgb_notation_val_regex.search(color) and
                not rgb_notation_per_regex.search(color)):
            raise ValueError("incorrect color (ex: 'green', '#aa8ef7', '#f00', 'rgb(122,17,234)', 'rgb(23%,5%,100%)', "
                             "...)")

        return color

    @staticmethod
    def _get_valid_size(size):
        """Return a valid size in [0, 100] or raise an error.

        Parameters
        ----------
        size: str
            Size string.

        Raises
        ------
        ValueError
            If the given size is not in [0, 100].
        """
        size = int(size)

        if size < 0 or size > 100:
            raise ValueError('the size has to be an integer in [0, 100]')

        return size

    def __repr__(self):
        """Return a string detailing the node style SVG characteristics."""
        return f'<NodeStyle: color={self.color!r}, size={self.size}>'

    def __str__(self):
        """Return a string representing the style."""
        return f'{self.color}@{self.size}'

    def get_color_id(self):
        """Return a string representing the color with a unique id that respects the SVG recommendation.

        Returns
        -------
        string
            Color id (unique and SVG-valid).

        Notes
        -----
        The `W3C SVG 1.1 (Second Edition) Recommendation - Section 5.10.1 
        <https://www.w3.org/TR/2011/REC-SVG11-20110816/struct.html#Core.attrib>`_ states that one should refer to the 
        `W3C XML 1.0 (Fifth Edition) Recommendation - Section 3.3.1 
        <https://www.w3.org/TR/2008/REC-xml-20081126/#sec-attribute-types>`_ when specifying the ``id`` attribute of an 
        object. This last document specifies that the possible names are defined in the `W3C XML 1.0 (Fifth Edition) 
        Recommendation - Section 2.3 <https://www.w3.org/TR/2008/REC-xml-20081126/#NT-Name>`_.

        This function returns an arbitrarily modified color name specifically built to respect this convention.

        Examples
        --------
        .. doctest::

            >>> NodeStyle('green@12').get_color_id()
            'green'
            >>> NodeStyle('#aa8ef7@3').get_color_id()
            'aa8ef7'
            >>> NodeStyle('rgb(122,17,234)@7').get_color_id()
            'rgb.122.17.234'
            >>> NodeStyle('rgb( 23%, 5 %, 100% )@8').get_color_id()
            'rgb.23p.5p.100p'
        """
        color_id = self.color

        color_id = re.sub(r'#|\)|\s', '', color_id) # remove '#', ')' and whitespace characters
        color_id = re.sub(r'\(|,', '.', color_id)   # replace '(' and ',' by '.'
        color_id = re.sub(r'%', 'p', color_id)      # replace '%' by 'p'

        return color_id


class NodeSVG:
    """This class defines a tree node and its SVG characteristics (style, position in the SVG image).

    A node is defined by a value and some children nodes (other ``NodeSVG`` objects). A node value can be of any type.

    Attributes
    ----------
    value: any
        Node value.
    children: list of ``NodeSVG``
        Node children, can be empty.
    style: ``NodeStyle``
        SVG style of the node.
    x: int
        Circle `x` position in the SVG image in pixel.
    y: int
        Circle `y` position in the SVG image in pixel.

    Notes
    -----
    The tree defined by the root node (the only node with no parent) is the equivalent of a mathematically defined 
    unordered tree (or algebraic tree). See `Wikipedia 'Tree (data structure)' article 
    <https://en.wikipedia.org/wiki/Tree_(data_structure)>`_.
    """

    def __init__(self, value=None, children=None, style='blue@12'):
        """Create a ``NodeSVG`` object.

        Parameters
        ----------
        value: any, optional
            Node value (`default=None`).
        children: list of ``NodeSVG``, optional
            Node children (`default=None`).
        style: ``NodeStyle`` string short representation, optional
            ``NodeStyle`` string short representation defining the SVG style of the node (`default='blue@12'`).

        Examples
        --------
        .. doctest::

            >>> NodeSVG('+', children=[NodeSVG(1, style='aqua@16'), NodeSVG(2), NodeSVG(3)])
            '+' (blue@12, x: 0.00, y: 0.00)
            └── 1 (aqua@16, x: 0.00, y: 0.00)
            └── 2 (blue@12, x: 0.00, y: 0.00)
            └── 3 (blue@12, x: 0.00, y: 0.00)
            >>> # lighter representation using print
            >>> print(NodeSVG('-', children=[NodeSVG(1),
            ...                              NodeSVG('*', children=[NodeSVG(5),
            ...                                                     NodeSVG(4)])]))
            -
            └── 1
            └── *
                └── 5
                └── 4
        """
        self.value    = value

        if children:
            self.children = children
        else:
            self.children = []

        self.style = NodeStyle(style)

        self.x = 0.0
        self.y = 0.0

    def __repr__(self, depth=0):
        """Return a string representing the node and its children as a tree (with their SVG style and position)."""
        string_tree = f'{self.value!r} ({self.style}, x: {self.x:.2f}, y: {self.y:.2f})'

        indentation = '    ' * depth

        for child in self.children:
            string_tree += f'\n{indentation}└── {child.__repr__(depth + 1)}'

        return string_tree

    def __str__(self, depth=0):
        """Return a string representing the node and its children as a tree."""
        string_tree = str(self.value)

        indentation = '    ' * depth

        for child in self.children:
            string_tree += f'\n{indentation}└── {child.__str__(depth + 1)}'

        return string_tree

    def add_child(self, child):
        """Add a child to the node.

        Parameters
        ----------
        child: ``NodeSVG``
            Child to add.
        
        Examples
        --------
        .. doctest::

            >>> tree = NodeSVG('+')
            >>> print(tree)
            +
            >>> tree.add_child(NodeSVG(1))
            >>> tree.add_child(NodeSVG(2))
            >>> print(tree)
            +
            └── 1
            └── 2

        Warnings
        --------
        This method is not doing a deep copy of the given ``NodeSVG`` object, any subsequent modification of the given 
        node will modify the current node.
        
        .. doctest::

            >>> tree = NodeSVG('root node')
            >>> child = NodeSVG('some value')
            >>> tree.add_child(child)
            >>> print(tree)
            root node
            └── some value
            >>> child.value = 'new value!'
            >>> print(tree)
            root node
            └── new value!
        """
        self.children.append(child)

    def is_leaf(self):
        """Return a boolean indicating if the node is a leaf or not (a node is a leaf if it has no children).

        Returns
        -------
        bool
            ``True`` if the node has no children, ``False`` otherwise.

        Examples
        --------
        .. doctest::

            >>> basic_tree = NodeSVG('+', children=[NodeSVG(1), NodeSVG(2), NodeSVG(3)])
            >>> basic_tree.is_leaf()
            False
            >>> basic_tree.children[0].is_leaf()
            True
        """
        return not self.children

    def get_depth(self, current_node_depth=0):
        """Find the depth of the tree from this node (the mathematically defined depth).
    
        Parameters
        ----------
        current_node_depth: int, optional
            Depth of the current node in the considered tree (`default=0`).

        Examples
        --------
        .. doctest::

            >>> basic_tree = NodeSVG('+', children=[NodeSVG('-', children=[NodeSVG(5)]), NodeSVG(2)])
            >>> print(basic_tree)
            +
            └── -
                └── 5
            └── 2
            >>> basic_tree.get_depth()
            2
        """
        if self.is_leaf():
            return current_node_depth
        else:
            return max([child.get_depth(current_node_depth + 1) for child in self.children])

    def to_svg(self, path='node.svg', width=400, height=400, gradient_color=True, image_border=True):
        """Create a SVG image and draw the tree.

        Danger
        ------
        The file at the given path will be overwritten if it exists.

        Parameters
        ----------
        path: str, optional
            Path to the ``.svg`` file to save (`default='node.svg'`).
        width: int, optional
            Width of the SVG image to produce, it has to be an integer in [10, 10000] (`default=400`).
        height: int, optional
            Height of the SVG image to produce, it has to be an integer in [10, 10000] (`default=400`).
        gradient_color: bool, optional
            Set to ``True`` to apply linear gradient colors to edges between differently colored nodes (`default=True`).
        image_border: bool, optional
            Set to ``True`` to draw the image border (`default=True`).
        
        Raises
        ------
        ValueError
            If the given width or height are not integers in [10, 10000].

        Notes
        -----
        The `DOCTYPE` for SVG 1.1 is

        ``<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN``
        ``"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"``
        
        However, the official `W3C SVG 1.1 (Second Edition) Recommendation - Section 1.3 
        <https://www.w3.org/TR/2011/REC-SVG11-20110816/intro.html#NamespaceAndDTDIdentifiers>`_ states that "It is not 
        recommended that a DOCTYPE declaration be included in SVG documents.".

        We respect the W3C recommendation and don't include the `DOCTYPE` in the output SVG file.
        """
        width  = int(width)
        height = int(height)

        if (width  < 10 or width  > 10000 or
            height < 10 or height > 10000):
            raise ValueError('the width and height of the SVG image have to be integers in [10, 10000]')

        self._recursively_compute_x_position(width)
        self._recursively_compute_y_position(height)

        with open(path, 'w') as SVG_file:
            header = (f'<?xml version="1.0" encoding="utf-8" standalone="no"?>\n\n'

                      f'<svg width="{width}" height="{height}" '
                      f'version="1.1" xmlns="http://www.w3.org/2000/svg">\n\n')

            if gradient_color:
                defs = ('    <defs>\n'
                        '        <!-- linear gradient definitions -->\n' +
                        self._recursively_get_svg_gradient_color_defs()[0] +
                        '    </defs>\n\n')
            else:
                defs = ''

            title = (f'    <!-- image title -->\n'
                     f'    <title>Tree graphic created with pytreesvg</title>\n\n')

            if image_border:
                border = (f'    <!-- image border -->\n'
                          f'    <rect x="0" y="0" width="{width}" height="{height}" '
                          f'style="stroke: #000000; fill: none;"/>\n\n')
            else:
                border = ''

            corpse = self._recursively_get_svg_representation(gradient_color)

            backer = ('</svg>\n')

            SVG_file.write(header + title + defs + border + corpse + backer)

    def _recursively_compute_y_position(self, SVG_height, current_node_depth=0, tree_depth=None):
        """Recursively compute the `y` position of the node and its children in the SVG image.

        The function used to compute the :math:`y` position of a node at depth :math:`t` belonging to a tree of total 
        depth :math:`T` in a SVG image of height :math:`h` is
        
        .. math::
            f : [0, T] & \\to     ]0, h[ \\\\
                t      & \\mapsto \\text{map}(t, -0.5, T + 0.5, 0, h)

        (see :func:`pytreesvg.tools.map`).

        Parameters
        ----------
        SVG_height: int
            Total height of the SVG image.
        current_node_depth: int, optional
            Depth of the current node in the tree (`default=0`).
        tree_depth: int, optional
            Total depth of the tree (`default=None`).
        """
        if not tree_depth:
            tree_depth = self.get_depth()

        self.y = map(current_node_depth, -0.5, tree_depth + 0.5, 0, SVG_height)

        for child in self.children:
            child._recursively_compute_y_position(SVG_height, current_node_depth + 1, tree_depth)

    def _recursively_compute_x_position(self,
                                        parent_SVG_width,
                                        level_SVG_offset=0.0,
                                        current_node_index=0,
                                        nb_node_current_level=1):
        """Recursively compute the `x` position of the node and its children in the SVG image.

        The function used to compute the :math:`x` position of a node at index :math:`i` belonging to a siblings group (
        later called a `level`) of :math:`n` nodes and a SVG parent node width of :math:`w` beginning at position 
        :math:`x_p` is
        
        .. math::
            f : [0, n-1] & \\to     ]0, w[ \\\\
                i        & \\mapsto x_p + \\text{map}(i, -0.5, n - 0.5, 0, w)

        (see :func:`pytreesvg.tools.map`).

        Parameters
        ----------
        parent_SVG_width: float
            SVG width of the parent node.
        level_SVG_offset: float, optional
            SVG x offset of the current level (`default=0`).
        current_node_index: int, optional
            Current node index in the current level (`default=0`).
        nb_node_current_level: int, optional
            Number of node in the current level (`default=1`).
        """
        self.x = level_SVG_offset + map(current_node_index, -0.5, nb_node_current_level - 0.5, 0, parent_SVG_width)

        new_parent_SVG_width = parent_SVG_width / nb_node_current_level
        new_level_SVG_offset = level_SVG_offset + map(current_node_index - 1, -1, nb_node_current_level - 1, 0, parent_SVG_width)

        for i, child in enumerate(self.children):
            child._recursively_compute_x_position(parent_SVG_width=new_parent_SVG_width,
                                                  level_SVG_offset=new_level_SVG_offset,
                                                  current_node_index=i,
                                                  nb_node_current_level=len(self.children))

    def _recursively_get_svg_representation(self, gradient_color, indentation='    '):
        """Recursively get the SVG representation of the node and its children.

        Parameters
        ----------
        gradient_color: bool
            If some gradient colors have been defined in the SVG `defs` section (by using 
            :meth:`_recursively_get_svg_gradient_color_defs` when creating the SVG image), set to ``True`` to use these 
            colors for the edges.
        indentation: str, optional
            Spaces before the current node SVG string to distinguish children from parents (`default='    '`).

        Returns
        -------
        str
            SVG representation of the node and its children.
        """
        current_node_SVG_representation = f'{indentation}<!-- Node {self.value!r} -->\n'

        # draw node edges
        for child in self.children:
            if gradient_color:
                if self.style.color == child.style.color:
                    # no need for gradient color
                    color = self.style.color
                else:
                    # find the gradient color previously defined
                    color = f'url(#grad_{self.style.get_color_id()}_{child.style.get_color_id()})'
            else:
                color = 'black'

            current_node_SVG_representation += (f'{indentation}<line x1="{self.x}" y1="{self.y}" '
                                                f'x2="{child.x}" y2="{child.y}" '
                                                f'stroke="{color}" stroke-width="2"/> '
                                                f'<!-- edge to node {child.value!r} -->\n')

        # draw node
        current_node_SVG_representation += (f'{indentation}<circle cx="{self.x}" cy="{self.y}" '
                                           f'r="{self.style.size}" fill="{self.style.color}"/>\n\n')

        children_SVG_representation = ''

        for child in self.children:
            children_SVG_representation += child._recursively_get_svg_representation(gradient_color,
                                                                                     indentation + '    ')

        return current_node_SVG_representation + children_SVG_representation

    def _recursively_get_svg_gradient_color_defs(self, created_gradient_list=None):
        """Recursively create all the necessary linear gradient color definitions.

        Parameters
        ----------
        created_gradient_list: list of str, optional
            List of gradient colors id already created (`default=None`)

        Returns
        -------
        (str, list of str)
            (gradient color definitions of the node and its children, already created gradient colors)
        """
        if not created_gradient_list:
            created_gradient_list = []

        self.svg_gradient = ''

        for child in self.children:
            gradient_id = f'grad_{self.style.get_color_id()}_{child.style.get_color_id()}'

            if self.style.color != child.style.color and gradient_id not in created_gradient_list:
                self.svg_gradient += (f'        <linearGradient id="{gradient_id}" x1="0%" x2="0%" y1="0%" y2="100%">\n'
                                      f'           <stop offset="0%" stop-color="{self.style.color}"/>\n'
                                      f'           <stop offset="100%" stop-color="{child.style.color}"/>\n'
                                      f'        </linearGradient>\n')
                created_gradient_list.append(gradient_id)
                (child_gradient, created_gradient_list) = child._recursively_get_svg_gradient_color_defs(created_gradient_list)
                self.svg_gradient += child_gradient

        return (self.svg_gradient, created_gradient_list)


class TreeSVG:
    def __init__(self, representation=None):
        lines = representation.split('\n')

        self.root_node = NodeSVG()
