__author__ = 'Martijn Schut'

from src.entities.Entity import Entity
from src.ai.CreatureAi import CreatureAi

class Creature(Entity):
    def __init__ (self, lbt, con, level, char, color):
        super(Creature, self).__init__(lbt, con, level, char, color)
        self.maxhp = 3
        self.hp = self.maxhp
        self.maxhunger = -1
        self.hunger = -1
        self.attack = 0
        self.defence = 0
        self.ai = CreatureAi(self)

    def set_maxhp(self, hp):
        self.maxhp = hp
        self.hp = self.maxhp

    def set_hp(self, hp):
        self.hp = hp

    def set_maxhunger(self, hunger):
        self.maxhunger = hunger
        self.hunger = self.maxhunger

    def set_hunger(self, hunger):
        if hunger <= self.maxhunger and self.maxhunger != -1:
            self.hunger = hunger
        else:
            self.hunger = self.maxhunger

    def set_attack(self, attack):
        self.attack = attack

    def set_defence(self, defence):
        self.defence = defence

    def set_Ai(self, ai):
        self.ai = ai

    def move(self, dx, dy):
        ux = self.x + dx
        uy = self.y + dy
        othercreature = self.level.check_for_creatures(ux, uy)

        if othercreature is not None:
            self.attack_creature(othercreature)
        else:
            self.ai.on_enter(ux, uy, self.level.map[ux][uy])

    def attack_creature(self, creature):
        self.level.remove(creature)

class Player(Creature):
    def __init__(self, lbt, con, level):
        char = '@'
        color = lbt.white
        super(Player, self).__init__(lbt, con, level, char, color)