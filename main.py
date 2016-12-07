__author__ = 'Martijn Schut'

from src.entities.creatures.CreatureFactory import CreatureFactory
from src.world.Level import Level
from src.entities.items.ItemFactory import ItemFactory

import libtcodpy as lbt

from src.input import keyboard as kb

from src import constants

import random
import textwrap

def getScrollX():
    return max(0, min(player.x - constants.SCREEN_WIDTH / 2 - constants.PANEL_WIDTH/2, level.level_width - constants.SCREEN_WIDTH - constants.PANEL_WIDTH/2.5))

def getScrollY():
    # adjust for size of the panel
    return max(0, min(player.y - constants.SCREEN_HEIGHT / 2, level.level_height - constants.SCREEN_HEIGHT))

def render_bar(x, y, total_width, value, maximum, name, bar_color, back_color, text_color = lbt.white, show_exact = False ):
    # M: I really liked this code, so I kept it pretty much the way it is.

    #now render the bar on top
    if show_exact:
        bar_width = int(float(value) / maximum * total_width)
        lbt.console_set_default_background(constants.panel, back_color)
        lbt.console_rect(constants.panel, x, y, total_width, 1, False, lbt.BKGND_SCREEN)
        lbt.console_set_default_background(constants.panel, bar_color)
        if bar_width > 0:
            lbt.console_rect(constants.panel, x, y, bar_width, 1, False, lbt.BKGND_SCREEN)
    else:
        bar_width = int(float(value) / maximum * (total_width - 8))
        lbt.console_set_default_background(constants.panel, back_color)
        lbt.console_rect(constants.panel, x + 8, y, total_width - 8, 1, False, lbt.BKGND_SCREEN)
        lbt.console_set_default_background(constants.panel, bar_color)
        if bar_width > 0:
            lbt.console_rect(constants.panel, x + 8, y, bar_width, 1, False, lbt.BKGND_SCREEN)

    #finally, some centered text with the values
    if show_exact:
        lbt.console_set_default_foreground(constants.panel, text_color)
        lbt.console_print_ex(constants.panel, x + total_width / 2, y, lbt.BKGND_NONE, lbt.CENTER,
            name + ': ' + str(value) + '/' + str(maximum))
    else:
        lbt.console_set_default_foreground(constants.panel, text_color)
        lbt.console_print_ex(constants.panel, total_width - 15 - x, y, lbt.BKGND_NONE, lbt.CENTER,
            name + ':')

def render_status(x, y, name, value, text_color = lbt.grey):
    lbt.console_set_default_foreground(constants.panel, text_color)

    lbt.console_print_ex(constants.panel, x + (len(name) - 2) + len(value)/2, y, lbt.BKGND_NONE, lbt.CENTER,
            '%s: %s' %(name, value))

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
iFactory = ItemFactory(lbt, con, level)

# add the player
messages = [[], []]
linecolors = []
for i in range(255, 15, -8):
    linecolors.append(lbt.Color(i,i,i))
all_messages = []
player = cFactory.make_player(messages)

# add some hostile and less hostile creatures & items
funguscount = 10
for funi in range(0, funguscount):
    fungus = cFactory.make_fungus()

batcount = 5
for bati in range(0, batcount):
    bat = cFactory.make_bat()

snakecount = 5
for snakei in range(0, snakecount):
    snake = cFactory.make_snake()

gargoylecount = 5
for gargi in range(0, gargoylecount):
    gargoyle = cFactory.make_gargoyle(player)

rockcount = 25
for rocki in range(0, rockcount):
    rock = iFactory.make_rock()

swordcount = 3
for swordi in range(0, swordcount):
    sword = iFactory.make_sword()

glovecount = 2
for glovei in range(0, glovecount):
    glove = iFactory.make_gauntlet()

potions = 15
for potioni in range(0, potions):
    potion = iFactory.make_random_potion()

necklacecount = 2
for necklacei in range(0, necklacecount):
    necklace = iFactory.make_amulet()

fedoracount = 2
for i in range(0, fedoracount):
    fedora = iFactory.make_fedora()

# main loop
# the draw loop is a bit insane right now, gonna fix that
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
                    if level.map[x][y].front_color is not None and player.can_see(x, y):
                        level.map[x][y].identified = 1
                        lbt.console_set_default_foreground(con, level.map[x][y].front_color)
                        lbt.console_put_char(con, wx, wy, level.map[x][y].char, lbt.BKGND_NONE)
                    elif player.can_see(x, y):
                        level.map[x][y].identified = 1
                        lbt.console_set_default_foreground(con, lbt.white)
                        lbt.console_put_char(con, wx, wy, level.map[x][y].char, lbt.BKGND_NONE)
                    elif level.map[x][y].identified == 1:
                        lbt.console_set_default_foreground(con, constants.colors['darkness_color'])
                        lbt.console_put_char(con, wx, wy, level.map[x][y].char, lbt.BKGND_NONE)
                    else:
                        lbt.console_set_default_foreground(con, constants.colors['darkness_color'])
                        lbt.console_set_char_background(con, wx, wy, constants.colors['darkness_color'], lbt.BKGND_SET )
                        lbt.console_put_char(con, wx, wy, constants.chars['darkness_char'], lbt.BKGND_NONE)

    for item in level.items:
        if player.can_see(item.x, item.y):
            wx = item.x - sx
            wy = item.y - sy
            item.draw(wx, wy)

    # player gets added to list first, but should be drawn last (over top of everything)
    # creatures get drawn over top of items
    for creature in reversed(level.creatures):
        if player.can_see(creature.x, creature.y):
            wx = creature.x - sx
            wy = creature.y - sy
            creature.draw(wx, wy)

    lbt.console_blit(con, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

    #prepare to render the bottom panel
    lbt.console_set_default_background(constants.panel, lbt.black)
    lbt.console_clear(constants.panel)

    #show the player's stats
    htext_color = lbt.grey
    if float(player.hp) / player.maxhp < 0.3:
        htext_color = lbt.white
    render_bar(1, 1, constants.BAR_WIDTH, player.hp, player.maxhp, 'Health',
               lbt.light_red, lbt.darker_red, text_color=htext_color)

    # show hunger
    hutext_color = lbt.grey
    if (float(player.hunger) / player.maxhunger) < 0.1:
        hutext_color = lbt.red
    elif (float(player.hunger) / player.maxhunger) < 0.3:
        hutext_color = lbt.white

    render_status(1, 3, 'Hunger', player.hunger_value, text_color=hutext_color)

    # show thirst (unimplemented)
    hutext_color = lbt.grey
    render_status(1, 5, 'Thirst', " ", text_color=hutext_color)

    # show message log

    y = constants.MSG_Y - 1
    for x in range(0, constants.MSG_WIDTH + 1):
        lbt.console_put_char(constants.panel, x, y, constants.chars['window_char'])
    lbt.console_rect(constants.panel, 1, y, 10, 10, False)

    y += 1
    for i in range(len(messages[0]) -1, 0, -1):
        line = messages[0][i]
        colorindex = messages[1][i]
        lbt.console_set_default_foreground(constants.panel, linecolors[colorindex])
        message = textwrap.wrap(line, width = constants.MSG_WIDTH)
        for lines in message:
            lbt.console_print_ex(constants.panel, 1, y, lbt.BKGND_NONE, lbt.LEFT, lines)
            y += 1

        if colorindex < len(linecolors) - 1:
            colorindex += 1

        messages[1][i] = colorindex

    if len(messages[0]) >= constants.MSG_HEIGHT:
        del messages[0][0]
        del messages[1][0]

        #if messages[1][i] >= len(linecolors) - 1:
        #    del messages[0][0]
        #    del messages[1][0]

    #blit the contents of "panel" to the root console
    lbt.console_blit(constants.panel, 0, 0, constants.SCREEN_WIDTH, constants.PANEL_HEIGHT, 0, 0, constants.PANEL_Y)

    lbt.console_flush()

    for creature in level.creatures:
        creature.clear()

    # get input
    key = []
    keylist = []

    while len(keylist) is 0:
        key = lbt.console_wait_for_keypress(True)
        keylist = kb.handle_keys(lbt, key)

    constants.debug_msg('Pressed key %s' %keylist[0])

    # respond to input
    lbt.console_set_default_background(con, lbt.black)
    kb.process_keylist(lbt, keylist, player)
    if keylist[0] == 'exit':
        break

    # npc turn
    level.update()

