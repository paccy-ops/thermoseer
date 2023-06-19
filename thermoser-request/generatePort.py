import serial.tools.list_ports


def get_port():
    # Get a list of all available serial ports
    ports = list(serial.tools.list_ports.comports())
    port = ''

    # for port in ports:
    #    print(port.description)

    # Filter the list to only include Arduino boards
    arduino_ports = [
        port.device for port in ports
        if 'USB Serial Device' or 'USB-SERIAL CH340' in port.description
    ]

    # Print the name of the Arduino port
    if arduino_ports:
        port = arduino_ports[0]
    return port
