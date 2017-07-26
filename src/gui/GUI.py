__author__ = 'Martijn Schut'

from src import constants
from src.util.Line import Line
from src.util.Point import Point
from src.entities.items.Inventory import Inventory


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
        self.window = self.lbt.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

    def draw(self):
        line = Line(self.orix, self.oriy, self.curx, self.cury)
        print self.orix, self.oriy, self.curx, self.cury

        for point in line.get_points():
            self.lbt.console_set_default_foreground(self.window, self.lbt.magenta)
            self.lbt.console_put_char(self.window, point.x, point.y, '*', self.lbt.BKGND_NONE)
        #self.lbt.console_flush()
        self.lbt.console_blit(self.window, 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 0, 0, 0)

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

            self.header_height = self.lbt.console_get_height_rect(self.con, 0, 0,
                                                                  self.width, constants.SCREEN_HEIGHT,
                                                                  self.header)
            self.height = self.length + self.header_height

    def draw(self):
        # create an off-screen console that represents the menu's window
        self.window = self.lbt.console_new(self.width, self.height)

        # print the header, with auto-wrap
        self.lbt.console_set_default_foreground(self.window, self.lbt.white)
        self.lbt.console_set_default_background(self.window, self.lbt.black)
        self.lbt.console_print_rect_ex(self.window, 0, 0, self.width, self.height,
                                       self.lbt.black, self.lbt.LEFT, self.header)

        # print all the options
        y = self.header_height
        letter_index = ord('a')

        if type(self.options) is not list:
            for option_item in self.options.get_items():
                if option_item is None:
                    self.lbt.console_print_ex(self.window, 0, y, self.lbt.black,
                                          self.lbt.LEFT, ' ')
                    y += 1
                    letter_index += 1
                    continue
                option_text = option_item.get_name()
                if option_item.equipped:
                    option_text += '    [E]'
                if option_item.worn:
                    option_text += '    [W]'
                text = '(' + chr(letter_index) + ') ' + option_text
                self.lbt.console_print_ex(self.window, 0, y, self.lbt.black,
                                          self.lbt.LEFT, text)
                y += 1
                letter_index += 1
        else:
            for option_item in self.options:
                if option_item is None:
                    self.lbt.console_print_ex(self.window, 0, y, self.lbt.black,
                                          self.lbt.LEFT, ' ')
                    y += 1
                    letter_index += 1
                    continue

                option_text = option_item.get_name()
                if option_item.equipped:
                    option_text += '    [E]'
                if option_item.worn:
                    option_text += '    [W]'
                text = '(' + chr(letter_index) + ') ' + option_text
                self.lbt.console_print_ex(self.window, 0, y, self.lbt.black,
                                          self.lbt.LEFT, text)
                y += 1
                letter_index += 1

        x = constants.SCREEN_WIDTH/2 - self.width/2
        y = constants.SCREEN_HEIGHT/2 - self.height/2
        self.lbt.console_blit(self.window, 0, 0, self.width, self.height, 0, x, y, 1.0, 0.7)
        self.lbt.console_flush()
        self.key = self.lbt.console_wait_for_keypress(True)

    def draw_submenu(self):
        # create an off-screen console that represents the menu's window
        self.window = self.lbt.console_new(self.width, self.height)

        # print the header, with auto-wrap
        self.lbt.console_set_default_background(self.window, self.lbt.black)
        self.lbt.console_set_default_foreground(self.window, self.lbt.white)
        self.lbt.console_print_rect_ex(self.window, 0, 0, self.width, self.height,
                                       self.lbt.BKGND_ADD, self.lbt.LEFT, self.header)

        # print all the options
        y = self.header_height

        for option_item in self.options:
            letter_index = ord(option_item[0])
            if option_item == 'drink' or 'equip':
                letter_index = ord(option_item[1])
            if option_item is None:
                self.lbt.console_print_ex(self.window, 0, y, self.lbt.BKGND_ADD,
                                      self.lbt.LEFT, ' ')
                y += 1
                letter_index += 1
                continue
            option_text = option_item
            text = '(' + chr(letter_index) + ') ' + option_text
            self.lbt.console_print_ex(self.window, 0, y, self.lbt.BKGND_ADD,
                                      self.lbt.LEFT, text)
            y += 1
            letter_index += 1

        x = constants.SCREEN_WIDTH/2 - self.width/2
        y = constants.SCREEN_HEIGHT/2 - self.height/2
        self.lbt.console_blit(self.window, 0, 0, self.width, self.height, 0, x, y, 1.0, 0.7)
        self.lbt.console_flush()
        self.key = self.lbt.console_wait_for_keypress(True)


class InventoryMenu(Menu):
    def __init__(self, lbt, con, header, player):
        self.player = player
        super(InventoryMenu, self).__init__(lbt, con, header, self.player.inventory, constants.INVENTORY_WIDTH)

    def draw(self):
        super(InventoryMenu, self).draw()
        index = self.key.c - ord('a')
        if index < 0 or index > self.options.get_len():
            return

        item = self.player.inventory.get_item_at_index(index)
        if item is not None:
            options2 = []
            options2.append('drop')
            if item.nutrition != 0:
                options2.append('eat')
            if item.drinkable:
                options2.append('drink')
            if item.holdable:
                options2.append('equip')
            if item.wearable:
                options2.append('wear')

            popup = Menu(self.lbt, self.con, 'Do what with %s?' %item.name, options2, constants.INVENTORY_WIDTH - 3)
            popup.update()
            popup.draw_submenu()
            index2 = popup.key.c - ord('a')

            if index2 < 0:
                return
            if popup.key.c - ord('d') == 0:
                self.player.drop(item)
            elif popup.key.c - ord('e') == 0:
                self.player.eat(item)
            elif popup.key.c - ord('r') == 0:
                self.player.drink(item)
            elif popup.key.c - ord('q') == 0:
                self.player.equip_to_limbtype(item, item.equipto)
            elif popup.key.c - ord('w') == 0:
                self.player.wear_on_limbtype(item, item.wearon)

class DropMenu(Menu):
    def __init__(self, lbt, con, header, player):
         self.player = player
         super(DropMenu, self).__init__(lbt, con, header, self.player.inventory, constants.INVENTORY_WIDTH)

    def draw(self):
        super(DropMenu, self).draw()

        index = self.key.c - ord('a')
        if type(self.options) == Inventory:
            if index < 0 or index > self.options.get_len():
                return
        elif index < 0 or index > len(self.options):
            return

        if type(self.options) == Inventory:
            items = self.options.get_items()
            item = items[index]
        else:
            item = self.options[index]
        if item is not None:
            self.player.drop(item)
            self.player.inventory.sort()

class EatMenu(Menu):
    def __init__(self, lbt, con, header, player):
         self.player = player
         super(EatMenu, self).__init__(lbt, con, header,
         self.player.inventory, constants.INVENTORY_WIDTH)

    def draw(self):
        super(EatMenu, self).draw()

        index = self.key.c - ord('a')
        if index < 0 or index > len(self.options):
            return

        itemlist = self.player.inventory.get_edible_items()
        item = itemlist[index]
        if item is not None:
            self.player.eat(item)
            self.player.inventory.sort()

class DrinkMenu(Menu):
    def __init__(self, lbt, con, header, player):
         self.player = player
         super(DrinkMenu, self).__init__(lbt, con, header,
         self.player.inventory, constants.INVENTORY_WIDTH)

    def draw(self):
        super(DrinkMenu, self).draw()

        index = self.key.c - ord('a')
        if index < 0 or index > len(self.options):
            return

        itemlist = self.player.inventory.get_drinkable_items()
        item = itemlist[index]
        if item is not None:
            self.player.drink(item)
            self.player.inventory.sort()

class EquipMenu(Menu):
    def __init__(self, lbt, con, header, player):
         self.player = player
         super(EquipMenu, self).__init__(lbt, con, header,
         self.player.inventory, constants.INVENTORY_WIDTH)

    def draw(self):
        super(EquipMenu, self).draw()

        index = self.key.c - ord('a')
        if index < 0 or index > len(self.options):
            return

        itemlist = self.player.inventory.get_equipable_items()
        item = itemlist[index]
        if item is not None:
            limbtoequip = None
            for limb in self.player.limbs:
                if type(limb) == item.equipto:
                    limbtoequip = limb
                    break

            if limbtoequip is not None:
                self.player.equip_to_limbtype(item, type(limbtoequip))
                self.player.inventory.sort()

class WearMenu(Menu):
    def __init__(self, lbt, con, header, player):
         self.player = player
         super(WearMenu, self).__init__(lbt, con, header,
         self.player.inventory, constants.INVENTORY_WIDTH)

    def draw(self):
        super(WearMenu, self).draw()

        index = self.key.c - ord('a')
        if index < 0 or index > len(self.options):
            return

        itemlist = self.player.inventory.get_wearable_items()
        item = itemlist[index]
        self.player.wear(item)

