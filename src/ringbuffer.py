import numpy as np


class RingBuffer(object):
    def __init__(self, size):
        self.__buffer = np.zeros(size, dtype=np.int)

    def add(self, x):
        self.__buffer = np.roll(self.__buffer, -1)
        self.__buffer[-1] = x

    @property
    def get_data(self):
        return self.__buffer


if __name__ == "__main__":
    test = RingBuffer(2000)
    for i in range(10000000):
        test.add(i)
        print(test.get_data)
