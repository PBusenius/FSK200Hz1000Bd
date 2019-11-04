import numpy as np


def interleaver(data_in):
    return data_in


def deinterleaver(data_in):
    raw = np.concatenate([np.reshape(data_in, (-1, 4))[i::4][:8] for i in range(4)], axis=None)
    ecc = np.concatenate([np.reshape(data_in, (-1, 4))[i::4][9:] for i in range(4)], axis=None)
    return raw, ecc
