from typing import Any, Dict


class Tileset:
    """
    Represents the tileset used in the :class:`PyxelImage`.

    Attributes
        :fixed_width: Whether the tileset has a fixed width or not.
        :tile_width: Width in pixels of each tile.
        :tile_height: Height in pixels of each tile.
        :tile_count: Number of individual tiles in the image.
        :columns: Number of columns in the tileset.
    """

    __slots__ = ('fixed_width', 'tile_width', 'tile_height', 'tile_count', 'columns')

    def __init__(self, data: Dict[str, Any]):
        self.fixed_width = data['fixedWidth']
        self.tile_width = data['tileWidth']
        self.tile_height = data['tileHeight']
        self.tile_count = data['numTiles']
        self.columns = data['tilesWide']
