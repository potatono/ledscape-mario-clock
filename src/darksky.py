import requests
import json
import time
import math
from config import Config

class Darksky(object):
    defaulturl = ("https://api.forecast.io/forecast/" + 
        Config.config.get('darksky','key') + "/" + 
        Config.config.get('darksky','lat') + "," +
        Config.config.get('darksky','long'))

    def __init__(self, url=defaulturl):
        self.url = url;
        self.last = 0;
        self.root = None;

    def fetch(self):
        try:
            r = requests.get(self.url)
            self.root = r.json()
            self.last = time.time()
        except Exception as e:
            print e
            pass

    def get(self):
        if (time.time() - self.last > 120):
            self.fetch()

        return self.root

if __name__ == '__main__':
    darksky = Darksky()
    print darksky.get()

