# Python 2.7 code to analyze sound and interface with Arduino
 
import pyaudio # from http://people.csail.mit.edu/hubert/pyaudio/
import numpy   # from http://numpy.scipy.org/
from pylab import *
import audioop
import sys
import math
import struct
import ArduinoLED
from datetime import datetime
'''
Sources
 
http://www.swharden.com/blog/2010-03-05-realtime-fft-graph-of-audio-wav-file-or-microphone-input-with-python-scipy-and-wckgraph/
http://macdevcenter.com/pub/a/python/2001/01/31/numerically.html?page=2

http://julip.co/2012/05/arduino-python-soundlight-spectrum/
 
'''
 
MAX = 0
 
def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print str(i)+'. '+dev['name']
        i += 1
 
def arduino_soundlight(dev):
    #Set Graphing
    graph = 2 #0, No graph. 1, Color. 2, Waveform
    if(graph==1):
        ch_v=14
        ion()
    if(graph==2):
        ch_v=12
        ion()
    if(graph==0):
        ch_v=11
        
    chunk      = 2**ch_v # Change if too fast/slow, never less than 2**11
    scale      = 30    # Change if too dim/bright
    exponent   = 6    # Change if too little/too much difference between loud and quiet sounds
    samplerate = 44100 
    divs = 15   #Defintion of wave form. Higher number = more definition
    alpha = 0.5 #Exponential Average, Levels Change Rate
    beta = 0.75 #Exponential Average, 'Value' Change Rate
    hueThresh = 0.7e13 #Difference needed in Low frequency value to count as a beat
    hueJump = 0.2 #Amount of colors to "skip" when beat detected
    colorWrap = 35 #Approximately the time (s) to come back to the same color - assuming no Beats
    
    h=0
    s=1
    v=0
    max_lvls=1
    
    device = dev

    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)

    print "Starting, use Ctrl+C to stop"
    t=1
    prevLowF =0
    try:
        while True:
            t1 = datetime.now()
            data  = stream.read(chunk)
 
            # Do FFT
            levels = calculate_levels(data, chunk, samplerate, divs)
            
            #Obtain value for 'Value' from levls
            avg_lvls = sum(levels)/len(levels)
            if(avg_lvls>max_lvls):
                max_lvls = avg_lvls
            temp_v = avg_lvls*(1.0/max_lvls)
            if (temp_v<0):
                temp_v=0
            v = temp_v*beta+v*(1-beta)
            
            #Process and filter levels to obtain modified waveform
            idx=0
            plotLev = zeros(divs)
            for level in levels:
                level = level**exponent 
                plotLev[idx] = level*alpha+(1-alpha)*plotLev[idx]
                idx = idx+1
            print "------"
            
            currLowF = (plotLev[0])
            if((currLowF-prevLowF)>hueThresh):
                h =h + hueJump
                print "BEAT"
                print
                print
                print
            prevLowF = currLowF
            t2 = datetime.now()
            delta = t2-t1
            Hue_Fraction = (delta.microseconds/1e6)/colorWrap

            h = h+Hue_Fraction
            if(h>1):
                h=0
            ArduinoLED.HSVtoSerial((h,s,v**2))    #Convert RGB to string for Arduino
            
            #Post Processing Steps
            if (graph==1):      #Graph Color
                rgb_tuple = ArduinoLED.convRGB((h,s,v**2))
                gca().add_patch(Rectangle((0,0),1,1, color=rgb_tuple))
                draw()
            if (graph==2):       #Graph Waves
                if(t==1):
                    hl, = plot(plotLev)
                    axis([0, divs, 0, 200**exponent/4])
                    draw()
                    t = t+1
                else:
                    hl.set_ydata(plotLev)
                    draw()     
    except KeyboardInterrupt:
        pass
    finally:
        print "\nStopping"
        stream.close()
        p.terminate()
        
 
def calculate_levels(data, chunk, samplerate, divs):
    # Use FFT to calculate volume for each frequency
    global MAX
 
    # Convert raw sound data to Numpy array
    fmt = "%dH"%(len(data)/2)
    data2 = struct.unpack(fmt, data)
    data2 = numpy.array(data2, dtype='h')
 
    # Apply FFT
    fourier = numpy.fft.fft(data2)
    ffty = numpy.abs(fourier[0:len(fourier)/2])/1000
    ffty1=ffty[:len(ffty)/2]
    ffty2=ffty[len(ffty)/2::]+2
    ffty2=ffty2[::-1]
    ffty=ffty1+ffty2
    ffty=numpy.log(ffty)-2
    
    fourier = list(ffty)[4:-4]
    fourier = fourier[:len(fourier)/2]
    
    size = len(fourier)
 
    levels = [sum(fourier[i:(i+size/divs)]) for i in xrange(0, size, size/divs)][:divs]
    
    return levels
    
def SelectAudio():
    print"Available Audio Devices:"
    list_devices()
    print
    return raw_input("Select Audio Device:")
        
if __name__ == '__main__':
    #dev = int(SelectAudio())

    dev=2 #Soundflower 2ch
    arduino_soundlight(dev)