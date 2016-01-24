__author__ = 'Martijn Schut'

class Effect(object):
    def __init__(self, duration, creature):
        self.duration = duration
        self.creature = creature

    def on_update(self):
        if self.duration > 0:
            self.duration -= 1
        else:
            self.creature.remove_effect(self)

class PoisonEffect(Effect):
    def __init__(self, duration, creature):
        super(PoisonEffect, self).__init__(duration, creature)
        self.duration = 3

    def on_update(self):
        super(PoisonEffect, self).on_update()
        self.creature.hurt(1)
        self.creature.doAction('writhe in pain')
