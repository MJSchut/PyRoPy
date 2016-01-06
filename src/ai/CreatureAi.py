__author__ = 'Martijn Schut'

import random
import textwrap
from src import constants

class CreatureAi(object):
    # base ai class
    def __init__(self, creature):
        self.creature = creature

    def on_enter(self, x, y, tile):
        if not tile.blocked:
            self.creature.set_postion(x,y)

    def on_update(self):
        if self.creature.hunger > 0 and self.creature.maxhunger > 0:
            self.creature.hunger -= 1

    def on_attacked(self, attacker):
        pass

    def on_notify(self, message):
        pass

    def wander(self):
        mx = int(random.random() * 3) - 1
        my = int(random.random() * 3) - 1
        self.creature.move(mx, my);

class PlayerAi(CreatureAi):
    def __init__(self, creature, messages):
        super(PlayerAi, self).__init__(creature)

        self.messages = messages

    def on_notify(self, message):
        message_lines = textwrap.wrap(message, constants.MSG_WIDTH)
        for line in message_lines:
            self.messages.append(line)

            if len(self.messages) == constants.MSG_HEIGHT:
                del self.messages[0]

class FungusAi(CreatureAi):
    # A stationary creature that occasionally spawns new copies of itself

    # TODO: spawn mutant versions of self that are more aggressive

    def __init__(self,creature, factory):
        super(FungusAi, self).__init__(creature)
        self.spreaded = random.randint(0,3)
        self.factory = factory

    def on_update(self):
        super(FungusAi, self).on_update()
        if self.spreaded <= 0 and random.random() < 0.005:
            self.spreaded = random.randint(0,3)

        if self.spreaded > 0 and random.random() < 0.01:
            self.spreaded -= 1

            newx = self.creature.x + random.randint(-5, 5)
            newy = self.creature.y + random.randint(-5, 5)

            if self.factory.level.is_empty(newx,newy):
                # check for mutant fungus
                if random.random() < 0.01:
                    fungus = self.factory.make_blood_fungus()
                    fungus.x = newx
                    fungus.y = newy
                    self.creature.doAction('shake violently')
                    self.creature.doAction('release a cloud of red spores')
                elif random.random() < 0.01:
                    fungus = self.factory.make_husk_fungus()
                    fungus.x = newx
                    fungus.y = newy
                    self.creature.doAction('release a cloud of blue spores')
                else:
                    fungus = self.factory.make_fungus()
                    fungus.x = newx
                    fungus.y = newy
                    fungus.ai.spreaded = self.spreaded
                    self.creature.doAction('releases a spore')

class BloodFungusAi(CreatureAi):
    # Mutant fungus that'll attack the player

    # TODO: implement
    def __init__(self,creature, factory):
        super(BloodFungusAi, self).__init__(creature)

class HuskFungusAi(CreatureAi):
    # Mutant fungus that'll sap any creature's hunger if it gets within a certain range

    # TODO: implement
    def __init__(self,creature, factory):
        super(HuskFungusAi, self).__init__(creature)

class BatAi(CreatureAi):
    def __init__(self, creature):
        super(BatAi, self).__init__(creature)

    def on_update(self):
        self.wander()
        self.wander()

