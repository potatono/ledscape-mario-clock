import hypermedia.net.*;

int WIDTH = 64;
int HEIGHT = 64;
int SCALE = 5;

UDP udp;
byte[] data = null;

void setup() {
  size(320,320);
  udp = new UDP(this,9999);
  udp.listen(true);
  background(0);
}

void draw() {
  if (data != null) {
    for (int y=0; y<HEIGHT; y++) {
      for (int x=0; x<WIDTH; x++) {
        int i = (y*WIDTH+x)*3+1;
        fill(int(data[i]),int(data[i+1]),int(data[i+2]));
        noStroke();
        rect(x*SCALE,y*SCALE,SCALE,SCALE);   
      }
    }
  }
}

void receive(byte[] data, String ip, int port) {
  //println("Received packet " + data.length);
  //background(0);
  this.data = data;
}