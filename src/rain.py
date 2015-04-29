from random import randint,uniform

class Rain(object):
    def __init__(self):
        self.drops = []
        for i in xrange(100):
            self.drops.append({'x':randint(0,64),'y':randint(0,64),'s':uniform(0.5,2)})

    def paint(self,draw,color=(96,96,200)):
        for drop in self.drops:
            draw.point((drop['x'],drop['y']),color)

    def move(self):
        for drop in self.drops:
            drop['y'] += drop['s']

            if (drop['y'] > 55):
                drop['x'] = randint(0,64)
                drop['y'] = 0
                drop['s'] = uniform(0.5,2)

