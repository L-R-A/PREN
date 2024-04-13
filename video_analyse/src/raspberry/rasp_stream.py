import cv2

class Stream:
    IP = '147.88.48.131'
    NAME = 'pren'
    PWD = '463997'
    PARAM = 'pren_profile_small'

    def getFrame(width, height, f, amount=1, delay=1):
        cap = cv2.VideoCapture('rtsp://'+
        Stream.NAME+
        ':'+Stream.PWD+
        '@'+Stream.IP+'/axis-media/media.amp'+
        '?streamprofile='+Stream.PARAM)
    
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', Stream.IP)
            return None
        
        frames=[]
        
        frame = None
        c = 0
        while c <= f:
            ret, frame = cap.read()
            c += 1

        found = 0

        while c <= (f + (amount * delay)) and (found < amount):
            ret, frame = cap.read()
            
            if ((c == (f + 1)) or c % delay == 0):
                print("FRAME FOUND: " + str(c))
                
                frame = cv2.resize(frame, (width, height))
                frames.append(frame)
                found = found + 1

            c += 1

        return frames
