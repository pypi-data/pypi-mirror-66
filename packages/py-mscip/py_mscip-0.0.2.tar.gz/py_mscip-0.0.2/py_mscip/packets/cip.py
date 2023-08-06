from enum import Enum


class AckCode(Enum):
    OK = 0x00
    ErrChecksum = 0x01
    ErrUnknownStructure = 0x02
    ErrUnknownField = 0x03
    ErrInvalidParameter = 0x04


class MsgType(Enum):
    Base = 0x01
    Imu = 0x02
    ImuOutput = 0xA2


class ImuMsgCode(Enum):
    BaudRate = 0x01
    Filter = 0x03
    Decimation = 0x04
    SelectSensorsOld = 0x05
    GetInternalSampleRate = 0x06
    ConfigAccelRange = 0x07
    ConfigGyroRange = 0x08
    ConfigAll = 0x09
    DataOnOff = 0x0A
    TriggerOnOff = 0x0B
    SelectSensorsRevB = 0x0C
    ConfigAuxAccelRange = 0x0D
    SetGyros = 0xCC

    Ack = 0x80

    BaudRateReply = 0x81
    # Getting 0x82 reply from SelectSensorsOld
    FilterReply = 0x83
    DecimationReply = 0x84
    SelectSensorsOldReply = 0x85
    GetInternalSampleRateReply = 0x86
    ConfigAccelRangeReply = 0x87
    ConfigGyroRangeReply = 0x88
    ConfigAllReply = 0x89
    DataOnOffReply = 0x8A
    TriggerOnOffReply = 0x8B
    SelectSensorsRevBReply = 0x8C
    ConfigAuxAccelRangeReply = 0x8D


class BaseMsgCode(Enum):
    GetBit = 0x01
    Ping = 0x02
    GetCmds = 0x03
    Reset = 0x04
    GetModel = 0x05
    GetSn = 0x06
    GetFw = 0x07
    GetCal = 0x08
    SetTime = 0x09

    Ack = 0x80

    GetBitReply = 0x81
    PingReply = 0x82
    GetCmdsReply = 0x83
    ResetReply = 0x84
    GetModelReply = 0x85
    GetSnReply = 0x86
    GetFwReply = 0x87
    GetCalReply = 0x88
    SetTimeReply = 0x89


class ImuOutputCode(Enum):
    Accel = 0x81
    Gyro = 0x82
    Mag = 0x83
    DeltaTheta = 0x84
    DeltaVelocity = 0x85
    Pressure = 0x86
    Temperature = 0x87
    Time = 0x88
    Internal = 0xAF
    MS3011Raw = 0xB4


class FunctionCode(Enum):
    Use = 0x01
    Request = 0x02
    Save = 0x03
    Load = 0x04
    Reset = 0x05


class FilterCode(Enum):
    Disable = 0x00
    F25 = 0x01
    F50 = 0x02
    F75 = 0x03
    F100 = 0x04
    F10 = 0x05
    F200 = 0x06


class AccelCode(Enum):
    A2 = 0x00
    A4 = 0x01
    A8 = 0x02
    A10 = 0x03
    A15 = 0x04
    A20 = 0x05
    A40 = 0x06


class GyroCode(Enum):
    G120 = 0x01
    G240 = 0x02
    G480 = 0x03
    G960 = 0x04
    G1920 = 0x05
    G75 = 0x06
    G200 = 0x07


def verify_checksum(raw_data):
    computed_fletcher = compute_fletcher(raw_data[:-2])
    raw_data_fletcher = (raw_data[-2] << 8) + raw_data[-1]
    # if computed_fletcher != raw_data_fletcher:
    # print(f'[{format_hex(computed_fletcher.to_bytes(2,"big"))}] [{format_hex(raw_data_fletcher.to_bytes(2,"big"))}]')
    return computed_fletcher == raw_data_fletcher


def format_hex(raw_data):
    return " ".join(format(p, "02x") for p in raw_data)


def compute_fletcher(packet):
    checksum_1 = 0
    checksum_2 = 0

    for p in packet:
        checksum_1 += p
        checksum_2 += checksum_1
        checksum_1 &= 0xFF
        checksum_2 &= 0xFF

    fletch = (checksum_1 << 8) + checksum_2
    return fletch & 0xFFFF
