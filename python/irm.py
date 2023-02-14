#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
ERROR = 0xFE
PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)

start = -1;

adrDef = 0x00;
t_1 = 0x00;
t_2 = 0x00;
rh_1 = 0x00;
rh_2 = 0x00;

t_ticks = 0;
rh_ticks = 0;

t_degC = 0;
rh_pRH = 0;

adr = 0;

def getKey():
    byte = [0, 0, 0, 0];
    if IRStart() == False:
        time.sleep(0.11);        # One message frame lasts 108 ms.
        return ERROR;
    else:
        for i in range(0, 4):
                byte[i] = getByte();
        # Start signal is followed by 4 bytes:
        # byte[0] is an 8-bit ADDRESS for receiving
        # byte[1] is an 8-bit logical inverse of the ADDRESS
        # byte[2] is an 8-bit COMMAND
        # byte[3] is an 8-bit logical inverse of the COMMAND
        if byte[0] + byte[1] == 0xff and byte[2] + byte[3] == 0xff:
            adr = byte[0];
            return byte[2];
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
        if timeSpan > 0.0016 and timeSpan < 0.0018:
            byte |= 1 << i;
    return byte;
print('IRM Test Start ...');
try:
    while True:
        key = getKey();
        if(key != ERROR):
            print("Address: 0x%02x" %adr);
            print("Key: 0x%02x" %key);
            print(start);
            if(adr != adrDef):
                t_1 = key;
                start = 0;
                adrDef = adr;
            elif((start >= 0) & (adr == adrDef)):
                if(start == 0):
                    t_2 = key;
                    start = 1;
                elif(start == 1):
                    rh_1 = key;
                    start = 3;
                elif(start == 3):
                    rh_2 = key;
                    start = -1;
                    t_ticks = (t_1 *256) + t_2;
                    rh_ticks = (rh_1 * 256) + rh_2;
                    t_degC = -45 + (175 * (t_ticks/65535));
                    rh_pRH = -6 + (125 * (rh_ticks/65535));
                    print(f'Temperature: {t_degC:.2f} deg C\nRelative Humidity: {rh_pRH:.2f} %%\n');
except KeyboardInterrupt:
    GPIO.cleanup();