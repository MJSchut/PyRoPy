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
        self.height = 0  # Initialize height
        self.update()

    def update(self, options = None, header = None, width = None):
        if options is not None:
            self.options = options
        if header is not None:
            self.header = header
        if width is not None:
            self.width = width

        if self.options is not None:
            if hasattr(self.options, 'get_len'):
                self.length = self.options.get_len()
            elif isinstance(self.options, list):
                self.length = len(self.options)
            else:
                self.length = 0

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
        self.window.clear(fg=(255, 255, 255), bg=(0, 0, 0))

        # print the header, with auto-wrap
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
            
        for line_idx, line in enumerate(lines):
            for char_idx, char in enumerate(line):
                if char_idx < self.width:
                    self.window.print(char_idx, line_idx, char, fg=(255, 255, 255), bg=(0, 0, 0))

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if hasattr(self.options, 'get_items'):
            for option_item in self.options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', fg=(255, 255, 255), bg=(0, 0, 0))
                else:
                    text = f"{chr(letter_index)}: {option_item.name}"
                    for char_idx, char in enumerate(text):
                        if char_idx < self.width:
                            self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1
        elif isinstance(self.options, list):
            for option_text in self.options:
                if option_text is not None:
                    text = f"{chr(letter_index)}: {option_text}"
                    for char_idx, char in enumerate(text):
                        if char_idx < self.width:
                            self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)
        
        # Force rendering the menu
        if hasattr(self.con, 'present'):
            self.con.present()
        
        # Wait for key press
        wait_for_input = True
        while wait_for_input:
            for event in tcod.event.wait():
                if event.type == "KEYDOWN" or event.type == "TEXTINPUT":
                    wait_for_input = False
                    break

    def draw_submenu(self):
        # create an off-screen console that represents the menu's window
        self.window = tcod.console.Console(self.width, self.height, order="F")

        # print the header, with auto-wrap
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
            
        for line_idx, line in enumerate(lines):
            for char_idx, char in enumerate(line):
                if char_idx < self.width:
                    self.window.print(char_idx, line_idx, char, fg=(255, 255, 255), bg=(0, 0, 0))

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if type(self.options) is not list:
            for option_item in self.options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', fg=(255, 255, 255), bg=(0, 0, 0))
                else:
                    text = f"{chr(letter_index)}: {option_item.name}"
                    for char_idx, char in enumerate(text):
                        if char_idx < self.width:
                            self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1
        else:
            for option_text in self.options:
                text = f"{chr(letter_index)}: {option_text}"
                for char_idx, char in enumerate(text):
                    if char_idx < self.width:
                        self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)


class InventoryMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(InventoryMenu, self).__init__(lbt, con, header, player.inventory, 40)

    def draw(self):
        # create an off-screen console that represents the menu's window
        self.window = tcod.console.Console(self.width, self.height, order="F")

        # print the header, with auto-wrap
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
            
        for line_idx, line in enumerate(lines):
            for char_idx, char in enumerate(line):
                if char_idx < self.width:
                    self.window.print(char_idx, line_idx, char, fg=(255, 255, 255), bg=(0, 0, 0))

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if type(self.options) is not list:
            for option_item in self.options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', fg=(255, 255, 255), bg=(0, 0, 0))
                else:
                    text = f"{chr(letter_index)}: {option_item.name}"
                    for char_idx, char in enumerate(text):
                        if char_idx < self.width:
                            self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1
        else:
            for option_text in self.options:
                text = f"{chr(letter_index)}: {option_text}"
                for char_idx, char in enumerate(text):
                    if char_idx < self.width:
                        self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)


class DropMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(DropMenu, self).__init__(lbt, con, header, player.inventory, 40)

    def draw(self):
        # create an off-screen console that represents the menu's window
        self.window = tcod.console.Console(self.width, self.height, order="F")

        # print the header, with auto-wrap
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
            
        for line_idx, line in enumerate(lines):
            for char_idx, char in enumerate(line):
                if char_idx < self.width:
                    self.window.print(char_idx, line_idx, char, fg=(255, 255, 255), bg=(0, 0, 0))

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if type(self.options) is not list:
            for option_item in self.options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', fg=(255, 255, 255), bg=(0, 0, 0))
                else:
                    text = f"{chr(letter_index)}: {option_item.name}"
                    for char_idx, char in enumerate(text):
                        if char_idx < self.width:
                            self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1
        else:
            for option_text in self.options:
                text = f"{chr(letter_index)}: {option_text}"
                for char_idx, char in enumerate(text):
                    if char_idx < self.width:
                        self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)


class EatMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(EatMenu, self).__init__(lbt, con, header, player.inventory.get_edible_items(), 40)


class DrinkMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(DrinkMenu, self).__init__(lbt, con, header, player.inventory.get_drinkable_items(), 40)


class EquipMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(EquipMenu, self).__init__(lbt, con, header, player.inventory.get_equipable_items(), 40)


class WearMenu(Menu):
    def __init__(self, lbt, con, header, player):
        super(WearMenu, self).__init__(lbt, con, header, player.inventory.get_wearable_items(), 40)

