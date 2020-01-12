from src.block import DataBlock


class MessageModeA(object):
    def __init__(self, metablock, valid_blocks, message_id):
        self.__metadata_block = metablock
        self.__valid_blocks = valid_blocks
        self.__header_len = 5
        self.__data_string = ""
        self.__output = ""
        self.__message_id = message_id

        self.__encode()

    def __encode(self):
        data_block = DataBlock()

        message_start = self.__metadata_block.message_start_blocks[self.__message_id]
        message_end = self.__metadata_block.message_start_blocks[self.__message_id + 1]

        if message_end == 0:
            message_end = len(self.__valid_blocks)

        for block_index in range(message_start, message_end):
            if block_index in self.__valid_blocks and block_index % 16 is not 0:
                self.__data_string += data_block.decode("".join([str(i) for i in self.__valid_blocks[block_index]]))

            elif block_index not in self.__valid_blocks:
                raise IndexError

        self.__encode_5er()

    def __encode_5er(self):
        _5er = [self.__data_string[i:i + 5] for i in range(0, len(self.__data_string), 5)]
        header = _5er[0:5]
        data_5er = _5er[5:]

        for j in range(5):
            self.__output += header[j]
            if j == 4:
                self.__output += "\n"
            else:
                self.__output += " "

        for i in range(1, len(data_5er)):
            self.__output += data_5er[i - 1]
            if i % 10 == 0 and i != 0:
                self.__output += "\n"
            else:
                self.__output += " "

    @property
    def id(self):
        return self.__message_id

    @property
    def content(self):
        return self.__output


class MessageModeB(object):
    def __init__(self, metablock, valid_blocks):
        self.__metablock = metablock
        self.__valid_blocks = valid_blocks

