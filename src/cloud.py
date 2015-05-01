from sprite import Sprite
from random import randint,uniform

class Cloud(Sprite):
    def __init__(self):
        Sprite.__init__(self, ["cloud"], (-32,-16), (0,0))
        self.active = False

    def activate(self, xs=0.02):
        if (xs == 0):
            xs = uniform(0.005,0.008)
        
        self.speed = (xs * uniform(0.9,1.2), 0)

        if (not self.active):
            self.active = True
            self.pos[0] = randint(-32,64+32)
            self.pos[1] = randint(-8,32)

    def deactivate(self):
        self.active = False

    def paint(self, canvas):
        if (self.active):
            super(Cloud, self).paint(canvas)

    def move(self):
        if (self.active):
            super(Cloud, self).move()

            if (self.pos[0] < -32):
                self.pos[0] = 64+randint(32,64)
                self.pos[1] = randint(-8,32)

            if (self.pos[0] > 64+32):
                self.pos[0] = randint(-64,-32)
                self.pos[1] = randint(-8,32)

    @staticmethod
    def create(n):
        result = []
        for i in xrange(n):
            result.append(Cloud())
        return result
