__author__ = 'Martijn Schut'

from src import constants
from src.util.Line import Line
from src.util.Point import Point
from src.entities.items.Inventory import Inventory
import tcod


class TargetMenu(object):
    def __init__(self, lbt, con, player, caption, orix, oriy):
        self.lbt = lbt
        self.con = con
        self.player = player
        self.caption = caption
        self.orix = orix
        self.oriy = oriy
        self.curx = orix
        self.cury = oriy
        self.window = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")

    def draw(self):
        line = Line(self.orix, self.oriy, self.curx, self.cury)

        for point in line.get_points():
            self.window.print(point.x, point.y, '*', (255, 0, 255))  # Magenta color
        self.window.blit(self.con, 0, 0, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

    def update(self):
        ax = 0
        ay = 0
        self.key = self.lbt.console_wait_for_keypress(True)
        if self.lbt.console_is_key_pressed(self.lbt.KEY_DOWN):
            ay = 1
        elif self.lbt.console_is_key_pressed(self.lbt.KEY_UP):
            ay = -1
        elif self.lbt.console_is_key_pressed(self.lbt.KEY_RIGHT):
            ax = 1
        elif self.lbt.console_is_key_pressed(self.lbt.KEY_LEFT):
            ax = -1

        self.curx += ax
        self.cury += ay


class ExamineMenu(TargetMenu):
    def __init__(self, lbt, con, player, caption, orix, oriy):
        super(ExamineMenu, self).__init__(lbt, con, player, caption, orix, oriy)


class Menu(object):
    def __init__(self, lbt, con, header, options, width):
        self.lbt = lbt
        self.header = header
        self.con = con
        self.options = options
        self.width = width

        self.update()

    def update(self, options = None, header = None, width = None):
        if options is not None:
            self.options = options
        if header is not None:
            self.header = header
        if width is not None:
            self.width = width

        if self.options is not None:
            if type(self.options) is not list:
                self.length = self.options.get_len()
            else:
                self.length = len(self.options)

            # Calculate header height based on text wrapping
            words = self.header.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in words:
                if current_length + len(word) + 1 <= self.width:
                    current_line.append(word)
                    current_length += len(word) + 1
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            self.header_height = len(lines)
            self.height = self.length + self.header_height

    def draw(self):
        # create an off-screen console that represents the menu's window
        self.window = tcod.console.Console(self.width, self.height, order="F")

        # print the header, with auto-wrap
        self.window.print(0, 0, self.header, (255, 255, 255), (0, 0, 0))

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if type(self.options) is not list:
            for option_item in self.options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', (255, 255, 255), (0, 0, 0))
                else:
                    text = f"{chr(letter_index)}: {option_item.name}"
                    self.window.print(0, y, text, (255, 255, 255), (0, 0, 0))
                y += 1
                letter_index += 1
        else:
            for option_text in self.options:
                text = f"{chr(letter_index)}: {option_text}"
                self.window.print(0, y, text, (255, 255, 255), (0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)

    def draw_submenu(self):
        # create an off-screen console that represents the menu's window
        self.window = tcod.console.Console(self.width, self.height, order="F")

        # print the header, with auto-wrap
        self.window.print(0, 0, self.header, (255, 255, 255), (0, 0, 0))

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if type(self.options) is not list:
            for option_item in self.options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', (255, 255, 255), (0, 0, 0))
                else:
                    text = f"{chr(letter_index)}: {option_item.name}"
                    self.window.print(0, y, text, (255, 255, 255), (0, 0, 0))
                y += 1
                letter_index += 1
        else:
            for option_text in self.options:
                text = f"{chr(letter_index)}: {option_text}"
                self.window.print(0, y, text, (255, 255, 255), (0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)


class InventoryMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(InventoryMenu, self).__init__(lbt, con, header, player.inventory, constants.INVENTORY_WIDTH)

    def draw(self):
        # create an off-screen console that represents the menu's window
        self.window = tcod.console.Console(self.width, self.height, order="F")

        # print the header, with auto-wrap
        self.window.print(0, 0, self.header, (255, 255, 255), (0, 0, 0))

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if type(self.options) is not list:
            for option_item in self.options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', (255, 255, 255), (0, 0, 0))
                else:
                    text = f"{chr(letter_index)}: {option_item.name}"
                    self.window.print(0, y, text, (255, 255, 255), (0, 0, 0))
                y += 1
                letter_index += 1
        else:
            for option_text in self.options:
                text = f"{chr(letter_index)}: {option_text}"
                self.window.print(0, y, text, (255, 255, 255), (0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)


class DropMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(DropMenu, self).__init__(lbt, con, header, player.inventory, constants.INVENTORY_WIDTH)

    def draw(self):
        # create an off-screen console that represents the menu's window
        self.window = tcod.console.Console(self.width, self.height, order="F")

        # print the header, with auto-wrap
        self.window.print(0, 0, self.header, (255, 255, 255), (0, 0, 0))

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if type(self.options) is not list:
            for option_item in self.options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', (255, 255, 255), (0, 0, 0))
                else:
                    text = f"{chr(letter_index)}: {option_item.name}"
                    self.window.print(0, y, text, (255, 255, 255), (0, 0, 0))
                y += 1
                letter_index += 1
        else:
            for option_text in self.options:
                text = f"{chr(letter_index)}: {option_text}"
                self.window.print(0, y, text, (255, 255, 255), (0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)


class EatMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(EatMenu, self).__init__(lbt, con, header, player.inventory, constants.INVENTORY_WIDTH)


class DrinkMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(DrinkMenu, self).__init__(lbt, con, header, player.inventory, constants.INVENTORY_WIDTH)


class EquipMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(EquipMenu, self).__init__(lbt, con, header, player.inventory, constants.INVENTORY_WIDTH)


class WearMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(WearMenu, self).__init__(lbt, con, header, player.inventory, constants.INVENTORY_WIDTH)

