__author__ = 'Martijn Schut'

from src.entities.Entity import Entity
from src.entities.creatures.Limb import Hand


class Item(Entity):
    def __init__(self, lbt, con, level, char, color):
        super(Item, self).__init__(lbt, con, level, char, color)

        self.name = 'unnamed artifact'
        self.type = 'unremarkable thing'
        self.nutrition = 0
        self.equipment = False
        self.equipto = None
        self.wearon = None
        self.attack_val = 0
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
        self.identified = True

    def get_name(self):
        if self.identified:
            return self.name
        else: return self.type

    def set_nutrition(self, value):
        self.nutrition = value

    def set_taste(self, taste):
        self.taste = taste

    def set_equipment(self, val):
        self.equipment = val

    def set_attack_value(self, val):
        self.attack_val = val

    def set_defence_value(self, val):
        self.defence_val = val

    def set_drink_effect(self, val):
        self.drink_effect = val
        self.drinkable = True

    def set_appearance(self, name):
        self.type = name

    def set_equip_to(self, equipto, wearable = False):
        self.equipment = True
        self.holdable = True
        self.equipto = equipto
        self.wearable = wearable

        if self.wearable:
            self.wearon = equipto

    def set_wear_to(self, wearon):
        self.equipment = True
        self.wearon = wearon
        self.wearable = True
        self.holdable = True

    def set_wear_effect(self, effect, duration = -1):
        self.wear_effect = effect
        self.wear_effect_duration = duration

    def on_update(self):
        if self.wear_effect is not None and self.worn:
            self.wear_effect.on_update()




