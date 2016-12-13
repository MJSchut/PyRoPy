__author__ = 'Martijn Schut'

from Items import Item
from src.effects.Effects import PoisonEffect
from src.effects.Effects import MinorHealEffect
from src.effects.Effects import AsphyxiationEffect
from src.constants import item_color_pointers
from src.constants import item_colors
from src.constants import item_adjective
from src.constants import appearance_potion_dictionary
from src.constants import effect_noun

from src.entities.creatures.Limb import Hand
from src.entities.creatures.Limb import Neck
from src.entities.creatures.Limb import Head

import random

class ItemFactory(object):
    def __init__(self, lbt, con, level):
        self.lbt = lbt
        self.con = con
        self.level = level

    def make_rock(self):
        rock = Item(self.lbt, self.con, self.level, ',', self.lbt.yellow)
        rock.set_equip_to(Hand)
        rock.set_attack_value(1)
        if random.random() < 0.5:
            rock.set_name('rock')
        else:
            rock.set_name('stone')
        self.level.add_at_empty_location(rock)

        return rock

    def make_random_potion(self):
        # choose an effect
        effect = random.choice([PoisonEffect, MinorHealEffect])

        # check if this effect is present in the appearance dictionary
        if appearance_potion_dictionary.get(effect) == None:
            # pick a random color and adjective, remove the color from the list
            color = random.choice(item_colors)
            item_colors.remove(color)
            adjective = random.choice(item_adjective)

            appearance = adjective + " " + color
            # add to the dictionary
            appearance_potion_dictionary[effect] = appearance
        else:
            appearance = appearance_potion_dictionary[effect]

        # the color in the terminal
        t_color = item_color_pointers[appearance.split(" ")[1]]
        # create item, add drink effect and add to level
        potion = Item(self.lbt, self.con, self.level, '!', t_color)
        potion.set_drink_effect(effect)
        potion.set_appearance('%s potion' % appearance)
        potion.set_name('potion of %s' %effect_noun[effect])
        potion.identified = False
        potion.set_equip_to(Hand)
        potion.item_factory = self
        potion.swings_to_break = 1

        self.level.add_at_empty_location(potion)

        return potion

    def make_sword(self):
        sword = Item(self.lbt, self.con, self.level, '/', self.lbt.white)
        sword.set_equip_to(Hand)
        sword.set_appearance('iron sword')
        sword.set_name('unremarkable iron sword')
        sword.set_attack_value(2)
        self.level.add_at_empty_location(sword)

    def make_gauntlet(self):
        glove = Item(self.lbt, self.con, self.level, ']', self.lbt.white)
        glove.set_equip_to(Hand, wearable=True)
        glove.set_appearance('iron gauntlet')
        glove.set_name('unremarkable iron gauntlet')
        glove.set_defence_value(1)
        self.level.add_at_empty_location(glove)

    def make_fedora(self):
        fedora = Item(self.lbt, self.con, self.level, '_', self.lbt.cyan)
        fedora.set_wear_to(Head)
        fedora.set_appearance('fedora')
        fedora.set_name('fedora')
        fedora.set_defence_value(1)
        self.level.add_at_empty_location(fedora)

    def make_amulet(self):
        necklace = Item(self.lbt, self.con, self.level, ';', self.lbt.cyan)
        necklace.set_wear_to(Neck)
        necklace.set_appearance('sparkling necklace')
        necklace.set_name('dangerous necklace')
        necklace.set_defence_value(10)
        necklace.set_wear_effect(AsphyxiationEffect)
        necklace.item_factory = self
        necklace.swings_to_break = 1
        self.level.add_at_empty_location(necklace)

    def make_shard(self, location = None, color = None):
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