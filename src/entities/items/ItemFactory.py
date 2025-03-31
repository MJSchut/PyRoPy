__author__ = 'Martijn Schut'

from typing import Dict, Any
from .Items import Item
from src.effects.Effects import PoisonEffect
from src.effects.Effects import MinorHealEffect
from src.effects.Effects import AsphyxiationEffect
from src.constants import item_color_pointers
from src.constants import item_colors
from src.constants import item_adjective
from src.constants import appearance_potion_dictionary
from src.constants import effect_noun
from src.util.config_loader import ConfigLoader

from src.entities.creatures.Limb import Hand
from src.entities.creatures.Limb import Neck
from src.entities.creatures.Limb import Head

import random

class ItemFactory(object):
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level
        self.config = ConfigLoader()

    def _create_item_from_config(self, config: Dict[str, Any]) -> Item:
        """Create an item from a configuration dictionary."""
        item = Item(self.lbt, self.con, self.level, config['char'], config['color'])
        
        # Set basic properties
        item.name = config['name']  # Direct assignment since no setter exists
        item.set_appearance(config['char'])
        item.set_description(config['description'])
        item.weight = config.get('weight', 1)  # Direct assignment since no setter exists
        
        # Set type-specific properties
        if config['type'] == 'weapon':
            item.set_attack_value(config['damage'])
            item.set_equip_to(Hand)  # Weapons are equipped to hand
        elif config['type'] == 'armor':
            item.set_defence_value(config['defense'])
            if config.get('wearable', False):
                item.set_wear_to(Head)  # Default to head for wearable items
        elif config['type'] == 'consumable':
            if config.get('effect') == 'heal':
                item.set_drink_effect(MinorHealEffect)  # Use the actual effect class
            elif config.get('effect') == 'hunger':
                item.set_nutrition(config['value'])
                item.set_taste(config.get('taste', 'delicious'))
        
        # Set equipment and wearable flags
        if config.get('equipment', False):
            item.set_equipment(True)
        if config.get('wearable', False):
            item.set_wearable(True)
        if config.get('holdable', False):
            item.holdable = True  # Direct assignment since no setter exists
        if config.get('edible', False):
            item.set_nutrition(config.get('value', 20))  # Use nutrition for edible items
            item.set_taste(config.get('taste', 'delicious'))
        if config.get('drinkable', False):
            item.drinkable = True  # Direct assignment since no setter exists
        
        # Add item to level
        self.level.add_at_empty_location(item)
        
        return item

    def make_rock(self):
        """Create a rock item."""
        config = self.config.get_item_definition('rock')
        spawn_config = self.config.get_item_spawn_config('rock')
        config.update(spawn_config)
        return self._create_item_from_config(config)

    def make_sword(self):
        """Create a sword item."""
        config = self.config.get_item_definition('sword')
        spawn_config = self.config.get_item_spawn_config('sword')
        config.update(spawn_config)
        return self._create_item_from_config(config)

    def make_gauntlet(self):
        """Create a gauntlet item."""
        config = self.config.get_item_definition('gauntlet')
        spawn_config = self.config.get_item_spawn_config('gauntlet')
        config.update(spawn_config)
        return self._create_item_from_config(config)

    def make_random_potion(self):
        """Create a random potion with effects."""
        config = self.config.get_item_definition('potion')
        spawn_config = self.config.get_item_spawn_config('potion')
        config.update(spawn_config)
        
        # Choose random effect
        effect = random.choice([PoisonEffect, MinorHealEffect])
        
        # Set appearance
        if appearance_potion_dictionary.get(effect) is None:
            color = random.choice(item_colors)
            item_colors.remove(color)
            adjective = random.choice(item_adjective)
            appearance = adjective + " " + color
            appearance_potion_dictionary[effect] = appearance
        else:
            appearance = appearance_potion_dictionary[effect]
        
        # Update config with effect-specific properties
        config['effect'] = effect.__name__.replace('Effect', '')
        config['color'] = item_color_pointers[appearance.split(" ")[1]]
        config['name'] = f'potion of {effect_noun[effect]}'
        config['appearance'] = f'{appearance} potion'
        
        return self._create_item_from_config(config)

    def make_amulet(self):
        """Create an amulet item."""
        config = self.config.get_item_definition('amulet')
        spawn_config = self.config.get_item_spawn_config('amulet')
        config.update(spawn_config)
        
        # Add special effects
        config['wear_effect'] = AsphyxiationEffect
        config['swings_to_break'] = 1
        
        return self._create_item_from_config(config)

    def make_fedora(self):
        """Create a fedora item."""
        config = self.config.get_item_definition('fedora')
        spawn_config = self.config.get_item_spawn_config('fedora')
        config.update(spawn_config)
        return self._create_item_from_config(config)

    def make_food(self):
        """Create a food item."""
        config = self.config.get_item_definition('food')
        spawn_config = self.config.get_item_spawn_config('food')
        config.update(spawn_config)
        
        # Add random food type
        food_types = [
            ('apple', '%', (255, 0, 0), 'juicy and sweet', 20),
            ('bread', '%', (139, 69, 19), 'freshly baked', 30),
            ('cheese', '%', (255, 255, 0), 'sharp and tangy', 25),
            ('meat', '%', (165, 42, 42), 'savory', 35),
            ('mushroom', '%', (160, 82, 45), 'earthy', 20)
        ]
        
        food_type = random.choice(food_types)
        name, char, color, taste, nutrition = food_type
        
        config['name'] = name
        config['char'] = char
        config['color'] = color
        config['taste'] = taste
        config['value'] = nutrition
        
        return self._create_item_from_config(config)

    def spawn_initial_items(self):
        """Spawn all initial items based on spawn configuration."""
        spawns = self.config.get_all_item_spawns()
        for item_type, spawn_config in spawns.items():
            count = spawn_config['count']
            for _ in range(count):
                if item_type == 'rock':
                    self.make_rock()
                elif item_type == 'sword':
                    self.make_sword()
                elif item_type == 'gauntlet':
                    self.make_gauntlet()
                elif item_type == 'potion':
                    self.make_random_potion()
                elif item_type == 'amulet':
                    self.make_amulet()
                elif item_type == 'fedora':
                    self.make_fedora()
                elif item_type == 'food':
                    self.make_food()

    def make_corpse_edible(self, corpse):
        """Increase nutrition value of corpses."""
        corpse.set_nutrition(random.randint(15, 30))  # Corpses have high nutrition
        tastes = ['gamey', 'stringy', 'salty', 'chewy', 'tender']
        corpse.set_taste(random.choice(tastes))
        return corpse

    def make_shard(self, location = None, color = None):
        """Create a shard item."""
        if color is None:
            color = self.lbt.cyan
        shard = Item(self.lbt, self.con, self.level, ',', color)
        shard.set_equip_to(Hand)
        shard.set_appearance('a shard')
        shard.set_name('a shard')
        shard.set_attack_value(2)

        if location is None:
            self.level.add_at_empty_location(shard)
        else:
            self.level.add_item(shard, location[0], location[1])