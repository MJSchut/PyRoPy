__author__ = 'Martijn Schut'

def handle_keys(lbt, key):
    keylist = []

    if key.vk == lbt.KEY_ENTER and key.lalt:
        keylist.append('fscreen')

    elif key.vk == lbt.KEY_ESCAPE:
        keylist.append('exit')

    if lbt.console_is_key_pressed(lbt.KEY_UP):
        keylist.append('up')

    elif lbt.console_is_key_pressed(lbt.KEY_DOWN):
        keylist.append('down')

    elif lbt.console_is_key_pressed(lbt.KEY_LEFT):
        keylist.append('left')

    elif lbt.console_is_key_pressed(lbt.KEY_RIGHT):
        keylist.append('right')

    if lbt.console_is_key_pressed(lbt.KEY_ENTER):
        keylist.append('enter')


    return keylist

def process_keylist(lbt, keylist, player):
    if not keylist:
        return
    if keylist[0] == 'left':
        player.move(-1, 0)
    if keylist[0] == 'right':
        player.move(1, 0)
    if keylist[0] == 'down':
        player.move(0, 1)
    if keylist[0] == 'up':
        player.move(0, -1)