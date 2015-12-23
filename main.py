__author__ = 'Martijn Schut'

from src.libtcod import libtcodpy as lbt

from src import constants

lbt.console_set_custom_font('assets/terminal12x12_gs_ro.png', lbt.FONT_TYPE_GREYSCALE | lbt.FONT_LAYOUT_ASCII_INROW)
lbt.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 'PyRoPy', False)
lbt.sys_set_fps(constants.LIMIT_FPS)

playerx = constants.SCREEN_WIDTH/2
playery = constants.SCREEN_HEIGHT/2

def handle_keys():
    global playerx, playery

    key = lbt.console_wait_for_keypress(True)

    if key.vk == lbt.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        lbt.console_set_fullscreen(not lbt.console_is_fullscreen())

    elif key.vk == lbt.KEY_ESCAPE:
        return True  #exit game

    #movement keys
    if lbt.console_is_key_pressed(lbt.KEY_UP):
        playery -= 1

    elif lbt.console_is_key_pressed(lbt.KEY_DOWN):
        playery += 1

    elif lbt.console_is_key_pressed(lbt.KEY_LEFT):
        playerx -= 1

    elif lbt.console_is_key_pressed(lbt.KEY_RIGHT):
        playerx += 1

while not lbt.console_is_window_closed():
    lbt.console_set_default_foreground(0, lbt.white)
    lbt.console_put_char(0, playerx, playery, '@', lbt.BKGND_NONE)
    lbt.console_flush()
    lbt.console_put_char(0, playerx, playery, ' ', lbt.BKGND_NONE)

    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break