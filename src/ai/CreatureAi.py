__author__ = 'Martijn Schut'

import math
import random

from src.util.Line import Line


class CreatureAi(object):
    # base AI class
    def __init__(self, creature):
        self.player = None
        self.creature = creature
        self.level = None  # Will be set by factory

    def on_enter(self, x, y, tile):
        if not tile.blocked:
            self.creature.set_postion(x,y)

    def on_update(self):
        if self.creature.hunger > 0 and self.creature.maxhunger > 0:
            # Slow down hunger decrease - only decrement every few turns
            if random.random() < 0.1:  # ~10% chance to decrease hunger each turn
                self.creature.hunger -= 1
            
            rat = (float(self.creature.hunger)/ float(self.creature.maxhunger))

            if rat < 0.05:
                self.creature.hunger_value = 'Starving!!'
            elif rat < 0.15:
                self.creature.hunger_value = 'Starving!'
            elif rat < 0.3:
                self.creature.hunger_value = 'Hungry'
            elif rat < 0.6:
                self.creature.hunger_value = 'Peckish'
            elif rat < 1:
                self.creature.hunger_value = ' '

            if 0.05 > rat < 0.15 and random.random() < 0.01:
                self.creature.doAction('feel hungry')

            if rat < 0.05 and random.random() < 0.1:
                self.creature.doAction('feel really hungry')

        if self.creature.hunger <= 0 < self.creature.maxhunger:
            # Reduce starvation damage
            self.creature.hurt(int(float(self.creature.maxhp / 20)))  # Changed from 10 to 20
            self.creature.doAction('starve')

        for effect in self.creature.effect_list:
            effect.on_update()

        if self.creature.inventory is not None:
            for item in self.creature.inventory.get_items():
                if item is None:
                    continue
                item.on_update()

    def on_attacked(self, attacker):
        pass

    def on_notify(self, message):
        # If this is a non-player creature and we have access to the player, send the message to them
        if self.creature.type != 'player' and self.level is not None:
            player = self.level.get_player()
            if player is not None and player.messages is not None:
                # Only show messages if the player can see the creature
                if player.can_see(self.creature.x, self.creature.y):
                    # Determine appropriate color based on message content
                    color_index = 1  # Default to white (index 1, after the pink)
                    
                    # Check for combat/damage related messages - use pink (index 0)
                    if any(keyword in message.lower() for keyword in ['attack', 'hit', 'hurt', 'damage', 'kill', 'die', 'pain', 'bleed', 'blood', 'wound', 'toxin', 'starve']):
                        color_index = 0
                    
                    # Add message with appropriate color index
                    player.messages[0].append(message)
                    player.messages[1].append(color_index)

    def can_see(self, x, y):
        # First check if the point is within vision radius
        distance = math.sqrt((self.creature.x-x)**2 + (self.creature.y-y)**2)
        if distance > self.creature.vision_radius:
            return False

        # Create a line from creature to target point
        n_line = Line(self.creature.x, self.creature.y, x, y)

        # Check each point in the line
        for point in n_line.get_points():
            # Skip the target point (we want to see it even if it's blocked)
            if point.x == x and point.y == y:
                continue
                
            # If we hit a blocked tile, we can't see past it
            if self.creature.level.get_tile(point.x, point.y).blocked:
                return False
                
        return True

    def stupid_hunt(self):
        dx = self.player.x - self.creature.x
        dy = self.player.y - self.creature.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
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
            self.creature.notify(f"You see a {item.get_name()} lying here.")

    def on_notify(self, message):
        # Determine appropriate color based on message content
        color_index = 1  # Default to white (index 1, after the pink)
        
        # Check for combat/damage related messages - use pink (index 0)
        if any(keyword in message.lower() for keyword in ['attack', 'hit', 'hurt', 'damage', 'kill', 'die', 'pain', 'bleed', 'blood', 'wound', 'toxin', 'starve']):
            color_index = 0
        
        # Add message with appropriate color index
        self.messages[0].append(message)
        self.messages[1].append(color_index)


class EOozeAi(CreatureAi):
    def __init__(self, creature, factory):
        super(EOozeAi, self).__init__(creature)
        self.factory = factory

    def on_update(self):
        if random.random() < 0.4:
            new_x = self.creature.x + random.randint(-1, 1)
            new_y = self.creature.y + random.randint(-1, 1)

            if self.factory.level.space_for_creature(new_x, new_y):
                self.factory.make_eooze()

class FungusAi(CreatureAi):
    # A stationary creature that occasionally spawns new copies of itself

    def __init__(self,creature, factory):
        super(FungusAi, self).__init__(creature)
        self.has_spread = random.randint(0, 3)

        self.factory = factory

    def on_update(self):
        if self.has_spread > 0 and random.random() < 0.01:
            self.has_spread -= 1

            new_x = self.creature.x + random.randint(-5, 5)
            new_y = self.creature.y + random.randint(-5, 5)

            if self.factory.level.space_for_creature(new_x,new_y):
                # check for mutant fungus
                if random.random() < 0.02:
                    fungus = self.factory.make_blood_fungus()
                    fungus.x = new_x
                    fungus.y = new_y
                    self.creature.doAction('shake violently')
                    self.creature.doAction('release a cloud of red spores')
                elif random.random() < 0.02:
                    fungus = self.factory.make_husk_fungus()
                    fungus.x = new_x
                    fungus.y = new_y
                    self.creature.doAction('release a cloud of blue spores')
                else:
                    fungus = self.factory.make_fungus()
                    fungus.x = new_x
                    fungus.y = new_y
                    self.creature.doAction('release a spore')

class BloodFungusAi(CreatureAi):
    # Mutant fungus that'll counter-attack

    def __init__(self, creature, factory):
        super(BloodFungusAi, self).__init__(creature)
        self.factory = factory

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
                if creature.type == 'player':
                    creature.notify("You feel drained.")
                else:
                    creature.doAction('feel drained')
            elif r < 0.6:
                if creature.type == 'player':
                    creature.notify("You feel fatigued.")
                else:
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
                    self.player.notify("You feel your ears are ringing.")
                elif random.random() < 0.1:
                    self.player.notify("You feel blood dripping from your ears.")
                    self.player.hurt(1)

        else:
            if self.creature.vision_radius > 3:
                self.creature.doAction('turn into stone')
                self.creature.vision_radius = 3

