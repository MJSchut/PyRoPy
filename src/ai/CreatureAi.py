__author__ = 'Martijn Schut'

import random
import textwrap
import math

from src import constants
from src.effects.Effects import PoisonEffect
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

        if self.creature.hunger <= 0 and self.creature.maxhunger > 0:
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
            self.creature.doAction('see a %s lying here' %item.get_name())

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
            newx = self.creature.x + random.randint(-1, 1)
            newy = self.creature.y + random.randint(-1, 1)

            if self.factory.level.space_for_creature(newx, newy):
                self.factory.make_eooze()

class FungusAi(CreatureAi):
    # A stationary creature that occasionally spawns new copies of itself

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

class DiggerAi(CreatureAi):
    def __init__(self, creature, level):
        super(DiggerAi, self).__init__(creature)
        self.level = level
        self.dig_cooldown = 0
    
    def on_update(self):
        super(DiggerAi, self).on_update()
        
        # Wander randomly
        self.wander()
        
        # Sometimes dig through walls
        if self.dig_cooldown <= 0 and random.random() < 0.1:
            # Choose a direction
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            target_x = self.creature.x + dx
            target_y = self.creature.y + dy
            
            # Only dig if the target is a wall
            if self.level.is_valid(target_x, target_y) and self.level.get_tile(target_x, target_y).blocked:
                self.level.dig(target_x, target_y)
                self.creature.doAction('dig through the wall')
                self.dig_cooldown = 20  # Wait 20 turns before digging again
        
        if self.dig_cooldown > 0:
            self.dig_cooldown -= 1

class JumperAi(CreatureAi):
    def __init__(self, creature):
        super(JumperAi, self).__init__(creature)
        self.jump_cooldown = 0
    
    def on_update(self):
        super(JumperAi, self).on_update()
        
        # Normally move like other creatures
        if self.jump_cooldown > 0:
            self.wander()
            self.jump_cooldown -= 1
        else:
            # 20% chance to jump
            if random.random() < 0.2:
                # Jump 2-3 spaces in a random direction
                jump_distance = random.randint(2, 3)
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                
                # Make sure we don't just stand still
                while dx == 0 and dy == 0:
                    dx = random.randint(-1, 1)
                    dy = random.randint(-1, 1)
                
                # Calculate target position
                target_x = self.creature.x + (dx * jump_distance)
                target_y = self.creature.y + (dy * jump_distance)
                
                # Only jump if the target is walkable
                if self.creature.level.is_valid(target_x, target_y) and not self.creature.level.get_tile(target_x, target_y).blocked:
                    old_x, old_y = self.creature.x, self.creature.y
                    self.creature.set_postion(target_x, target_y)
                    self.creature.doAction('leap through the air')
                    self.jump_cooldown = 10  # Wait 10 turns before jumping again
                else:
                    self.wander()
            else:
                self.wander()

class HunterAi(CreatureAi):
    def __init__(self, creature, level):
        super(HunterAi, self).__init__(creature)
        self.level = level
        self.target = None
        self.target_type = 'fungus'  # Default to hunting fungus
    
    def on_update(self):
        super(HunterAi, self).on_update()
        
        # Look for prey if we don't have a target or randomly switch targets
        if self.target is None or random.random() < 0.05:
            self._find_target()
        
        # If we have a target, hunt it
        if self.target and self.target.alive:
            # Check if target is still in sight
            if self.can_see(self.target.x, self.target.y):
                # Move towards target
                dx = 0
                dy = 0
                if self.target.x < self.creature.x:
                    dx = -1
                elif self.target.x > self.creature.x:
                    dx = 1
                
                if self.target.y < self.creature.y:
                    dy = -1
                elif self.target.y > self.creature.y:
                    dy = 1
                
                self.creature.move(dx, dy)
                
                # If adjacent, attack
                if (abs(self.target.x - self.creature.x) <= 1 and 
                    abs(self.target.y - self.creature.y) <= 1):
                    self.creature.doAction(f'attack the {self.target.type}')
                    self.target.hurt(self.creature.attack)
            else:
                # Lost sight of target
                self.target = None
                self.wander()
        else:
            # No target, just wander
            self.wander()
    
    def _find_target(self):
        # Find all creatures in vision range
        for creature in self.level.creatures:
            # Skip self
            if creature == self.creature:
                continue
            
            # Skip if not the type we hunt
            if self.target_type not in creature.type:
                continue
            
            # Check if in vision range
            distance = ((self.creature.x - creature.x) ** 2 + 
                       (self.creature.y - creature.y) ** 2) ** 0.5
            if distance <= self.creature.vision_radius:
                if self.can_see(creature.x, creature.y):
                    self.target = creature
                    self.creature.doAction(f'spot a {creature.type}')
                    return

class MimicAi(CreatureAi):
    def __init__(self, creature):
        super(MimicAi, self).__init__(creature)
        self.revealed = False
        self.original_char = creature.char
        self.original_color = creature.color
    
    def on_update(self):
        super(MimicAi, self).on_update()
        
        # Mimics don't move when disguised
        if not self.revealed:
            pass
        else:
            # When revealed, chase any creature that attacked it
            self.wander()
    
    def on_attacked(self, attacker):
        if not self.revealed:
            self.revealed = True
            self.creature.char = self.original_char
            self.creature.color = self.original_color
            self.creature.doAction('reveal its true form')
            # Counter-attack
            attacker.hurt(self.creature.attack)

class ShadowAi(CreatureAi):
    def __init__(self, creature, player):
        super(ShadowAi, self).__init__(creature)
        self.player = player
        self.visible = False
    
    def on_update(self):
        super(ShadowAi, self).on_update()
        
        # Only visible/active at night or in darkness
        player_vision = self.player.vision_radius
        distance_to_player = ((self.creature.x - self.player.x) ** 2 + 
                            (self.creature.y - self.player.y) ** 2) ** 0.5
        
        # If player is nearby but not too close, become active
        if distance_to_player <= player_vision and distance_to_player > 2:
            if not self.visible:
                self.creature.doAction('materialize from the shadows')
                self.visible = True
            
            # Move toward player
            if self.player.x < self.creature.x:
                dx = -1
            elif self.player.x > self.creature.x:
                dx = 1
            else:
                dx = 0
                
            if self.player.y < self.creature.y:
                dy = -1
            elif self.player.y > self.creature.y:
                dy = 1
            else:
                dy = 0
                
            self.creature.move(dx, dy)
        else:
            # Too far or too close, fade away
            if self.visible:
                self.creature.doAction('fade back into the shadows')
                self.visible = False

class PoisonousAi(CreatureAi):
    def __init__(self, creature, factory):
        super(PoisonousAi, self).__init__(creature)
        self.factory = factory
    
    def on_update(self):
        super(PoisonousAi, self).on_update()
        self.wander()
    
    def on_attacked(self, attacker):
        # Chance to poison attacker
        if random.random() < 0.4:
            self.creature.doAction('release poison')
            if hasattr(attacker, 'add_effect'):
                poison_effect = PoisonEffect(attacker, 5)
                attacker.add_effect(poison_effect)
                attacker.doAction('feel poison coursing through their veins')

class PackHunterAi(CreatureAi):
    def __init__(self, creature, level):
        super(PackHunterAi, self).__init__(creature)
        self.level = level
        self.pack = []
        self.target = None
        self.leader = True  # First one created is the leader
    
    def on_update(self):
        super(PackHunterAi, self).on_update()
        
        # Find pack members if we haven't already
        if not self.pack:
            self._find_pack()
        
        # Leader behavior
        if self.leader:
            # Look for target if we don't have one
            if self.target is None or not self.target.alive:
                self._find_target()
            
            # If we have a target, hunt it
            if self.target and self.target.alive:
                # Move towards target
                dx = 0
                dy = 0
                if self.target.x < self.creature.x:
                    dx = -1
                elif self.target.x > self.creature.x:
                    dx = 1
                
                if self.target.y < self.creature.y:
                    dy = -1
                elif self.target.y > self.creature.y:
                    dy = 1
                
                self.creature.move(dx, dy)
                
                # If adjacent, attack
                if (abs(self.target.x - self.creature.x) <= 1 and 
                    abs(self.target.y - self.creature.y) <= 1):
                    self.creature.doAction(f'attack the {self.target.type}')
                    self.target.hurt(self.creature.attack)
            else:
                # No target, just wander
                self.wander()
        else:
            # Follower behavior - find nearest pack member and move towards them
            nearest_member = None
            min_distance = float('inf')
            
            for member in self.pack:
                if member == self.creature:
                    continue
                    
                distance = ((self.creature.x - member.x) ** 2 + 
                           (self.creature.y - member.y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_member = member
            
            if nearest_member and min_distance > 3:  # Don't get too close
                # Move towards nearest member
                dx = 0
                dy = 0
                if nearest_member.x < self.creature.x:
                    dx = -1
                elif nearest_member.x > self.creature.x:
                    dx = 1
                
                if nearest_member.y < self.creature.y:
                    dy = -1
                elif nearest_member.y > self.creature.y:
                    dy = 1
                
                self.creature.move(dx, dy)
            else:
                self.wander()
    
    def _find_pack(self):
        # Find all creatures of same type in vision range
        for creature in self.level.creatures:
            # Skip self
            if creature == self.creature:
                continue
            
            # Only include same type
            if creature.type != self.creature.type:
                continue
            
            self.pack.append(creature)
            
            # If we find another with leader=True, make this one a follower
            if hasattr(creature.ai, 'leader') and creature.ai.leader:
                self.leader = False
    
    def _find_target(self):
        # Hunt the player or other large creatures
        for creature in self.level.creatures:
            # Skip self and pack members
            if creature == self.creature or creature in self.pack:
                continue
            
            # Only target larger creatures
            if creature.type == 'player' or 'fungus' in creature.type:
                # Check if in vision range
                distance = ((self.creature.x - creature.x) ** 2 + 
                           (self.creature.y - creature.y) ** 2) ** 0.5
                if distance <= self.creature.vision_radius:
                    if self.can_see(creature.x, creature.y):
                        self.target = creature
                        self.creature.doAction(f'howl at the {creature.type}')
                        return

class TrapperAi(CreatureAi):
    def __init__(self, creature):
        super(TrapperAi, self).__init__(creature)
        self.hiding = True
        self.hide_cooldown = 0
        self.original_char = creature.char
        self.original_color = creature.color
    
    def on_update(self):
        super(TrapperAi, self).on_update()
        
        if self.hiding:
            # Don't move while hiding
            pass
        else:
            # When revealed, move around
            self.wander()
            
            # Eventually go back into hiding
            self.hide_cooldown -= 1
            if self.hide_cooldown <= 0:
                self.hiding = True
                self.creature.char = '.'  # Look like floor
                self.creature.color = (127, 127, 127)  # Grey
                self.creature.doAction('burrow into the ground')
    
    def on_enter(self, x, y, tile):
        if self.hiding:
            # Spring the trap!
            self.hiding = False
            self.creature.char = self.original_char
            self.creature.color = self.original_color
            self.creature.doAction('spring out from hiding!')
            self.hide_cooldown = 20  # Wait 20 turns before hiding again
            
            # Try to attack whatever stepped on us
            creature = self.creature.level.check_for_creatures(x, y)
            if creature and creature != self.creature:
                creature.hurt(self.creature.attack)
        else:
            super(TrapperAi, self).on_enter(x, y, tile)

class ScavengerAi(CreatureAi):
    def __init__(self, creature, level):
        super(ScavengerAi, self).__init__(creature)
        self.level = level
        self.target_item = None
    
    def on_update(self):
        super(ScavengerAi, self).on_update()
        
        # Look for items if we don't have a target
        if self.target_item is None:
            self._find_item()
        
        # If we have a target item, go to it
        if self.target_item:
            # Check if item still exists
            if self.target_item not in self.level.items:
                self.target_item = None
                self.wander()
                return
            
            # Move towards item
            dx = 0
            dy = 0
            if self.target_item.x < self.creature.x:
                dx = -1
            elif self.target_item.x > self.creature.x:
                dx = 1
            
            if self.target_item.y < self.creature.y:
                dy = -1
            elif self.target_item.y > self.creature.y:
                dy = 1
            
            self.creature.move(dx, dy)
            
            # If at item location, pick it up (destroy it)
            if (self.target_item.x == self.creature.x and 
                self.target_item.y == self.creature.y):
                self.creature.doAction(f'consume the {self.target_item.get_name()}')
                self.level.remove_item(self.target_item)
                self.target_item = None
                
                # Heal a bit from eating
                self.creature.hp = min(self.creature.hp + 1, self.creature.maxhp)
        else:
            # No target, just wander
            self.wander()
    
    def _find_item(self):
        # Find nearest item
        nearest_item = None
        min_distance = float('inf')
        
        for item in self.level.items:
            distance = ((self.creature.x - item.x) ** 2 + 
                       (self.creature.y - item.y) ** 2) ** 0.5
            if distance < min_distance and self.can_see(item.x, item.y):
                min_distance = distance
                nearest_item = item
        
        if nearest_item:
            self.target_item = nearest_item
            self.creature.doAction(f'spot a {nearest_item.get_name()}')

class SlimeAi(CreatureAi):
    def __init__(self, creature, level):
        super(SlimeAi, self).__init__(creature)
        self.level = level
        self.split_threshold = creature.maxhp // 2
        self.split_cooldown = 0
    
    def on_update(self):
        super(SlimeAi, self).on_update()
        
        # Move randomly
        self.wander()
        
        # Check if we can split
        if (self.creature.hp >= self.split_threshold and 
            self.split_cooldown <= 0 and 
            random.random() < 0.05):  # 5% chance each turn
            
            # Find an adjacent empty tile
            for _ in range(8):  # Try 8 times
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                
                # Skip if it's the same tile
                if dx == 0 and dy == 0:
                    continue
                
                target_x = self.creature.x + dx
                target_y = self.creature.y + dy
                
                if (self.level.is_valid(target_x, target_y) and 
                    not self.level.get_tile(target_x, target_y).blocked and
                    self.level.check_for_creatures(target_x, target_y) is None):
                    
                    # Split the slime
                    self.creature.hp = self.creature.hp // 2
                    self.creature.doAction('split into two')
                    
                    # Create a new slime at the target location
                    # We'll assume the factory method is called make_slime
                    # This will be implemented in CreatureFactory
                    if hasattr(self.level, 'factory'):
                        new_slime = self.level.factory.make_slime()
                        new_slime.x = target_x
                        new_slime.y = target_y
                        new_slime.hp = self.creature.hp
                    
                    self.split_cooldown = 50  # Wait 50 turns before splitting again
                    break
        
        if self.split_cooldown > 0:
            self.split_cooldown -= 1



