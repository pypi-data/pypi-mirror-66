class Parser:
    def __init__(self):
        self.buffer = []
        self.sync_cnt = 0
        self.packet_length = 0
        self.first_time = True

    def _sample_complete(self):
        self.packets.append(self.buffer)
        self.buffer = []
        self.packet_length = 0
        self.sync_cnt = 0

    def parse(self, raw_bytes):
        self.packets = []

        for b in raw_bytes:
            if self.sync_cnt == 2:  # All synched up

                if self.first_time and (b == 0xA5):
                    pass
                else:
                    self.buffer.append(b)
                self.first_time = False

                if len(self.buffer) == 3 + 1:  # get packet length
                    self.packet_length = b + 2 + 4
                elif len(self.buffer) == self.packet_length:
                    self._sample_complete()
            elif b == 0xA5:
                self.buffer.append(b)
                self.sync_cnt += 1
            else:
                self.__init__()

        return self.packets
