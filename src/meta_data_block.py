

class MetaDataBlock(object):
    def __init__(self, block_data):
        block_data = "".join([str(i) for i in block_data])
        self._block_count = int(block_data[:11], 2)
        self._message_count = int(block_data[11:16], 2)

    @property
    def block_count(self):
        return self._block_count

    @property
    def message_count(self):
        return self._message_count
