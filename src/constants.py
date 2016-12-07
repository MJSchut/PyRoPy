__author__ = 'Martijn Schut'

import libtcodpy as lbt
from src.effects.Effects import *

import random

SCREEN_WIDTH = 88
SCREEN_HEIGHT = 50
MAP_WIDTH = 180
MAP_HEIGHT = 150
LIMIT_FPS = 30
DEBUG = 1

BAR_WIDTH = 20
PANEL_WIDTH = 30
PANEL_HEIGHT = SCREEN_HEIGHT
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
panel = lbt.console_new(PANEL_WIDTH, SCREEN_HEIGHT)

MSG_Y = BAR_WIDTH + 3
MSG_WIDTH = PANEL_WIDTH - 1
MSG_HEIGHT = 20

INVENTORY_WIDTH = MSG_WIDTH

appearance_potion_dictionary = {}
player_name = 'Steve'

colors = {
    "floor_color" : lbt.Color(30, 30, 30),
    "floor_color_front" : lbt.Color(40, 40, 40),
    "wall_color" : lbt.Color(50, 50, 50),
    "wall_color_front" : lbt.Color(150, 110, 110),
    "darkness_color" : lbt.Color(10, 10, 10),
}

chars = {
    "floor_char" : '.',
    "wall_char" : lbt.CHAR_BLOCK1,
    "darkness_char" : lbt.CHAR_BLOCK2,
    "window_char" : lbt.CHAR_HLINE
}

item_color_pointers = {
    'red' : lbt.red,
    'purple' : lbt.purple,
    'cyan' : lbt.dark_cyan,
    'blue' : lbt.dark_azure,
    'turqoise' : lbt.turquoise,
    'green' : lbt.green,
    'yellow' : lbt.dark_yellow,
    'amber' : lbt.amber,
    'orange' : lbt.orange,
    'pink' : lbt.dark_pink
}

item_colors = [
    'red',
    'purple',
    'cyan',
    'blue',
    'turqoise',
    'green',
    'yellow',
    'amber',
    'orange',
    'pink'
]
item_adjective = [
    'swirling',
    'bubbling',
    'clear',
    'muddy',
    'murky',
    'watery',
    'slimy',
    'foul-smelling',
    'rancid',
    'radiant',
    'fizzy'
]

effect_noun = {
    PoisonEffect : "poison",
    MinorHealEffect : "minor healing"
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

def debug_msg(message):
    if DEBUG == 1:
        print message


