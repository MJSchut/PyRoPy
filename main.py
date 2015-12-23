__author__ = 'Martijn Schut'

from src.creatures.Player import Player

from src.libtcod import libtcodpy as lbt

from src.input import keyboard as kb

from src import constants

lbt.console_set_custom_font('assets/terminal12x12_gs_ro.png', lbt.FONT_TYPE_GREYSCALE | lbt.FONT_LAYOUT_ASCII_INROW)
lbt.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 'PyRoPy', False)
lbt.sys_set_fps(constants.LIMIT_FPS)

player = Player(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)

while not lbt.console_is_window_closed():
    key = lbt.console_wait_for_keypress(True)

    lbt.console_set_default_foreground(0, lbt.white)
    lbt.console_put_char(0, player.player_x, player.player_y, '@', lbt.BKGND_NONE)
    lbt.console_flush()
    lbt.console_put_char(0, player.player_x, player.player_y, ' ', lbt.BKGND_NONE)

    #handle keys and exit game if needed
    keylist = kb.handle_keys(lbt, key)
    kb.process_keylist(lbt, keylist, player)

