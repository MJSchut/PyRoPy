__author__ = 'Martijn Schut'

import random

from src.ai.CreatureAi import CreatureAi
from src.entities.Entity import Entity
from src.entities.items.Inventory import Inventory
from src.entities.items.Items import Item
from src.gui.GUI import DrinkMenu
from src.gui.GUI import DropMenu
from src.gui.GUI import EatMenu
from src.gui.GUI import EquipMenu
from src.gui.GUI import ExamineMenu
from src.gui.GUI import InventoryMenu
from src.gui.GUI import WearMenu


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
        self.cause_of_death = 'Plain old bad luck'
        self.alive = True
        self.blood_color = (255, 0, 0)  # Red

        self.maxhunger = -1
        self.hunger = -1
        self.hunger_value = ' '
        self.corpse_nutrition = 0
        self.taste = 'bland'

        self.attack = 0
        self.attack_effect = None
        self.attack_effectduration = 3
        self.crit_chance = 0.01

        self.defence = 0

        self.ai = CreatureAi(self)
        self.vision_radius = 11

        self.effect_list = []

        self.inventory = None
        self.inv_size = 3
        self.limbs = []

    def set_maxhp(self, hp):
        self.maxhp = hp
        self.hp = self.maxhp

    def set_hp(self, hp):
        self.hp = hp

    def hurt(self, amnt):
        self.hp -= amnt
        # make tile bloody
        b_tile = self.level.get_tile(self.x, self.y)
        b_tile.front_color = self.blood_color
        b_tile2 = self.level.get_random_surrounding_tile(self.x, self.y)
        b_tile2.front_color = self.blood_color

        if self.hp < 0:
            self.doAction('die')
            self.level.remove_creature(self)
            self.die()

            self.ai = None

    def heal(self, amnt):
        if self.hp + amnt <= self.maxhp:
            self.hp += amnt

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
        item = None
        items = []
        amnt = max(0, self.attack - creature.get_defence())
        for limb in self.limbs:
            item = limb.holding
            if item is not None:
                amnt += (item.attack_val - creature.get_defence())
                items.append(item)
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

            for ii in range(0, len(items)):
                if items[ii].swings_to_break >= 1:
                    items[ii].swings_to_break -= 1
                    if items[ii].swings_to_break <= 0:
                        self.notify("The %s breaks into pieces!" %(items[ii].get_name()))
                        if items[ii].item_factory is not None:
                            items[ii].item_factory.make_shard(location=[self.x,self.y])
                        self.inventory.remove(items[ii])

        creature.hurt(amnt)

    def set_defence(self, defence):
        self.defence = defence

    def get_defence(self):
        idefence = 0
        for limb in self.limbs:
            if limb.wearing is not None:
                item = limb.wearing
                idefence += item.defence_val
        return self.defence + idefence

    def set_Ai(self, ai):
        self.ai = ai

    def set_vision_radius(self, radius):
        self.vision_radius = radius

    def can_see(self, x, y):
        return self.ai.can_see(x, y)

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

        if self.inventory.is_full() or item is None:
            self.doAction("grab at the ground")
        else:
            self.doAction("pick up a %s" %item.get_name())
            self.level.remove_item(item)
            self.inventory.add(item)
            if item.wear_effect is not None:
                item.wear_effect = item.wear_effect(item.wear_effect_duration, self)

    def drop(self, item):
        if self.level.space_for_item(self.x, self.y):
            self.level.add_item(item, self.x, self.y)
            self.doAction('drop the %s' %item.get_name())
            self.inventory.remove(item)


    def set_inventory_size(self, size):
        self.inv_size = size
        self.activate_inventory()

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
        if item.eat_effect is not None:
            self.add_effect(item.eat_effect)

        self.hunger += item.nutrition
        self.doAction('eat a %s' %item.get_name())
        if item.taste is not None:
            self.notify('Tastes %s.' %item.taste)

        self.inventory.remove(item)

    def drink(self, item):
        if item.drink_effect is not None:
            effect = item.drink_effect(item.drink_effect_duration, self)
            self.add_effect(effect)

        self.doAction('drink a %s' %item.get_name())
        self.inventory.remove(item)

    def set_taste(self, taste):
        self.taste = taste

    def set_corpse_nutrition(self, value):
        self.corpse_nutrition = value

    def add_limb(self, limb):
        self.limbs.append(limb)

        return limb

    def lose_limb(self, limb):
        self.limbs.remove(limb)

        return limb

    def get_random_limb(self):
        i = random.randint(0, len(self.limbs) - 1)

        if self.limbs[i] is not None:
            return self.limbs[i]
        else: return None

    def check_for_limb(self, limbtype):
        for limb in self.limbs:
            if type(limb) == limbtype:
                return True
        return False

    def get_limb_of_type(self, limbtype):
        for limb in self.limbs:
            if type(limb) == limbtype:
                return limb
        return None

    def wear(self, item):
        if item is None:
            return

        limbtowear = None
        for limb in self.limbs:
            if type(limb) == item.wearon:
                limbtowear = limb
                break

        if limbtowear is not None:
            self.wear_on_limbtype(item, type(limbtowear))
            self.inventory.sort()

    def wear_on_limbtype(self, item, limbtype):
        if item is None:
            return

        if not item.wearable:
            self.doAction('cannot wear a %s' %item.get_name())
            return

        if item.worn:
            self.take_off_item(item)
            return

        for limb in self.limbs:
            if type(limb) == limbtype and limb.wearing is None:
                limb.wearing = item
                self.doAction('put the %s on your %s' %(item.get_name(), limb.name))
                item.worn = True
                return

    def equip_to_limbtype(self, item, limbtype):
        if item is None:
            return

        if not item.holdable:
            self.doAction('cannot equip a %s' %item.get_name())
            return

        if item.equipped:
            self.unequip_item(item)
            return

        for limb in self.limbs:
            if type(limb) == limbtype and limb.holding is None:
                limb.holding = item
                self.doAction('equip the %s to %s' %(item.get_name(), limb.name))
                item.equipped = True
                return

    def unequip_item(self, item):
        if item is None:
            return

        for limb in self.limbs:
            if limb.holding is item:
                self.doAction('unequip the %s' %item.get_name())
                limb.holding = None
                item.equipped = False

    def take_off_item(self, item):
        if item is None:
            return

        for limb in self.limbs:
            if limb.wearing is item:
                self.doAction('take off the %s' %item.get_name())
                limb.wearing = None
                item.worn = False

    def notify(self, message):
        if self.ai is not None:
            self.ai.on_notify(str(message))
        else:
            self = None

    # TODO: a to an
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
        char = '@'  # Player character
        color = (255, 255, 255)  # White

        super(Player, self).__init__(lbt, con, level, char, color)
        self.inventorymenu = InventoryMenu(lbt, con, 'Inventory', self)
        self.dropmenu = DropMenu(lbt, con, 'Drop items', self)
        self.eatmenu = EatMenu(lbt, con, 'Eat stuff', self)
        self.drinkmenu = DrinkMenu(lbt, con, 'Drink stuff', self)
        self.equipmenu = EquipMenu(lbt, con, 'Equip stuff', self)
        self.wearmenu = WearMenu(lbt, con, 'Wear stuff', self)
        self.examinemenu = ExamineMenu(lbt, con, self, 'examine', self.x, self.y)

    def show_examine_menu(self):
        self.examinemenu.orix = self.examinemenu.curx = self.x
        self.examinemenu.oriy = self.examinemenu.cury = self.y

        while True:
            self.examinemenu.draw()
            self.examinemenu.update()

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
            self.eatmenu.update(options = [None for i in range(self.inv_size)], header = 'Nothing to eat...')

        else:
            self.eatmenu.update(options = self.inventory.get_edible_items(), header = 'Eat stuff')

        self.eatmenu.draw()

    def show_drink_menu(self):
        if self.inventory.get_drinkable_items() == [None] * len(self.inventory.get_drinkable_items()):
            self.drinkmenu.update(options = [None for i in range(self.inv_size)], header = 'Nothing to drink...')

        else:
            self.drinkmenu.update(options = self.inventory.get_drinkable_items(), header = 'Drink stuff')

        self.drinkmenu.draw()

    def show_equip_menu(self):
        if self.inventory.get_equipable_items() == [None] * len(self.inventory.get_equipable_items()):
            self.equipmenu.update(options = [None for i in range(self.inv_size)], header = 'Nothing to equip')
        else:
            self.equipmenu.update(options = self.inventory.get_equipable_items(), header = 'Equip stuff')

        self.equipmenu.draw()

    def show_wear_menu(self):
        if self.inventory.get_wearable_items() == [None] * len(self.inventory.get_wearable_items()):
            self.wearmenu.update(options = [None for i in range(self.inv_size)], header = 'Nothing to wear')
        else:
            self.wearmenu.update(options = self.inventory.get_wearable_items(), header = 'Wear stuff')

        self.wearmenu.draw()
