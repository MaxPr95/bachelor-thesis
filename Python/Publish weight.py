import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
#import mysql.connector;
#import time;
#import Adafruit_DHT as dht
import paho.mqtt.publish as publish
#import paho.mqtt.client as mqtt
#import json



###################### Calibration start ########################

try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    hx = HX711(dout_pin=21, pd_sck_pin=20)
    err = hx.zero()
    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')

    reading = hx.get_raw_data_mean()
    if reading:  # always check if you get correct value or only False
        # now the value is close to 0
        print('Data subtracted by offset but still not converted to units:',
              reading)
    else:
        print('invalid data', reading)

    input('Put known weight on the scale and then press Enter')
    reading = hx.get_data_mean()
    if reading:
        print('Mean value from HX711 subtracted by offset:', reading)
        known_weight_grams = input(
            'Write how many grams it was and press Enter: ')
        try:
            value = float(known_weight_grams)
            print(value, 'grams')
        except ValueError:
            print('Expected integer or float and I have got:',
                  known_weight_grams)

        ratio = reading / value  # calculate the ratio for channel A and gain 128
        hx.set_scale_ratio(ratio)  # set ratio for current channel
        print('Ratio is set.')
    else:
        raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    input('Press Enter to begin reading')
    print('Current weight on the scale in grams is: ')
    
###################### Calibration end ########################
    
###################### Weighing ########################
    while True:
        weight = float(hx.get_weight_mean()) # saving weight in variable "weight"
        try:
            publish.single('WS/shelf/#', (weight), hostname="192.168.2.112")  #via MQTT, sending variable to broker          
        except:
            print('cant');
    
    
    
    
except (KeyboardInterrupt, SystemExit):
    print('Bye :)')