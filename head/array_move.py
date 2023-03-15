# Importing Libraries
import serial
import time

arduino = serial.Serial(port='/dev/ttyACM1', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

#while True:
    #num = input("Enter a number: ") # Taking input from user
with open('/home/pi/odas/bin/angle.txt', 'r') as f:
    angle = f.readline()
    angle = angle[0]
    print(type(angle))
val = write_read("0")
print(val) # printing the value
        


