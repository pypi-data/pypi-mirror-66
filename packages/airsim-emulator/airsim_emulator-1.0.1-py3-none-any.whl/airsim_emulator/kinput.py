from pynput.keyboard import Listener, Events
import time

class KeyBoard:
    def __init__(self):
        self.keyCommand = ''
        self.dt = 0
        self.i = 1
        self.bounce_time = 0
        self.listener = Listener(on_press=self.get_stroke, on_release=self.delta_time)

    def get_stroke(self, key):
        key_p = str(key)
        if self.i:
            self.dt = time.time()
            self.i = 0

        if 'Key' in key_p:
            key_p = key_p.split('.')[1]
        else:
            key_p = str(key)
        if key_p.lower() == "'w'":
            self.keyCommand = 'p+'
        elif key_p.lower() == "'s'":
            self.keyCommand = 'p-'
        elif key_p.lower() == "'a'":
            self.keyCommand = 'y-'
        elif key_p.lower() == "'a'":
            self.keyCommand = 'y-'
        elif key_p.lower() == "'d'":
            self.keyCommand = 'y+'
        elif key_p.lower() == "'e'":
            self.keyCommand = 'r+'
        elif key_p.lower() == "'q'":
            self.keyCommand = 'r-'
        elif key_p.lower() == 'up':
            self.keyCommand = 'fov-'
        elif key_p.lower() == 'down':
            self.keyCommand = 'fov+'
        else:
            self.keyCommand = ''
        # print(self.keyCommand)

    def delta_time(self, key):
        if not self.i:
            self.bounce_time = self.dt - time.time()
            self.i = 1

    def start_listener(self):
        # listener.join()
        pass



if __name__ == '__main__':
    keyI = KeyBoard()
