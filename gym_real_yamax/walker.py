import gym, gym.spaces, gym.utils, gym.utils.seeding
import numpy as np

from icsservo import IOProvider
from Adafruit_ADXL345 import ADXL345

import math

class YamaXRealForwardWalk(gym.Env):
    def __init__(self, num_joints=10, imu_address=0x54, ics_port="/dev/serial0", ics_en=26):
        high = np.ones([num_joints])
        self.action_space = gym.spaces.Box(-high, high)
        high = np.inf*np.ones([num_joints + 3])
        self.observation_space = gym.spaces.Box(-high, high)
        self._seed()

        self.ics_io = IOProvider(ics_port, ics_en)
        self.servos = [self.ics_io.servo(i) for i in range(num_joints)]
        self.imu = ADXL345(imu_address)

        self.stands = np.array([
            -1.2211,
             0.8722,
             0,
             0.5233,
            -0.1744,
            -0.2616,
             0.1395,
             0.4361,
             0.2616,
             0.1744,
             0.5233,
            -0.2616,
            -0.9594,
             1.0117
            ])

    def _seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def _reset(self):
        self.sa[:14] = self.stands
        self.state = self.calc_state()
        return self.state # initial obs

    def _step(self, action):
        self.apply_action(action)

        self.state = self.calc_state()

        return self.state, 0, False, {} # state, reward, done, info

    def _render(self, mode, close):
        return

    def calc_state(self):
        x, y, z = accel.read()
        roll  = math.atan2(y, math.sqrt(x**2 + z**2))
        pitch = math.atan2(x, math.sqrt(y**2 + z**2))
        yaw   = math.atan2(z, math.sqrt(x**2 + z**2))
        return np.append(self.joint_states(), [roll, pitch, yaw])

    def joint_states(self):
        return self.sa[:14]

    def apply_action(self, action):
        self.sa[:14] = self.sa[:14] + action


