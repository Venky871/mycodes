#!/usr/bin/env python
__author__ = 'skunda'
# This program logs a Raspberry Pi's CPU temperature to a Thingspeak Channel
# To use, get a Thingspeak.com account, set up a channel, and capture the Channel Key at https://thingspeak.com/docs/tutorials/ 
# Then paste your channel ID in the code for the value of "key" below.
# Then run as sudo python pitemp.py (access to the CPU temp requires sudo access)
# You can see my channel at https://thingspeak.com/channels/41518
#!/usr/bin/python
import sys
import Adafruit_DHT
import httplib, urllib
import time
from random import randint
import serial
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
sleep = 30 # how many seconds to sleep between posts to the channel
key = 'DKJDKYBFR1HPLJWJ'  # Thingspeak channel to update
#Report Raspberry Pi internal temperature to Thingspeak Channel
def thermometer():
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        ser=serial.Serial('/dev/ttyACM0',9600)
        GPIO.wait_for_edge(23, GPIO.FALLING)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        print "\nFalling edge detected. Now your program can continue with"  
        read_serial=ser.readline()
        print read_serial
        ser.close()
        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        ran01 =randint (0,10)       
        humidity1, temperature1 = Adafruit_DHT.read_retry(11, 4)
        print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature1, humidity1)
        params = urllib.urlencode({'field1': temperature1 , 'field2': read_serial , 'key':key}) 
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print ran01
            print response.status, response.reason
            data = response.read()
            conn.close()
        except:
            print "connection failed"
        break
#sleep for desired amount of time
if __name__ == "__main__":
        while True:
                thermometer()
                time.sleep(sleep)


