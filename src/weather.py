import urllib
from xml.etree.ElementTree import parse
import time
import math

class Weather(object):
    def __init__(self, url="http://w1.weather.gov/xml/current_obs/display.php?stid=KJFK"):
        self.url = url
        self.last = 0
        self.root = None

        self.fetch()

    def fetch(self):
        try:
            text = urllib.urlopen(self.url)
            self.root = parse(text).getroot()
            self.last = time.time()
        except:
            pass

    def find(self,e):
        if (time.time() - self.last > 60):
            self.fetch()

        return self.root.find(e).text

    def heatindex(self):
        t = float(self.find('temp_f'))
        rh = float(self.find('relative_humidity'))


        if (t < 80):
            return  0.5 * (t + 61.0 + ((t-68.0)*1.2) + (rh*0.094))
        else:
            hi = -42.379 + 2.04901523*t + 10.14333127*rh - .22475541*t*rh - \
                    .00683783*t*t - .05481717*rh*rh + .00122874*t*t*rh + \
                    .00085282*t*rh*rh - .00000199*t*t*rh*rh

            if rh < 13:
                hi -= ((13-rh)/4)*math.sqrt(((17-abs(t-95))/17))
            elif rh > 85:
                hi += ((rh-85)/10) * ((87-t)/5)

            return hi

if __name__ == '__main__':
    weather = Weather()
    print weather.find('weather')

