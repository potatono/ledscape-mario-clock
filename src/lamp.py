import socket
import time, datetime
from visualization import Visualization
from config import Config

dest = (Config.config.get("general","host"), Config.config.getint("general","port"))
width = Config.config.getint("general","width")
height = Config.config.getint("general","height")
sleeptime = Config.config.getfloat("general","sleeptime")

visualization = Visualization(width,height)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, width*height*3+1);

while True:
    visualization.draw()
    sock.sendto(chr(0) + visualization.pixels, dest)
    time.sleep(sleeptime)
        
    if visualization.frame % 100 == 0:
        print "{:0.2f} FPS".format(visualization.fps())
        
