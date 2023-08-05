import serial
import threading
import time
import struct
import timeit
import itertools
import math
from pysimplebgc import SimpleBGC32
from multiprocessing import Queue
SBGC_CMD_START_BYTE = b'\x3e'  # b'>'
SBGC_CMD_CONTROL = b'\x43'  # b'C'
SBGC_CMD_GET_ANGLES = b'\x49'  # b'I'
SBGC_CMD_RESET = b'\x72'  # b'r'
SBGC_FULL_TURN = 16384
SBGC_CONTROL_MODE_ANGLE = b'\x02'

pi = math.pi

class sBGCAdaper:
    def __init__(self):
        self.raw_pitch = 0
        self.raw_roll = 0
        self.raw_yaw = 0
        self.target_pitch = 0
        self.data = []
        self.prev_angle = 0
        self.update_pitch = False
        self.command = []
        self.get_angle = b''
        # self.target_roll  = 100
        # self.target_yaw    = 100
        self.ser = serial.Serial('/dev/tnt3', timeout=2, baudrate=115200)
        time.sleep(1)

        while not self.is_ready(self.ser):
            print("Establishing Connection")
            time.sleep(1)
        print("Connection complete")
        time.sleep(2)
        print(self.ser.name)

    @staticmethod
    def is_ready(ser):
        try:
            ser.write(b'\x00')
            return True
        except:
            return False

    def angle_to_deg(self, angle):
        new_angle = float((360 / SBGC_FULL_TURN) * angle)
        self.target_pitch = round(new_angle * 1.0, ndigits=3)
        if False and (abs(self.prev_angle - self.target_pitch) <= 0.5):
            pass
        else:
            self.update_pitch = True
            # print("Prev. Angle=" + str(self.prev_angle))
            # print("Angle=" + str(self.target_pitch))

    def parser(self):
        times = time.time()
        total_time = 0
        i = -1

        tx_comm = [SBGC_CMD_START_BYTE, SBGC_CMD_GET_ANGLES, b'\x12',
                   b'\x00', b'\x00',
                   b'\x00', b'\x00',
                   b'\x00', b'\x00',

                   b'\x00', b'\x00',
                   b'\x00', b'\x00',
                   b'\x00', b'\x00',

                   b'\x00', b'\x00',
                   b'\x00', b'\x00',
                   b'\x00', b'\x00']

        while True:
            i = i + 1
            elapsed_time = time.time() - times
            times = time.time()
            total_time = total_time + elapsed_time
            if i != 0:
                avg_time = total_time / i
                # print("Time: " + str(avg_time))
                # print("Freq: " + str(1 / avg_time) + "Hz")

            self.command = []
            n = 0
            tx_hb = [SBGC_CMD_START_BYTE, SBGC_CMD_CONTROL, b'\x00', b'\x81', b'\x01', b'\x01', b'\x01']
            for byte in tx_hb:
                self.ser.write(byte)

            if len(self.data):
                data = self.data
                # print("data: " + str(self.data))
                indices = [i for i, x in enumerate(data) if x == b'>']
                # print("indices: " + str(indices))
                if len(indices) > 1:
                    for x in range(len(indices)):
                        if indices[x] != indices[-1]:
                            # print("x:" + str(x))
                            self.command.append(data[indices[x]: indices[x + 1]])
                            empty = [i for i, x in enumerate(self.command[n]) if x == b'']
                            empty.reverse()
                            for z in empty:
                                self.command[n].pop(z)

                            n = n + 1
                # command.sort()
                # list(command for command, _ in itertools.groupby(command))

            for k in range(len(self.command)):
                if len(self.command[k]) >= 2:
                    if self.command[k][1] == SBGC_CMD_GET_ANGLES:
                        pitch = self.deg_to_angle(self.raw_pitch)
                        roll = [b'\x00', b'\x00']  # self.deg_to_angle(self.raw_roll)
                        yaw = [b'\x00', b'\x00']   # self.deg_to_angle(self.raw_yaw)
                        tx_comm[11] = pitch[0]
                        tx_comm[10] = pitch[1]
                        # print(self.raw_pitch)
                        # print(pitch)
                        for byte in tx_comm:
                            self.ser.write(byte)

                    if self.command[k][1] == SBGC_CMD_CONTROL:
                        # print("Command:" + str(command[k]) + "k:" + str(k))
                        self.prev_angle = self.target_pitch
                        if SBGC_CONTROL_MODE_ANGLE in self.command[k] and len(self.command[k]) >= 12:
                            n = self.command[k].index(SBGC_CONTROL_MODE_ANGLE)
                            # if self.checksum_verify(rx_packet[:3]) == rx_packet[len(rx_packet)-1]:
                            # print(rx_packet)

                            self.get_angle = b''.join([self.command[k][n + 7], self.command[k][n + 8]])

    def sBGC_listener(self):
        rx_packet = []
        tx_hb = [SBGC_CMD_START_BYTE, SBGC_CMD_CONTROL, b'\x00', b'\x81', b'\x01', b'\x01', b'\x01']
        for byte in tx_hb:
            self.ser.write(byte)

        temp = self.ser.read()
        if temp == SBGC_CMD_START_BYTE:
            rx_packet.append(temp)
            temp = self.ser.read()
            while not temp == SBGC_CMD_START_BYTE:
                rx_packet.append(temp)
                temp = self.ser.read()

            if len(rx_packet) >= 2:
                if rx_packet[1] == SBGC_CMD_GET_ANGLES:
                    pitch = self.deg_to_angle(self.raw_pitch)
                    roll = self.deg_to_angle(self.raw_roll)
                    yaw = self.deg_to_angle(self.raw_yaw)

                    tx_comm = [SBGC_CMD_START_BYTE, SBGC_CMD_GET_ANGLES, b'\x12',
                               b'\x00', b'\x00',
                               roll[1], roll[0],
                               b'\x00', b'\x00',
                               b'\x00', b'\x00',
                               pitch[1], pitch[0],
                               b'\x00', b'\x00',
                               b'\x00', b'\x00',
                               yaw[1], yaw[0],
                               b'\x00', b'\x00']
                    for byte in tx_comm:
                        self.ser.write(byte)
                if rx_packet[1] == SBGC_CMD_CONTROL:
                    if SBGC_CONTROL_MODE_ANGLE in rx_packet and len(rx_packet) >= 12:
                        n = rx_packet.index(SBGC_CONTROL_MODE_ANGLE)
                        # if self.checksum_verify(rx_packet[:3]) == rx_packet[len(rx_packet)-1]:
                        # print(rx_packet)
                        angle = b''.join([rx_packet[n + 7], rx_packet[n + 8]])
                        self.angle_to_deg(struct.unpack('<h', angle)[0])
        # for byte in tx_hb:
        #    self.ser.write(byte)

    @staticmethod
    def deg_to_angle(deg):
        d = int((SBGC_FULL_TURN / 360) * deg)
        # print("Angle =" + str(d))
        angle = []
        d_h = struct.pack('>h', d)
        for D in d_h:
            angle.append(D.to_bytes(1, byteorder="little"))
        return angle

    @staticmethod
    def calculate_h_checksum(header):
        return bytes((header[1] + header[2]) % 256)

    def run(self, que, que_raw):
        listenerT = threading.Thread(target=self.listener)
        listenerT.start()
        parserT = threading.Thread(target=self.parser)
        parserT.start()

        while True:
            if not que_raw.empty():
                raw_data = que_raw.get()
                self.raw_pitch = raw_data[0]*-180/pi
                self.raw_roll = raw_data[1]*-180/pi
                self.raw_yaw = raw_data[2]*-180/pi
                if not que_raw.empty():
                    raw_data = que_raw.get()
                    self.raw_pitch = raw_data[0] * -180 / pi
                    self.raw_roll = raw_data[1] * -180 / pi
                    self.raw_yaw = raw_data[2] * -180 / pi

            if self.get_angle != b'':
                self.prev_angle = self.target_pitch
                self.angle_to_deg(struct.unpack('<h', self.get_angle)[0])
                # self.get_angle = b''

                if self.update_pitch:
                    diff = abs(self.target_pitch - self.prev_angle)
                    # if diff != 0: print(diff)
                    if diff > 0.01:
                        if not que.full():
                            que.put([self.update_pitch, self.target_pitch])
                        # else:
                        # print("full")
                self.update_pitch = False

    def get_raw_orientation(self, p, r, y):
        self.raw_pitch = p
        self.raw_roll = r
        self.raw_yaw = y

    def set_orientation(self, p, r, y):
        return p, r, y

    def listener(self):
        while True:
            self.data.append(self.ser.read())

            if len(self.data) > 100:
                self.data = []


if __name__ == '__main__':
    gimbalI = sBGCAdaper()
    gimbalI.run()
