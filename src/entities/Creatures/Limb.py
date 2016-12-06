__author__ = 'Martijn Schut'

class Limb(object):
    def __init__(self, creature, attachedto = None):
        self.creature = creature
        # what's this limb attached to
        self.attachedto = attachedto
        # can you use to hold stuff?
        self.cangrab = False
        # by how much does this limb boost your speed
        self.mobility = 0
        # name for log
        self.name = 'Unnamed limb'

        # can you live if you lose this?
        self.essential = False

        # is the limb holding or wearing anything
        # self.holding can only be true of cangrab is true
        self.holding = None
        self.wearing = None

# all the limb subclasses
class Torso(Limb):
    def __init__(self, creature, attachedto, name = 'torso'):
        super(Torso, self).__init__(creature, attachedto)
        self.name = name
        self.essential = True

class Hand(Limb):
    def __init__(self, creature, attachedto, name = 'hand'):
        super(Hand, self).__init__(creature, attachedto)
        self.cangrab = True
        self.name = name

class LowerArm(Limb):
    def __init__(self, creature, attachedto, name = 'lower arm'):
        super(LowerArm, self).__init__(creature, attachedto)
        self.name = name

class UpperArm(Limb):
    def __init__(self, creature, attachedto, name = 'upper arm'):
        super(UpperArm, self).__init__(creature, attachedto)
        self.name = name

class Neck(Limb):
    def __init__(self, creature, attachedto, name = 'neck'):
        super(Neck, self).__init__(creature, attachedto)
        self.name = name
        self.essential = True

# yes, I'm aware that the head nor the torso is a limb, shut up
class Head(Limb):
    def __init__(self, creature, attachedto, name = 'head'):
        super(Head, self).__init__(creature, attachedto)
        self.name = name
        self.essential = True

class Foot(Limb):
    def __init__(self, creature, attachedto, name = 'foot'):
        super(Foot, self).__init__(creature, attachedto)
        self.mobility = 0.5
        self.name = name

class LowerLeg(Limb):
    def __init__(self, creature, attachedto, name = 'lower leg'):
        super(LowerLeg, self).__init__(creature, attachedto)
        self.mobility = 0.2
        self.name = name

class UpperLeg(Limb):
    def __init__(self, creature, attachedto, name = 'upper leg'):
        super(UpperLeg, self).__init__(creature, attachedto)
        self.name = name
