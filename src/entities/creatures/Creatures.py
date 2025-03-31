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
        self.vision_radius = 0  # Initialize to 0, will be set by config

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
        items = []
        amnt = max(0, self.attack - creature.get_defence())
        for limb in self.limbs:
            item = limb.holding
            if item is not None:
                amnt += (item.attack_value - creature.get_defence())
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
        # If AI is None (dead), can't see anything
        if self.ai is None:
            return False
        return self.ai.can_see(x, y)

    def add_effect(self, effect):
        self.effect_list.append(effect)

    def remove_effect(self, effect):
        self.effect_list.remove(effect)

    def die(self):
        self.alive = False
        # Use RGB tuple instead of tcod constant to avoid FutureWarning
        corpse = Item(self.lbt, self.con, self.level, self.char, (95, 95, 95))  # dark grey
        corpse.set_name('dead %s' %self.type)
        corpse.set_postion(self.x, self.y)
        
        # Enhance corpse nutrition - all corpses are now more nutritious
        if self.corpse_nutrition == 0:
            # Default nutrition value for corpses with none specified
            corpse.set_nutrition(max(10, int(self.maxhp / 3)))
        else:
            corpse.set_nutrition(self.corpse_nutrition)
            
        # All corpses have a taste now
        if self.taste == 'bland' or self.taste is None:
            tastes = ['chewy', 'gamey', 'stringy', 'odd', 'meaty', 'tender']
            corpse.set_taste(random.choice(tastes))
        else:
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

        other_creature = self.level.check_for_creatures(ux, uy)

        if other_creature is not None:
            if other_creature is not self:
                self.attack_creature(other_creature)
        else:
            if self.ai is not None:
                self.ai.on_enter(ux, uy, self.level.map[ux][uy])

    def eat(self, item):
        if item.eat_effect is not None:
            self.add_effect(item.eat_effect)

        # Apply the nutrition with a bonus to make eating more worthwhile
        nutrition_bonus = int(item.nutrition * 0.5)  # 50% bonus
        total_nutrition = item.nutrition + nutrition_bonus
        
        # Cap nutrition at maximum hunger
        if self.hunger + total_nutrition > self.maxhunger:
            self.hunger = self.maxhunger
        else:
            self.hunger += total_nutrition
            
        # Display eat message
        self.doAction('eat a %s' %item.get_name())
        
        # Health bonus from eating
        if random.random() < 0.3:  # 30% chance to heal from food
            heal_amount = max(1, int(total_nutrition / 10))
            self.heal(heal_amount)
            self.notify("The food restores some of your strength.")
            
        if item.taste is not None:
            self.notify('Tastes %s.' %item.taste)

        self.inventory.remove(item)

    def drink(self, item):
        if item.drink_effect is not None:
            # Create a new instance of the effect with proper duration and target
            try:
                effect = item.drink_effect(item.drink_effect_duration, self)
                self.add_effect(effect)
                self.notify(f"You feel the effects of the {item.get_name()}.")
            except Exception as e:
                # Fallback if the effect creation fails
                self.notify(f"You drink the {item.get_name()} but nothing happens.")
                print(f"Effect error: {e}")

        self.doAction(f'drink a {item.get_name()}')
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

    # TODO: a to an
    def doAction(self, message):
        r = 9
        for ox in range(-r, r+1):
            for oy in range(-r, r+1):
                if ox*ox + oy*oy > r*r:
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
        super(Player, self).__init__(lbt, con, level, '@', (255, 255, 255))
        self._in_menu = False
        self.messages = None
        print(f"Creating player at ({self.x}, {self.y})")  # Debug print
        self.type = 'player'
        self.name = 'Player'
        self.inv_size = 20  # Set inventory size before activating
        self.activate_inventory()  # Activate inventory before creating menus
        
        # Initialize menus with empty lists first
        self.inventorymenu = InventoryMenu(lbt, con, 'Inventory', [])
        self.dropmenu = DropMenu(lbt, con, 'Drop items', [])
        self.eatmenu = EatMenu(lbt, con, 'Eat stuff', [])
        self.drinkmenu = DrinkMenu(lbt, con, 'Drink stuff', [])
        self.equipmenu = EquipMenu(lbt, con, 'Equip stuff', [])
        self.wearmenu = WearMenu(lbt, con, 'Wear stuff', [])
        self.examinemenu = ExamineMenu(lbt, con, self, 'examine', self.x, self.y)
        
        # Update menus with actual inventory
        self.inventorymenu.options = self.inventory
        self.dropmenu.options = self.inventory
        self.eatmenu.options = self.inventory.get_edible_items()
        self.drinkmenu.options = self.inventory.get_drinkable_items()
        self.equipmenu.options = self.inventory.get_equipable_items()
        self.wearmenu.options = self.inventory.get_wearable_items()

    @property
    def in_menu(self):
        return self._in_menu

    @in_menu.setter
    def in_menu(self, value):
        self._in_menu = value

    def draw(self, wx, wy):
        super(Player, self).draw(wx, wy)

    def show_examine_menu(self):
        self.examinemenu.orix = self.examinemenu.curx = self.x
        self.examinemenu.oriy = self.examinemenu.cury = self.y

        while True:
            self.examinemenu.draw()
            self.examinemenu.update()

    def show_inventory(self):
        self._in_menu = True
        self.inventorymenu.header = 'Inventory: %s/%s' %(self.inventory.get_fill(), self.inv_size)
        self.inventorymenu.options = self.inventory
        choice = self.inventorymenu.draw()
        if choice is not None:
            index = ord(choice) - ord('a')
            if 0 <= index < len(self.inventory.get_items()):
                item = self.inventory.get_items()[index]
                if item is not None:
                    self.notify(f"Selected {item.get_name()}")
        self.in_menu = False

    def show_drop_menu(self):
        self.in_menu = True
        if self.inventory.get_fill() == 0:
            self.dropmenu.header = 'Nothing to drop'
            self.dropmenu.options = [None for _ in range(self.inv_size)]
        else:
            self.dropmenu.header = 'Drop items'
            self.dropmenu.options = sorted(self.inventory.get_items(), key=lambda x: x is None)
        
        choice = self.dropmenu.draw()
        if choice is not None:
            index = ord(choice) - ord('a')
            if 0 <= index < len(self.inventory.get_items()):
                item = self.inventory.get_items()[index]
                if item is not None:
                    self.drop(item)
        self.in_menu = False

    def show_drink_menu(self):
        self.in_menu = True
        if self.inventory.get_drinkable_items() == [None] * len(self.inventory.get_drinkable_items()):
            self.drinkmenu.header = 'Nothing to drink...'
            self.drinkmenu.options = [None for _ in range(self.inv_size)]
        else:
            self.drinkmenu.header = 'Drink stuff'
            self.drinkmenu.options = self.inventory.get_drinkable_items()

        choice = self.drinkmenu.draw()
        if choice is not None:
            index = ord(choice) - ord('a')
            if 0 <= index < len(self.inventory.get_drinkable_items()):
                item = self.inventory.get_drinkable_items()[index]
                if item is not None:
                    self.drink(item)
        self.in_menu = False

    def show_eat_menu(self):
        self.in_menu = True
        if self.inventory.get_edible_items() == [None] * len(self.inventory.get_edible_items()):
            self.eatmenu.header = 'Nothing to eat...'
            self.eatmenu.options = [None for _ in range(self.inv_size)]
        else:
            self.eatmenu.header = 'Eat stuff'
            self.eatmenu.options = self.inventory.get_edible_items()

        choice = self.eatmenu.draw()
        if choice is not None:
            index = ord(choice) - ord('a')
            if 0 <= index < len(self.inventory.get_edible_items()):
                item = self.inventory.get_edible_items()[index]
                if item is not None:
                    self.eat(item)
        self.in_menu = False

    def show_equip_menu(self):
        self.in_menu = True
        if self.inventory.get_equipable_items() == [None] * len(self.inventory.get_equipable_items()):
            self.equipmenu.header = 'Nothing to equip'
            self.equipmenu.options = [None for _ in range(self.inv_size)]
        else:
            self.equipmenu.header = 'Equip stuff'
            self.equipmenu.options = self.inventory.get_equipable_items()

        choice = self.equipmenu.draw()
        if choice is not None:
            index = ord(choice) - ord('a')
            if 0 <= index < len(self.inventory.get_equipable_items()):
                item = self.inventory.get_equipable_items()[index]
                if item is not None:
                    self.equip(item)
        self.in_menu = False

    def show_wear_menu(self):
        self.in_menu = True
        if self.inventory.get_wearable_items() == [None] * len(self.inventory.get_wearable_items()):
            self.wearmenu.header = 'Nothing to wear'
            self.wearmenu.options = [None for i in range(self.inv_size)]
        else:
            self.wearmenu.header = 'Wear stuff'
            self.wearmenu.options = self.inventory.get_wearable_items()

        choice = self.wearmenu.draw()
        if choice is not None:
            index = ord(choice) - ord('a')
            if 0 <= index < len(self.inventory.get_wearable_items()):
                item = self.inventory.get_wearable_items()[index]
                if item is not None:
                    self.wear(item)
        self.in_menu = False

    def equip(self, item):
        """Equip an item (weapon) from inventory"""
        if item and item in self.inventory.get_items():
            # Get the appropriate limb type from the item
            if hasattr(item, 'wearon'):
                limb_type = item.wear_on
                self.equip_to_limbtype(item, limb_type)
                return True
            else:
                self.notify(f"You can't figure out how to equip the {item.get_name()}")
                return False
        return False
        
    def wear(self, item):
        """Wear an item (armor) from inventory"""
        if item and item in self.inventory.get_items():
            # Get the appropriate limb type from the item
            if hasattr(item, 'wearon'):
                limb_type = item.wearon
                self.wear_on_limbtype(item, limb_type)
                return True
            else:
                self.notify(f"You can't figure out how to wear the {item.get_name()}")
                return False
        return False

    def doAction(self, message):
        if self.messages is not None:
            self.notify(message)
