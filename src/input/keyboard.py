__author__ = 'Martijn Schut'

import tcod

def handle_keys(event):
    keylist = []

    if isinstance(event, tcod.event.TextInput):
        if event.text == '8':
            keylist.append('up')
        elif event.text == '2':
            keylist.append('down')
        elif event.text == '4':
            keylist.append('left')
        elif event.text == '6':
            keylist.append('right')
        elif event.text == '7':
            keylist.append('leftup')
        elif event.text == '9':
            keylist.append('rightup')
        elif event.text == '1':
            keylist.append('leftdown')
        elif event.text == '3':
            keylist.append('rightdown')
        elif event.text == 'g':
            keylist.append('pickup')
        elif event.text == 'i':
            keylist.append('inventory')
        elif event.text == 'd':
            keylist.append('dropmenu')
        elif event.text == 'e':
            keylist.append('eatmenu')
        elif event.text == 'w':
            keylist.append('wearmenu')
        elif event.text == 'q':
            keylist.append('equipmenu')
        elif event.text == 'r':
            keylist.append('drinkmenu')
        elif event.text == ';':
            keylist.append('examine')
    elif isinstance(event, tcod.event.KeyDown):
        if event.sym == tcod.event.KeySym.ESCAPE:
            keylist.append('exit')
        elif event.sym == tcod.event.KeySym.UP:
            keylist.append('up')
        elif event.sym == tcod.event.KeySym.DOWN:
            keylist.append('down')
        elif event.sym == tcod.event.KeySym.LEFT:
            keylist.append('left')
        elif event.sym == tcod.event.KeySym.RIGHT:
            keylist.append('right')
        elif event.sym == tcod.event.KeySym.RETURN:
            keylist.append('enter')

    return keylist

def process_keylist(tcod, keylist, player):
    if not keylist or keylist[0] is None:
        return
    if keylist[0] == 'pickup':
        player.pickup()
        return
    if keylist[0] == 'inventory':
        player.inventorymenu.draw()
        return
    if keylist[0] == 'drinkmenu':
        player.drinkmenu.draw()
        return
    if keylist[0] == 'dropmenu':
        player.dropmenu.draw()
        return
    if keylist[0] == 'equipmenu':
        player.equipmenu.draw()
        return
    if keylist[0] == 'wearmenu':
        player.wearmenu.draw()
        return
    if keylist[0] == 'eatmenu':
        player.eatmenu.draw()
        return
    if keylist[0] == 'examine':
        player.show_examine_menu()
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

