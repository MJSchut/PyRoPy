import tcod.event

class InputHandler:
    def __init__(self):
        self.key = tcod.event.KeySym

    def handle_events(self):
        action = {}
        
        for event in tcod.event.wait():
            action = self.handle_event(event)
            if action:
                return action
                
        return action

    def handle_event(self, event):
        if isinstance(event, tcod.event.Quit):
            return {'quit': True}
            
        if isinstance(event, tcod.event.KeyDown):
            if event.sym == tcod.event.K_ESCAPE:
                return {'quit': True}
            elif event.sym == tcod.event.K_i:
                return {'inventory': True}
            elif event.sym == tcod.event.K_d:
                return {'drop': True}
            elif event.sym == tcod.event.K_e:
                return {'eat': True}
            elif event.sym == tcod.event.K_r:
                return {'drink': True}
            elif event.sym == tcod.event.K_q:
                return {'equip': True}
            elif event.sym == tcod.event.K_w:
                return {'wear': True}
            elif event.sym == tcod.event.K_x:
                return {'examine': True}
            elif event.sym == tcod.event.K_UP:
                return {'move': (0, -1)}
            elif event.sym == tcod.event.K_DOWN:
                return {'move': (0, 1)}
            elif event.sym == tcod.event.K_LEFT:
                return {'move': (-1, 0)}
            elif event.sym == tcod.event.K_RIGHT:
                return {'move': (1, 0)}
            elif event.sym == tcod.event.K_y:
                return {'move': (-1, -1)}
            elif event.sym == tcod.event.K_u:
                return {'move': (1, -1)}
            elif event.sym == tcod.event.K_b:
                return {'move': (-1, 1)}
            elif event.sym == tcod.event.K_n:
                return {'move': (1, 1)}
                
        return {} 