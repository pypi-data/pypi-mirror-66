# import airsim
import airsim_adaptor

airsim = airsim_adaptor

import setup_path
from pynput.keyboard import Listener, Events
import time
import threading
from multiprocessing import Process, Queue
import pprint
from visca_adapter import viscaAdapter
from sBGC_adapter import sBGCAdaper
import math

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

fpv = "0"
pi = math.pi


class Quaternion:
    def __init__(self, ):
        self.w_val = 0
        self.x_val = 0
        self.y_val = 0
        self.z_val = 0


class Platform:
    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.fov = 0
        self.fov_read = 0
        self.value = 0
        self.q = Quaternion()
        self.q1 = Quaternion()
        self.update_pitch = False

    def getCameraInfo(self, camera_):
        cam_info = client.simGetCameraInfo(camera_)
        veh_info = client.simGetVehiclePose("PX4")
        sss = (str(cam_info).split("<CameraInfo>")[1])
        sss1 = sss.split(':')
        self.fov_read = float(sss1[1].split("'")[0].split(",")[0])
        self.q.w_val = float(sss1[4].split(",")[0])
        self.q.x_val = float(sss1[5].split(",")[0])
        self.q.y_val = float(sss1[6].split(",")[0])
        self.q.z_val = float(sss1[7].split(",")[0].split('}')[0])

        ddd = (str(veh_info).split("<Pose>")[1])
        ddd1 = ddd.split(':')
        self.q1.w_val = float(ddd1[2].split(",")[0])
        self.q1.x_val = float(ddd1[3].split(",")[0])
        self.q1.y_val = float(ddd1[4].split(",")[0])
        self.q1.z_val = float(ddd1[5].split(",")[0].split('}')[0])

    def gimbal_update(self, target_pitch):
        self.getCameraInfo(fpv)
        (self.pitch, self.roll, self.yaw) = airsim.to_eularian_angles(self.q)
        (pitch_bd, _, __) = airsim.to_eularian_angles(self.q1)
        pitch_rad = target_pitch*pi/-180
        pitch_bdrad = pitch_bd*pi/-180
        client.simSetCameraPitch(fpv, airsim.to_quaternion(pitch_rad+pitch_bdrad, 0, 0))

    @staticmethod
    def zoom_update(zoom):
        client.simSetCameraFov(fpv, zoom)


if __name__ == '__main__':
    platform = Platform()
    que = Queue()
    que_raw = Queue()
    camera = viscaAdapter()
    gimbal = sBGCAdaper()
    q = Quaternion()
    viscaAdapterT = threading.Thread(target=camera.run)
    viscaAdapterT.start()
    j = False
    sBGCAdapterT = Process(target=gimbal.run, args=(que, que_raw,))
    sBGCAdapterT.start()

    # viscaAdapterI.epoch()
    platform.fov = platform.fov_read
    target_pitch = 0
    while True:
        if not que.empty():
            [platform.update_pitch, target_pitch] = que.get()

        platform.getCameraInfo(fpv)
        (platform.pitch, platform.roll, platform.yaw) = airsim.to_eularian_angles(platform.q)

        if not que_raw.full():
            que_raw.put([platform.pitch, platform.roll, platform.yaw])

        if camera.zoom_update and camera.zoom_fov != 0:
            platform.zoom_update(camera.zoom_fov)
            camera.zoom_update = False

        gimbal.get_raw_orientation(platform.pitch * -180 / pi, platform.roll * -180 / pi, platform.yaw * -180 / pi)
        if platform.update_pitch:
            platform.gimbal_update(target_pitch)
            platform.update_pitch = False





