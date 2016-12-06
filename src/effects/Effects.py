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
    def __init__(self, duration, creature):
        super(PoisonEffect, self).__init__(duration, creature)

    def on_update(self):
        super(PoisonEffect, self).on_update()
        self.creature.hurt(1)
        self.creature.doAction('writhe in pain')

class MinorHealEffect(Effect):
    def __init__(self, duration, creature = None):
        super(MinorHealEffect, self).__init__(duration,creature)

    def on_update(self):
        super(MinorHealEffect, self).on_update()
        self.creature.heal(1)
        self.creature.doAction('feel better')

class AsphyxiationEffect(Effect):
    def _init__(self, duration, creature = None):
        super(AsphyxiationEffect, self).__init__(duration, creature)
        self.val = 0

    def on_update(self):
        super(AsphyxiationEffect, self).on_update()
        self.creature.hurt(self.val)

        if random.random() < 0.02 * self.val + 1:
            self.val += 1

        if 0 < self.val <= 3 and random.random() < 0.5:
            self.creature.doAction('feel short of breath')
        if 3 < self.val <= 10 and random.random() < 0.5:
            self.creature.doAction('cannot breathe')
        if 10 < self.val and random.random() < 0.1:
            #TODO: add panic effect
            self.creature.doAction('panic')
        if 10 < self.val:
            random.choice(self.creature.doAction('gasp for air'),
                          self.creature.doAction('try in vain to breathe'),
                          self.creature.doAction('feel everything go black'))