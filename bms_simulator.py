import serial
import struct

# Function to calculate CRC16
def calculate_crc16(data: bytes) -> int:
    crc = 0xFFFF
    polynomial = 0xA001
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
    return crc

# Opening the serial port connection
ser = serial.Serial('COM5', 9600)  

while True:
    # Reading data from the serial port
    data = ser.read()
    
    # If data is received, read the slave address and function code
    if len(data) == 2:
        slave_addr = data[0]
        func_code = data[1]
        
        # Checking if the function code is the one you're expecting (0x03 in your case)
        if func_code == 0x03:
            # Next, reading the data length
            data_length_byte = ser.read()
            data_length = int(data_length_byte[0])
            
            # Generating a dummy response for the data
            response_data = bytes([i for i in range(data_length)])
            
            # Constructing the response
            response = struct.pack('!B B B', slave_addr, func_code, data_length) + response_data
            
            # Calculating CRC16 for the response
            crc = calculate_crc16(response)
            
            # Adding CRC16 to the response
            response += struct.pack('!H', crc)
            
            # Sending the response
            ser.write(response)

ser.close()
