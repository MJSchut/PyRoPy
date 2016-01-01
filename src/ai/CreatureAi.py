__author__ = 'Martijn Schut'

class CreatureAi(object):
    def __init__(self, creature):
        self.creature = creature

    def on_enter(self, x, y, tile):
        if not tile.blocked:
            self.creature.set_postion(x,y)

class PlayerAi(CreatureAi):
    def __init__(self,creature):
        super(PlayerAi, self).__init__(creature)
