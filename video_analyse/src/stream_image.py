import cv2
import copy as cp
import helper as hp

class Stream:
    IP = '147.88.48.131'
    NAME = 'pren'
    PWD = '463997'
    PARAM = 'pren_profile_small'

    def getFrame(width, height, f):
        cap = cv2.VideoCapture('rtsp://'+
        Stream.NAME+
        ':'+Stream.PWD+
        '@'+Stream.IP+'/axis-media/media.amp'+
        '?streamprofile='+Stream.PARAM)
    
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', Stream.IP)
            return None
        
        frame = None
        c = 0
        while c <= f:
            ret, frame = cap.read()
            c += 1

        frame = cv2.resize(frame, (width, height))
        return frame

img1 = Stream.getFrame(600, 400, 0)
img2 = Stream.getFrame(600, 400, 13*21)

if img1 is not None and img2 is not None:

    while True:
        cv2.imshow('0', img1)
        cv2.imshow('180', img2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break