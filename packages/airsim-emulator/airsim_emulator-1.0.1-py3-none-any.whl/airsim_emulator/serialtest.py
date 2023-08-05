import serial

ser = serial.Serial('/dev/tnt3', timeout=2, baudrate=115200)
while True:
    print(ser.read())

    tx_hb = [b'>', b'I', b'\x12', b'\x00', b'\x00', b'\x00', b'\x00',b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
    for byte in tx_hb:
        ser.write(byte)
