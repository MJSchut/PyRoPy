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

    def hurt(self, amnt):
        self.hp -= amnt

        if self.hp < 0:
            self.doAction('die')
            self.level.remove(self)

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
            if othercreature is not self:
                self.attack_creature(othercreature)
        else:
            self.ai.on_enter(ux, uy, self.level.map[ux][uy])

    def notify(self, message):
        self.ai.on_notify(str(message))

    def attack_creature(self, creature):
        creature.ai.on_attacked(self)

        amnt = max(0, self.attack - creature.defence)

        self.notify("You attack the %s for %d damage." %(creature.type, amnt));
        creature.notify("The %s attacks you for %d damage." %(self.type, amnt));

        creature.hurt(amnt)

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

def makeSecondPerson(text):
    new_text_array = text.split(" ")
    new_text_array[0] += "s"

    new_text = " ".join(new_text_array)

    return new_text


def sap_creature(self, creature, value):
    if creature.maxhunger > 0:
        amnt = creature.hunger - abs(value)
        creature.set_hunger(amnt)

class Player(Creature):
    def __init__(self, lbt, con, level):
        char = '@'
        color = lbt.white
        super(Player, self).__init__(lbt, con, level, char, color)