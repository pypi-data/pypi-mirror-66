import py_mscip.packets.packet as p
from py_mscip.packets.cip import MsgType, BaseMsgCode, AckCode


def ping():
    """ 
    Generates a ping packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.NoPayload(BaseMsgCode.Ping))
    return packet


def ping_reply():
    """ 
    Generates a ping reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.Ping, AckCode.OK))
    return packet


def reset():
    """ 
    Generates a reset packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.NoPayload(BaseMsgCode.Reset))
    return packet


def reset_reply():
    """ 
    Generates a reset reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.Reset, AckCode.OK))
    return packet


def get_bit():
    """ 
    Generates a time data bit request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.NoPayload(BaseMsgCode.GetBit))
    return packet


def get_bit_reply(bit):
    """ 
    Generates a time data bit reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.GetBit, AckCode.OK))
    packet.add_subpacket(p.Bit(BaseMsgCode.GetBitReply, bit))
    return packet


def get_cmds():
    """ 
    Generates an available commands request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.NoPayload(BaseMsgCode.GetCmds))
    return packet


def get_cmds_reply(cmds):
    """ 
    Generates an available commands reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.GetCmds, AckCode.OK))
    packet.add_subpacket(p.GetCmds(BaseMsgCode.GetCmdsReply, cmds))
    return packet


def get_model():
    """ 
    Generates a model request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.NoPayload(BaseMsgCode.GetModel))
    return packet


def get_model_reply(model_name):
    """ 
    Generates a model reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.GetModel, AckCode.OK))
    packet.add_subpacket(p.GetString(BaseMsgCode.GetModelReply, model_name))
    return packet


def get_sn():
    """ 
    Generates a serial number request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.NoPayload(BaseMsgCode.GetSn))
    return packet


def get_sn_reply(serial_number):
    """ 
    Generates a serial number reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.GetSn, AckCode.OK))
    packet.add_subpacket(p.GetString(BaseMsgCode.GetSnReply, serial_number))
    return packet


def get_fw():
    """ 
    Generates a firmware version request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.NoPayload(BaseMsgCode.GetFw))
    return packet


def get_fw_reply(firmware_version):
    """ 
    Generates a firmware version reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.GetFw, AckCode.OK))
    packet.add_subpacket(p.GetString(BaseMsgCode.GetFwReply, firmware_version))
    return packet


def get_cal():
    """ 
    Generates a calibration date request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.NoPayload(BaseMsgCode.GetCal))
    return packet


def get_cal_reply(cal_date):
    """ 
    Generates a calibration date reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.GetCal, AckCode.OK))
    packet.add_subpacket(p.GetString(BaseMsgCode.GetCalReply, cal_date))
    return packet


def set_time(week, second):
    """ 
    Generates a GPS time set request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.SetTime(BaseMsgCode.SetTime, week, second))
    return packet


def set_time_reply():
    """ 
    Generates a GPS time set reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Base)
    packet.add_subpacket(p.Ack(BaseMsgCode.SetTime, AckCode.OK))
    return packet
