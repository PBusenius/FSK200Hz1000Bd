import numpy as np

from src.block import Block
from src.block import DataBlock
from src.block import MetadataBlock
from src.ringbuffer import RingBuffer
from src.frame_detection import FrameDetection


class CIS200decoder(object):
    def __init__(self):
        # "7D12B0E6"
        # 01111101000100101011000011100110
        self.__start_pattern = np.array([0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1,
                                         1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0])
        self.__start_pattern_inv = 1 - self.__start_pattern
        self.__block_length = 288
        self.__ring_buffer = RingBuffer(buffer_length=self.__block_length)
        self.__mode_a_start = "11166"
        self.__mode_b_start = "11100"
        self.__correlation_threshold_factor = 0.66
        self.__frame = FrameDetection(self.__start_pattern, self.__block_length, correlation_threshold=5)
        self.__messages = []
        self.__valid_block_dict = {}
        self.__data = None
        self.__blocks = None
        self.__blocks_received = 0
        self.__processing_done = False
        self.__metadata_block = None
        self.__metadata_block_found = None

    def format_text(self):
        data_string = ""
        data_block = DataBlock()

        print("\n\nDecode Messages:")

        for block_index in range(1, len(self.__valid_block_dict) - 1):
            if block_index in self.__valid_block_dict and block_index % 16 != 0:
                data_string += data_block.decode("".join([str(i) for i in self.__valid_block_dict[block_index]]))
            elif block_index % 16 == 0:
                pass
            else:
                print("missing block {} -> stop processing".format(block_index))
        print("message: ", data_string)

    def decode(self, bit):
        self.__ring_buffer.add(bit)
        # if self.__ring_buffer.is_full:
        self.__frame.perform_detection(self.__ring_buffer.get_data)
        if self.__frame.is_valid_frame:
            # self.__ring_buffer.flush()
            try:
                if self.__frame.is_inverted:
                    self.__process_block(self.__ring_buffer.get_data, is_inverted=True)
                else:
                    self.__process_block(self.__ring_buffer.get_data, is_inverted=False)
            except ValueError:
                pass

        return self.__processing_done

    def __process_block(self, data, is_inverted):
        if is_inverted:
            block = Block(1 - data)
        else:
            block = Block(data)
        if block.is_crc_ok:
            if block.is_metadata_block:
                if self.__metadata_block is None:
                    self.__process_metadata_block(block)
            else:
                if self.__metadata_block_found:
                    self.__process_message_block(block)
                    if self.__blocks_received == self.__metadata_block.get_block_count() - 1:
                        self.__processing_done = True
                        self.format_text()

        return self.__processing_done

    def __process_metadata_block(self, block):
        self.__metadata_block = MetadataBlock(block)
        self.__metadata_block_found = True

        self.__create_block_dict(self.__metadata_block.get_block_count())

        try:
            self.__valid_block_dict[block.index] = block.original_data
            self.__blocks_received += 1
        except KeyError:
            pass

    def __process_message_block(self, block):
        print("message block with index ", block.index)
        try:
            self.__valid_block_dict[block.index] = block.original_data
            self.__blocks_received += 1
        except KeyError:
            pass

    def __create_block_dict(self, block_count):
        for index in range(1, block_count):
            self.__valid_block_dict[index] = np.zeros(144, dtype=np.int)


if __name__ == "__main__":
    import os

    with open(os.path.join("test", "content.id.1.1.txt"), "r") as f:
        data_in = np.array([int(x) for x in f.read()])
    test = CIS200decoder()
    for i in data_in:
        all_blocks_found = test.decode(i)
        if all_blocks_found:
            break
