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

# Global context for menu rendering
global_context = None

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
    # Make the context available globally
    global_context = context
    
    # Store the context in constants for easy access
    constants.game_context = context
    
    level = Level(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    cFactory = CreatureFactory(tcod, console, level)
    iFactory = ItemFactory(tcod, console, level)

    # add the player
    messages = [[], []]
    linecolors = []
    linecolors.append((255, 255, 255))  # White (default text color)
    linecolors.append((255, 160, 160))  # Light red/pink (for combat messages)
    for i in range(255, 15, -8):
        linecolors.append((i, i, i))  # Grayscale fade
    all_messages = []
    player = cFactory.make_player(messages)

    # Add test messages directly to the message list
    messages[0].append("Welcome to PyRoPy!")
    messages[1].append(0)  # Use white (index 0)
    messages[0].append("Use arrow keys to move.")
    messages[1].append(0)  # Use white (index 0)
    messages[0].append("Press 'i' for inventory.")
    messages[1].append(0)  # Use white (index 0)
    messages[0].append("Press 'd' to drop items.")
    messages[1].append(0)  # Use white (index 0)
    messages[0].append("Press 'e' to eat items.")
    messages[1].append(0)  # Use white (index 0)
    messages[0].append("Press 'r' to drink items.")
    messages[1].append(0)  # Use white (index 0)
    messages[0].append("Press 'q' to equip items.")
    messages[1].append(0)  # Use white (index 0)
    messages[0].append("Press 'w' to wear items.")
    messages[1].append(0)  # Use white (index 0)
    messages[0].append("Press 'x' to examine items.")
    messages[1].append(0)  # Use white (index 0)
    
    # Set reference to the factory in the level for slime splitting
    level.factory = cFactory
    
    # Add original creatures
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
    
    # Add new creatures with balanced spawning
    
    # Docile creatures (more common)
    frogcount = 8
    for _ in range(frogcount):
        frog = cFactory.make_frog()
    
    ratcount = 12  # Scavengers, not threatening
    for _ in range(ratcount):
        rat = cFactory.make_rat()
    
    diggercount = 4  # Helpful by creating passages
    for _ in range(diggercount):
        digger = cFactory.make_digger()
    
    huntercount = 3  # Hunts fungus, not the player
    for _ in range(huntercount):
        hunter = cFactory.make_hunter()
    
    slimecount = 3  # Slow and weak
    for _ in range(slimecount):
        slime = cFactory.make_slime()
    
    # Dangerous creatures (less common)
    mimiccount = 2  # Disguised as items
    for _ in range(mimiccount):
        mimic = cFactory.make_mimic()
    
    spidercount = 3  # Poisonous
    for _ in range(spidercount):
        spider = cFactory.make_spider()
    
    trap_spidercount = 2  # Hidden traps
    for _ in range(trap_spidercount):
        trap_spider = cFactory.make_trap_spider()
    
    wolfcount = 3  # Pack hunters
    for _ in range(wolfcount):
        wolf = cFactory.make_wolf()
    
    shadowcount = 2  # Appear in darkness
    for _ in range(shadowcount):
        shadow = cFactory.make_shadow(player)
    
    # Add original items
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
        
    # Add food items to the game world
    foodcount = 20
    for _ in range(foodcount):
        food = iFactory.make_food()

    while True:
        # show stuff
        sx = getScrollX()
        sy = getScrollY()

        console.clear()
        root_console.clear()

        # Only render the game world if not in a menu and player is alive
        if (not hasattr(player, '_in_menu') or not player._in_menu) and player.alive:
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
        
        # Display messages with proper wrapping
        max_messages = constants.MSG_HEIGHT
        max_chars_per_line = constants.MSG_WIDTH - 2  # Leave a little margin
        
        # Get the messages to display (up to maximum message height)
        display_messages = messages[0][-max_messages:] if len(messages[0]) > max_messages else messages[0]
        display_colors = messages[1][-max_messages:] if len(messages[1]) > max_messages else messages[1]
        
        # Reverse the messages and colors lists to display newest messages at the top
        display_messages = list(reversed(display_messages))
        display_colors = list(reversed(display_colors))
        
        current_y = y
        for i, message in enumerate(display_messages):
            color_age = display_colors[i]
            
            # Get the color based on age (fade from white to dark gray)
            if color_age >= len(linecolors):
                color_age = len(linecolors) - 1
            message_color = linecolors[color_age]
            
            # Split message into lines if needed
            if len(message) <= max_chars_per_line:
                # Short message, display as is
                constants.panel.print(1, current_y, message, fg=message_color, bg=(0, 0, 0))
                current_y += 1
            else:
                # Long message, wrap it
                words = message.split()
                line = ""
                for word in words:
                    if len(line) + len(word) + 1 <= max_chars_per_line:
                        if line:
                            line += " " + word
                        else:
                            line = word
                    else:
                        # Line is full, print it and start a new line
                        constants.panel.print(1, current_y, line, fg=message_color, bg=(0, 0, 0))
                        current_y += 1
                        line = word
                        
                # Print any remaining text
                if line:
                    constants.panel.print(1, current_y, line, fg=message_color, bg=(0, 0, 0))
                    current_y += 1
            
            # Increment color age for older messages
            messages[1][i] += 1
        
        if len(messages[0]) >= max_messages * 2:  # Keep twice as many messages in memory before pruning
            del messages[0][0]
            del messages[1][0]

        # blit the contents of "panel" to the root console
        constants.panel.blit(console, 0, 0, 0, 0, constants.PANEL_WIDTH, constants.PANEL_HEIGHT)

        # Present the console
        context.present(console)

        # Clear creatures for next frame
        for creature in level.creatures:
            creature.clear()
        
        # Check if player is dead and show game over message
        if player and not player.alive:
            # Draw game over screen
            console.clear(fg=(255, 0, 0), bg=(0, 0, 0))
            
            # Show game over message
            game_over_text = "GAME OVER"
            console.print(constants.SCREEN_WIDTH // 2 - len(game_over_text) // 2, 
                        constants.SCREEN_HEIGHT // 2 - 2, 
                        game_over_text, fg=(255, 0, 0), bg=(0, 0, 0))
            
            restart_text = "Press SPACE to restart or ESC to quit"
            console.print(constants.SCREEN_WIDTH // 2 - len(restart_text) // 2, 
                        constants.SCREEN_HEIGHT // 2, 
                        restart_text, fg=(255, 255, 255), bg=(0, 0, 0))
            
            context.present(console)
            
            # Wait for player input
            waiting_for_input = True
            while waiting_for_input:
                for event in tcod.event.wait():
                    if event.type == "QUIT":
                        raise SystemExit()
                    elif event.type == "KEYDOWN":
                        if event.sym == tcod.event.KeySym.ESCAPE:
                            raise SystemExit()
                        elif event.sym == tcod.event.KeySym.SPACE:
                            # Restart the game
                            waiting_for_input = False
                            player = cFactory.make_player(messages)
                            break

        # get input
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
            if event.type == "KEYDOWN":
                keylist = kb.handle_keys(event)
                if keylist:
                    constants.debug_msg(f'Pressed key {keylist[0]}')
                    # Set menu state before processing key
                    if keylist[0] in ['inventory', 'drop', 'eat', 'drink', 'equip', 'wear']:
                        player._in_menu = True
                    kb.process_keylist(tcod, keylist, player)
                    
                    # Process enemy turns if player made a move (not just opened a menu)
                    if keylist[0] in ['up', 'down', 'left', 'right', 'leftup', 'rightup', 'leftdown', 'rightdown']:
                        # Update player state first when they take a turn
                        if player and player.ai and player.alive:
                            player.ai.on_update()
                            
                        # Give all other creatures a turn
                        for creature in level.creatures:
                            if creature != player and creature.ai:
                                creature.ai.on_update()
                    
                    if keylist[0] == 'exit':
                        raise SystemExit()
            elif event.type == "TEXTINPUT":
                keylist = kb.handle_keys(event)
                if keylist:
                    constants.debug_msg(f'Pressed key {keylist[0]}')
                    kb.process_keylist(tcod, keylist, player)
                    if keylist[0] == 'exit':
                        raise SystemExit()

