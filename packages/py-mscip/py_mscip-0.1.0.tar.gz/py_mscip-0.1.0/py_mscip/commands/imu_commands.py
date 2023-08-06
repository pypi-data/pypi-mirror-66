import py_mscip.packets.packet as p
from py_mscip.packets.cip import MsgType, FilterCode, ImuMsgCode, FunctionCode, AckCode


def get_isr():
    """ 
    Generates an isr request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.NoPayload(ImuMsgCode.GetInternalSampleRate))
    return packet


def get_isr_reply(value):
    """ 
    Generates an isr reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.Ack(ImuMsgCode.GetInternalSampleRate, AckCode.OK))
    packet.add_subpacket(p.GetShort(ImuMsgCode.GetInternalSampleRateReply, value))
    return packet


def get_select_sensors():
    """ 
    Generates a select sensors request packet.

    Returns:
        packet: A request packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.Request(ImuMsgCode.SelectSensorsRevB, FunctionCode.Request))
    return packet


def get_select_sensors_reply(sensors):
    """ 
    Generates an select sensors reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.Ack(ImuMsgCode.SelectSensorsRevB, AckCode.OK))
    packet.add_subpacket(p.ReplyListOfBytes(ImuMsgCode.SelectSensorsRevBReply, sensors))
    return packet


def configure_baudrate(baudrate):
    """ 
    Generates a baudrate configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.ConfigInt(ImuMsgCode.BaudRate, FunctionCode.Use, baudrate))
    return packet


def configure_baudrate_reply():
    """ 
    Generates a baudrate configuration reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.Ack(ImuMsgCode.Filter, AckCode.OK))
    return packet


def configure_filter(filter_code):
    """ 
    Generates a filter configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.ConfigByte(ImuMsgCode.Filter, FunctionCode.Use, filter_code))
    return packet


def configure_filter_reply():
    """ 
    Generates a filter configuration reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.Ack(ImuMsgCode.Filter, AckCode.OK))
    return packet


def configure_accel(accel_range):
    """ 
    Generates a accel configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(
        p.ConfigByte(ImuMsgCode.ConfigAccelRange, FunctionCode.Use, accel_range)
    )
    return packet


def configure_gyro(gyro_range):
    """ 
    Generates a gyro configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(
        p.ConfigByte(ImuMsgCode.ConfigGyroRange, FunctionCode.Use, gyro_range)
    )
    return packet


def configure_decimation(decimation):
    """ 
    Generates a decimation configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(
        p.ConfigShort(ImuMsgCode.Decimation, FunctionCode.Use, decimation)
    )
    return packet


def configure_data_on_off(data_on_off):
    """ 
    Generates a data configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(
        p.ConfigByte(ImuMsgCode.DataOnOff, FunctionCode.Use, data_on_off)
    )
    return packet


def configure_trigger_on_off(trigger_on_off):
    """ 
    Generates a trigger configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(
        p.ConfigByte(ImuMsgCode.TriggerOnOff, FunctionCode.Use, trigger_on_off)
    )
    return packet


def configure_select_sensors(data_types):
    """ 
    Generates a select sensors configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(
        p.ConfigListOfBytes(ImuMsgCode.SelectSensorsRevB, FunctionCode.Use, data_types)
    )
    return packet


def configure_select_sensors_reply():
    """ 
    Generates a select sensors configuration reply packet.

    Returns:
        packet: A reply packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.Ack(ImuMsgCode.SelectSensorsRevB, AckCode.OK))
    return packet


def configure_select_sensors_old(data_types):
    """ 
    Generates a select sensors configuration packet.

    Returns:
        packet: A configuration packet.

    Note:
        This has been depreciated for configure_select_sensors.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(
        p.ConfigListOfBytes(ImuMsgCode.SelectSensorsOld, FunctionCode.Use, data_types)
    )
    return packet


def config_all(function_code):
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.Request(ImuMsgCode.ConfigAll, function_code))
    return packet


def config_all_reply():
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.Ack(ImuMsgCode.ConfigAll, AckCode.OK))
    return packet


def set_gyros(function_code, on_off):
    """ 
    Generates a gyros configuration packet.

    Returns:
        packet: A configuration packet.
    """
    packet = p.Packet(MsgType.Imu)
    packet.add_subpacket(p.SetListOfBytes(ImuMsgCode.SetGyros, function_code, on_off))

    return packet
