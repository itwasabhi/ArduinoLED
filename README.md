ArduinoLED
==========

Python scripts to control LED String. This repository contains a series of files for controlling different lighting effects, as well as the code to run on the Arduino.

1) Music-LED

The 'Soundlight_Color.py' is used to control the lights using sound/music for any input-audio device. Installing the application "Soundflowerbed" allows for treating the computer's build-in output audio as an input-audio device.  

The following is a list of required dependencies for Soundlight_Color:
- pyaudio
- matplotlib (can be removed)
- pyserial

Contains many parameters to modify the performance of the music-processing within the file.  

2) Meld

Slowly loop through colors. 


*Note the Arduino pins being used are 9,10, and 11. Other pins can be used provided they are PWM pins. 
