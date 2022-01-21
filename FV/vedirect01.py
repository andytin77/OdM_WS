#!/usr/bin/python
# -*- coding: utf-8 -*-

# This code is heavily based on the code written by Janne Kario for his
# Simple VE.Direct reader for Python project available at
# https://github.com/karioja/vedirect and listed on the Victron Energy
# Open Source webpage https://www.victronenergy.com/live/open_source:start

import os, serial
from sys import stdout
from time import sleep
from time import time
import requests

ports = {
    #'mppt': '/dev/serial/by-id/usb-FTDI_FT232EX-if00-port0',
    'bmv': '/dev/serial/by-id/usb-VictronEnergy_BV_VE_Direct_cable_VE4ARI91-if00-port0'
	#VE3AP7M4
    #'conv': '/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_011D4D72-if00-port0'
    }

divs = {'V': ['bmv', 'V'],
	'VPV': ['bmv', 'VPV'],
	'PPV': ['bmv', 'PPV'],
	'I': ['bmv', 'I'],
#	'Load Current': ['bmv', 'IL'],
#	'Load output state (ON/OFF)': [ 'LOAD'], 
	#'batteries_bdy': ['bmv', 'V', 'I'], 
	'H19': ['bmv','H19'], 
	'H20': ['bmv', 'H20'],
	'H21': ['bmv', 'H21'],
	'H22': ['bmv', 'H22'],
	'H23': ['bmv', 'H23'],
	'ERR': ['bmv', 'ERR'],
	'CS': ['bmv', 'CS'],	
	#'Firmware version': ['bmv', 'FW'],
	#'Product ID': ['bmv', 'PID'],
	'SER#': ['bmv', 'SER#'],
	'HSDS': ['bmv', 'HSDS']
    }

units = {
    'V': 'mV',
    'VS': 'mV',
    'VM': 'mV', 
    'DM': '%', 
    'VPV': 'mV', 
    'PPV': 'W', 
    'I': 'mA', 
    'IL': 'mA', 
    'LOAD': '', 
    'T': '°C', 
    'P': 'W', 
    'CE': 'mAh', 
    'SOC': '%', 
    'TTG': 'Minutes', 
    'Alarm': '', 
    'Relay': '', 
    'AR': '', 
    'H1': 'mAh', 
    'H2': 'mAh', 
    'H3': 'mAh', 
    'H4': '',
    'H5': '', 
    'H6': 'mAh', 
    'H7': 'mV', 
    'H8': 'mV', 
    'H9': 'Seconds', 
    'H10': '', 
    'H11': '', 
    'H12': '', 
    'H15': 'mV', 
    'H16': 'mV', 
    'H17': '0.01 kWh', 
    'H18': '0.01 kWh', 
    'H19': '0.01 kWh', 
    'H20': '0.01 kWh', 
    'H21': 'W', 
    'H22': '0.01 kWh', 
    'H23': 'W', 
    'ERR': '', 
    'CS': '*', 
    'BMV': '', 
    'FW': '', 
    'PID': '', 
    'SER#': '', 
    'HSDS': '', 
    }
    
cs = {
    '0': 'Off', '2': 'Fault', '3': 'Bulk', 
    '4': 'Abs', '5': 'Float'
    }
    
fmt = {
    '%': ['%',10,1], 
    '°C': ['°C',1,0], 
    '0.01 kWh': ['Wh',.1,2], 
    'mA': ['A',1000,2], 
    'mAh': ['Ah', 1000,2], 
    'Minutes': ['Mins',1,0], 
    'mV': ['V',1000,2], 
    'Seconds': ['Secs',1,0], 
    'W': ['W',1,0]
    }

class vedirect:

    def __init__(self, serialport):
        self.serialport = serialport
        self.ser = serial.Serial(serialport, 19200, timeout=60)
        self.header1 = '\r'
        self.header2 = '\n'
        self.hexmarker = ':'
        self.delimiter = '\t'
        self.key = ''
        self.start = ''
        self.value = ''
        self.bytes_sum = 0;
        self.state = self.WAIT_HEADER
        self.dict = {}

    (HEX, WAIT_HEADER, IN_KEY, IN_VALUE, IN_CHECKSUM) = range(5)

    def input(self, byte):
        if byte == self.hexmarker and self.state != self.IN_CHECKSUM:
            self.state = self.HEX
            
        
        if self.state == self.WAIT_HEADER:
            self.bytes_sum += ord(byte)
            if byte == self.header1:
                self.state = self.WAIT_HEADER
            elif byte == self.header2:
                self.state = self.IN_KEY
            return None
        elif self.state == self.IN_KEY:
            self.bytes_sum += ord(byte)
            if byte == self.delimiter:
                if self.start == self.key:
                    self.start = 'ALL'
                elif self.start == '':
                    self.start = self.key
            
                if (self.key == 'Checksum'):
                    self.state = self.IN_CHECKSUM
                else:
                    self.state = self.IN_VALUE
            else:
                self.key += byte
            return None
        elif self.state == self.IN_VALUE:
            self.bytes_sum += ord(byte)
            if byte == self.header1:
                self.state = self.WAIT_HEADER
                self.dict[self.key] = self.value;
                self.key = '';
                self.value = '';
            else:
                self.value += byte
            return None
        elif self.state == self.IN_CHECKSUM:
            self.bytes_sum += ord(byte)
            self.key = ''
            self.value = ''
            self.state = self.WAIT_HEADER
            if (self.bytes_sum % 256 == 0):
                self.bytes_sum = 0
                if self.start == 'ALL':
                    self.start = ''
                    return self.dict
                else:
                    return None
            else:
                #print 'Malformed packet'
                self.bytes_sum = 0
                self.start = ''
                self.dict = {}
        elif self.state == self.HEX:
            self.bytes_sum = 0
            if byte == self.header2:
                self.state = self.WAIT_HEADER
        else:
            raise AssertionError()

    def read_data(self):
        while True:
            byte = self.ser.read(1)
            packet = self.input(byte)

    def get_data(self):
        if (self.ser.isOpen() != True):
            self.ser.open()
        self.ser.flushInput()
	count = 0
        while True:
	    try:
		count += 1
            	byte = self.ser.read(1)
            	packet = self.input(byte)
            	if (packet != None):
                   return packet

	    except:
		if count > 10:
		    return packet
		print(count)

    def read_data_callback(self, callbackFunction):
        while True:
            byte = self.ser.read(1)
            if byte:
                packet = self.input(byte)
                if (packet != None):
                    callbackFunction(packet)
            else:
                break


class TSComms:

    def __init__(self, serialport):
        self.serialport = serialport
        self.ser = serial.Serial(serialport)
        
    def load_settings(self):
        loadsettings = bytearray([0xfe, 0x11, 0x1f, 0x2a, 0x36])
        recbuf = self.enquire(5, 54, 1, loadsettings)
        # self.vincorrection
        b3 = ord(recbuf[33])
        b4 = ord(recbuf[34])
        if b3 == 0:
            self.vincorrection = 0 - b4
        else:
            self.vincorrection = b4
        # self.voutcorrection
        b5 = ord(recbuf[35])
        b6 = ord(recbuf[36])
        if b5 == 0:
            self.voutcorrection = 0 - b6
        else:
            self.voutcorrection = b6   
        # aself.mpcorrection
        self.ampcorrection1 = ord(recbuf[52])
        self.ampcorrection2 = ord(recbuf[53])
    
    def enquire(self, numsend, numrec, timeout, sbuf):
        self.ser.timeout = timeout
        recbuf = {}
        if (self.ser.isOpen() != True):
            self.ser.open()
        self.ser.flushInput()
        b = self.ser.write(sbuf)
        recbuf = self.ser.read(numrec)
        return recbuf
    
    def get_data(self):
        getdata = bytearray([0xfe, 0xd0])
        recbuf = self.enquire(2, 19, 0.3, getdata)
        dict = {}
        # vin
        vin = (ord(recbuf[6]) * 256 + ord(recbuf[7])) / 1024.0 * 2.048 / 0.0636
        vin += self.vincorrection / 1000.0 * vin
        dict['VS'] = vin * 1000.0
        # vout
        vout = (ord(recbuf[4]) * 256.0 + ord(recbuf[5])) / 1024.0 * 2.048 / 0.0636
        vout += self.voutcorrection / 1000.0 * vout
        dict['V'] = vout * 1000.0
        # aout
        aout1 = (ord(recbuf[0]) * 256.0) + ord(recbuf[1]) - self.ampcorrection1
        aout1 = (aout1 / 1024.0 * 2.048) / 10.0 / 0.0018 * 1000.0
        aout2 = (ord(recbuf[8]) * 256.0) + ord(recbuf[9]) - self.ampcorrection2
        aout2 = (aout2 / 1024.0 * 2.048) / 10.0 / 0.0018 * 1000.0
        aout = aout1 + aout2
        if aout < 0:
            aout = 0
        dict['I'] = aout
        #PCBtemp
        b1 = ord(recbuf[16])
        b2 = ord(recbuf[17])
        if b1 > 127:
            b1 = b1 - 256
        if b2 > 127:
            b2 = b2 - 256
        if b1 > b2:
            PCBtemp = b1
        else:
            PCBtemp = b2
        dict['T'] = PCBtemp
        return dict                
                

def print_data_callback(data):
    print data
    
def format_output (items, reading):
    text = ''
    parm = []
    for i in range(1, len(items)):
        #if i > 1:
        #    text += "\\r\\n"
        #if units[items[i]] == '*':
        #     text += cs[reading[items[i]]]
        #elif units[items[i]] == '':
	    text += reading[items[i]]
        #else:
        #    for p in range(3):
        #        parm.insert(p,fmt[units[items[i]]][p])
        #    text += '{:01.{}f}{}'.format(float(reading[items[i]]) / parm[1], parm[2], parm[0])     
    return text  
    

if __name__ == '__main__':  

    devices = []
    names = []
    timer = time() - 1

    for port in ports:
        devices.append(vedirect(ports[port]))
        names.append(port)

    readings = {}           
    for i in range(len(devices)):
        readings[names[i]] = devices[i].get_data()
        
    output = '{'
    
    count = 1
    total = len(divs)
    print(total)
    for div in divs:
        output += '"' + div + '": "'
        output += format_output(divs[div], readings[divs[div][0]])
        #output += readings[divs[div][1]];
	output += '"'
	if count < total:
	   output += ','
	count += 1

    output += '}'	
    
    try:
	url = 'http://www.ortodimontagna.com/meteo/victron/sendPVdata.php'
	r = requests.post(url, data=output)
	msg  = r.text.splitlines()
 	print('OK!');
    except:
	print('Error sending data')

    print (output)
    #stdout.flush()
       
