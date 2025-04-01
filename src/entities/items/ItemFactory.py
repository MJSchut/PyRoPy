__author__ = 'Martijn Schut'

from typing import Dict, Any
from .Items import Item
from src.effects.Effects import PoisonEffect
from src.effects.Effects import MinorHealEffect
from src.effects.Effects import StrongHealEffect
from src.effects.Effects import FoodPoisoningEffect  
from src.effects.Effects import HallucinationEffect
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
        item.type = config.get('type', 'item')  # Use generic type for unidentified items
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
                item.set_equipment(True)  # Make sure it's marked as equipment
                item.set_wearable(True)  # Make sure it's marked as wearable
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
        config['type'] = 'potion'  # Set potion type
        
        # Create the item
        item = self._create_item_from_config(config)
        
        # Set the appearance directly on the item
        item.appearance = f'{appearance} potion'
        
        return item

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
        """Create a food item with variations."""
        config = self.config.get_item_definition('food')
        spawn_config = self.config.get_item_spawn_config('food')
        config.update(spawn_config)
        
        # Base food types
        food_types = [
            # name, char, color, base_taste
            ('bread', '%', (139, 69, 19)),
            ('meat', '%', (165, 42, 42)),
            ('apple', '%', (255, 0, 0)),
            ('cheese', '%', (255, 255, 0)),
            ('mushroom', '%', (160, 82, 45))
        ]
        
        # Choose a base food type
        food_type = random.choice(food_types)
        name, char, color = food_type
        
        # Apply variations based on food type
        if name == 'bread':
            # Bread variations
            variations = [
                # name, description, taste, nutrition, effect, duration
                ('freshly baked bread', 'A warm, crusty loaf of bread.', 'warm and satisfying', 30, None, 0),
                ('stale bread', 'A hardened loaf of bread.', 'dry and bland', 20, None, 0),
                ('moldy bread', 'A loaf covered in blue-green spots.', 'foul and sour', 10, FoodPoisoningEffect, 5),
                ('enriched bread', 'A hearty, nutrient-rich loaf.', 'hearty and nourishing', 40, StrongHealEffect, 3),
                ('sweet bread', 'A sugary, dessert-like bread.', 'sweet and delicious', 25, MinorHealEffect, 2),
            ]
        
        elif name == 'meat':
            # Meat variations
            variations = [
                # name, description, taste, nutrition, effect, duration
                ('fresh meat', 'A raw piece of meat.', 'juicy and savory', 35, None, 0),
                ('cooked meat', 'A well-prepared piece of meat.', 'perfectly cooked and delicious', 45, MinorHealEffect, 2),
                ('rotten meat', 'A putrid piece of meat.', 'putrid and revolting', 15, FoodPoisoningEffect, 8),
                ('smoked meat', 'A preserved piece of meat.', 'smoky and rich', 40, None, 0),
                ('strange meat', 'An unusual-looking piece of meat.', 'unusual but not unpleasant', 30, HallucinationEffect, 10),
            ]
            
        elif name == 'mushroom':
            # Mushroom variations
            variations = [
                # name, description, taste, nutrition, effect, duration
                ('common mushroom', 'An ordinary-looking mushroom.', 'earthy and mild', 20, None, 0),
                ('red-capped mushroom', 'A mushroom with a bright red cap.', 'spicy and tangy', 15, MinorHealEffect, 3),
                ('pale mushroom', 'A pale, sickly-looking mushroom.', 'bitter and unpleasant', 10, FoodPoisoningEffect, 6),
                ('glowing mushroom', 'A mushroom that emits a faint glow.', 'sweet and intoxicating', 25, HallucinationEffect, 12),
                ('spotted mushroom', 'A mushroom with unusual spots.', 'nutty and rich', 30, StrongHealEffect, 4),
            ]
            
        else:  # Apple or cheese or other foods
            # Generic variations
            variations = [
                # name, description, taste, nutrition, effect
                (f'fresh {name}', f'A fresh {name}.', 'fresh and delicious', 25, None, 0),
                (f'aged {name}', f'An aged {name}.', 'rich and complex', 30, MinorHealEffect, 2),
                (f'spoiled {name}', f'A spoiled {name}.', 'sour and off-putting', 15, FoodPoisoningEffect, 4),
                (f'exotic {name}', f'An unusual variety of {name}.', 'complex and unusual', 35, HallucinationEffect, 6),
            ]
        
        # Select a variation
        variation = random.choice(variations)
        variant_name, description, taste, nutrition, effect, duration = variation
        
        # Update config with the variation details
        config['name'] = variant_name
        config['char'] = char
        config['color'] = color
        config['description'] = description
        config['taste'] = taste
        config['value'] = nutrition
        
        # Create the item
        item = self._create_item_from_config(config)
        
        # Set the eat effect if applicable
        if effect:
            item.eat_effect = effect
            item.drink_effect_duration = duration  # Reuse this field for eat effects too
            
        return item

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