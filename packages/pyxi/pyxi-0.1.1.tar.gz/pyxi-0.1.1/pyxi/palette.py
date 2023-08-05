from typing import Any, Dict


class Palette:
    """
    Represents the palette used in the :class:`PyxelImage`.

    Attributes
        :width: Number of columns in the palette..
        :height: Number of rows in the palette.
        :color_count: Number of unique colors in the palette.
        :colors: A dictionary containing an index key and hexadecimal value of each color. Value can be `None`.
    """

    __slots__ = ('width', 'height', 'color_count', 'colors')

    def __init__(self, data: Dict[str, Any]):
        self.width = data['width']
        self.height = data['height']
        self.color_count = data['numColors']
        self.colors = {k: v for k, v in data['colors'].items()}
