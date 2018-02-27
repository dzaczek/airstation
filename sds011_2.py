#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
import serial, struct, sys, time
import string
import time
import urllib2
import subprocess
import numpy as np
DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1
SAVE_PATHJ='/root/data/JSON.txt'
SAVE_PATH='/root/data/1.txt'
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'# sys.argv[1]
ser.baudrate = 9600

ser.open()
ser.flushInput()

byte, data = 0, ""

def dump(d, prefix=''):
    print(prefix + ' '.join(x.encode('hex') for x in d))

def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret

def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    #print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))
    return([pm25,pm10])

def process_data2(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    #print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))
    JSON_FILE(pm25,pm10)



def SAVE_FILE(pm25,pm10,mean25,mean10):
    f=open(SAVE_PATH,'a+b')
    f.write(time.strftime("%Y-%m-%d %H:%M:%S")+","+str(pm25)+","+str(pm10)+","+str(mean25)+","+str(mean10)+"\n")
    f.close()

def SEND_FILE():
    #bashCommand='rsync -z -e \"ssh -p4891\" /root/{1.txt,JSON.txt} ppm@80.211.240.159:/srv/html/ppm/'
    bashCommand='/root/send.sh'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def JSON_FILE(pm25,pm10,m25,m10):
    f=open(SAVE_PATHJ,'w')
    f.write('[{"median25":'+str(pm25)+',"median10":'+str(pm10)+',"mean25":'+str(m25)+',"mean10":'+str(m10)+',"timedate":"'+time.strftime("%Y-%m-%d %H:%M:%S")+'" }]')
    f.close



def process_version(d):
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(ord(v) for v in d[2:8])%256
    #print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]), "OK" if (checksum==r[4] and r[5]==0xab) else "NOK"))

def read_response():
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)

    d = ser.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d

def cmd_set_mode(mode=MODE_QUERY):
    ser.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()

def cmd_query_datai3():
    ser.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    if d[1] == "\xc0":
        process_data(d)

def cmd_query_data():
    m25=[]
    m10=[]
    for x in range(0,21):
        time.sleep(1)
        ser.write(construct_command(CMD_QUERY_DATA))
        d = read_response()
        if d[1] == "\xc0":
            val=process_data(d)
            #print(val)
            m25.append(val[0])
            m10.append(val[1])
    #print(m25)
    #print(m10)
    m25.sort()
    m10.sort()
    median25=np.median(m25)
    median10=np.median(m10)
    mean25=round(np.mean(m25),2)
    mean10=round(np.mean(m10),2)
    SAVE_FILE(median25,median10,mean25,mean10)
    JSON_FILE(median25,median10,mean25,mean10)

def cmd_set_sleep(sleep=1):
    mode = 0 if sleep else 1
    ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()

def cmd_set_working_period(period):
    ser.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()

def cmd_firmware_ver():
    ser.write(construct_command(CMD_FIRMWARE))
    d = read_response()
    process_version(d)

def cmd_set_id(id):
    id_h = (id>>8) % 256
    id_l = id % 256
    ser.write(construct_command(CMD_DEVICE_ID, [0]*10+[id_l, id_h]))
    read_response()

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
         return False


if __name__ == "__main__":
    cmd_set_sleep(0)
    cmd_set_mode(1);
    cmd_firmware_ver()
    time.sleep(70)
    cmd_query_data();
    cmd_set_mode(0);
    cmd_set_sleep()
    if internet_on():
        SEND_FILE();

