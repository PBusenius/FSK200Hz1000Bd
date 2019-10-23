import numpy as np
from src.correlation import FrameSync
from src.ringbuffer import RingBuffer


class FSK200Bd1000Hz(object):
    def __init__(self):
        self.__frame_len = 288
        self.__sync_pattern = np.array([])
        self.__sync_detection = FrameSync(self.__sync_pattern)
        self.__buffer = RingBuffer(self.__frame_len)

    def decode(self, x):
        self.__buffer.add(x)
        frame_found = self.__sync_detection.check(self.__buffer)
        if frame_found:
            print("found")
