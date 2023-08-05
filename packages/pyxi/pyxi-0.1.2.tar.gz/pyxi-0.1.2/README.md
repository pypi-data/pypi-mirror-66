# Pyxi
[![PyPI version](https://badge.fury.io/py/pyxi.svg)](https://badge.fury.io/py/pyxi) [![Documentation Status](https://readthedocs.org/projects/pyxi/badge/?version=latest)](https://pyxi.readthedocs.io/en/latest/?badge=latest)

`pyxi` is a small library for interfacing with PyxelEdit `.pyxel` files in an object-oriented manner.
Currently it is extremely barebones, only letting you access all the values of your `.pyxel` files and loading a 
`PIL.Image.Image` object from a single tile. In the future, it should allow you to programatically modify image
values, save files, and handle export/import needs; both single file and large tilesets.

### Example
Loading a `.pyxel` file as a texture in `arcade`.
```python
from pyxi import image

p = image.PyxelImage('assets/wizard.pyxel')
texture = p.get_tile()  # returns a Pillow Image object
player = arcade.Sprite(scale=4)
player.texture = arcade.Texture(name='S8dhS7dja', image=texture)
```
