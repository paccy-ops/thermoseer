import serial
import time
from main import post_data
from generatePort import get_port

device = get_port()

arduino = serial.Serial(device, 9600)
try:
    print("Trying...", device)
except:
    print("Failed to connect on", device)
while 1:
    time.sleep(1)

    try:
        data = arduino.readline().decode('utf')
        if 'Error' in data:
            pass
        else:
            print(data)
            post_data(data.split(' '))
    except:
        print("Processing")