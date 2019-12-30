import numpy as np


class RingBuffer(object):
    def __init__(self, buffer_length):
        self.__buffer_size = 0
        self.__buffer_length = buffer_length
        self.__buffer = np.zeros(self.__buffer_length, dtype=np.int)

    def add(self, x):
        self.__buffer = np.roll(self.__buffer, -1)
        self.__buffer[-1] = x
        if self.__buffer_size < self.__buffer_length:
            self.__buffer_size += 1

    @property
    def get_data(self):
        return self.__buffer

    @property
    def is_full(self):
        return self.__buffer_size == self.__buffer_length

    def flush(self):
        self.__buffer = np.zeros(self.__buffer_size, dtype=np.int)
        self.__buffer_size += 1


if __name__ == "__main__":
    test = RingBuffer(2000)
    for i in range(10000000):
        test.add(i)
        print(test.get_data)
