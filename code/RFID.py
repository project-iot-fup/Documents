import serial
import time

def arduino():
    port = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    read = port.readline()
    hexa = read.decode('utf-8')
    port.close()
    return hexa
