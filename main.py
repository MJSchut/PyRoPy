__author__ = 'Martijn Schut'

from src.entities.Creatures.CreatureFactory import CreatureFactory
from src.world.Level import Level

from src.libtcod import libtcodpy as lbt

from src.input import keyboard as kb

from src import constants

import random


def getScrollX():
    return max(0, min(player.x - constants.SCREEN_WIDTH / 2, level.level_width - constants.SCREEN_WIDTH))

def getScrollY():
    # adjust for size of the panel
    return max(0, min(player.y - constants.SCREEN_HEIGHT / 2, level.level_height - constants.SCREEN_HEIGHT + constants.PANEL_HEIGHT))

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # M: I really liked this code, so I kept it the way it is.
    #render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    #render the background first
    lbt.console_set_default_background(constants.panel, back_color)
    lbt.console_rect(constants.panel, x, y, total_width, 1, False, lbt.BKGND_SCREEN)

    #now render the bar on top
    lbt.console_set_default_background(constants.panel, bar_color)
    if bar_width > 0:
        lbt.console_rect(constants.panel, x, y, bar_width, 1, False, lbt.BKGND_SCREEN)

    #finally, some centered text with the values
    lbt.console_set_default_foreground(constants.panel, lbt.white)
    lbt.console_print_ex(constants.panel, x + total_width / 2, y, lbt.BKGND_NONE, lbt.CENTER,
        name + ': ' + str(value) + '/' + str(maximum))


# basic libtcod initialization
lbt.console_set_custom_font('assets/terminal12x12_gs_ro.png', lbt.FONT_TYPE_GREYSCALE | lbt.FONT_LAYOUT_ASCII_INROW)
lbt.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 'PyRoPy', False)
lbt.sys_set_fps(constants.LIMIT_FPS)
con = lbt.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
lbt.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)
lbt.console_set_default_foreground(0, lbt.white)

msg_panel = lbt.console_new(constants.SCREEN_WIDTH, 8)

level = Level(constants.MAP_WIDTH, constants.MAP_HEIGHT)
cFactory = CreatureFactory(lbt, con, level)

# add the player
messages = []
player = cFactory.make_player(messages)

# add some non-hostile creatures
funguscount = 10
for funi in range(0, funguscount):
    fungus = cFactory.make_fungus()

batcount = 20
for bati in range(0, batcount):
    bat = cFactory.make_bat()

while not lbt.console_is_window_closed():
    # show stuff
    sx = getScrollX()
    sy = getScrollY()

    for y in range(level.level_height):
        for x in range(level.level_width):
            wx = x - sx
            wy = y - sy

            if 0 <= wx <= constants.SCREEN_WIDTH and 0 <= wy <= constants.SCREEN_HEIGHT:

                lbt.console_set_char_background(con, wx, wy, level.map[x][y].color, lbt.BKGND_SET )

                if level.map[x][y].char is not None:
                    if level.map[x][y].front_color is not None:
                        lbt.console_set_default_foreground(con, level.map[x][y].front_color)
                    else:
                        lbt.console_set_default_foreground(con, lbt.white)

                    lbt.console_put_char(con, wx, wy, level.map[x][y].char, lbt.BKGND_NONE)


    # player gets added to list first, but should be drawn last (over top of everything)
    for creature in reversed(level.creatures):
        wx = creature.x - sx
        wy = creature.y - sy
        creature.draw(wx, wy)

    lbt.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

    #prepare to render the GUI panel
    lbt.console_set_default_background(constants.panel, lbt.black)
    lbt.console_clear(constants.panel)

    #show the player's stats
    render_bar(1, 1, constants.BAR_WIDTH, 'HP', player.hp, player.maxhp,
        lbt.light_red, lbt.darker_red)

    # show message log
    y = 1
    for line in messages:
        lbt.console_set_default_foreground(constants.panel, lbt.white)
        lbt.console_print_ex(constants.panel, constants.MSG_X, y, lbt.BKGND_NONE, lbt.LEFT, line)
        y += 1

    #blit the contents of "panel" to the root console
    lbt.console_blit(constants.panel, 0, 0, constants.SCREEN_WIDTH, constants.PANEL_HEIGHT, 0, 0, constants.PANEL_Y)

    lbt.console_flush()

    for creature in level.creatures:
        creature.clear()

    # get input
    key = lbt.console_wait_for_keypress(True)

    # respond to input
    keylist = kb.handle_keys(lbt, key)
    kb.process_keylist(lbt, keylist, player)

    # creature turn
    level.update()

