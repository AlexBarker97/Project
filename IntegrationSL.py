import time, RPi.GPIO as gpio, numpy as np, matplotlib.pyplot as plt, serial, binascii

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(22, gpio.OUT) #pin 22 (panservo) set to output
p = gpio.PWM(22, 366)
duty = 90
p.start(duty)

hex2dec = {"0": 0,  "1": 1,  "2": 2,  "3": 3,
           "4": 4,  "5": 5,  "6": 6,  "7": 7,
           "8": 8,  "9": 9,  "a": 10, "b": 11,
           "c": 12, "d": 13, "e": 14, "f": 15}

ser = serial.Serial()
ser.close()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 115200
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 10
ser.open()
ser.write(bytes('P', 'UTF-8'))
ser.write(bytes('T', 'UTF-8'))

r = []
theta = []

while True:
    result = binascii.hexlify(ser.read(8))
    result = str(result)
    res0 = hex2dec[result[2]]
    res1 = hex2dec[result[3]]
    res2 = hex2dec[result[4]]
    res3 = hex2dec[result[5]]
    res4 = hex2dec[result[6]]
    res5 = hex2dec[result[7]]
    res6 = hex2dec[result[8]]
    res7 = hex2dec[result[9]]
    if ((str(res0) == "5") and (str(res1) == "4")):
        duty -= 1        
        p.ChangeDutyCycle(duty)
        if duty >= 10:
            value = 0
            value = value + (res2*(16**5)) + (res3*(16**4)) + (res4*(16**3)) + (res5*(16**2)) + (res6*(16**1)) + (res7*(16**0))
            value = ((value-35811)/2446.1)
            r.append(value)
            theta.append(duty)
        else:
            break
    else:
        ser.close()
        ser.port = '/dev/ttyUSB0'
        ser.baudrate = 115200
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.bytesize = serial.EIGHTBITS
        ser.timeout = 10
        ser.open()
        ser.write(bytes('P', 'UTF-8'))
        ser.write(bytes('T', 'UTF-8'))
for x in range(0, 80):
    print(r[x],theta[x])

#ax = plt.subplot(111, projection='polar')
#ax.plot(theta, r)
#ax.set_rmax(100)
#ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
#ax.grid(True)
#plt.show()
