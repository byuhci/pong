#!/usr/bin/env python3

import random
import cv2
import numpy as np
import time
from operator import itemgetter
from data.control import Control  # pong game


class ArucoBigKnob:
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    def __init__(self, display=False):
        self.cam = cv2.VideoCapture(0)
        self.angle = 0
        self.display = display
        self.knob_detect()

    def knob_detect(self, angle=0):
        success, frame = self.cam.read()
        if success:
            corners, ids, params = cv2.aruco.detectMarkers(frame, self.aruco_dict)
            if corners:
                if self.display:
                    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                if set([0, 1, 2]).issuperset(list(ids.flatten())):
                    arcs = [corners[x][0][0] for x in
                            next(zip(*sorted(enumerate(ids),
                                             key=itemgetter(1))))]
                    vecs = [corners[x][0][1] for x in
                            next(zip(*sorted(enumerate(ids),
                                             key=itemgetter(1))))]
                    avec = np.zeros(2)
                    for arc, vec in zip(arcs, vecs):
                        if self.display:
                            cv2.line(frame, tuple(arc.astype('int')),
                                     tuple(vec.astype('int')), (255,0,0), 5)
                        avec += vec - arc
                    angle = np.arctan2(-avec[1], avec[0])
                    if self.display:
                        cv2.putText(frame, str(angle), (10, 1000),
                                    cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 3)
            elif self.display:            
                cv2.putText(frame, "No markers found", (10, 1000),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 3)
            if self.display:
                cv2.imshow("Knob", frame)
                cv2.waitKey(1)
        return angle

    def get_delta(self):
        old_angle = self.angle
        self.angle = self.knob_detect(old_angle)
        diff = 25*np.subtract(*np.unwrap((self.angle, old_angle)))
        ret = round(diff)
        self.angle -= (diff-ret)/25
        return -ret


def main():
    
    Control(False, 'hard', (800, 600), ArucoBigKnob()).run()

    # cv2.destroyAllWindows()
    # cam.release()  # Seems to cause segfaults (at least on mac)
    # cv2.waitKey(1000)
    time.sleep(2)
    
    print('Goodbye')


if __name__ == '__main__':
    main()
