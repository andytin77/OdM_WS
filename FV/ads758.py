#!/usr/bin/python 

##################################################################################
# laika_gas_sensors.py - reads MQ series gas sensors and prints out their data 
# values. Based on the Adafruit ads1x15_ex_singleended.py example script, so credit 
# for the code goes to Adafruit. 
# 
# Philip R. Moyer 
# March 2016 
################################################################################## 

######################### 
# Imports 
######################### 

import time, signal, sys 
import Adafruit_ADS1x15
import requests
######################### 
# Globals 
######################### 
# Classes and Methods 
######################### 


######################### 
# Functions 
######################### 

def signal_handler(signal, frame): 
    print('You pressed Ctrl+C!') 
    sys.exit(0) 
signal.signal(signal.SIGINT, signal_handler) 
#print('Press Ctrl+C to exit') 

######################### 
# Main 
######################### 

ADS1015 = 0x00 # 12-bit ADC 
ADS1115 = 0x01 # 16-bit ADC 

# Select the gain 
# gain = 2/3 # +/- 6.144V 
GAIN = 1 # +/- 4.096V 
# gain = 2 # +/- 2.048V 
# gain = 4 # +/- 1.024V 
# gain = 8 # +/- 0.512V 
# gain = 16 # +/- 0.256V 


# Initialise the ADCs using the default mode (use appropriate I2C address) 
adc = Adafruit_ADS1x15.ADS1115()
url ="http://www.ortodimontagna.com/meteo/victron/saveCurrent.php"
#1
i = 0
while(i < 40):
	out = (2.49 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)
out = (2.49 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04

obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)
#2
i = 0
while(i < 40):
	out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)


out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04
print(out)
obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)
time.sleep(1)
#3
i = 0
while(i < 40):
	out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)
out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04

print(out)
obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)

#1
i = 0
while(i < 40):
	out = (2.49 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)
out = (2.49 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04

obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)
#2
i = 0
while(i < 40):
	out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)


out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04
print(out)
obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)
time.sleep(1)
#3
i = 0
while(i < 40):
	out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)
out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04

print(out)
obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)

#1
i = 0
while(i < 40):
	out = (2.49 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)
out = (2.49 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04

obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)
#2
i = 0
while(i < 40):
	out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)


out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04
print(out)
obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)
time.sleep(1)
#3
i = 0
while(i < 40):
	out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04 
	print(out)
	i = i+1
	time.sleep(0.5)
out = (2.50 - (float)(adc.read_adc(0, gain=GAIN) / 32768.0 * 4.096)) / 0.04

print(out)
obj = {'current' : str(out)} 
r = requests.post(url, data=obj)
print(r.text)



