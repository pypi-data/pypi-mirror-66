class Parser:
    def __init__(self):
        self.buffer = []
        self.sync_cnt = 0
        self.packet_length = 40
        self.first_time = True
        self.sync = [0xAA, 0x55]

    def _sample_complete(self):
        self.packets.append(self.buffer)
        self.buffer = []
        self.sync_cnt = 0

    def parse(self, raw_bytes):
        self.packets = []

        for b in raw_bytes:
            if self.sync_cnt == 2:  # All synched up
                self.buffer.append(b)

                if len(self.buffer) == self.packet_length:
                    self._sample_complete()
            elif b == self.sync[self.sync_cnt]:
                self.buffer.append(b)
                self.sync_cnt += 1
            else:
                self.__init__()

        return self.packets
