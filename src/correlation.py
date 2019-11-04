import numpy as np


class FrameSync(object):
    def __init__(self, sync, pattern_offset=0):
        self.__sync_pattern = sync
        self.__sync_pattern_len = len(self.__sync_pattern)
        self.__pattern_offset = pattern_offset

    def check(self, frame_data):
        cor = np.correlate(frame_data[self.__pattern_offset:self.__sync_pattern_len], self.__sync_pattern)
        return True
