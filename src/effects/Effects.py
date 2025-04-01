__author__ = 'Martijn Schut'

import random

class Effect(object):
    def __init__(self, duration, creature):
        self.duration = duration
        self.creature = creature
        self.val = 0

    def on_update(self):
        if self.duration == -1:
            pass
        elif self.duration > 0:
            self.duration -= 1
        else:
            self.creature.remove_effect(self)

class PoisonEffect(Effect):
    def __init__(self, duration, creature = None):
        super(PoisonEffect, self).__init__(duration, creature)

    def on_update(self):
        super(PoisonEffect, self).on_update()
        self.creature.hurt(1)
        if self.creature.type == 'player':
            self.creature.notify("You writhe in pain.")
        else:
            self.creature.doAction('writhe in pain')

class MinorHealEffect(Effect):
    def __init__(self, duration, creature = None):
        super(MinorHealEffect, self).__init__(duration,creature)

    def on_update(self):
        super(MinorHealEffect, self).on_update()
        self.creature.heal(1)
        if self.creature.type == 'player':
            self.creature.notify("You feel better.")
        else:
            self.creature.doAction('feel better')

class AsphyxiationEffect(Effect):
    def _init__(self, duration, creature = None):
        super(AsphyxiationEffect, self).__init__(duration, creature)
        self.val = 0

    def on_update(self):
        super(AsphyxiationEffect, self).on_update()
        self.creature.hurt(self.val)

        if random.random() < (0.02 * self.val):
            self.val += 1

        if 0 < self.val <= 3 and random.random() < 0.5:
            if self.creature.type == 'player':
                self.creature.notify("You feel short on breath.")
            else:
                self.creature.doAction('feel short on breath')
        elif 3 < self.val <= 10 and random.random() < 0.5:
            if self.creature.type == 'player':
                self.creature.notify("You cannot breathe.")
            else:
                self.creature.doAction('cannot breathe')
        elif 10 < self.val and random.random() < 0.1:
            if self.creature.type == 'player':
                self.creature.notify("You panic.")
            else:
                self.creature.doAction('panic')
        elif 10 < self.val:
            messages = [
                "You gasp for air.",
                "You try in vain to breathe.",
                "You feel everything go black."
            ] if self.creature.type == 'player' else [
                'gasp for air',
                'try in vain to breathe',
                'feel everything go black'
            ]
            if self.creature.type == 'player':
                self.creature.notify(random.choice(messages))
            else:
                self.creature.doAction(random.choice(messages))

class FoodPoisoningEffect(Effect):
    def __init__(self, duration, creature = None):
        super(FoodPoisoningEffect, self).__init__(duration, creature)
        
    def on_update(self):
        super(FoodPoisoningEffect, self).on_update()
        if random.random() < 0.5:  # 50% chance to trigger each turn
            self.creature.hurt(1)
            if self.creature.type == 'player':
                messages = [
                    "Your stomach churns violently.",
                    "You feel sick to your stomach.",
                    "You retch painfully."
                ]
                self.creature.notify(random.choice(messages))
            else:
                actions = [
                    "retches",
                    "looks sick",
                    "groans in pain"
                ]
                self.creature.doAction(random.choice(actions))

class StrongHealEffect(Effect):
    def __init__(self, duration, creature = None):
        super(StrongHealEffect, self).__init__(duration, creature)
        
    def on_update(self):
        super(StrongHealEffect, self).on_update()
        self.creature.heal(2)  # Heals for more than MinorHealEffect
        if self.creature.type == 'player':
            self.creature.notify("You feel much stronger.")
        else:
            self.creature.doAction('looks reinvigorated')

class HallucinationEffect(Effect):
    def __init__(self, duration, creature = None):
        super(HallucinationEffect, self).__init__(duration, creature)
        
    def on_update(self):
        super(HallucinationEffect, self).on_update()
        if random.random() < 0.3:  # 30% chance to trigger each turn
            if self.creature.type == 'player':
                hallucinations = [
                    "The walls seem to breathe.",
                    "You see colors that shouldn't exist.",
                    "Shadows dance at the edge of your vision.",
                    "You hear whispers from nowhere.",
                    "The floor appears to undulate beneath you."
                ]
                self.creature.notify(random.choice(hallucinations))
            else:
                self.creature.doAction('looks disoriented')