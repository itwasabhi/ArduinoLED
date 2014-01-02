import serial
import colorsys
ser = serial.Serial('/dev/tty.usbmodem1411')

def convRGB(hsv):
    rgb = colorsys.hsv_to_rgb(hsv[0],hsv[1],hsv[2]**2) #Convert HSV to RGB
    return rgb
    
def HSVtoSerial(hsv):
    rgb = convRGB(hsv) #Convert HSV to RGB
    output=str(int(rgb[0]*255))+","+str(int(rgb[1]*255))+","+str(int(rgb[2]*255))+";"
    print str(int(hsv[0]*360))+","+str(int(hsv[1]*100))+","+str(int(hsv[2]*100))+";"
    #Send output through serial
    ser.write(output)
    

