import serial, time
arduino = serial.Serial('COM3', 9600)
time.sleep(2)
rawString = arduino.readline()
print(rawString)
while True:
    sarduino = arduino.readline()
    print (sarduino.strip())
arduino.close()
