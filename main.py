__author__ = 'Martijn Schut'

from src.entities.creatures.CreatureFactory import CreatureFactory
from src.world.Level import Level
from src.entities.items.ItemFactory import ItemFactory

import tcod
import numpy as np
from tcod import libtcodpy

from src.input import keyboard as kb
from src import constants

import random
import textwrap

def getScrollX():
    return max(0, min(player.x - constants.SCREEN_WIDTH // 2 - constants.PANEL_WIDTH//2, 
                     level.level_width - constants.SCREEN_WIDTH - constants.PANEL_WIDTH//2.5))

def getScrollY():
    # adjust for size of the panel
    return max(0, min(player.y - constants.SCREEN_HEIGHT // 2, 
                     level.level_height - constants.SCREEN_HEIGHT))

def render_bar(x, y, total_width, value, maximum, name, bar_color, back_color, text_color = (255, 255, 255), show_exact = False):
    # M: I really liked this code, so I kept it pretty much the way it is.

    #now render the bar on top
    if show_exact:
        bar_width = int(float(value) / maximum * total_width)
        constants.panel.bg[x:x + total_width, y] = back_color
        if bar_width > 0:
            constants.panel.bg[x:x + bar_width, y] = bar_color
    else:
        bar_width = int(float(value) / maximum * (total_width - 8))
        constants.panel.bg[x + 8:x + total_width, y] = back_color
        if bar_width > 0:
            constants.panel.bg[x + 8:x + 8 + bar_width, y] = bar_color

    #finally, some centered text with the values
    if show_exact:
        text = f"{name}: {value}/{maximum}"
    else:
        text = f"{name}:"
    
    for i, char in enumerate(text):
        x_pos = x + total_width // 2 - len(text) // 2 + i
        constants.panel.print(x_pos, y, char, fg=text_color, bg=(0, 0, 0))

def render_status(x, y, name, value, text_color = (127, 127, 127)):
    text = f"{name}: {value}"
    for i, char in enumerate(text):
        x_pos = x + i
        constants.panel.print(x_pos, y, char, fg=text_color, bg=(0, 0, 0))

# basic tcod initialization
tileset = tcod.tileset.load_tilesheet(
    "assets/terminal12x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437
)

console = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")
root_console = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")

with tcod.context.new(
    columns=constants.SCREEN_WIDTH,
    rows=constants.SCREEN_HEIGHT,
    tileset=tileset,
    title="PyRoPy",
    vsync=True,
) as context:
    level = Level(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    cFactory = CreatureFactory(tcod, console, level)
    iFactory = ItemFactory(tcod, console, level)

    # add the player
    messages = [[], []]
    linecolors = []
    linecolors.append((255, 160, 160))  # Light red
    for i in range(255, 15, -8):
        linecolors.append((i, i, i))  # Grayscale
    all_messages = []
    player = cFactory.make_player(messages)

    # Add test messages directly to the message list
    messages[0].append("Welcome to PyRoPy!")
    messages[1].append(0)
    messages[0].append("Use arrow keys to move.")
    messages[1].append(0)
    messages[0].append("Press 'i' for inventory.")
    messages[1].append(0)
    messages[0].append("Press 'd' to drop items.")
    messages[1].append(0)
    messages[0].append("Press 'e' to eat items.")
    messages[1].append(0)
    messages[0].append("Press 'r' to drink items.")
    messages[1].append(0)
    messages[0].append("Press 'q' to equip items.")
    messages[1].append(0)
    messages[0].append("Press 'w' to wear items.")
    messages[1].append(0)
    messages[0].append("Press 'x' to examine items.")
    messages[1].append(0)
    
    # add some hostile and less hostile creatures & items
    funguscount = 10
    for _ in range(funguscount):
        fungus = cFactory.make_fungus()

    batcount = 5
    for _ in range(batcount):
        bat = cFactory.make_bat()

    snakecount = 5
    for _ in range(snakecount):
        snake = cFactory.make_snake()

    gargoylecount = 5
    for _ in range(gargoylecount):
        gargoyle = cFactory.make_gargoyle(player)

    rockcount = 25
    for _ in range(rockcount):
        rock = iFactory.make_rock()

    swordcount = 3
    for _ in range(swordcount):
        sword = iFactory.make_sword()

    glovecount = 2
    for _ in range(glovecount):
        glove = iFactory.make_gauntlet()

    potions = 15
    for _ in range(potions):
        potion = iFactory.make_random_potion()

    necklacecount = 2
    for _ in range(necklacecount):
        necklace = iFactory.make_amulet()

    fedoracount = 2
    for _ in range(fedoracount):
        fedora = iFactory.make_fedora()

    while True:
        # show stuff
        sx = getScrollX()
        sy = getScrollY()

        console.clear()
        root_console.clear()

        for y in range(level.level_height):
            for x in range(level.level_width):
                wx = x - sx
                wy = y - sy
                if 0 <= wx < constants.SCREEN_WIDTH and 0 <= wy < constants.SCREEN_HEIGHT:
                    console.bg[wx, wy] = level.map[x][y].color

                    if level.map[x][y].char is not None:
                        if level.map[x][y].front_color is not None and player.can_see(x, y):
                            level.map[x][y].identified = 1
                            console.print(wx, wy, level.map[x][y].char, level.map[x][y].front_color)
                        elif player.can_see(x, y):
                            level.map[x][y].identified = 1
                            console.print(wx, wy, level.map[x][y].char, (255, 255, 255))
                        elif level.map[x][y].identified == 1:
                            console.print(wx, wy, level.map[x][y].char, constants.colors['darkness_color'])
                        else:
                            console.bg[wx, wy] = constants.colors['darkness_color']
                            console.print(wx, wy, constants.chars['darkness_char'], constants.colors['darkness_color'])

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

        # prepare to render the bottom panel
        constants.panel.clear(fg=constants.PANEL_FG, bg=constants.PANEL_BG)

        # Add a debug indicator in the corner
        constants.panel.print(0, 0, "PyRoPy", fg=(255, 0, 0), bg=(0, 0, 0))
        
        # show the player's stats
        htext_color = (255, 255, 255)
        if float(player.hp) / player.maxhp < 0.3:
            htext_color = (255, 0, 0)
        render_bar(1, 1, constants.BAR_WIDTH, player.hp, player.maxhp, 'Health',
                   (255, 0, 0), (127, 0, 0), text_color=htext_color)

        # show hunger
        hutext_color = (127, 127, 127)
        if (float(player.hunger) / player.maxhunger) < 0.1:
            hutext_color = (255, 0, 0)
        elif (float(player.hunger) / player.maxhunger) < 0.3:
            hutext_color = (255, 255, 255)

        render_status(1, 3, 'Hunger', player.hunger_value, text_color=hutext_color)

        # show thirst (unimplemented)
        hutext_color = (127, 127, 127)
        render_status(1, 5, 'Thirst', " ", text_color=hutext_color)

        # show message log
        y = constants.MSG_Y - 1
        constants.panel.print(0, y, "Messages:", fg=(255, 255, 255), bg=(0, 0, 0))
        constants.panel.draw_rect(0, y, constants.MSG_WIDTH, 1, ord('-'), fg=(255, 255, 255), bg=(0, 0, 0))

        y += 1
        
        # Display at most 5 most recent messages for debugging
        display_messages = messages[0][-5:] if len(messages[0]) > 5 else messages[0]
        
        for i, message in enumerate(display_messages):
            constants.panel.print(1, y + i, message, fg=(255, 255, 255), bg=(0, 0, 0))
        
        if len(messages[0]) >= constants.MSG_HEIGHT:
            del messages[0][0]
            del messages[1][0]

        # blit the contents of "panel" to the root console
        constants.panel.blit(console, 0, 0, 0, 0, constants.PANEL_WIDTH, constants.PANEL_HEIGHT)

        context.present(console)

        for creature in level.creatures:
            creature.clear()

        # get input
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
            if event.type == "KEYDOWN":
                keylist = kb.handle_keys(event)
                if keylist:
                    constants.debug_msg(f'Pressed key {keylist[0]}')
                    kb.process_keylist(tcod, keylist, player)
                    if keylist[0] == 'exit':
                        raise SystemExit()
            elif event.type == "TEXTINPUT":
                keylist = kb.handle_keys(event)
                if keylist:
                    constants.debug_msg(f'Pressed key {keylist[0]}')
                    kb.process_keylist(tcod, keylist, player)
                    if keylist[0] == 'exit':
                        raise SystemExit()

