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


if __name__ == "__main__":
    test_data_out = ""
    test_data = "AJS1BKT2CLU3DMV4ENW5FOX6GPY7HQZ8IR09agmsbhntcioudjpvekqwflrx"

    for i in test_data:
        test_data_out += i + ", "
        test_data_out += i + ", "
        test_data_out += i + ", "
        test_data_out += i + ", "

    array_data = np.array(test_data_out[:-2].split(", "))
    deinter_test = Deinterleaver(array_data)
    print(len(array_data))
    print(array_data)
    print(deinter_test.original_data)
    print(deinter_test.original_data_ecc)
