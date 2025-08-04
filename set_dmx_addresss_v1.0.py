// for running this file type python filename.py

import serial
import time

# Set your FTDI COM port here
COM_PORT = "COM4"  # <-- Change to match your FTDI port
DEVICE_ID = 0x1234
NEW_DMX_ADDRESS = 480  # 0x0168

# Split into bytes
device_id_high = (DEVICE_ID >> 8) & 0xFF
device_id_low  = DEVICE_ID & 0xFF
address_high = (NEW_DMX_ADDRESS >> 8) & 0xFF
address_low  = NEW_DMX_ADDRESS & 0xFF

# Create DMX-like frame with start code 0xBB
frame = bytearray()
frame.append(0xBB)            # Start code
frame.append(device_id_high)  # Device ID High
frame.append(device_id_low)   # Device ID Low
frame.append(address_high)    # DMX address High
frame.append(address_low)     # DMX address Low

# Open serial port with 250000 baud, 8N2
ser = serial.Serial(
    port=COM_PORT,
    baudrate=250000,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    timeout=1
)

# Send BREAK by pulling TX low for at least 88µs
ser.break_condition = True
time.sleep(0.001)  # 1ms = valid BREAK
ser.break_condition = False

# Send Mark After Break (8 µs minimum)
time.sleep(0.00001)  # 10µs

# Send the frame
ser.write(frame)

print("Custom DMX frame sent.")
ser.close()
