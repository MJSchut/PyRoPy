__author__ = 'Martijn Schut'

from .Creatures import Creature
from .Creatures import Player
from .Limb import *

from src import constants
from src.ai.CreatureAi import PlayerAi
from src.ai.CreatureAi import BloodFungusAi
from src.ai.CreatureAi import FungusAi
from src.ai.CreatureAi import HuskFungusAi
from src.ai.CreatureAi import BatAi
from src.ai.CreatureAi import SnakeAi
from src.ai.CreatureAi import GargoyleAi
from src.ai.CreatureAi import EOozeAi
# Import new AIs
from src.ai.CreatureAi import DiggerAi
from src.ai.CreatureAi import JumperAi
from src.ai.CreatureAi import HunterAi
from src.ai.CreatureAi import MimicAi
from src.ai.CreatureAi import ShadowAi
from src.ai.CreatureAi import PoisonousAi
from src.ai.CreatureAi import PackHunterAi
from src.ai.CreatureAi import TrapperAi
from src.ai.CreatureAi import ScavengerAi
from src.ai.CreatureAi import SlimeAi

from src.effects.Effects import PoisonEffect

import random

class CreatureFactory:
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level

    def _add_human_limbs(self, creature):
        # Add Torso
        torso = creature.add_limb(Torso(creature, None))
        ruarm = creature.add_limb(UpperArm(creature, torso, 'right upper arm'))
        rlarm = creature.add_limb(LowerArm(creature, ruarm, 'right lower arm'))
        creature.add_limb(Hand(creature, rlarm, 'right hand'))

        luarm = creature.add_limb(UpperArm(creature, torso, 'left upper arm'))
        llarm = creature.add_limb(LowerArm(creature, luarm, 'left lower arm'))
        creature.add_limb(Hand(creature, llarm, 'left hand'))

        # Neck, Head
        neck = creature.add_limb(Neck(creature, torso))
        creature.add_limb(Head(creature, neck))

        # Upper legs, Lower legs, Feet
        ruleg = creature.add_limb(UpperLeg(creature, torso, 'right upper leg'))
        rlleg = creature.add_limb(LowerLeg(creature, ruleg, 'right lower leg'))
        creature.add_limb(Foot(creature, rlleg, 'right foot'))

        luleg = creature.add_limb(UpperLeg(creature, torso, 'left upper leg'))
        llleg = creature.add_limb(LowerLeg(creature, luleg, 'left lower leg'))
        creature.add_limb(Foot(creature, llleg, 'left foot'))

    def make_player(self, messages):
        player = Player(self.lbt, self.con, self.level)
        player.set_maxhp(100)
        player.set_maxhunger(100)
        player.set_hunger(100)
        player.set_attack(5)
        player.set_defence(2)
        player.set_vision_radius(9)
        player.set_inventory_size(20)

        self._add_human_limbs(player)

        player.type = 'player'
        player.messages = messages
        player.set_Ai(PlayerAi(player, messages, self.level))

        self.level.add_at_empty_location(player)

        return player

    def make_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', (0, 255, 0))
        fungus.set_maxhp(10)
        fungus.set_attack(0)
        fungus.set_defence(0)
        fungus.set_vision_radius(0)
        fungus.set_inventory_size(0)

        fungus.blood_color = (0, 191, 0)  # Dark green
        fungus.type = 'fungus'

        fungus.set_Ai(FungusAi(fungus, self))

        self.level.add_at_empty_location(fungus)

        return fungus

    def make_blood_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', (255, 0, 0))
        fungus.set_maxhp(10)
        fungus.set_attack(0)
        fungus.set_defence(0)
        fungus.set_vision_radius(0)
        fungus.set_inventory_size(0)

        fungus.blood_color = (191, 0, 0)  # Dark red
        fungus.type = 'blood fungus'

        fungus.set_Ai(BloodFungusAi(fungus, self))

        self.level.add_at_empty_location(fungus)

        return fungus

    def make_husk_fungus(self):
        fungus = Creature(self.lbt, self.con, self.level, 'f', (0, 127, 127))  # Dark cyan
        fungus.set_Ai(HuskFungusAi(fungus, self.level))
        fungus.set_maxhp(60 + random.randint(0,5))
        fungus.set_attack(1 + random.randint(0,1))
        fungus.set_name('Husky Fungus known as %s' %constants.random_name())
        fungus.set_type('husk fungus')
        fungus.set_taste('like smoke')
        self.level.add_at_empty_location(fungus)

        return fungus

    def make_bat(self):
        bat = Creature(self.lbt, self.con, self.level, 'b', (191, 95, 0))  # Dark orange
        bat.set_maxhp(3)
        bat.set_attack(2)
        bat.set_defence(0)
        bat.set_vision_radius(5)
        bat.set_inventory_size(0)

        bat.blood_color = (255, 0, 0)  # Red
        bat.type = 'bat'

        bat.set_Ai(BatAi(bat))

        self.level.add_at_empty_location(bat)

        return bat

    def make_snake(self):
        snake = Creature(self.lbt, self.con, self.level, 's', (0, 191, 0))  # Dark green
        snake.set_maxhp(4)
        snake.set_attack(3)
        snake.set_defence(1)
        snake.set_vision_radius(7)
        snake.set_inventory_size(0)

        snake.blood_color = (255, 0, 0)  # Red
        snake.type = 'snake'

        snake.set_Ai(SnakeAi(snake))

        self.level.add_at_empty_location(snake)

        return snake

    def make_gargoyle(self, player):
        gargoyle = Creature(self.lbt, self.con, self.level, 'G', (127, 127, 127))  # Grey
        gargoyle.set_maxhp(15)
        gargoyle.set_attack(5)
        gargoyle.set_defence(4)
        gargoyle.set_vision_radius(8)
        gargoyle.set_inventory_size(0)

        gargoyle.blood_color = (95, 95, 95)  # Dark grey
        gargoyle.type = 'gargoyle'

        gargoyle.set_Ai(GargoyleAi(gargoyle, player))

        self.level.add_at_empty_location(gargoyle)

        return gargoyle

    def make_eooze(self):
        ooze = Creature(self.lbt, self.con, self.level, 'O', (0, 127, 127))  # Dark cyan
        ooze.set_Ai(EOozeAi(ooze, self))
        ooze.set_maxhp(1)
        ooze.set_attack(3)
        ooze.set_vision_radius(1)
        ooze.set_name('Endless Ooze')
        ooze.set_type('eldritch')
        self.level.add_at_empty_location(ooze)
        ooze.blood_color = (255, 255, 255)  # White

        return ooze

    def make_digger(self):
        digger = Creature(self.lbt, self.con, self.level, 'D', (139, 69, 19))  # Saddle Brown
        digger.set_maxhp(15)
        digger.set_attack(2)
        digger.set_defence(3)
        digger.set_vision_radius(4)
        digger.set_inventory_size(0)

        digger.blood_color = (139, 69, 19)  # Saddle Brown
        digger.type = 'digger'

        digger.set_Ai(DiggerAi(digger, self.level))

        self.level.add_at_empty_location(digger)

        return digger
    
    def make_frog(self):
        frog = Creature(self.lbt, self.con, self.level, 'F', (0, 128, 0))  # Green
        frog.set_maxhp(5)
        frog.set_attack(1)
        frog.set_defence(0)
        frog.set_vision_radius(6)
        frog.set_inventory_size(0)

        frog.blood_color = (0, 128, 0)  # Green
        frog.type = 'frog'

        frog.set_Ai(JumperAi(frog))

        self.level.add_at_empty_location(frog)

        return frog
    
    def make_hunter(self):
        hunter = Creature(self.lbt, self.con, self.level, 'h', (165, 42, 42))  # Brown
        hunter.set_maxhp(10)
        hunter.set_attack(4)
        hunter.set_defence(1)
        hunter.set_vision_radius(8)
        hunter.set_inventory_size(0)

        hunter.blood_color = (165, 42, 42)  # Brown
        hunter.type = 'hunter'

        hunter.set_Ai(HunterAi(hunter, self.level))

        self.level.add_at_empty_location(hunter)

        return hunter
    
    def make_mimic(self):
        mimic = Creature(self.lbt, self.con, self.level, '¤', (139, 69, 19))  # Chest-like
        # Store original appearance, then disguise
        mimic.original_char = '¤'
        mimic.original_color = (139, 69, 19)
        # Disguise as an item
        mimic.char = '*'
        mimic.color = (255, 215, 0)  # Gold
        
        mimic.set_maxhp(12)
        mimic.set_attack(6)
        mimic.set_defence(2)
        mimic.set_vision_radius(3)
        mimic.set_inventory_size(0)

        mimic.blood_color = (139, 69, 19)  # Brown
        mimic.type = 'mimic'

        mimic.set_Ai(MimicAi(mimic))

        self.level.add_at_empty_location(mimic)

        return mimic
    
    def make_shadow(self, player):
        shadow = Creature(self.lbt, self.con, self.level, 'S', (50, 50, 50))  # Dark grey
        shadow.set_maxhp(8)
        shadow.set_attack(3)
        shadow.set_defence(1)
        shadow.set_vision_radius(10)  # Good vision to find the player
        shadow.set_inventory_size(0)

        shadow.blood_color = (0, 0, 0)  # Black
        shadow.type = 'shadow'

        shadow.set_Ai(ShadowAi(shadow, player))

        self.level.add_at_empty_location(shadow)

        return shadow
    
    def make_spider(self):
        spider = Creature(self.lbt, self.con, self.level, 's', (0, 0, 0))  # Black
        spider.set_maxhp(6)
        spider.set_attack(2)
        spider.set_defence(1)
        spider.set_vision_radius(5)
        spider.set_inventory_size(0)

        spider.blood_color = (0, 100, 0)  # Dark green
        spider.type = 'spider'

        spider.set_Ai(PoisonousAi(spider, self))

        self.level.add_at_empty_location(spider)

        return spider
    
    def make_wolf(self):
        wolf = Creature(self.lbt, self.con, self.level, 'w', (128, 128, 128))  # Grey
        wolf.set_maxhp(8)
        wolf.set_attack(3)
        wolf.set_defence(1)
        wolf.set_vision_radius(7)
        wolf.set_inventory_size(0)

        wolf.blood_color = (255, 0, 0)  # Red
        wolf.type = 'wolf'

        wolf.set_Ai(PackHunterAi(wolf, self.level))

        self.level.add_at_empty_location(wolf)

        return wolf
    
    def make_trap_spider(self):
        spider = Creature(self.lbt, self.con, self.level, 'T', (165, 42, 42))  # Brown
        # Store original appearance
        spider.original_char = 'T'
        spider.original_color = (165, 42, 42)
        # Disguise as floor
        spider.char = '.'
        spider.color = (127, 127, 127)  # Grey
        
        spider.set_maxhp(7)
        spider.set_attack(5)  # Strong attack when it traps you
        spider.set_defence(0)
        spider.set_vision_radius(2)
        spider.set_inventory_size(0)

        spider.blood_color = (0, 100, 0)  # Dark green
        spider.type = 'trap spider'

        spider.set_Ai(TrapperAi(spider))

        self.level.add_at_empty_location(spider)

        return spider
    
    def make_rat(self):
        rat = Creature(self.lbt, self.con, self.level, 'r', (128, 128, 128))  # Grey
        rat.set_maxhp(3)
        rat.set_attack(1)
        rat.set_defence(0)
        rat.set_vision_radius(6)
        rat.set_inventory_size(0)

        rat.blood_color = (255, 0, 0)  # Red
        rat.type = 'rat'

        rat.set_Ai(ScavengerAi(rat, self.level))

        self.level.add_at_empty_location(rat)

        return rat
    
    def make_slime(self):
        slime = Creature(self.lbt, self.con, self.level, 'j', (0, 255, 0))  # Green
        slime.set_maxhp(10)
        slime.set_attack(2)
        slime.set_defence(2)
        slime.set_vision_radius(3)
        slime.set_inventory_size(0)

        slime.blood_color = (0, 255, 0)  # Green
        slime.type = 'slime'

        slime.set_Ai(SlimeAi(slime, self.level))

        self.level.add_at_empty_location(slime)

        return slime