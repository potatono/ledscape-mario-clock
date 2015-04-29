import time, datetime
from PIL import Image, ImageFont, ImageDraw
from weather import Weather
from cloud import Cloud
from rain import Rain

class Visualization(object):
    def __init__(self, width=64, height=64):
        self.width = width
        self.height = height
        self.frame = 0
        self.starttime = time.time()

        self.im = Image.new("RGBA", (width,height), "black")
        self.im_draw = ImageDraw.Draw(self.im)

        self.bg = Image.open("images/bg_normal_big.png")
        self.bgofs = 0

        self.font = ImageFont.truetype("fonts/spincycle.ttf", 18)
        self.font_sm = ImageFont.truetype("fonts/pf_tempesta_seven.ttf", 8)

        self.clouds = Cloud.create(20)
        self.weather = Weather()
        self.rain = Rain()
        self.conditions = ""

    def drawtime(self):
        now = datetime.datetime.now()
        t = now.strftime("%H:%M")
        self.im_draw.text((8,0), t, (16,16,16) ,font=self.font)

    def updateweather(self):

        self.weather.update()

        if (self.weather.wind == 0):
            cloudspeed = 0
        elif (self.weather.windbearing <= 90 or self.weather.windbearing >= 270):
            cloudspeed = float(self.weather.wind)/-30.0
        else:
            cloudspeed = float(self.weather.wind)/30.0
        
        for i in xrange(self.weather.cover,20):
            if self.clouds[i].active:
                self.clouds[i].deactivate()

        for i in xrange(self.weather.cover):
            if not self.clouds[i].active:
                self.clouds[i].activate(cloudspeed)

        if (self.weather.conditions == 'snow' or self.weather.conditions == 'hail' or self.weather.conditions == 'sleet'):
            self.bg = Image.open('images/bg_icy_normal.png')
        elif (time.time() > self.weather.sunset + 1800 or time.time() < self.weather.sunrise):
            self.bg = Image.open('images/bg_night.png')
        elif (self.weather.cover > 10):
            self.bg = Image.open('images/bg_dark.png')
        elif (time.time() >= self.weather.sunset and time.time() <= self.weather.sunset + 1800):
            self.bg = Image.open('images/bg_sunset_big.png')
        elif (time.time() >= self.weather.sunrise and time.time() <= self.weather.sunrise + 1800):
            self.bg = Image.open('images/bg_sunset_big.png')
        else:
            self.bg = Image.open('images/bg_normal_big.png')

    def applysunset(self):
        pix = self.bg.load()
        for x in xrange(self.width):
            for y in xrange(self.height):
                if (x == 0 and y == 0):
                    print pix[x,y]
                if pix[x,y] == (0,96,184):
                    pix[x,y] = (255,255,255)


    def drawweather(self):
        cond = self.weather.conditions
        if (cond == "rain" or cond == "hail" or 
            cond == "thunderstorm" or cond == "snow" or
            cond == "sleet"):
                self.rain.move()
                self.rain.paint(self.im_draw, (225,225,225) if (cond =="snow" or cond == "sleet") else (96,96,200))

        for i in xrange(20):
            self.clouds[i].move()
            self.clouds[i].paint(self.im)
    
        self.im_draw.text((17,53), "{0}".format(int(float(self.weather.temp))), (0,0,0) ,font=self.font_sm)
        self.im_draw.point((30,57),(0,0,0))
        self.im_draw.point((31,58),(0,0,0))
        self.im_draw.point((30,59),(0,0,0))
        self.im_draw.point((29,58),(0,0,0))

        self.im_draw.text((33,53), "{0}".format(int(float(self.weather.rf))), (0,0,0) ,font=self.font_sm)
        self.im_draw.point((46,57),(0,0,0))
        self.im_draw.point((47,58),(0,0,0))
        self.im_draw.point((46,59),(0,0,0))
        self.im_draw.point((45,58),(0,0,0))

    def drawbg(self):
        if self.bg.size[0] > self.width:
            if self.frame % 30 == 0:
                self.bgofs = self.bgofs + 1

                if self.bgofs > self.bg.size[0]:
                    self.bgofs = 0

            self.im.paste(self.bg.crop((self.bgofs,0,self.width+self.bgofs,self.height)), (0,0,self.width,self.height))

            if self.bgofs > self.bg.size[0]-self.width:
                o = self.width-(self.bg.size[0]-self.bgofs)
                self.im.paste(self.bg.crop((0,0,o,self.height)), (self.width-o,0,self.width,self.height))

        else:
            self.im.paste(self.bg, (0,0,self.width,self.height))

    def fps(self):
        return self.frame/(time.time()-self.starttime)

    def draw(self):
        if self.frame % 1800 == 0:
            self.updateweather()

        self.drawbg()
        self.drawweather()
        self.drawtime()

        self.pixels = self.im.convert("RGB").tostring()
        self.frame = self.frame + 1
