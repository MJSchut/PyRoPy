__author__ = 'Martijn Schut'

from src.libtcod import libtcodpy as lbt

import random

SCREEN_WIDTH = 60
SCREEN_HEIGHT = 40
MAP_WIDTH = 80
MAP_HEIGHT = 60
LIMIT_FPS = 30

player_name = 'Steve'

colors = {
    "floor_color" : lbt.Color(30, 30, 30),
    "floor_color_front" : lbt.Color(40, 40, 40),
    "wall_color" : lbt.Color(50, 50, 50),
    "wall_color_front" : lbt.Color(150, 110, 110),
    "darkness_color" : lbt.Color(0, 0, 0),
}

chars = {
    "floor_char" : '.',
    "wall_char" : lbt.CHAR_BLOCK1,
    "darkness_char" : lbt.CHAR_BLOCK2
}

def random_name():
    name_list = [
        'Bob',
        'Bianca',
        'Dave',
        'Danny',
        'Joe',
        'Joelle',
        'Joey',
        'Manfred',
        'Milfred',
        'Sally',
        'Steve'
        ]

    return random.choice(name_list)


