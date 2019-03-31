import re


class NodeStyle:
    """This class defines a node style by detailing its SVG characteristics.

    Each node SVG style is defined by a short string representation of the
    form ``'<node color>@<node size>'`` like  ``'green@12'``,
    ``'#aa8ef7@3'``, ``'#f00@38'``, ``'rgb(122,17,234)@7'``, ``'rgb(23%,5%,
    100%)@10'``, ...

    Attributes:
        color: Background color of the node circle, see **Notes** under.
        size: Radius of the node circle in pixel, has to be an integer in
            [0, 100].

    Notes:
        To respect the
        `W3C SVG 1.1 (Second Edition) Recommendation - Section 4.2 <https://www.w3.org/TR/2011/REC-SVG11-20110816/types.html#BasicDataTypes>`_
        , the following color notations are allowed:

        - base color: ``aliceblue``, ``darkturquoise``, ``lightcoral``, ... (see
          `W3C SVG 1.1 (Second Edition) Recommendation - Section 4.4 <https://www.w3.org/TR/2011/REC-SVG11-20110816/types.html#ColorKeywords>`_
          )
        - hexadecimal notation (short or long): ``#aa8ef7``, ``#F7AA9E``,
          ``#f00``, ``#FFF``, ...
        - rgb notation (value or percentage): ``rgb(122,17,234)``, ``rGb(13, 0,
          137)``, ``rgb(23%,5%,100%)``, ``RGB(23 %, 5 %, 100 %)``, ...
    """

    def __init__(self, representation: str = 'blue@12'):
        """Create a ``NodeStyle`` object.

        Args:
            representation: Short representation of the node style.

        Raises:
            ValueError: If the given representation is incorrect (i.e. the
            representation syntax is invalid or the color or the size don't
            respect the requirements described above).

        Examples:
            >>> NodeStyle('green@12')
            <NodeStyle: color='green', size=12>
            >>> NodeStyle('#aa8ef7@3')
            <NodeStyle: color='#aa8ef7', size=3>
            >>> NodeStyle('rgb(122,17,234)@62')
            <NodeStyle: color='rgb(122,17,234)', size=62>
            >>> NodeStyle('bug_color@62')
            Traceback (most recent call last):
            ...
            ValueError: incorrect color (ex: 'green', '#aa8ef7', '#f00',
            'rgb(122,17,234)', 'rgb(23%,5%,100%)', ...)
        """
        if not re.search(r'^.+@[0-9]+$', representation):
            raise ValueError(
                "incorrect SVG node style representation (ex: 'green@12', "
                "'#aa8ef7@3', '#f00@38', 'rgb(122,17,234)@7', 'rgb(23%,5%,"
                "100%)@10', ..."
            )

        # we need to remove extra ''
        # see https://docs.python.org/2/library/re.html#re.split
        chuncks = [s for s in re.split(r'@', representation) if s != '']

        self.color = NodeStyle._get_valid_color(chuncks[0])
        self.size = NodeStyle._get_valid_size(chuncks[1])

    @staticmethod
    def _get_valid_color(color: str) -> str:
        """Return a valid SVG color or raise an error.

        Args:
            color: Color string.

        Raises:
            ValueError: If the given color doesn't match the SVG colors
            requirements described above.
        """
        # see https://www.w3.org/TR/2011/REC-SVG11-20110816/types.html#ColorKeywords
        base_color_list = [
            'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
            'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
            'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse',
            'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson',
            'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray',
            'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta',
            'darkolivegreen', 'darkorange', 'darkorchid', 'darkred',
            'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
            'darkslategrey', 'darkturquoise',
            'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey',
            'dodgerblue', 'firebrick', 'floralwhite',
            'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold',
            'goldenrod', 'gray', 'grey', 'green',
            'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
            'ivory', 'khaki', 'lavender', 'lavenderblush',
            'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
            'lightgoldenrodyellow', 'lightgray',
            'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon',
            'lightseagreen', 'lightskyblue', 'lightslategray',
            'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime',
            'limegreen', 'linen', 'magenta', 'maroon',
            'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple',
            'mediumseagreen', 'mediumslateblue',
            'mediumspringgreen', 'mediumturquoise', 'mediumvioletred',
            'midnightblue', 'mintcream', 'mistyrose',
            'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab',
            'orange', 'orangered', 'orchid',
            'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred',
            'papayawhip', 'peachpuff', 'peru', 'pink',
            'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue',
            'saddlebrown', 'salmon', 'sandybrown',
            'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
            'slategray', 'slategrey', 'snow',
            'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
            'turquoise', 'violet', 'wheat', 'white',
            'whitesmoke', 'yellow', 'yellowgreen'
        ]

        # match one or two groups of 3 alphanumeric characters ('#aa8ef7',
        # '#F7AA9E', '#f00', '#FFF', ...)
        hexadec_notation_regex = re.compile(
            r'^#([a-f0-9]{3}){1,2}$',
            re.IGNORECASE
        )

        # match colors like 'rgb(122,17,234)', 'rGb(122,17,234)', 'rgb( 122,
        # 17, 234 )', ...
        rgb_notation_val_regex = re.compile(
            r'^rgb\(\s?[0-9]{1,3}\s?(,\s?[0-9]{1,3}\s?){2}\)',
            re.IGNORECASE
        )

        # match colors like 'rgb(23%,5%,100%)', 'rGb(23%,5%,100%)',
        # 'rgb( 23%, 5 %, 100% )', ...
        rgb_notation_per_regex = re.compile(
            r'^rgb\(\s?[0-9]{1,3}\s?%\s?(,\s?[0-9]{1,3}\s?%\s?){2}\)$',
            re.IGNORECASE
        )

        if (color not in base_color_list and
                not hexadec_notation_regex.search(color) and
                not rgb_notation_val_regex.search(color) and
                not rgb_notation_per_regex.search(color)
        ):
            raise ValueError(
                "incorrect color (ex: 'green', '#aa8ef7', '#f00', 'rgb(122,"
                "17,234)', 'rgb(23%,5%,100%)', ...)"
            )

        return color

    @staticmethod
    def _get_valid_size(size: str) -> int:
        """Return a valid size in [0, 100] or raise an error.

        Args:
            size: Size string.

        Raises:
            ValueError: If the given size is not in [0, 100].
        """
        size = int(size)

        if size < 0 or size > 100:
            raise ValueError('the size has to be an integer in [0, 100]')

        return size

    def __repr__(self) -> str:
        """Return a string detailing the node style SVG characteristics."""
        return f'<NodeStyle: color={self.color!r}, size={self.size}>'

    def __str__(self) -> str:
        """Return a string representing the style."""
        return f'{self.color}@{self.size}'

    def get_color_id(self) -> str:
        """Return a string representing the color with a unique id that
        respects the SVG recommendation.

        Notes:
            The
            `W3C SVG 1.1 (Second Edition) Recommendation - Section 5.10.1 <https://www.w3.org/TR/2011/REC-SVG11-20110816/struct.html#Core.attrib>`_
            states that one should refer to the
            `W3C XML 1.0 (Fifth Edition) Recommendation - Section 3.3.1 <https://www.w3.org/TR/2008/REC-xml-20081126/#sec-attribute-types>`_
            when specifying the ``id`` attribute of an object. This last document
            specifies that the possible names are defined in the
            `W3C XML 1.0 (Fifth Edition) Recommendation - Section 2.3 <https://www.w3.org/TR/2008/REC-xml-20081126/#NT-Name>`_
            .

            This function returns an arbitrarily modified color name specifically
            built to respect this convention.

        Examples:
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

        # remove '#', ')' and whitespace characters
        color_id = re.sub(r'#|\)|\s', '', color_id)
        color_id = re.sub(r'\(|,', '.', color_id)  # replace '(' and ',' by '.'
        color_id = re.sub(r'%', 'p', color_id)  # replace '%' by 'p'

        return color_id