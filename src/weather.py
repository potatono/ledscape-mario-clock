from darksky import Darksky
from config import Config

class Weather(object):
    def __init__(self):
        self.darksky = Darksky()
        self.temp = Config.config.getfloat("weather","temp")
        self.rf = Config.config.getfloat("weather","rf")
        self.conditions = Config.config.get("weather","conditions")
        self.wind = Config.config.getfloat("weather","wind")
        self.windbearing = Config.config.getfloat("weather","windbearing")
        self.cover = Config.config.getint("weather","cover")
        self.sunset = Config.config.getint("weather","sunset")
        self.sunrise = Config.config.getint("weather","sunrise")

    def update(self):
        if (Config.config.getboolean("weather","fake")):
            print "Using fake weather data from config"
        else:
            currently = self.darksky.get()['currently']
	
            # clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, 
            # partly-cloudy-day, or partly-cloudy-night. 
            # (Developers should ensure that a sensible default is defined, as additional 
            # values, such as hail, thunderstorm, or tornado, may be defined in the future.)
            self.conditions = currently['icon']
            
            self.wind = currently['windSpeed']
            self.windbearing = currently['windBearing']
            self.cover = int(currently['cloudCover'] * 20);
            
            self.temp = currently['temperature']
            self.rf = currently['apparentTemperature']
            self.sunset = self.darksky.get()['daily']['data'][0]['sunsetTime']
            self.sunrise = self.darksky.get()['daily']['data'][0]['sunriseTime']

        print "temp=",self.temp,"wind=",self.wind,"cover=",self.cover, "conditions=",self.conditions,"rf=",self.rf
