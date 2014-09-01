from PIL import Image, ImageFont, ImageDraw
import socket
import time, datetime
from colorsys import hsv_to_rgb
from cloud import Cloud
from weather import Weather
from rain import Rain

dest = ("localhost", 9999)
width = 64
height = 64
frame = 0
temp = 0
starttime = time.time()
sleeptime = 0.02
rf = 0

im = Image.new("RGBA", (width,height), "black")
im_draw = ImageDraw.Draw(im)
bg = Image.open("images/bg_normal_big.png")
bgofs = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, width*height*3+1);
font = ImageFont.truetype("fonts/spincycle.ttf", 18)
font_sm = ImageFont.truetype("fonts/pf_tempesta_seven.ttf", 8)

clouds = Cloud.create(20)
weather = Weather()
rain = Rain()
conditions = ""

def drawtime():
    now = datetime.datetime.now()
    t = now.strftime("%H:%M")
    im_draw.text((8,0), t, (16,16,16) ,font=font)

def calcweather():
    global bg
    global temp
    global rf
    global conditions

    print "Calculating weather"
    hour = datetime.datetime.now().hour
    # Mostly Cloudy, Partly Cloudy, Fair | Clear, Clouds, Overcast, Fog, Smoke, 
    # Freezing, Ice, Snow, Rain, Thunderstorm, Windy, Funnel / Tornado, Dust, Haze
    conditions = weather.find('weather')
    wind = weather.find('wind_mph')
    cloudspeed = float(wind)/30.0 * { 
            'North':-1, 
            'East':-1, 
            'Northeast':-1 
            }.get(weather.find("wind_dir"),1)

    cover = {
            'Partly Cloudy': 3,
            'Cloudy': 7,
            'Mostly Cloudy': 10,
            'Light Rain': 12,
            'Overcast': 15,
            'Fog': 20,
            'Rain': 20,
            'Thunderstorm': 20,
            'Snow': 20 }.get(conditions, 0)

    if (conditions == 'Snow' or conditions == 'Ice' or conditions == 'Freezing'):
        bg = Image.open('images/bg_icy_normal.png')
    elif (hour > 18 or hour < 5):
        bg = Image.open('images/bg_night.png')
    elif (cover > 10):
        bg = Image.open('images/bg_dark.png')
    else:
        bg = Image.open('images/bg_normal_big.png')

    for i in xrange(cover,20):
        if clouds[i].active:
            clouds[i].deactivate()

    for i in xrange(cover):
        if not clouds[i].active:
            clouds[i].activate(cloudspeed)

    temp = float(weather.find('temp_f'))
    hum = float(weather.find('relative_humidity'))
    rf = weather.heatindex()

    print "temp=",temp,"wind=",wind,"cover=",cover, "conditions=",conditions,"rf=",rf, "hum=",hum

def drawweather():
    if conditions == "Rain" or conditions == "Light Rain" or conditions == "Thunderstorms":
        rain.move()
        rain.paint(im_draw)

    for i in xrange(10):
        clouds[i].move()
        clouds[i].paint(im)
    
    im_draw.text((1,53), "{0}".format(int(float(temp))), (0,0,0) ,font=font_sm)
    im_draw.point((14,57),(0,0,0))
    im_draw.point((15,58),(0,0,0))
    im_draw.point((14,59),(0,0,0))
    im_draw.point((13,58),(0,0,0))

    im_draw.text((17,53), "{0}".format(int(float(rf))), (0,0,0) ,font=font_sm)
    im_draw.point((30,57),(0,0,0))
    im_draw.point((31,58),(0,0,0))
    im_draw.point((30,59),(0,0,0))
    im_draw.point((29,58),(0,0,0))

def drawbg():
    global bgofs

    if bg.size[0] > width:
        if frame % 30 == 0:
            bgofs = bgofs + 1

            if bgofs > bg.size[0]:
                bgofs = 0

        im.paste(bg.crop((bgofs,0,width+bgofs,height)), (0,0,width,height))

        if bgofs > bg.size[0]-width:
            o = width-(bg.size[0]-bgofs)
            im.paste(bg.crop((0,0,o,height)), (width-o,0,width,height))

    else:
        im.paste(bg, (0,0,width,height))


while True:
    if frame % 1800 == 0:
        calcweather()

    drawbg()
    drawweather()
    drawtime()

    sock.sendto(chr(0) + im.convert("RGB").tostring(), dest)
    time.sleep(sleeptime)

    frame = frame + 1

    if frame % 100 == 0:
        fps = frame/(time.time()-starttime)
        print "{:0.2f} FPS".format(fps)


