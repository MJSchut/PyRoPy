__author__ = 'Martijn Schut'

from src.entities.Entity import Entity
from src.entities.creatures.Limb import Hand


class Item(Entity):
    def __init__(self, lbt, con, level, char, color):
        super(Item, self).__init__(lbt, con, level, char, color)

        self.name = 'unnamed artifact'
        self.type = 'unremarkable thing'
        self.display_char = char  # Store the display character separately
        self.nutrition = 0
        self.equipment = False
        self.equip_to = None
        self.description = "Undefined"
        self.wear_on = None
        self.weight = 1
        self.attack_value = 0
        self.defence_val = 0
        self.taste = None
        self.eat_effect = None
        self.drink_effect = None
        self.drink_effect_duration = 2
        self.wear_effect = None
        self.wear_effect_duration = 0
        self.drinkable = False
        self.holdable = False
        self.wearable = False
        self.equipped = False
        self.worn = False
        self.identified = False
        self.item_factory = None
        self.swings_to_break = 0
        self.is_corpse = False
        self.is_food = False
        self.creature_type = None

    def get_name(self):
        if self.identified:
            return self.name
        elif self.is_corpse:
            return f"corpse of a {self.creature_type}"
        elif self.is_food:
            return f"piece of {self.creature_type} meat"
        elif self.nutrition > 0 or self.taste is not None:
            # For unidentified food items, show basic type
            if 'bread' in self.name.lower():
                return "bread"
            elif 'meat' in self.name.lower():
                return "meat"
            elif 'apple' in self.name.lower():
                return "apple"
            elif 'cheese' in self.name.lower():
                return "cheese"
            elif 'mushroom' in self.name.lower():
                return "mushroom"
            else:
                return "food"
        elif self.drinkable and hasattr(self, 'appearance'):
            # For unidentified potions, show appearance
            return self.appearance
        else:
            return self.type

    def set_nutrition(self, value):
        self.nutrition = value

    def set_taste(self, taste):
        self.taste = taste

    def set_equipment(self, val):
        self.equipment = val

    def set_attack_value(self, val):
        self.attack_value = val

    def set_defence_value(self, val):
        self.defence_val = val

    def set_drink_effect(self, val):
        self.drink_effect = val
        self.drinkable = True

    def set_appearance(self, char):
        """Set the display character for the item"""
        self.display_char = char
        self.char = char  # Update the Entity's char as well

    def set_equip_to(self, equipto, wearable = False):
        self.equipment = True
        self.holdable = True
        self.equip_to = equipto
        self.wearable = wearable

        if self.wearable:
            self.wear_on = equipto

    def set_wear_to(self, wearon):
        self.equipment = True
        self.wear_on = wearon
        self.wearable = True
        self.holdable = True
        self.equip_to = Hand

    def set_wear_effect(self, effect, duration = -1):
        self.wear_effect = effect
        self.wear_effect_duration = duration

    def on_update(self):
        if self.wear_effect is not None and self.worn:
            self.wear_effect.on_update()

    def set_description(self, param):
        self.description = param

    def set_wearable(self, param):
        self.wearable = True

    def identify(self):
        """Identify the item, revealing its true name and properties"""
        self.identified = True

    def on_equip(self, creature):
        """Called when the item is equipped"""
        self.identify()
        if self.wear_effect is not None:
            self.wear_effect = self.wear_effect(self.wear_effect_duration, creature)

    def on_wear(self, creature):
        """Called when the item is worn"""
        self.identify()
        if self.wear_effect is not None:
            self.wear_effect = self.wear_effect(self.wear_effect_duration, creature)

    def on_drink(self, creature):
        """Called when the item is drunk"""
        self.identify()
        if self.drink_effect is not None:
            effect = self.drink_effect(self.drink_effect_duration, creature)
            creature.add_effect(effect)
            creature.notify(f"You drink the {self.get_name()}.")

    def on_eat(self, creature):
        """Called when the item is eaten"""
        self.identify()
        if self.eat_effect is not None:
            effect = self.eat_effect(self.drink_effect_duration, creature)
            creature.add_effect(effect)
            
        # Give feedback about the taste (only here, not in Creatures.py)
        if self.taste:
            creature.notify(f"You eat the {self.name}. It tastes {self.taste}.")
            return True  # Signal that we've already sent a message
            
        return False  # No message sent

    def set_corpse(self, creature_type):
        """Set this item as a corpse of a specific creature type"""
        self.is_corpse = True
        self.creature_type = creature_type
        self.name = f"dead {creature_type}"
        self.type = f"corpse of a {creature_type}"

    def set_food(self, creature_type):
        """Set this item as food from a specific creature type"""
        self.is_food = True
        self.creature_type = creature_type
        self.name = f"{creature_type} meat"
        self.type = f"piece of {creature_type} meat"
