

class FrameSync(object):
    def __init__(self, sync, pattern_offset=0):
        self.__sync_pattern = sync
        self.__pattern_offset = pattern_offset

    def check(self, frame_data):
        return True
