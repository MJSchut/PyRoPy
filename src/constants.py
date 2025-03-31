from src.util.config_loader import ConfigLoader

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
PANEL_Y = 0  # Position panel at the top
PANEL_FG = (255, 255, 255)  # White text
PANEL_BG = (0, 0, 0)  # Black background
panel = tcod.console.Console(PANEL_WIDTH, SCREEN_HEIGHT, order="F")
panel.clear(fg=PANEL_FG, bg=PANEL_BG)  # Clear with background color
MSG_Y = BAR_WIDTH + 3
MSG_WIDTH = PANEL_WIDTH - 1
MSG_HEIGHT = 20

INVENTORY_WIDTH = MSG_WIDTH

appearance_potion_dictionary = {}
player_name = 'Steve'

# Load colors from config
config_loader = ConfigLoader()
colors = {
    "floor_color": config_loader.get_color("floor_color"),
    "floor_color_front": config_loader.get_color("floor_color_front"),
    "wall_color": config_loader.get_color("wall_color"),
    "wall_color_front": config_loader.get_color("wall_color_front"),
    "darkness_color": config_loader.get_color("darkness_color"),
}

chars = {
    "floor_char": '.',
    "wall_char": '#',  # Wall character
    "darkness_char": ' ',  # Empty space for darkness
    "window_char": '-'  # Horizontal line
}

item_color_pointers = {
    'red': config_loader.get_color("red"),
    'purple': config_loader.get_color("purple"),
    'green': config_loader.get_color("green"),
    'blue': config_loader.get_color("blue"),
    'yellow': config_loader.get_color("yellow"),
    'white': config_loader.get_color("white"),
    'black': config_loader.get_color("black"),
    'gray': config_loader.get_color("gray"),
    'orange': config_loader.get_color("orange"),
    'brown': config_loader.get_color("brown"),
    'pink': config_loader.get_color("pink"),
    'cyan': config_loader.get_color("cyan"),
    'magenta': config_loader.get_color("magenta"),
    'lime': config_loader.get_color("lime"),
    'maroon': config_loader.get_color("maroon"),
    'navy': config_loader.get_color("navy"),
    'olive': config_loader.get_color("olive"),
    'teal': config_loader.get_color("teal"),
    'aqua': config_loader.get_color("aqua"),
    'fuchsia': config_loader.get_color("fuchsia"),
    'silver': config_loader.get_color("silver"),
    'gold': config_loader.get_color("gold"),
    'beige': config_loader.get_color("beige"),
    'ivory': config_loader.get_color("ivory"),
    'lavender': config_loader.get_color("lavender"),
    'linen': config_loader.get_color("linen"),
    'moccasin': config_loader.get_color("moccasin"),
    'oldlace': config_loader.get_color("oldlace"),
    'papayawhip': config_loader.get_color("papayawhip"),
    'seashell': config_loader.get_color("seashell"),
    'mintcream': config_loader.get_color("mintcream"),
    'slategray': config_loader.get_color("slategray"),
    'snow': config_loader.get_color("snow"),
    'springgreen': config_loader.get_color("springgreen"),
    'steelblue': config_loader.get_color("steelblue"),
    'tan': config_loader.get_color("tan"),
    'thistle': config_loader.get_color("thistle"),
    'tomato': config_loader.get_color("tomato"),
    'turquoise': config_loader.get_color("turquoise"),
    'violet': config_loader.get_color("violet"),
    'wheat': config_loader.get_color("wheat"),
    'whitesmoke': config_loader.get_color("whitesmoke"),
    'yellowgreen': config_loader.get_color("yellowgreen"),
    'rebeccapurple': config_loader.get_color("rebeccapurple"),
    'amber': config_loader.get_color("amber")
}

item_colors = [
    'red',
    'purple',
    'cyan',
    'blue',
    'turquoise',
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


