import numpy as np


class Deinterleaver:
    def __init__(self, data_in):
        data = data_in
        self.__ecc = np.concatenate([np.reshape(data, (-1, 4))[i::4][9:] for i in range(4)], axis=None)
        self.__raw = np.concatenate([np.reshape(data, (-1, 4))[i::4][:9] for i in range(4)], axis=None)

    @property
    def original_data(self):
        return self.__raw[:144]

    @property
    def original_data_ecc(self):
        return self.__ecc
