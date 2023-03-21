#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import numpy as np
import pandas as pd
import json
from flask import Flask
import threading

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

# All test data
array = np.array([[0b000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
                  [0b001, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0],
                  [0b010, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 0],
                  [0b011, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0],
                  [0b100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 0],
                  [0b101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0],
                  [0b110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 70, 0],
                  [0b111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0]])
df = pd.DataFrame(array, columns = ['adr', 'msg_id', 't_ms', 'key_t_ms', 't_ls', 'key_t_ls', 'rh_ms', 'key_rh_ms', 'rh_ls', 'key_rh_ls', 'temperature', 'relative_humidity'])







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



@app.route("/")
def helloWorld():
    return "<p>Hello, World!</p>";

testData = 1771;

@app.route("/test")                                                                                                                                                                
def testing():
    return f"{testData}";

@app.route("/data/all")
def dataAll():
    return df.to_json(orient = 'records');

@app.route("/data/0")
def data0():
    return df[df["adr"]==0b000].to_json(orient = 'records');

@app.route("/data/1")
def data1():
    return df[df["adr"]==0b001].to_json(orient = 'records');

@app.route("/data/2")
def data2():
    return df[df["adr"]==0b010].to_json(orient = 'records');
    
@app.route("/data/3")
def data3():
    return df[df["adr"]==0b011].to_json(orient = 'records');
    
@app.route("/data/4")
def data4():
    return df[df["adr"]==0b100].to_json(orient = 'records');

@app.route("/data/5")
def data5():
    return df[df["adr"]==0b101].to_json(orient = 'records');
    
@app.route("/data/6")
def data6():
    return df[df["adr"]==0b110].to_json(orient = 'records');
    
@app.route("/data/7")
def data7():
    return df[df["adr"]==0b111].to_json(orient = 'records');
    


app.run(host=host_name, port=port, debug=True, use_reloader=False)




