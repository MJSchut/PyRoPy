__author__ = 'Martijn Schut'

from src.entities.Creatures.Player import Player
from src.entities.Creatures.Creature import Creature

from src.libtcod import libtcodpy as lbt

from src.input import keyboard as kb

from src import constants

import random

# basic libtcod initialization
lbt.console_set_custom_font('assets/terminal12x12_gs_ro.png', lbt.FONT_TYPE_GREYSCALE | lbt.FONT_LAYOUT_ASCII_INROW)
lbt.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 'PyRoPy', False)
lbt.sys_set_fps(constants.LIMIT_FPS)
con = lbt.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
lbt.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)
lbt.console_set_default_foreground(0, lbt.white)

# make a creature list, a bit unrefined for now, and add some creatures to it
creatures = []

# add the player
player = Player(lbt, con, constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
creatures.append(player)

# add some non-hostile creatures
funguscount = 10
for funi in range(0, funguscount):
    fungus = Creature(lbt, con, constants.SCREEN_WIDTH/2 + random.randint(-10, 10), constants.SCREEN_HEIGHT/2 - + random.randint(-20, 20), 'f', lbt.green)
    creatures.append(fungus)

while not lbt.console_is_window_closed():
    # show stuff
    # player gets added to list first, but should be drawn last (over top of everything)
    for creature in reversed(creatures):
        creature.draw()

    lbt.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)
    lbt.console_flush()

    for creature in creatures:
        creature.clear()


    # get input
    key = lbt.console_wait_for_keypress(True)

    # respond to input
    keylist = kb.handle_keys(lbt, key)
    kb.process_keylist(lbt, keylist, player)

