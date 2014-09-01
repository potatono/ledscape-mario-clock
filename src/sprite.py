import Image

class Sprite(object):
    def __init__(self, images, pos=(0,0), speed=(0,0), fs=0):
        self.images = map(self.load, images)
        self.image = self.images[0]
        self.pos = list(pos)
        self.speed = speed
        self.fs = fs
        self.f = 0

    def load(self,i):
        return Image.open("images/{0}.png".format(i)).convert("RGBA")

    def move(self):
        self.f += self.fs
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        
        if (self.f > len(self.images)):
            self.f = 0

        self.image = self.images[int(self.f)]
        
    def paint(self,canvas):
        canvas.paste(self.image, tuple(map(int,self.pos)), mask=self.image)


