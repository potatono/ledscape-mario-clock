import ConfigParser
import os

class Config:
    config = ConfigParser.ConfigParser()
    config.add_section("weather")
    config.set("weather","fake","false")
    config.set("weather","temp","45")
    config.set("weather","rf","40")
    config.set("weather","conditions","rain")
    config.set("weather","wind","10")
    config.set("weather","windbearing","30")
    config.set("weather","cover","20")
    config.set("weather","sunset","0")
    config.set("weather","sunrise","0")
    config.read(os.path.expanduser('~/.config/mario-clock.cfg'))

