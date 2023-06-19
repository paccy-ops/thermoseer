import serial
import time
from main import post_data
from generatePort import get_port

max_retries = 20
retry_delay = 2  # seconds
device = get_port()

print(device)
for retry in range(max_retries):
    try:
        arduino = serial.Serial(device, 9600)
        data = arduino.readline().decode('utf')
        if 'Error' in data:
            pass
        else:
            print(data)
            post_data(data.split(' '))
        print("Processing")

    except serial.SerialException as e:
        print(f"Failed to open port: {e}")
        print("Retrying in {} seconds...".format(retry_delay))
        time.sleep(retry_delay)
else:
    print("Exceeded maximum retries. Unable to open port.")
