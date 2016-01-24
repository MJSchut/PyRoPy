__author__ = 'Martijn Schut'

import random

from src.entities.Entity import Entity
from src.gui.GUI import InventoryMenu
from src.gui.GUI import DropMenu
from src.gui.GUI import EatMenu
from src.entities.items.Items import Item
from src.ai.CreatureAi import CreatureAi
from src.entities.items.Inventory import Inventory

def makeSecondPerson(text):
    new_text_array = text.split(" ")

    for x in range(0, len(new_text_array)):
        if new_text_array[x] == 'feel':
            new_text_array[x] = 'look'

    new_text_array[0] += "s"

    new_text = " ".join(new_text_array)

    return new_text


class Creature(Entity):
    def __init__ (self, lbt, con, level, char, color):
        super(Creature, self).__init__(lbt, con, level, char, color)
        self.maxhp = 3
        self.hp = self.maxhp
        self.maxhunger = -1
        self.hunger = -1
        self.attack = 0
        self.attack_effect = None
        self.attack_effectduration = 3
        self.crit_chance = 0.01
        self.defence = 0
        self.ai = CreatureAi(self)
        self.vision_radius = 7
        self.effect_list = []
        self.hunger_value = ' '
        self.cause_of_death = 'Plain old bad luck'
        self.corpse_nutrition = 0
        self.taste = 'bland'
        self.alive = True
        self.inventory = None
        self.inv_size = 10

    def set_maxhp(self, hp):
        self.maxhp = hp
        self.hp = self.maxhp

    def set_hp(self, hp):
        self.hp = hp

    def hurt(self, amnt):
        self.hp -= amnt

        if self.hp < 0:
            self.doAction('die')
            self.level.remove_creature(self)
            self.die()
            self.ai = None

    def set_maxhunger(self, hunger):
        self.maxhunger = hunger
        self.hunger = self.maxhunger

    def set_hunger(self, hunger):
        if hunger <= self.maxhunger and self.maxhunger != -1:
            self.hunger = hunger
        else:
            self.hunger = self.maxhunger

    def starve(self, amnt):
        self.hunger -= amnt

    def set_attack(self, attack):
        self.attack = attack

    def set_attack_effect(self,ae):
        self.attack_effect = ae

    def set_attack_effect_duration(self, dur):
        self.attack_effectduration = dur

    def set_crit_chance(self, chance):
        self.crit_chance = chance

    def attack_creature(self, creature):
        creature.ai.on_attacked(self)

        amnt = max(0, self.attack - creature.defence)
        r = random.random()

        if self.attack_effect is not None:
            creature.add_effect(self.attack_effect(self.attack_effectduration, creature))

        # check for crit
        if r < self.crit_chance:
            amnt * ((random.random() * 2) + 1)
            self.notify('You violently attack the %s for %d damage!' %(creature.type, amnt))
            creature.notify('The %s attacks you with great force for %d damage!!' %(self.type, amnt))
        else:
            self.notify("You attack the %s for %d damage." %(creature.type, amnt))
            creature.notify("The %s attacks you for %d damage." %(self.type, amnt))

        creature.hurt(amnt)

    def set_defence(self, defence):
        self.defence = defence

    def set_Ai(self, ai):
        self.ai = ai

    def set_vision_radius(self, radius):
        self.vision_radius = radius

    def can_see(self, x, y):
        self.ai.can_see(x, y)

    def add_effect(self, effect):
        self.effect_list.append(effect)

    def remove_effect(self, effect):
        self.effect_list.remove(effect)

    def die(self):
        self.alive = False
        corpse = Item(self.lbt, self.con, self.level, self.char, self.lbt.dark_grey)
        corpse.set_name('dead %s' %self.type)
        corpse.set_postion(self.x, self.y)
        corpse.set_nutrition(self.corpse_nutrition)
        corpse.set_taste(self.taste)
        self.level.items.append(corpse)

    def revive(self):
        self.alive = True
        self.hp = self.maxhp

    def activate_inventory(self):
        self.inventory = Inventory(self.inv_size, self)

    def pickup(self):
        item = self.level.check_for_items(self.x, self.y)
        print item

        if self.inventory.is_full() or item is None:
            self.doAction("grab at the ground")
        else:
            self.doAction("pick up a %s" %item.name)
            self.level.remove_item(item)
            self.inventory.add(item)

    def drop(self, item):
        if self.level.space_for_item(self.x, self.y):
            self.level.add_item(item, self.x, self.y)
            self.doAction('drop the %s' %item.name)
            self.inventory.remove(item)


    def set_inventory_size(self, size):
        self.inv_size = size

    def move(self, dx, dy):
        ux = self.x + dx
        uy = self.y + dy

        othercreature = self.level.check_for_creatures(ux, uy)

        if othercreature is not None:
            if othercreature is not self:
                self.attack_creature(othercreature)
        else:
            if self.ai is not None:
                self.ai.on_enter(ux, uy, self.level.map[ux][uy])
            else:
                self = None

    def eat(self, item):
        self.hunger += item.nutrition
        self.doAction('eat a %s' %item.name)
        if item.taste is not None:
            self.notify('Tastes %s.' %item.taste)

        self.inventory.remove(item)

    def set_taste(self, taste):
        self.taste = taste

    def set_corpse_nutrition(self, value):
        self.corpse_nutrition = value

    def notify(self, message):
        if self.ai is not None:
            self.ai.on_notify(str(message))
        else:
            self = None

    def doAction(self, message):
        r = 9
        for ox in range(-r, r+1):
            for oy in range(-r, r+1):
                if (ox*ox + oy*oy > r*r):
                    continue

                other_creature = self.level.check_for_creatures(self.x+ox, self.y+oy)

                if other_creature is None:
                    continue

                if other_creature == self:
                    other_creature.notify("You " + message + ".")
                else:
                    other_creature.notify(str("The %s %s.") %(self.type, makeSecondPerson(message)))


class Player(Creature):
    def __init__(self, lbt, con, level):
        char = '@'
        color = lbt.white

        super(Player, self).__init__(lbt, con, level, char, color)
        self.inventorymenu = InventoryMenu(lbt, con, 'Inventory', self)
        self.dropmenu = DropMenu(lbt, con, 'Drop items', self)
        self.eatmenu = EatMenu(lbt, con, 'Eat stuff', self)

    def show_inventory(self):
        self.inventorymenu.update(options=self.inventory, header = 'Inventory: %s/%s' %(self.inventory.get_fill(), self.inv_size))
        self.inventorymenu.draw()

    def show_drop_menu(self):
        if self.inventory.get_fill() == 0:
            self.dropmenu.update(options=self.inventory, header = 'Nothing to drop')
        else:
            itemlist = sorted(self.inventory.get_items(), key=lambda x: (x is None, x))
            self.dropmenu.update(options=itemlist, header = 'Drop items')
        self.dropmenu.draw()

    def show_eat_menu(self):
        if self.inventory.get_edible_items() == [None] * len(self.inventory.get_edible_items()):
            self.eatmenu.update(options = [None for i in range(10)], header = 'Nothing to eat...')

        else:
            self.eatmenu.update(options = self.inventory.get_edible_items(), header = 'Eat stuff')

        self.eatmenu.draw()