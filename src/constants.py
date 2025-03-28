__author__ = 'Martijn Schut'

import tcod
from tcod import libtcodpy
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
panel = tcod.console.Console(PANEL_WIDTH, SCREEN_HEIGHT, order="F")

MSG_Y = BAR_WIDTH + 3
MSG_WIDTH = PANEL_WIDTH - 1
MSG_HEIGHT = 20

INVENTORY_WIDTH = MSG_WIDTH

appearance_potion_dictionary = {}
player_name = 'Steve'

colors = {
    "floor_color": (30, 30, 30),
    "floor_color_front": (40, 40, 40),
    "wall_color": (50, 50, 50),
    "wall_color_front": (150, 110, 110),
    "darkness_color": (10, 10, 10),
}

chars = {
    "floor_char": '.',
    "wall_char": '#',  # Wall character
    "darkness_char": ' ',  # Empty space for darkness
    "window_char": '-'  # Horizontal line
}

item_color_pointers = {
    'red': (255, 0, 0),
    'purple': (191, 0, 255),
    'cyan': (0, 191, 191),
    'blue': (0, 95, 191),
    'turqoise': (0, 255, 191),
    'green': (0, 255, 0),
    'yellow': (191, 191, 0),
    'amber': (255, 191, 0),
    'orange': (255, 127, 0),
    'pink': (191, 0, 95)
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
    PoisonEffect: "poison",
    MinorHealEffect: "minor healing"
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
        print(message)


