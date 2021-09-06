import numpy as np
from src.crc import CRC
from src.ecc import ECC
from src.deinterleaver import Deinterleaver


class BlockIndex:
    def __init__(self, data_in):
        self.__index = data_in[32:43].dot(2 ** np.arange(data_in[32:43].size)[::-1])
        self.__index_ecc = data_in[43:48]

    @property
    def index(self):
        return self.__index

    @property
    def index_ecc(self):
        return self.__index_ecc

    @property
    def is_index_ecc_correct(self):
        return ECC.check(self.__index, self.__index_ecc)


class DataBlock(object):
    def __init__(self):
        self._3_digit_data = None
        self._1_digit_data = None

    def _decode_3_digit(self):
        return [str(int(self._3_digit_data[i:i+10], 2)).zfill(3) for i in range(0, len(self._3_digit_data), 10)]

    def _decode_1_digit(self):
        return str(int(self._1_digit_data[:4], 2)) + str(int(self._1_digit_data[4:], 2))

    def decode(self, block_data):
        self._3_digit_data = block_data[:120]
        self._1_digit_data = block_data[120:128]
        return "".join(self._decode_3_digit()) + self._decode_1_digit()


class MetadataBlock(object):
    def __init__(self, block):
        block_data = "".join([str(i) for i in block.original_data])
        self._block_count = int(block_data[:11], 2)
        self._message_count = int(block_data[11:16], 2)
        self._start_message_one = int(block_data[16:27], 2)
        self._start_message_two = int(block_data[32:43], 2)
        self._start_message_three = int(block_data[48:59], 2)
        self._start_message_four = int(block_data[64:75], 2)
        self._start_message_five = int(block_data[80:91], 2)
        self._start_message_six = int(block_data[96:107], 2)
        self._start_message_seven = int(block_data[112:123], 2)

        print("metadata block with index ", block.index)
        print("block count: ", self.block_count)
        print("message count: ", self.message_count)
        print("message start at block:", self.message_start_blocks)

    @property
    def block_count(self):
        return self._block_count

    @property
    def message_count(self):
        return self._message_count

    @property
    def message_start_blocks(self):
        return [self._start_message_one, self._start_message_two, self._start_message_three, self._start_message_four,
                self._start_message_five, self._start_message_six, self._start_message_seven]


class Block(BlockIndex, CRC, Deinterleaver):
    def __init__(self, data_in):
        if data_in.size != 288:
            raise ValueError
        Deinterleaver.__init__(self, data_in[48:])
        CRC.__init__(self, self.original_data)
        BlockIndex.__init__(self, data_in)

    @property
    def is_metadata_block(self):
        result = False
        if self.index % 16 == 0:
            result = True
        return result

