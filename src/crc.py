import numpy as np
import crcmod


class CRC:
    def __init__(self, raw):
        self.__raw = raw[:128]
        self.__ecc = raw[128:]
        self.__crc = crcmod.predefined.Crc("x-25")

    @property
    def is_crc_ok(self):
        data = np.packbits(np.reshape(self.__raw, (-1, 8))).tobytes()
        crc = np.packbits(np.reshape(self.__ecc, (-1, 8))).tobytes()

        self.__crc.update(data)

        return self.__crc.digest() == crc
