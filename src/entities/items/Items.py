__author__ = 'Martijn Schut'

from src.entities.Entity import Entity
from src.entities.creatures.Limb import Hand


class Item(Entity):
    def __init__(self, lbt, con, level, char, color):
        super(Item, self).__init__(lbt, con, level, char, color)

        self.name = 'Unnamed artifact'
        self.nutrition = 0
        self.equipment = False
        self.equipto = None
        self.wearon = None
        self.attack_val = 0
        self.defence_val = 0
        self.taste = None
        self.holdable = False
        self.wearable = False
        self.equipped = False
        self.worn = False

    def get_name(self):
        return self.name

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

    def set_equip_to_hand(self, wearable = False):
        self.equipment = True
        self.holdable = True
        self.equipto = Hand
        self.wearable = wearable

        if self.wearable:
            self.wearon = Hand



