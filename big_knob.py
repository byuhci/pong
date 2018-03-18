#!/usr/bin/env python3

import time
import serial
from threading import Thread
from data.control import Control  # pong game


class BigKnob:

    def __init__(self, port):
        self.port = serial.Serial(port=port)

        self.running = True
        self.thread = Thread(target=self.receiving).start()
        
        self.knob_angle = 0
        self.knob_old_angle = 0
        self.slider_pos = 0
        self.solder_old_pos = 0
        self.button_pressed = False

    def stop(self):
        self.running = False
        
    def get_knob_delta(self):
        ret = self.knob_angle - self.knob_old_angle
        self.knob_old_angle = self.knob_angle
        return ret

    def get_slider_delta(self):
        ret = self.slider_pos - self.slider_old_pos
        self.slider_old_pos = self.slider_pos
        return ret

    def get_button_pressed(self):
        return self.button_pressed
        
    def receiving(self):
        buf = ''
        while not self.port.isOpen():
            time.sleep(0.5)
        while self.running:
            time.sleep(0.05)
            buf += self.port.read(self.port.inWaiting()).decode()
            if '\n' in buf:
                lines = buf.split('\n')
                last = lines[-2].split()
                buf = lines[-1]
                print(', '.join(last))
                self.knob_angle = int(last[0])
                self.slider_pos = int(last[1])
                self.button_pressed = True if last[2] == '1' else False
        self.port.close()
                
                
def main(*args):

    hid = BigKnob(args[1])
    Control(False, 'hard', (800, 600), hid).run()
    hid.thread.join()
    
    print('Goodbye')


if __name__ == '__main__':
    import sys
    main(*sys.argv)
