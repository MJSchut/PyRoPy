__author__ = 'Martijn Schut'

import random
import textwrap
import math

from src import constants
from src.util.Line import Line

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
            rat = (float(self.creature.hunger)/ float(self.creature.maxhunger))

            if rat < 0.05:
                self.creature.hunger_value = 'Starving!!!'
            elif rat < 0.15:
                self.creature.hunger_value = 'Starving!'
            elif rat < 0.3:
                self.creature.hunger_value = 'Hungry'
            elif rat < 0.6:
                self.creature.hunger_value = 'Peckish'
            elif rat < 1:
                self.creature.hunger_value = ' '

            if rat < 0.15 and random.random() < 0.1:
                self.creature.doAction('feel hungry')

            if rat < 0.05 and random.random() < 0.1:
                self.creature.doAction('feel really hungry')

        if self.creature.hunger <= 0 and self.creature.maxhunger > 0:
            self.creature.hurt(int(float(self.creature.maxhp / 10)))
            self.creature.doAction('starve')

        for effect in self.creature.effect_list:
            effect.on_update()

    def on_attacked(self, attacker):
        pass

    def on_notify(self, message):
        pass

    def can_see(self, x, y):
        if ((self.creature.x-x)**2 + (self.creature.y-y)**2 >
                    self.creature.vision_radius**2):
            return False;

        nLine = Line(self.creature.x, self.creature.y, x, y)

        for point in nLine.get_points():
            if not self.creature.level.get_tile(point.x, point.y).blocked or (point.x == x and point.y == y):
                continue

            return False
        return True

    def stupid_hunt(self):
        dx = self.player.x - self.creature.x
        dy = self.player.y - self.creature.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance is not 0:
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))
            self.creature.move(dx, dy)

    def smart_hunt(self):
        pass

    def wander(self):
        mx = int(random.random() * 3) - 1
        my = int(random.random() * 3) - 1
        self.creature.move(mx, my)

class PlayerAi(CreatureAi):
    def __init__(self, creature, messages, level):
        super(PlayerAi, self).__init__(creature)

        self.messages = messages
        self.level = level

    def on_enter(self, x, y, tile):
        super(PlayerAi, self).on_enter(x, y, tile)
        item = self.level.check_for_items(x, y)

        if item is not None:
            self.creature.doAction('see a %s lying here' %item.name)

    def on_notify(self, message):
        print self.messages
        message_lines = textwrap.wrap(message, constants.MSG_WIDTH)
        for x, line in enumerate(message_lines):
            self.messages[0].append(line)
            self.messages[1].append(0)

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
        if self.spreaded > 0 and random.random() < 0.01:
            self.spreaded -= 1

            newx = self.creature.x + random.randint(-5, 5)
            newy = self.creature.y + random.randint(-5, 5)

            if self.factory.level.space_for_creature(newx,newy):
                # check for mutant fungus
                if random.random() < 0.02:
                    fungus = self.factory.make_blood_fungus()
                    fungus.x = newx
                    fungus.y = newy
                    self.creature.doAction('shake violently')
                    self.creature.doAction('release a cloud of red spores')
                elif random.random() < 0.02:
                    fungus = self.factory.make_husk_fungus()
                    fungus.x = newx
                    fungus.y = newy
                    self.creature.doAction('release a cloud of blue spores')
                else:
                    fungus = self.factory.make_fungus()
                    fungus.x = newx
                    fungus.y = newy
                    self.creature.doAction('release a spore')

class BloodFungusAi(CreatureAi):
    # Mutant fungus that'll counter attack

    def __init__(self,creature, factory):
        super(BloodFungusAi, self).__init__(creature)

    def on_attacked(self, attacker):
        attacker.hurt(self.creature.attack)
        self.creature.doAction('release a toxin')

class HuskFungusAi(CreatureAi):
    # Mutant fungus that'll sap any creature's hunger if it gets within a certain range

    def __init__(self,creature, level):
        super(HuskFungusAi, self).__init__(creature)
        self.level = level

    def on_attacked(self, attacker):
        clist = self.level.check_for_creatures_in_range(self.creature.x, self.creature.y, 3, ignore = [self.creature])
        for creature in clist:
            creature.starve(random.randint(3, 7))

            r = random.random()
            if r < 0.3:
                creature.doAction('feel drained')
            elif r < 0.6:
                creature.doAction('feel fatigued')

class BatAi(CreatureAi):
    def __init__(self, creature):
        super(BatAi, self).__init__(creature)

    def on_update(self):
        super(BatAi, self).on_update()

        self.wander()
        self.wander()

class SnakeAi(CreatureAi):
    def __init__(self, creature):
        super(SnakeAi, self).__init__(creature)

    def on_update(self):
        super(SnakeAi, self).on_update()

        self.wander()

class GargoyleAi(CreatureAi):
    def __init__(self, creature, player):
        super(GargoyleAi, self).__init__(creature)
        self.player = player

    def on_update(self):
        super(GargoyleAi, self).on_update()

        if self.can_see(self.player.x, self.player.y):
            self.stupid_hunt()

            if self.creature.vision_radius == 3:
                self.creature.doAction('awaken and lunges towards you')
                if random.random() < 0.3:
                    self.creature.doAction('scream')
                elif random.random() < 0.6:
                    self.creature.doAction('shriek')
                else:
                    self.creature.doAction('wail')
                self.creature.vision_radius = 6

                if random.random() < 0.3:
                    self.player.doAction('feel your ears are ringing')
                elif random.random() < 0.1:
                    self.player.doAction('feel blood dripping from your ears')
                    self.player.hurt(1)

        else:
            if self.creature.vision_radius > 3:
                self.creature.doAction('turn into stone')
                self.creature.vision_radius = 3



