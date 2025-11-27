# Electronic balance communication
# PC: Host; Electronic balance: Slave
# Interface: RS485
# Protocol: Modbus-RTU
import serial
import binascii

def scale_oprate(order):
    """
    Electronic balance
    order:
    1. clear
    2. read
    :return:
    """
    ser = serial.Serial('COM3', 9600, timeout=1)
    command_read = bytearray([0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xc4, 0x0b])
    command_dot = bytearray([0x01, 0x03, 0x00, 0x02, 0x00, 0x01, 0x25, 0xca])
    command_clear = bytearray([0x01, 0x06, 0x00, 0x04, 0x00, 0x01, 0x09, 0xcb])

    # Clear
    if order == 'clear':
        ser.write(command_clear)
        print('Scale has been cleared')
        ser.close()
        return

    # Read weight
    elif order == 'read':
        ser.write(command_read)
        response = ser.read(8)
        response_hex = binascii.hexlify(response).decode()
        sub_str = response_hex[6:14]
        decimal_data = int(sub_str, 16) / 1000
        if 0 <= decimal_data <= 300:
            print(decimal_data)
        else:
            print("Overload")
        ser.close()
        return decimal_data


