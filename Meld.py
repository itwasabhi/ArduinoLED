import ArduinoLED
import time

if __name__ == '__main__':
    h=0
    s=1
    v=1
    rate = 0.01 #Change rate
    while True:
        h=h+rate
        if (h>1):
            print "Wraparound"
            h=0
        time.sleep(.1)
        ArduinoLED.HSVtoSerial((h,s,v))