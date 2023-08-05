import serial
import time
import threading



VISCA_CAM_STABILIZER    = b'4'
VISCA_ZOOM_VALUE        = b'G'
VISCA_CATEGORY_IF       = b'\x00'
VISCA_CMD               = b'\x01'
VISCA_CAM_STABILIZER_ON = b'\x02'
VISCA_CAM_STABILIZER_OFF= b'\x03'
VISCA_CATEGORY_CAMERA1  = b'\x04'
VISCA_INQUIRY           = b'\x10'
VISCA_RSP               = b'\x81'
VISCA_CALL              = b'\x88'
VISCA_TERMINATOR        = b'\xff'

VENDOR_H    = b'S'
VENDOR_L    = b'T'
MODEL_H     = b'M'
MODEL_L     = b' '
ROM_H       = b'V'
ROM_L       = b'1'
DEV_SOCK    = b'\x01'
ADP_ADDR    = b'\x02'
HEAD        = b'\x80'

STABILIZER_INIT = [VISCA_RSP, VISCA_CMD, VISCA_CATEGORY_CAMERA1, VISCA_CAM_STABILIZER, VISCA_CAM_STABILIZER_ON, VISCA_TERMINATOR]


class viscaAdapter:
    def __init__(self, ):
        self.zoom_fov = 0
        self.epoch_flag = True
        self.zoom_update = False
        self.ser = serial.Serial('/dev/tnt1', timeout=2)
        print(self.ser.name)

        self.zoom_map_list = {
            # 0: 110,
            # 262144: 100,
            # 524288: 90,
            # 786432: 80,
            # 16777216: 70,
            # 17039360: 60,
            # 17563648: 50,
            # 33554432: 40,
            # 34078720: 30,
            # 50331648: 20,
            # 50855936: 10,
            # 67108864: 1

            0: 65.9155922,
            1024: 59.0054079,
            2048: 52.9629756,
            3072: 47.2879077,
            4096: 42.1146225,
            5120: 37.3802374,
            6144: 33.2133223,
            7168: 29.1496556,
            8192: 25.340908,
            9216: 22.0776279,
            10240: 18.8118776,
            11264: 15.9241344,
            12288: 13.4961993,
            13312: 11.2971676,
            14336: 9.55587665,
            15360: 7.9487979,
            16384: 6.7890118
                        }

    def wait_for_call(self):
        rx_packet = []
        temp = self.ser.read()
        if temp == VISCA_CALL:
            rx_packet.append(VISCA_CALL)
            while not temp == VISCA_TERMINATOR:
                temp = self.ser.read()
                rx_packet.append(temp)
        elif temp == VISCA_RSP:
            self.visca_listener()
        if rx_packet == [VISCA_CALL, b'\x30', b'\x01', VISCA_TERMINATOR]:
            tx_comm = rx_packet
            tx_comm[2] = ADP_ADDR
            for byte in tx_comm:
                self.ser.write(byte)
                # print(byte)
            self.set_addr_rsp()

    def set_addr_rsp(self):
        rx_packet = []
        temp = self.ser.read()
        if temp == VISCA_RSP:
            rx_packet.append(VISCA_RSP)
            while not temp == VISCA_TERMINATOR:
                temp = self.ser.read()
                rx_packet.append(temp)
            # print(rx_packet)
        if rx_packet == [VISCA_RSP, VISCA_CMD, VISCA_CATEGORY_IF, b'\x01', VISCA_TERMINATOR]:
            tx_comm = [VISCA_RSP, b'\x50', VISCA_TERMINATOR]
            for byte in tx_comm:
                self.ser.write(byte)
                # print(byte)
            self.device_inquiry_rsp()

    def device_inquiry_rsp(self):
        rx_packet = []
        temp = self.ser.read()
        if temp == VISCA_RSP:
            rx_packet.append(VISCA_RSP)
            while not temp == VISCA_TERMINATOR:
                temp = self.ser.read()
                rx_packet.append(temp)
        if rx_packet == [VISCA_RSP, b'\t', VISCA_CATEGORY_IF, b'\x02', VISCA_TERMINATOR]:
            tx_comm = [VISCA_RSP, b'\x50', VENDOR_H, VENDOR_L, MODEL_H, MODEL_L, ROM_H, ROM_L, DEV_SOCK, VISCA_TERMINATOR]
            for byte in tx_comm:
                self.ser.write(byte)
        self.visca_listener()

    def visca_listener(self):
        while True:
            rx_packet = []
            temp = self.ser.read()
            if not temp == b'':
                rx_packet.append(temp)
            while not temp == VISCA_TERMINATOR or temp == VISCA_RSP:
                temp = self.ser.read()
                rx_packet.append(temp)
            # print(rx_packet)
            if VISCA_CMD in rx_packet:
                if VISCA_CAM_STABILIZER in rx_packet:
                    n = rx_packet.index(VISCA_CAM_STABILIZER)
                    if rx_packet[n+1] == VISCA_CAM_STABILIZER_ON:
                        print("Stabilizer Enabled")
                    else:
                        print("Stabilizer not Enabled")
                    if rx_packet == STABILIZER_INIT:
                        print("Stabilizer Initialized")

                elif VISCA_ZOOM_VALUE in rx_packet:
                    n = rx_packet.index(VISCA_ZOOM_VALUE)
                    # zoom_bytes = b''.join([rx_packet[n+1], rx_packet[n+2], rx_packet[n+3], rx_packet[n+4]])
                    zoom_bytes = [rx_packet[n+1], rx_packet[n+2], rx_packet[n+3], rx_packet[n+4]]
                    zoom = 0
                    for i in range(4):
                        zoom = zoom + int.from_bytes(zoom_bytes[3-i], byteorder='little')*pow(16, i)
                    # for byte in zoom_bytes:
                    #     self.zoom = self.zoom + byte,
                    self.zoom_to_fov(zoom)
                else:
                    print("Unknown Command {}".format(rx_packet))

            tx_comm = [VISCA_RSP, b'\x50', VENDOR_H, VENDOR_L, MODEL_H, MODEL_L, ROM_H, ROM_L, DEV_SOCK,
                       VISCA_TERMINATOR]
            for byte in tx_comm:
                self.ser.write(byte)

    def zoom_to_fov(self, zoom):
        mapped_key = min(self.zoom_map_list, key=lambda x: abs(x-zoom))
        self.zoom_fov = self.zoom_map_list[mapped_key]
        # print("Fov:" + str(self.zoom_fov))
        self.zoom_update = True

    def bytes_to_int(self, byte):
        result = 0
        for b in byte:
            result = result * 256 + int(b)
        return result

    def epoch(self):
        self.epoch_flag = True
        threading.Timer(2, self.epoch).start()

    def run(self):
        # self.epoch()
        while True:
            self.wait_for_call()


if __name__ == '__main__':
    viscaAdapterI = viscaAdapter()
    viscaAdapterI.epoch()
    viscaAdapterI.run()
