__author__ = 'Martijn Schut'

def handle_keys(lbt, key):
    keylist = []

    key_char = chr(key.c)

    if lbt.console_is_key_pressed(lbt.KEY_ESCAPE):
        keylist.append('exit')

    if lbt.console_is_key_pressed(lbt.KEY_UP) or key_char == '8':
        keylist.append('up')

    elif lbt.console_is_key_pressed(lbt.KEY_DOWN) or key_char == '2':
        keylist.append('down')

    elif lbt.console_is_key_pressed(lbt.KEY_LEFT) or key_char == '4':
        keylist.append('left')

    elif lbt.console_is_key_pressed(lbt.KEY_RIGHT) or key_char == '6':
        keylist.append('right')

    elif key_char == '7':
        keylist.append('leftup')
    elif key_char == '9':
        keylist.append('rightup')
    elif key_char == '1':
        keylist.append('leftdown')
    elif key_char == '3':
        keylist.append('rightdown')

    if lbt.console_is_key_pressed(lbt.KEY_ENTER):
        keylist.append('enter')

    if key_char == 'g':
        keylist.append('pickup')
    if key_char == 'i':
        keylist.append('inventory')
    if key_char == 'd':
        keylist.append('dropmenu')
    if key_char == 'e':
        keylist.append('eatmenu')
    if key_char == 'w':
        keylist.append('wearmenu')
    if key_char == 'q':
        keylist.append('equipmenu')
    if key_char == 'r':
        keylist.append('drinkmenu')

    return keylist

def process_keylist(lbt, keylist, player):
    if keylist[0] is None:
        return
    if keylist[0] == 'pickup':
        player.pickup()
        return
    if keylist[0] == 'inventory':
        player.show_inventory()
        return
    if keylist[0] == 'drinkmenu':
        player.show_drink_menu()
        return
    if keylist[0] == 'dropmenu':
        player.show_drop_menu()
        return
    if keylist[0] == 'equipmenu':
        player.show_equip_menu()
        return
    if keylist[0] == 'wearmenu':
        player.show_wear_menu()
        return
    if keylist[0] == 'eatmenu':
        player.show_eat_menu()
        return
    if keylist[0] == 'left':
        player.move(-1, 0)
    if keylist[0] == 'right':
        player.move(1, 0)
    if keylist[0] == 'down':
        player.move(0, 1)
    if keylist[0] == 'up':
        player.move(0, -1)
    if keylist[0] == 'leftup':
        player.move(-1, -1)
    if keylist[0] == 'rightup':
        player.move(1, -1)
    if keylist[0] == 'leftdown':
        player.move(-1, 1)
    if keylist[0] == 'rightdown':
        player.move(1, 1)

