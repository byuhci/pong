#!/usr/bin/env python3

import random
import time
import serial
from threading import Thread
from operator import itemgetter
from data.control import Control  # pong game


class BigKnob:

    def __init__(self, port):
        self.port = serial.Serial(port=port)
        self.last = ''
        self.thread = Thread(target = self.receiving).start()        
        self.angle = 0
        self.slider = 0

    def get_knob_delta(self):
        old_angle = self.angle
        if self.last:
            self.angle = int(self.last.split()[0])
            return self.angle - old_angle
        else:
            return 0

    def get_slider_delta(self):
        old_slider = self.slider
        if self.last:
            self.slider = int(self.last.split()[1])
            return self.slider - old_slider
        else:
            return 0

    def get_button_pressed(self):
        return True if self.last and self.last.split()[2]=='1' else False
        
    def receiving(self):
        buf = ''
        while not self.port.isOpen():
            time.sleep(0.5)
        while True:
            buf += self.port.read(self.port.inWaiting()).decode()
            if '\n' in buf:
                lines = buf.split('\n')
                self.last = lines[-2]
                buf = lines[-1]
                print(self.last)

def main(*args):
    
    Control(False, 'hard', (800, 600), BigKnob(args[1])).run()

    # cv2.destroyAllWindows()
    # cam.release()  # Seems to cause segfaults (at least on mac)
    # cv2.waitKey(1000)
    time.sleep(2)
    
    print('Goodbye')


if __name__ == '__main__':
    import sys
    main(*sys.argv)
