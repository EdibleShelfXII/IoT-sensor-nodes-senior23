#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import numpy as np
import pandas as pd
ERROR = 0xFE
PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)

start = -1;

last_key = 0x00;
t_ms = 0x00;
t_ls = 0x00;
rh_ms = 0x00;
rh_ls = 0x00;

t_ticks = 0;
rh_ticks = 0;

t_degC = 0;
rh_pRH = 0;

array = np.array([[0b000, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b001, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b010, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b011, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b101, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b110, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b111, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
df = pd.DataFrame(array, columns = ['adr', 'msg_id', 't_ms', 't_ls', 'rh_ms', 'rh_ls', 'key', 'last_rcvd', 'temperature', 'relative_humidity'])

def getMessage():
    bytes = [0, 0, 0, 0];
    if IRStart() == False:
        time.sleep(0.11);        # One message frame lasts 108 ms.
        return ERROR;
    else:
        for i in range(0, 4):
            bytes[i] = getByte();
        # Start signal is followed by 4 bytes:
        # byte[0] is an 8-bit ADDRESS for receiving
        # byte[1] is an 8-bit logical inverse of the ADDRESS
        # byte[2] is an 8-bit COMMAND
        # byte[3] is an 8-bit logical inverse of the COMMAND
        print(bytes);
        if bytes[0] + bytes[1] == 0xff and bytes[2] + bytes[3] == 0xff:
            message = (bytes[0] << 8) + bytes[2]; 
            return message;
        else:
            return ERROR;
            
def IRStart():
    timeFallingEdge = [0, 0];
    timeRisingEdge = 0;
    timeSpan = [0, 0];
    GPIO.wait_for_edge(PIN, GPIO.FALLING);
    timeFallingEdge[0] = time.time();
    GPIO.wait_for_edge(PIN, GPIO.RISING);
    timeRisingEdge = time.time();
    GPIO.wait_for_edge(PIN, GPIO.FALLING);
    timeFallingEdge[1] = time.time();
    timeSpan[0] = timeRisingEdge - timeFallingEdge[0];
    timeSpan[1] = timeFallingEdge[1] - timeRisingEdge;
    #print(timeSpan[0]);
    #print(timeSpan[1]);
    # Start signal is composed with a 9 ms leading space and a 4.5 ms pulse.
    if timeSpan[0] > 0.0085 and \
       timeSpan[0] < 0.0095 and \
       timeSpan[1] > 0.004 and \
       timeSpan[1] < 0.005:
        return True;
    else:
        return False;

def getByte():
    byte = 0;
    timeRisingEdge = 0;
    timeFallingEdge = 0;
    timeSpan = 0;
    # Logic '0' == 0.56 ms LOW and 0.56 ms HIGH
    # Logic '1' == 0.56 ms LOW and 0.169 ms HIGH
    for i in range(0, 8):
        GPIO.wait_for_edge(PIN, GPIO.RISING);
        timeRisingEdge = time.time();
        GPIO.wait_for_edge(PIN, GPIO.FALLING);
        timeFallingEdge = time.time();
        timeSpan = timeFallingEdge - timeRisingEdge;
        #print(f"bit {i}: {timeSpan}");
        if timeSpan > 0.0016 and timeSpan < 0.0018:
            byte |= 1 << i;
    return byte;

def storeData(adr, msg_id, data, key):
    if(msg_id == 0):
        df.loc[adr, ['t_ms']] = [data];
        df.loc[adr, ['key']] = [key];
    elif(msg_id == 1 & key == df.loc[adr, ['key']] & df.loc[adr, ['last_rcvd']] == 0):
        df.loc[adr, ['t_ls']] = [data];
    elif(msg_id == 2 & key == df.loc[adr, ['key']] & df.loc[adr, ['last_rcvd']] == 1):
        df.loc[adr, ['rh_ms']] = [data];
    elif(msg_id == 3 & key == df.loc[adr, ['key']] & df.loc[adr, ['last_rcvd']] == 2):
        df.loc[adr, ['rh_ls']] = [data];
        t_ticks = (t_ms *256) + t_ls;
        rh_ticks = (rh_ms * 256) + rh_ls;
        t_degC = -45 + (175 * (t_ticks/65535));
        rh_pRH = -6 + (125 * (rh_ticks/65535));
        df.loc[adr, ['temperature']] = [t_degC];
        df.loc[adr, ['relative_humidity']] = [rh_pRH];

print('IRM Test Start ...');
try:
    while True:
        message = getMessage();
        rx_address = (message & 0xFF00) >> 8;
        rx_data = message & 0x00FF;
        if(rx_data != ERROR):
            adr = (rx_address & 0b11100000) >> 5;
            key = (rx_address & 0b00011100) >> 2;
            msg_id = rx_address & 0b00000011;
            print("Address: 0x%02x" %rx_address);
            print("Data: 0x%02x" %rx_data);
            storeData(adr, msg_id, rx_data, key);
            
            
            #print(f'Temperature: {t_degC:.2f} deg C\nRelative Humidity: {rh_pRH:.2f} %%\n');
except KeyboardInterrupt:
    GPIO.cleanup();