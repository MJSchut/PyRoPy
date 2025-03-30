__author__ = 'Martijn Schut'

from src import constants
from src.util.Line import Line
from src.util.Point import Point
from src.entities.items.Inventory import Inventory
import tcod
import textwrap


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
        self.con = con
        self.header = header
        self._options = options
        self.width = width
        self.header_height = 1
        self.height = self._get_options_length() + self.header_height
        self.window = tcod.console.Console(self.width, self.height, order="F")

    def _get_options_length(self):
        if hasattr(self._options, 'get_items'):
            return len(self._options.get_items())
        elif isinstance(self._options, list):
            return len(self._options)
        return 0

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value
        self.height = self._get_options_length() + self.header_height
        self.window = tcod.console.Console(self.width, self.height, order="F")

    def _format_item_text(self, item, letter_index):
        # Use get_name method if available, otherwise fallback to item.name or str representation
        if hasattr(item, 'get_name'):
            item_name = item.get_name()
        elif hasattr(item, 'name'):
            item_name = item.name
        else:
            item_name = str(item)
            
        # Add special markers for equipped or worn items
        status = ""
        if hasattr(item, 'equipped') and item.equipped:
            status = " (equipped)"
        elif hasattr(item, 'worn') and item.worn:
            status = " (worn)"
            
        return f"{chr(letter_index)}: {item_name}{status}"
        
    def draw(self):
        # Calculate position for centered menu
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2

        # Track the area we're modifying for restoration
        menu_x_start = max(0, x - 1)
        menu_y_start = max(0, y - 1)
        menu_width = min(constants.SCREEN_WIDTH - menu_x_start, self.width + 2)
        menu_height = min(constants.SCREEN_HEIGHT - menu_y_start, self.height + 2)
        
        # Store the original background and foreground colors for this region
        bg_backup = []
        fg_backup = []
        for cy in range(menu_y_start, menu_y_start + menu_height):
            bg_row = []
            fg_row = []
            for cx in range(menu_x_start, menu_x_start + menu_width):
                if 0 <= cx < constants.SCREEN_WIDTH and 0 <= cy < constants.SCREEN_HEIGHT:
                    bg_row.append(self.con.bg[cx, cy])
                    fg_row.append(self.con.fg[cx, cy])
            bg_backup.append(bg_row)
            fg_backup.append(fg_row)
        
        # Create a black background for the menu
        for ny in range(self.height + 2):
            for nx in range(self.width + 2):
                menu_x = x + nx - 1
                menu_y = y + ny - 1
                if 0 <= menu_x < constants.SCREEN_WIDTH and 0 <= menu_y < constants.SCREEN_HEIGHT:
                    self.con.bg[menu_x, menu_y] = (0, 0, 0)
        
        # Draw a border
        for nx in range(self.width + 2):
            menu_x = x + nx - 1
            if 0 <= menu_x < constants.SCREEN_WIDTH:
                if 0 <= y-1 < constants.SCREEN_HEIGHT:
                    self.con.print(menu_x, y-1, '─', fg=(255, 255, 255), bg=(0, 0, 0))
                if 0 <= y+self.height < constants.SCREEN_HEIGHT:
                    self.con.print(menu_x, y+self.height, '─', fg=(255, 255, 255), bg=(0, 0, 0))
        
        for ny in range(self.height + 2):
            menu_y = y + ny - 1
            if 0 <= menu_y < constants.SCREEN_HEIGHT:
                if 0 <= x-1 < constants.SCREEN_WIDTH:
                    self.con.print(x-1, menu_y, '│', fg=(255, 255, 255), bg=(0, 0, 0))
                if 0 <= x+self.width < constants.SCREEN_WIDTH:
                    self.con.print(x+self.width, menu_y, '│', fg=(255, 255, 255), bg=(0, 0, 0))
        
        # Draw corners
        if 0 <= x-1 < constants.SCREEN_WIDTH and 0 <= y-1 < constants.SCREEN_HEIGHT:
            self.con.print(x-1, y-1, '┌', fg=(255, 255, 255), bg=(0, 0, 0))
        if 0 <= x+self.width < constants.SCREEN_WIDTH and 0 <= y-1 < constants.SCREEN_HEIGHT:
            self.con.print(x+self.width, y-1, '┐', fg=(255, 255, 255), bg=(0, 0, 0))
        if 0 <= x-1 < constants.SCREEN_WIDTH and 0 <= y+self.height < constants.SCREEN_HEIGHT:
            self.con.print(x-1, y+self.height, '└', fg=(255, 255, 255), bg=(0, 0, 0))
        if 0 <= x+self.width < constants.SCREEN_WIDTH and 0 <= y+self.height < constants.SCREEN_HEIGHT:
            self.con.print(x+self.width, y+self.height, '┘', fg=(255, 255, 255), bg=(0, 0, 0))
        
        # Print the header
        header_lines = []
        words = self.header.split()
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= self.width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                header_lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            header_lines.append(' '.join(current_line))
        
        for i, line in enumerate(header_lines):
            if i < self.header_height:
                header_x = x + (self.width - len(line)) // 2
                self.con.print(header_x, y + i, line, fg=(255, 255, 255), bg=(0, 0, 0))
        
        # Print options
        menu_y = y + self.header_height
        letter_index = ord('a')
        
        if hasattr(self._options, 'get_items'):
            for option_item in self._options.get_items():
                if option_item is not None:
                    text = self._format_item_text(option_item, letter_index)
                    self.con.print(x + 1, menu_y, text, fg=(255, 255, 255), bg=(0, 0, 0))
                menu_y += 1
                letter_index += 1
        elif isinstance(self._options, list):
            for option_text in self._options:
                if option_text is not None:
                    text = self._format_item_text(option_text, letter_index)
                    self.con.print(x + 1, menu_y, text, fg=(255, 255, 255), bg=(0, 0, 0))
                menu_y += 1
                letter_index += 1
        
        # Present the console
        if hasattr(constants, 'game_context') and constants.game_context:
            constants.game_context.present(self.con)
        
        # Wait for key press
        result = None
        while result is None:
            for event in tcod.event.wait():
                if event.type == "KEYDOWN":
                    try:
                        # Use the correct enum for key symbols
                        if event.sym == tcod.event.KeySym.ESCAPE:
                            result = None
                            break
                        elif event.sym == tcod.event.KeySym.RETURN:
                            result = chr(letter_index - 1)
                            break
                    except AttributeError:
                        # Fall back to deprecated constants if needed
                        if event.sym == 27:  # ESCAPE
                            result = None
                            break
                        elif event.sym == 13:  # RETURN
                            result = chr(letter_index - 1)
                            break
                elif event.type == "TEXTINPUT":
                    if event.text.isalpha():
                        key_index = ord(event.text.lower()) - ord('a')
                        if 0 <= key_index < letter_index - ord('a'):
                            result = event.text.lower()
                            break
                elif event.type == "QUIT":
                    raise SystemExit()
            
            # Redraw the menu while waiting for input
            if result is None and hasattr(constants, 'game_context') and constants.game_context:
                constants.game_context.present(self.con)
        
        # Restore the original console background and foreground
        for cy in range(menu_height):
            for cx in range(menu_width):
                if (menu_y_start + cy < constants.SCREEN_HEIGHT and 
                    menu_x_start + cx < constants.SCREEN_WIDTH):
                    self.con.bg[menu_x_start + cx, menu_y_start + cy] = bg_backup[cy][cx]
                    self.con.fg[menu_x_start + cx, menu_y_start + cy] = fg_backup[cy][cx]
        
        # Present the console one last time to clear the menu
        if hasattr(constants, 'game_context') and constants.game_context:
            constants.game_context.present(self.con)
            
        return result

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

        if hasattr(self._options, 'get_items'):
            for option_item in self._options.get_items():
                if option_item is None:
                    self.window.print(0, y, ' ', fg=(255, 255, 255), bg=(0, 0, 0))
                else:
                    # Use the _format_item_text method for consistent display
                    text = self._format_item_text(option_item, letter_index)
                    for char_idx, char in enumerate(text):
                        if char_idx < self.width:
                            self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1
        elif isinstance(self._options, list):
            for option_text in self._options:
                if option_text is None:
                    self.window.print(0, y, ' ', fg=(255, 255, 255), bg=(0, 0, 0))
                else:
                    # Use the _format_item_text method for consistent display
                    text = self._format_item_text(option_text, letter_index)
                    for char_idx, char in enumerate(text):
                        if char_idx < self.width:
                            self.window.print(char_idx, y, char, fg=(255, 255, 255), bg=(0, 0, 0))
                y += 1
                letter_index += 1

        # blit the contents of "window" to the root console
        x = constants.SCREEN_WIDTH // 2 - self.width // 2
        y = constants.SCREEN_HEIGHT // 2 - self.height // 2
        
        # Correct blit order
        self.window.blit(self.con, 0, 0, x, y, self.width, self.height)


class InventoryMenu(Menu):
    def __init__(self, lbt, con, header, options):
        super(InventoryMenu, self).__init__(lbt, con, header, options, 40)


class DropMenu(Menu):
    def __init__(self, lbt, con, header, options):
        super(DropMenu, self).__init__(lbt, con, header, options, 40)


class EatMenu(Menu):
    def __init__(self, lbt, con, header, options):
        super(EatMenu, self).__init__(lbt, con, header, options, 40)


class DrinkMenu(Menu):
    def __init__(self, lbt, con, header, options):
        super(DrinkMenu, self).__init__(lbt, con, header, options, 40)


class EquipMenu(Menu):
    def __init__(self, lbt, con, header, options):
        super(EquipMenu, self).__init__(lbt, con, header, options, 40)


class WearMenu(Menu):
    def __init__(self, lbt, con, header, options):
        super(WearMenu, self).__init__(lbt, con, header, options, 40)

