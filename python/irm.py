#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import numpy as np
import pandas as pd
from flask import Flask
import threading
ERROR = 0xFE
PIN = 18 #GPIO pin for tsop382
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)

host_name = "0.0.0.0"
port = 23336
app = Flask(__name__)

adr = 8;

last_key = 0x00;
t_ms = 0x00;
t_ls = 0x00;
rh_ms = 0x00;
rh_ls = 0x00;

t_ticks = 0;
rh_ticks = 0;

t_degC = 0;
rh_pRH = 0;

array = np.array([[0b000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b001, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b010, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b011, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0b111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
df = pd.DataFrame(array, columns = ['adr', 'msg_id', 't_ms', 'key_t_ms', 't_ls', 'key_t_ls', 'rh_ms', 'key_rh_ms', 'rh_ls', 'key_rh_ls', 'temperature', 'relative_humidity'])

def getMessage():
    bytes = [0, 0, 0, 0];
    if IRStart() == False:
        #time.sleep(0.11);        # One message frame lasts 108 ms.
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
            print(message);
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
        print(f"bit {i}: {timeSpan}");
        if timeSpan > 0.0016 and timeSpan < 0.0018:
            byte |= 1 << i;
    return byte;

def storeData(adr, msg_id, data, key):
    if (msg_id == 0):
        df.loc[adr, ['t_ms']] = [data];
        df.loc[adr, ['key_t_ms']] = [key];
    elif (msg_id == 1):
        df.loc[adr, ['t_ls']] = [data];
        df.loc[adr, ['key_t_ls']] = [key];
    elif (msg_id == 2):
        df.loc[adr, ['rh_ms']] = [data];
        df.loc[adr, ['key_rh_ms']] = [key];
    elif (msg_id == 3):
        df.loc[adr, ['rh_ls']] = [data];
        df.loc[adr, ['key_rh_ls']] = [key];

def updateAPI(adr):
        key_t_ms = df.loc[adr, ['key_t_ms']].item();
        key_t_ls = df.loc[adr, ['key_t_ls']].item();
        key_rh_ms = df.loc[adr, ['key_rh_ms']].item();
        key_rh_ls = df.loc[adr, ['key_rh_ls']].item();
        if (((key_t_ms == key_t_ls) & (key_rh_ms == key_rh_ls)) & (key_t_ms == key_rh_ms)):
            t_ticks = (df.loc[adr, ['t_ms']].item() *256) + df.loc[adr, ['t_ls']].item();
            rh_ticks = (df.loc[adr, ['rh_ms']].item() * 256) + df.loc[adr, ['rh_ls']].item();
            #print(t_ticks, rh_ticks);
            t_degC = -45 + (175 * (t_ticks/65535));
            rh_pRH = -6 + (125 * (rh_ticks/65535));
            #print(t_degC, rh_pRH);
            df.loc[adr, ['temperature']] = [t_degC];
            df.loc[adr, ['relative_humidity']] = [rh_pRH];
        print(df);
        #time.sleep(0.1);

def readIR():
    print('IRM Test Start ...');
    global adr;
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
        else:
            if(adr < 8):
                updateAPI(adr);
            else:
                for i in range (0, 8):
                    updateAPI(i);
try:

    @app.route("/")
    def helloWorld():
        return "<p>Hello, World!</p>";

    testData = 1771;

    @app.route("/test")                                                                                                                                                                
    def testing():
        return f"{testData}";

    @app.route("/data/all")
    def dataAll():
        string = "";
        for i in range(0, 8):
            string = string + f"adr:{i},temperature:{df.loc[i, ['temperature']].item()},relative_humidity:{df.loc[i, ['relative_humidity']].item()}\n";
        return string;

    @app.route("/data/0")
    def data0():
        return f"adr:{0},temperature:{df.loc[0, ['temperature']].item()},relative_humidity:{df.loc[0, ['relative_humidity']].item()}\n";
        
    @app.route("/data/1")
    def data1():
        return f"adr:{1},temperature:{df.loc[1, ['temperature']].item()},relative_humidity:{df.loc[1, ['relative_humidity']].item()}\n";
        
    @app.route("/data/2")
    def data2():
        return f"adr:{2},temperature:{df.loc[2, ['temperature']].item()},relative_humidity:{df.loc[2, ['relative_humidity']].item()}\n";
        
    @app.route("/data/3")
    def data3():
        return f"adr:{3},temperature:{df.loc[3, ['temperature']].item()},relative_humidity:{df.loc[3, ['relative_humidity']].item()}\n";
        
    @app.route("/data/4")
    def data4():
        return f"adr:{4},temperature:{df.loc[4, ['temperature']].item()},relative_humidity:{df.loc[4, ['relative_humidity']].item()}\n";
        
    @app.route("/data/5")
    def data5():
        return f"adr:{5},temperature:{df.loc[5, ['temperature']].item()},relative_humidity:{df.loc[5, ['relative_humidity']].item()}\n";
        
    @app.route("/data/6")
    def data6():
        return f"adr:{6},temperature:{df.loc[6, ['temperature']].item()},relative_humidity:{df.loc[6, ['relative_humidity']].item()}\n";
        
    @app.route("/data/7")
    def data7():
        return f"adr:{7},temperature:{df.loc[7, ['temperature']].item()},relative_humidity:{df.loc[7, ['relative_humidity']].item()}\n";
        


    if __name__ == "__main__":
        threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start();
    
    for i in range (0, 8):
        updateAPI(i);

    readIR();


except KeyboardInterrupt:
    GPIO.cleanup();







