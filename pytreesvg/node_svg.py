"""This module implements a set of classes to draw a SVG tree."""

from __future__ import annotations
import random
from typing import Any, List, Optional, Tuple

from pytreesvg.node_style import NodeStyle
from pytreesvg.utils.tools import map_value


class NodeSVG:
    """This class defines a tree node and its SVG characteristics (style,
    position in the SVG image).

    A node is defined by a value and some children nodes (other ``NodeSVG``
    objects). A node value can be of any type.

    Attributes:
        value: Node value.
        children: Node children, can be empty.
        style: SVG style of the node.
        x: Circle `x` position in the SVG image in pixel.
        y: Circle `y` position in the SVG image in pixel.

    Notes:
        The tree defined by the root node (the only node with no parent) is the
        equivalent of a mathematically defined
        unordered tree (or algebraic tree). See
        `Wikipedia 'Tree (data structure)' article <https://en.wikipedia.org/wiki/Tree_(data_structure)>`_
        .
    """

    def __init__(self,
                 value: Optional[Any] = None,
                 children: Optional[List[Any]] = None,
                 style: str = 'blue@12'):
        """Create a ``NodeSVG`` object.

        Args:
            value: Node value.
            children: Node children.
            style: ``NodeStyle`` string short representation defining the SVG
                style of the node.

        Examples:
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

    def __repr__(self, depth: int = 0) -> str:
        """Return a string representing the node and its children as a tree (
        with their SVG style and position)."""
        string_tree = (f'{self.value!r} ({self.style}, x: {self.x:.2f}, '
                       f'y: {self.y:.2f})')

        indentation = '    ' * depth

        for child in self.children:
            string_tree += f'\n{indentation}└── {child.__repr__(depth + 1)}'

        return string_tree

    def __str__(self, depth: int = 0) -> str:
        """Return a string representing the node and its children as a tree."""
        string_tree = str(self.value)

        indentation = '    ' * depth

        for child in self.children:
            string_tree += f'\n{indentation}└── {child.__str__(depth + 1)}'

        return string_tree

    def add_child(self, child: NodeSVG):
        """Add a child to the node.

        Args:
            child: Child to add.

        Raises:
            TypeError: If child is not of type ``NodeSVG``.

        Examples
        --------
            >>> tree = NodeSVG('+')
            >>> print(tree)
            +
            >>> tree.add_child(NodeSVG(1))
            >>> tree.add_child(NodeSVG(2))
            >>> print(tree)
            +
            └── 1
            └── 2

        Warnings:
            This method is not doing a deep copy of the given ``NodeSVG``
            object, any subsequent modification of the given node will modify
            the current node.
        
        Examples:
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
        if type(child) is not NodeSVG:
            raise TypeError('child parameter has to be of type NodeSVG')

        self.children.append(child)

    def is_leaf(self) -> bool:
        """Return a boolean indicating if the node is a leaf or not (a node
        is a leaf if it has no children).

        Returns:
            ``True`` if the node has no children, ``False`` otherwise.

        Examples:
            >>> basic_tree = NodeSVG('+', children=[NodeSVG(1), NodeSVG(2), NodeSVG(3)])
            >>> basic_tree.is_leaf()
            False
            >>> basic_tree.children[0].is_leaf()
            True
        """
        return not self.children

    def get_depth(self, current_node_depth: int = 0) -> int:
        """Find the depth of the tree from this node (the mathematically
        defined depth).
    
        Args:
            current_node_depth: Depth of the current node in the considered tree
                .

        Examples
        --------
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
            return max(
                [child.get_depth(current_node_depth + 1) for child in self.children]
            )

    @staticmethod
    def get_random_node(values: List[Any] = range(0, 10),
                        sizes: List[int] = range(5, 21),
                        colors: Optional[List[str]] = None) -> NodeSVG:
        """Return a random ``NodeSVG`` object.

        Args:
            values: List of possible values for the random node.
            sizes: List of possible sizes for the random node.
            colors: List of possible colors for the random node, if not
                specified the color will be selected randomly over the whole
                color spectrum.

        Notes:
            This functions uses the ``random`` module. If you need reproducible
            results please set the random number generator seed before calling
            this function::

                import random

                random.seed(42) # set random number generator seed to 42

        Examples:
            >>> import random
            >>> random.seed(42)
            >>> NodeSVG.get_random_node()
            3 (rgb(57,12,140)@12, x: 0.00, y: 0.00)
            >>> NodeSVG.get_random_node(values=['Michel', 'Julia', 'Robert'],
            ...                         sizes=[18, 1, 2],
            ...                         colors=['aqua', 'salmon', '#ff8', 'rgb(10%, 22%, 13%)'])
            'Robert' (salmon@18, x: 0.00, y: 0.00)

        Warnings:
            If you want to specify a unique value for one of the parameters,
            please still use a list format::

                # bad syntax
                NodeSVG.get_random_node(values=1)

                # good syntax
                NodeSVG.get_random_node(values=[1])
        """
        if colors:
            color = random.choice(colors)
        else:
            # pick random color over the whole color spectrum
            color = (f'rgb({random.randint(0, 255)},{random.randint(0, 255)},'
                     f'{random.randint(0, 255)})')

        return NodeSVG(
            value=random.choice(values),
            style=f'{color}@{random.choice(sizes)}'
        )

    @staticmethod
    def get_random_tree(max_depth: int = 5,
                        n_children: List[int] = range(0, 5),
                        values: List[Any] = range(0, 10),
                        sizes: List[int] = range(5, 21),
                        colors: List[str] = None) -> Optional[NodeSVG]:
        """Return a ``NodeSVG`` object being the root node of a random tree.

        Args:
            max_depth: Random tree max depth (the mathematically defined depth).
            n_children: List of possible values for the number of children
                per node.
            values: List of possible values for the random nodes.
            sizes: List of possible sizes for the random nodes.
            colors: List of possible colors for the random nodes,
                if not specified the color will be selected randomly over the
                whole color spectrum.

        Notes:
            This functions uses the ``random`` module. If you need reproducible
            results please set the random number
            generator seed before calling this function::

                import random

                random.seed(42) # set random number generator seed to 42

        Examples:
            >>> import random
            >>> random.seed(16)
            >>> print(NodeSVG.get_random_tree())
            4
            └── 4
                └── 5
                    └── 9
                    └── 7
                        └── 6
                            └── 9
                            └── 0
                    └── 4
                        └── 7
                            └── 1
                            └── 2
                            └── 6
                        └── 1
                            └── 6
                            └── 4
                            └── 1
                            └── 0
                        └── 0
                    └── 8
            >>> NodeSVG.get_random_tree(max_depth=2,
            ...                         n_children=[2],
            ...                         values=['Michel', 'Julia', 'Robert'],
            ...                         sizes=[18, 1, 2],
            ...                         colors=['aqua', 'salmon', '#ff8', 'rgb(10%, 22%, 13%)'])
            'Michel' (salmon@1, x: 0.00, y: 0.00)
            └── 'Michel' (#ff8@1, x: 0.00, y: 0.00)
                └── 'Julia' (salmon@18, x: 0.00, y: 0.00)
                └── 'Julia' (salmon@1, x: 0.00, y: 0.00)
            └── 'Michel' (rgb(10%, 22%, 13%)@1, x: 0.00, y: 0.00)
                └── 'Julia' (salmon@18, x: 0.00, y: 0.00)
                └── 'Julia' (aqua@1, x: 0.00, y: 0.00)

        Warnings:
            If you want to specify a unique value for one of the parameters,
            please still use a list format::

                # bad syntax
                NodeSVG.get_random_tree(n_children=4)

                # good syntax
                NodeSVG.get_random_node(n_children=[4])
        """
        if max_depth < 0:
            return None

        # create random root node
        root_node = NodeSVG.get_random_node(values, sizes, colors)

        # choose a random number of children
        n_children_per_node = random.choice(n_children)

        for i in range(n_children_per_node):
            # create new random subtree
            new_node = NodeSVG.get_random_tree(
                max_depth - 1,
                n_children,
                values,
                sizes,
                colors
            )
            if new_node is not None:
                root_node.add_child(new_node)

        return root_node

    def to_svg(self,
               path: str = 'node.svg',
               width: int = 400,
               height: int = 400,
               gradient_color: bool = True,
               image_border: bool = True):
        """Create a SVG image and draw the tree.

        Danger:
            The file at the given path will be overwritten if it exists.

        Args:
            path: Path to the ``.svg`` file to save.
            width: Width of the SVG image to produce, it has to be an integer
                in [10, 10000].
            height: Height of the SVG image to produce, it has to be an
                integer in [10, 10000].
            gradient_color: Set to ``True`` to apply linear gradient colors
                to edges between differently colored nodes.
            image_border: Set to ``True`` to draw the image border.
        
        Raises:
            ValueError: If the given width or height are not integers in [10,
                10000].

        Notes:
            The `DOCTYPE` for SVG 1.1 is

            ``<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN``
            ``"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"``
        
            However, the official
            `W3C SVG 1.1 (Second Edition) Recommendation - Section 1.3 <https://www.w3.org/TR/2011/REC-SVG11-20110816/intro.html#NamespaceAndDTDIdentifiers>`_
            states that "It is not recommended that a DOCTYPE declaration be
            included in SVG documents.".

            We respect the W3C recommendation and don't include the `DOCTYPE` in
            the output SVG file.
        """
        width = int(width)
        height = int(height)

        if (width < 10 or width > 10000 or
            height < 10 or height > 10000):
            raise ValueError(
                'the width and height of the SVG image have to be integers '
                'in [10, 10000]'
            )

        self._recursively_compute_x_position(width)
        self._recursively_compute_y_position(height)

        with open(path, 'w') as SVG_file:
            header = (
                f'<?xml version="1.0" encoding="utf-8" standalone="no"?>\n\n'
                f'<svg width="{width}" height="{height}" '
                f'version="1.1" xmlns="http://www.w3.org/2000/svg">\n\n'
            )

            if gradient_color:
                defs = ('    <defs>\n'
                        '        <!-- linear gradient definitions -->\n' +
                        self._recursively_get_svg_gradient_color_defs()[0] +
                        '    </defs>\n\n')
            else:
                defs = ''

            title = (
                f'    <!-- image title -->\n'
                f'    <title>Tree graphic created with pytreesvg</title>\n\n'
            )

            if image_border:
                border = (
                    f'    <!-- image border -->\n'
                    f'    <rect x="0" y="0" width="{width}" height="{height}" '
                    f'style="stroke: #000000; fill: none;"/>\n\n'
                )
            else:
                border = ''

            corpse = self._recursively_get_svg_representation(gradient_color)

            backer = '</svg>\n'

            SVG_file.write(header + title + defs + border + corpse + backer)

    def _recursively_compute_y_position(self,
                                        svg_height: int,
                                        current_node_depth: int = 0,
                                        tree_depth: Optional[int] = None):
        """Recursively compute the `y` position of the node and its children
        in the SVG image.

        The function used to compute the :math:`y` position of a node at
        depth :math:`t` belonging to a tree of total depth :math:`T` in a SVG
        image of height :math:`h` is
        
        .. math::
            f : [0, T] & \\to     ]0, h[ \\\\
                t      & \\mapsto \\text{map}(t, -0.5, T + 0.5, 0, h)

        (see :func:`pytreesvg.tools.map`).

        Args:
            svg_height: Total height of the SVG image.
            current_node_depth: Depth of the current node in the tree.
            tree_depth: Total depth of the tree.
        """
        if not tree_depth:
            tree_depth = self.get_depth()

        self.y = map_value(
            current_node_depth,
            -0.5, tree_depth + 0.5,
            0, svg_height
        )

        for child in self.children:
            child._recursively_compute_y_position(
                svg_height,
                current_node_depth + 1,
                tree_depth
            )

    def _recursively_compute_x_position(self,
                                        parent_svg_width: float,
                                        level_svg_offset: float = 0.0,
                                        current_node_index: int = 0,
                                        nb_node_current_level: int = 1):
        """Recursively compute the `x` position of the node and its children
        in the SVG image.

        The function used to compute the :math:`x` position of a node at
        index :math:`i` belonging to a siblings group (later called a
        `level`) of :math:`n` nodes and a SVG parent node width of :math:`w`
        beginning at position :math:`x_p` is
        
        .. math::
            f : [0, n-1] & \\to     ]0, w[ \\\\
                i        & \\mapsto x_p + \\text{map}(i, -0.5, n - 0.5, 0, w)

        (see :func:`pytreesvg.tools.map`).

        Args:
            parent_svg_width: SVG width of the parent node.
            level_svg_offset: SVG x offset of the current level.
            current_node_index: Current node index in the current level.
            nb_node_current_level: Number of node in the current level.
        """
        self.x = level_svg_offset + map_value(
            current_node_index,
            -0.5, nb_node_current_level - 0.5,
            0, parent_svg_width
        )

        new_parent_svg_width = parent_svg_width / nb_node_current_level
        new_level_svg_offset = level_svg_offset + map_value(
            current_node_index - 1,
            -1, nb_node_current_level - 1,
            0, parent_svg_width
        )

        for i, child in enumerate(self.children):
            child._recursively_compute_x_position(
                parent_svg_width=new_parent_svg_width,
                level_svg_offset=new_level_svg_offset,
                current_node_index=i,
                nb_node_current_level=len(self.children)
            )

    def _recursively_get_svg_representation(self,
                                            gradient_color: bool,
                                            indentation: str = '    ') -> str:
        """Recursively get the SVG representation of the node and its children.

        Args:
            gradient_color: If some gradient colors have been defined in the
                SVG `defs` section (by using
                :meth:`_recursively_get_svg_gradient_color_defs` when
                creating the SVG image), set to ``True`` to use these colors
                for the edges.
            indentation: Spaces before the current node SVG string to
                distinguish children from parents.

        Returns:
            SVG representation of the node and its children.
        """
        current_node_svg_representation = (f'{indentation}<!-- Node '
                                           f'{self.value!r} -->\n')

        # draw node edges
        for child in self.children:
            if gradient_color:
                if self.style.color == child.style.color:
                    # no need for gradient color
                    color = self.style.color
                else:
                    # find the gradient color previously defined
                    color = (f'url(#grad_{self.style.get_color_id()}_'
                             f'{child.style.get_color_id()})')
            else:
                color = 'black'

            current_node_svg_representation += (
                f'{indentation}<line x1="{self.x}" y1="{self.y}" '
                f'x2="{child.x}" y2="{child.y}" '
                f'stroke="{color}" stroke-width="2"/> '
                f'<!-- edge to node {child.value!r} -->\n'
            )

        # draw node
        current_node_svg_representation += (
            f'{indentation}<circle cx="{self.x}" cy="{self.y}" '
            f'r="{self.style.size}" fill="{self.style.color}"/>\n\n'
        )

        children_svg_representation = ''

        for child in self.children:
            children_svg_representation += \
            child._recursively_get_svg_representation(
                gradient_color,
                indentation + '    '
            )

        return current_node_svg_representation + children_svg_representation

    def _recursively_get_svg_gradient_color_defs(
            self,
            created_gradient_list: Optional[List[str]] = None
    ) -> Tuple[str, List[str]]:
        """Recursively create all the necessary linear gradient color
        definitions.

        Args:
            created_gradient_list: List of gradient colors id already created.

        Returns:
            (gradient color definitions of the node and its children, already
            created gradient colors)
        """
        if not created_gradient_list:
            created_gradient_list = []

        self.svg_gradient = ''

        for child in self.children:
            gradient_id = (f'grad_{self.style.get_color_id()}_'
                           f'{child.style.get_color_id()}')

            if (self.style.color != child.style.color and
                gradient_id not in created_gradient_list):
                self.svg_gradient += (
                    f'        <linearGradient id="{gradient_id}" x1="0%" x2="0%" y1="0%" y2="100%">\n'
                    f'           <stop offset="0%" stop-color="{self.style.color}"/>\n'
                    f'           <stop offset="100%" stop-color="{child.style.color}"/>\n'
                    f'        </linearGradient>\n')
                created_gradient_list.append(gradient_id)
                (child_gradient, created_gradient_list) = \
                    child._recursively_get_svg_gradient_color_defs(
                        created_gradient_list
                    )
                self.svg_gradient += child_gradient

        return self.svg_gradient, created_gradient_list
