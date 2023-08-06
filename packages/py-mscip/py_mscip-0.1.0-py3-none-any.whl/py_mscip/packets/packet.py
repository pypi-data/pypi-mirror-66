import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from packets.cip import (
    compute_fletcher,
    AckCode,
    BaseMsgCode,
    ImuOutputCode,
    ImuMsgCode,
    FunctionCode,
)
import struct


class Packet:
    def __init__(self, packet_type):
        self.sub_packets = []
        self.packet_type = packet_type

    def __len__(self):
        return len(self.header) + self.payload_length + len(self.checksum)

    def __str__(self):
        return " ".join([str(sub_packet) for sub_packet in self.sub_packets])

    @property
    def payload_length(self):
        return len(self.payload)

    @property
    def payload(self):
        return [item for sub_packet in self.sub_packets for item in sub_packet.bytes]

    @property
    def header(self):
        return [0xA5, 0xA5] + [self.packet_type.value, self.payload_length]

    @property
    def checksum(self):
        cs = compute_fletcher(self.header + self.payload)
        return [cs >> 8, cs & 0xFF]

    @property
    def bytes(self):
        return self.header + self.payload + self.checksum

    def add_subpacket(self, sub_packet):
        self.sub_packets.append(sub_packet)

    @classmethod
    def from_hex_string(cls, hex_string):
        return Packet()


class SubPacket:
    def __init__(self, code):
        self.message_code = code
        self.message_size = len(self.payload)

    @property
    def bytes(self):
        ret = [self.message_code.value, self.message_size]
        ret.extend(self.payload)
        return ret

    def __len__(self):
        return len(self.bytes)

    def __repr__(self):
        return "%s(0x%x)" % (self.__class__.__name__, self.message_code)


class Ack(SubPacket):
    def __init__(self, message_echo, error_code=AckCode.OK):
        self.payload = [message_echo.value, error_code.value]
        self.error_code = error_code
        self.message_echo = message_echo
        super().__init__(BaseMsgCode.Ack)

    def __repr__(self):
        return "%s(0x%02x, 0x%02x)" % (
            self.__class__.__name__,
            self.message_code,
            self.error_code,
        )

    def __str__(self):
        return f"[Ack: {self.message_echo.name} {self.error_code.name}]"

    @classmethod
    def from_bytes(cls, data):
        message_echo = data[2]
        error_code = data[3]
        return cls(BaseMsgCode(message_echo), AckCode(error_code))


class AckImu(SubPacket):
    def __init__(self, message_echo, error_code=AckCode.OK):
        self.payload = [message_echo.value, error_code.value]
        self.error_code = error_code
        self.message_echo = message_echo
        super().__init__(ImuMsgCode.Ack)

    def __repr__(self):
        return "%s(0x%02x, 0x%02x)" % (
            self.__class__.__name__,
            self.message_code,
            self.error_code,
        )

    def __str__(self):
        return f"[Ack: {self.message_echo.name} {self.error_code.name}]"

    @classmethod
    def from_bytes(cls, data):
        message_echo = data[2]
        error_code = data[3]
        return cls(ImuMsgCode(message_echo), AckCode(error_code))


class NoPayload(SubPacket):
    def __init__(self, message_code):
        self.payload = []
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x)" % (self.__class__.__name__, self.message_code)

    def __str__(self):
        return f"[{self.message_code.name}]"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        return cls(BaseMsgCode(message_code))


class NoPayloadImu(SubPacket):
    def __init__(self, message_code):
        self.payload = []
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x)" % (self.__class__.__name__, self.message_code)

    def __str__(self):
        return f"[{self.message_code.name}]"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        return cls(ImuMsgCode(message_code))


class GetString(SubPacket):
    def __init__(self, message_code, string):
        self.payload = string.rjust(16).encode()
        self.message_code = message_code
        self.string = string
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, '%s')" % (
            self.__class__.__name__,
            self.message_code,
            self.string,
        )

    def __str__(self):
        return f"[{self.message_code.name}:  {self.string}]"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        string = data[2:18].decode().lstrip()
        return cls(BaseMsgCode(message_code), string)


class GetShort(SubPacket):
    def __init__(self, message_code, value):
        self.payload = list(value.to_bytes(2, byteorder="big"))
        self.message_code = message_code
        print(message_code)
        self.value = value
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, '%d')" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f"[{self.message_code.name}:  {self.value}]"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        value = (data[2] << 8) + data[3]
        return cls(ImuMsgCode(message_code), value)


class ConfigListOfBytes(SubPacket):
    def __init__(self, message_code, function_code, values):
        self.value = values
        value_ints = [x.value for x in values]
        self.payload = [function_code.value] + value_ints
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "TODO"

    def __str__(self):
        return f"Message code = {self.message_code}"


class ReplyListOfBytes(SubPacket):
    def __init__(self, message_code, values):
        self.value = values
        value_ints = [x.value for x in values]
        self.payload = value_ints
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "TODO"

    def __str__(self):
        return f"Message code = {self.message_code}"


class Request(SubPacket):
    def __init__(self, message_code, function_code):
        self.payload = [function_code.value]
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x)" % (self.__class__.__name__, self.message_code)

    def __str__(self):
        return f"Message code = {self.message_code}"


class ConfigShort(SubPacket):
    def __init__(self, message_code, function_code, value):
        self.value = value
        self.payload = [function_code.value] + list(value.to_bytes(2, byteorder="big"))
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, %d)" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f"Message code = {self.message_code}"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        bit = int.from_bytes(data[2:3], byteorder="big")
        return cls(BaseMsgCode(message_code), FunctionCode.Request, 4)


class ConfigInt(SubPacket):
    def __init__(self, message_code, function_code, value):
        self.value = value
        self.payload = [function_code.value] + list(value.to_bytes(4, byteorder="big"))
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, %d)" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f"Message code = {self.message_code}"


class GetCmds(SubPacket):
    def __init__(self, message_code, cmds):
        self.cmds = cmds
        self.payload = [b for cmd in cmds for b in cmd.to_bytes(2, byteorder="big")]
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x)" % (self.__class__.__name__, self.message_code)

    def __str__(self):
        return f'[Cmds: {", ".join([format(cmd, "04x") for cmd in self.cmds])}]'

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        cmds = []
        for i in range(2, len(data), 2):
            cmds.append(int.from_bytes(data[i : i + 2], byteorder="big"))

        return cls(BaseMsgCode(message_code), cmds)


class Floats(SubPacket):
    def __init__(self, message_code, values):
        self.values = values
        self.payload = [b for value in values for b in struct.pack(">f", value)]
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x)" % (self.__class__.__name__, self.message_code)

    def __str__(self):
        # return f'[{self.message_code.name}: {", ".join([format(value, "f") for value in self.values])}]'
        return " ".join([format(value, "f") for value in self.values])

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        values = []
        for i in range(2, len(data), 4):
            values.append(struct.unpack(">f", data[i : i + 4])[0])

        return cls(ImuOutputCode(message_code), values)


class SetTime(SubPacket):
    def __init__(self, message_code, week, second):
        self.payload = list((week.to_bytes(2, byteorder="big"))) + list(
            (second.to_bytes(4, byteorder="big"))
        )
        self.message_code = message_code
        self.week = week
        self.second = second
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, %d)" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f"[Set Time: Week = {self.week},  Second = {self.second}]"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        week = int.from_bytes(data[2:4], byteorder="big")
        second = int.from_bytes(data[4:8], byteorder="big")

        return cls(BaseMsgCode(message_code), week, second)


class GetTime(SubPacket):
    def __init__(self, message_code, second, week, flags):
        self.payload = (
            list(struct.pack(">d", second))
            + list((week.to_bytes(2, byteorder="big")))
            + list((flags.to_bytes(2, byteorder="big")))
        )
        self.message_code = message_code
        self.week = week
        self.second = second
        self.flags = flags
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, %d)" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f"[Get Time: Week = {self.week},  Second = {self.second}, Flags = {self.flags}]"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        second = struct.unpack(">d", data[2:10])[0]
        week = int.from_bytes(data[10:12], byteorder="big")
        flags = int.from_bytes(data[12:14], byteorder="big")
        return cls(BaseMsgCode(message_code), second, week, flags)


class Bit(SubPacket):
    def __init__(self, message_code, value):
        self.value = value
        self.payload = list((value.to_bytes(3, byteorder="big")))
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, %d)" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f'[BIT: 0x{format(self.value, "06x")}]'

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        bit = int.from_bytes(data[2:5], byteorder="big")
        return cls(BaseMsgCode(message_code), bit)


class ConfigByte(SubPacket):
    def __init__(self, message_code, function_code, value):
        self.value = value
        if type(value) == int:
            self.payload = [function_code.value, value]
        else:
            self.payload = [function_code.value, value.value]
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, %d)" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f"Message code = {self.message_code}"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        value = int.from_bytes(data[2:5], byteorder="big")
        return cls(BaseMsgCode(message_code), bit)


class SetByte(SubPacket):
    def __init__(self, message_code, value):
        self.value = value
        if type(value) == int:
            self.payload = [value]
        else:
            self.payload = [value.value]
        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, %d)" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f"Message code = {self.message_code}"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        value = int.from_bytes(data[2:5], byteorder="big")
        return cls(BaseMsgCode(message_code), bit)


class SetListOfBytes(SubPacket):
    def __init__(self, message_code, function_code, value):
        self.value = value
        self.payload = [function_code.value] + value

        self.message_code = message_code
        super().__init__(message_code)

    def __repr__(self):
        return "%s(0x%02x, %d)" % (
            self.__class__.__name__,
            self.message_code,
            self.value,
        )

    def __str__(self):
        return f"Message code = {self.message_code}"

    @classmethod
    def from_bytes(cls, data):
        message_code = data[0]
        value = int.from_bytes(data[2:5], byteorder="big")
        return cls(BaseMsgCode(message_code), bit)


if __name__ == "__main__":
    print(
        Floats.from_bytes(
            bytearray.fromhex("81 0c 3c d2 cb 4e bd 43 12 fe 3f 7f b1 5b")
        )
    )

    packet = Packet(0xA2)
    packet.add_subpacket(Floats(ImuOutputCode.Accel, [0.025732, -0.047626, 0.998800]))
    print(packet)
    print(GetTime(ImuOutputCode.Time, 100, 4, 0))
    print(GetTime.from_bytes(bytearray.fromhex("880C410944c000000000072F0008")))
