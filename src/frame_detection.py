import numpy as np


class FrameDetection(object):
    def __init__(self, pattern, frame_length, correlation_threshold=10):
        self.__pattern = pattern
        self.__pattern_inverted = 1 - self.__pattern
        self.__frame_length = frame_length
        self.__correlation_threshold = correlation_threshold
        self.__inverted_pattern_found = False
        self.__frame_found = False

    @property
    def is_valid_frame(self):
        return self.__frame_found

    @property
    def is_inverted(self):
        return self.__inverted_pattern_found

    @staticmethod
    def __correlate(data, pattern):
        return np.correlate(
            data - data.mean(),
            pattern - pattern.mean(),
            mode="valid"
        )

    def perform_detection(self, data):
        if data.size == 288:
            self.__frame_found = False
            self.__inverted_pattern_found = False
            pattern_correlation = self.__correlate(data, self.__pattern)
            pattern_correlation_inv = self.__correlate(data, self.__pattern_inverted)

            if pattern_correlation[0] >= self.__correlation_threshold:
                self.__frame_found = True
            elif pattern_correlation_inv[0] >= self.__correlation_threshold:
                self.__frame_found = True
                self.__inverted_pattern_found = True
