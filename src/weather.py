import time
import datetime
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
            daily = self.darksky.get()['daily']['data']
	
            # clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, 
            # partly-cloudy-day, or partly-cloudy-night. 
            # (Developers should ensure that a sensible default is defined, as additional 
            # values, such as hail, thunderstorm, or tornado, may be defined in the future.)
            self.conditions = currently['icon']
            
            self.wind = currently['windSpeed']
            self.windbearing = currently['windBearing']
            self.cover = currently['cloudCover'];
            
            self.temp = currently['temperature']
            self.rf = currently['apparentTemperature']
            
            if (datetime.datetime.now().hour >= 12):
                self.sunrise = daily[1]['sunriseTime']
                self.sunset = daily[0]['sunsetTime']
            else:
                self.sunrise = daily[0]['sunriseTime']
                self.sunset = time.time() - 43200

        print "temp=",self.temp,"wind=",self.wind,"cover=",self.cover, "conditions=",self.conditions,"rf=",self.rf
        print "sunrise=",self.sunrise,"sunset=",self.sunset
