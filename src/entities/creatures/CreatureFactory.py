__author__ = 'Martijn Schut'

import random
from typing import Dict, Any

from src import constants
from src.ai.CreatureAi import BatAi
from src.ai.CreatureAi import BloodFungusAi
from src.ai.CreatureAi import EOozeAi
from src.ai.CreatureAi import FungusAi
from src.ai.CreatureAi import GargoyleAi
from src.ai.CreatureAi import HuskFungusAi
from src.ai.CreatureAi import PlayerAi
from src.ai.CreatureAi import SnakeAi
from src.util.config_loader import ConfigLoader
from .Creatures import Creature
from .Creatures import Player
from .Limb import *


class CreatureFactory:
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level
        self.config = ConfigLoader()

    @staticmethod
    def _add_human_limbs(creature):
        # Add Torso
        torso = creature.add_limb(Torso(creature, None))
        right_upper_arm = creature.add_limb(UpperArm(creature, torso, 'right upper arm'))
        right_lower_arm = creature.add_limb(LowerArm(creature, right_upper_arm, 'right lower arm'))
        creature.add_limb(Hand(creature, right_lower_arm, 'right hand'))

        left_upper_arm = creature.add_limb(UpperArm(creature, torso, 'left upper arm'))
        left_lower_arm = creature.add_limb(LowerArm(creature, left_upper_arm, 'left lower arm'))
        creature.add_limb(Hand(creature, left_lower_arm, 'left hand'))

        # Neck, Head
        neck = creature.add_limb(Neck(creature, torso))
        creature.add_limb(Head(creature, neck))

        # Upper legs, Lower legs, Feet
        right_upper_leg = creature.add_limb(UpperLeg(creature, torso, 'right upper leg'))
        right_lower_leg = creature.add_limb(LowerLeg(creature, right_upper_leg, 'right lower leg'))
        creature.add_limb(Foot(creature, right_lower_leg, 'right foot'))

        left_upper_leg = creature.add_limb(UpperLeg(creature, torso, 'left upper leg'))
        left_lower_leg = creature.add_limb(LowerLeg(creature, left_upper_leg, 'left lower leg'))
        creature.add_limb(Foot(creature, left_lower_leg, 'left foot'))

    def _create_creature_from_config(self, creature_type: str, config: Dict[str, Any], messages=None, player=None) -> Creature:
        """Create a creature from its configuration."""
        # Validate required fields
        required_fields = ['name', 'char', 'color', 'hp', 'max_hp', 'attack', 'defense', 'ai_type']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field '{field}' in creature configuration for {creature_type}")

        if creature_type == 'player':
            if messages is None:
                raise ValueError("Messages must be provided when creating a player")
            creature = Player(self.lbt, self.con, self.level)
            self._add_human_limbs(creature)
            # Set player-specific properties
            creature.messages = messages
            creature.set_maxhunger(config.get('max_hunger', 100))
            creature.set_hunger(config.get('hunger', 100))
        else:
            creature = Creature(self.lbt, self.con, self.level, config['char'], config['color'])

        # Set basic properties
        creature.set_maxhp(config['max_hp'])
        creature.set_attack(config['attack'])
        creature.set_defence(config['defense'])
        
        # Set vision radius with proper default
        vision_radius = config.get('vision_radius', 0)
        creature.set_vision_radius(vision_radius)
        
        # Set inventory size with proper default
        inventory_size = config.get('inventory_size', 0)
        creature.set_inventory_size(inventory_size)
        
        creature.type = creature_type

        # Set AI based on type
        ai_type = config['ai_type']
        if ai_type == 'player':
            if messages is None:
                raise ValueError("Messages must be provided when creating a player AI")
            ai = PlayerAi(creature, messages, self.level)
        elif ai_type == 'fungus':
            ai = FungusAi(creature, self)
        elif ai_type == 'bat':
            ai = BatAi(creature)
        elif ai_type == 'snake':
            ai = SnakeAi(creature)
        elif ai_type == 'gargoyle':
            if player is None:
                raise ValueError("Player reference must be provided when creating a gargoyle")
            ai = GargoyleAi(creature, player)
        else:
            raise ValueError(f"Unknown AI type '{ai_type}' for creature {creature_type}")

        # Set the level reference for the AI
        ai.level = self.level
        creature.set_Ai(ai)

        # Add to level
        if creature_type == 'player':
            # Get a random walkable tile for the player
            x, y = self.level.get_random_walkable_tile()
            creature.x = x
            creature.y = y
            self.level.creatures.append(creature)  # Add player to level's creatures list
        else:
            self.level.add_at_empty_location(creature)

        return creature

    def make_player(self, messages):
        """Create a player character."""
        config = self.config.get_creature_definition('player')
        spawn_config = self.config.get_spawn_config('player')
        # Merge spawn config over base config
        config.update(spawn_config)
        
        player = self._create_creature_from_config('player', config, messages)
        return player

    def make_fungus(self):
        """Create a fungus creature."""
        config = self.config.get_creature_definition('fungus')
        spawn_config = self.config.get_spawn_config('fungus')
        config.update(spawn_config)
        return self._create_creature_from_config('fungus', config)

    def make_bat(self):
        """Create a bat creature."""
        config = self.config.get_creature_definition('bat')
        spawn_config = self.config.get_spawn_config('bat')
        config.update(spawn_config)
        return self._create_creature_from_config('bat', config)

    def make_snake(self):
        """Create a snake creature."""
        config = self.config.get_creature_definition('snake')
        spawn_config = self.config.get_spawn_config('snake')
        config.update(spawn_config)
        return self._create_creature_from_config('snake', config)

    def make_gargoyle(self, player):
        """Create a gargoyle creature."""
        config = self.config.get_creature_definition('gargoyle')
        spawn_config = self.config.get_spawn_config('gargoyle')
        config.update(spawn_config)
        return self._create_creature_from_config('gargoyle', config, player=player)

    def spawn_initial_creatures(self, player):
        """Spawn all initial creatures based on spawn configuration."""
        spawns = self.config.get_all_creature_spawns()
        for creature_type, spawn_config in spawns.items():
            if creature_type == 'player':  # Skip player as it's already spawned
                continue
            count = spawn_config['count']
            for _ in range(count):
                if creature_type == 'fungus':
                    self.make_fungus()
                elif creature_type == 'bat':
                    self.make_bat()
                elif creature_type == 'snake':
                    self.make_snake()
                elif creature_type == 'gargoyle':
                    self.make_gargoyle(player)

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
