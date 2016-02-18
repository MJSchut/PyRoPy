__author__ = 'Martijn Schut'

class Limb(object):
    def __init__(self, creature, attachedto = None):
        self.creature = creature
        self.attachedto = attachedto
        self.cangrab = False
        self.name = 'Unnamed limb'
        self.holding = None
        self.wearing = None

        self.canwalk = False

class Hand(Limb):
    def __init__(self, creature, attachedto, name = 'hand'):
        super(Hand, self).__init__(creature, attachedto)
        self.cangrab = True
        self.name = name
