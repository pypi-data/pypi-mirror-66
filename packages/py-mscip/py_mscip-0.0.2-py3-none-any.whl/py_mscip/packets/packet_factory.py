import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from packets.packet import (
    Packet,
    Ack,
    NoPayload,
    GetString,
    SetTime,
    GetCmds,
    Bit,
    Floats,
    GetTime,
    ConfigShort,
    GetShort,
    NoPayloadImu,
    AckImu,
)
from packets.cip import BaseMsgCode, ImuMsgCode, MsgType, ImuOutputCode

imu_lookup = {
    ImuMsgCode.Decimation: GetShort,
    ImuMsgCode.Ack: AckImu,
    ImuMsgCode.GetInternalSampleRate: NoPayloadImu,
    ImuMsgCode.GetInternalSampleRateReply: GetShort,
    ImuMsgCode.SelectSensorsRevB: NoPayloadImu,
    ImuMsgCode.SelectSensorsRevBReply: GetShort,
}

imu_output_lookup = {
    ImuOutputCode.Accel: Floats,
    ImuOutputCode.Gyro: Floats,
    ImuOutputCode.Mag: Floats,
    ImuOutputCode.Pressure: Floats,
    ImuOutputCode.Temperature: Floats,
    ImuOutputCode.DeltaTheta: Floats,
    ImuOutputCode.DeltaVelocity: Floats,
    ImuOutputCode.Time: GetTime,
    ImuOutputCode.Internal: Floats,
    ImuOutputCode.MS3011Raw: Floats,
}


base_lookup = {
    BaseMsgCode.GetBit: NoPayload,
    BaseMsgCode.Ping: NoPayload,
    BaseMsgCode.GetCmds: NoPayload,
    BaseMsgCode.Reset: NoPayload,
    BaseMsgCode.GetModel: NoPayload,
    BaseMsgCode.GetSn: NoPayload,
    BaseMsgCode.GetFw: NoPayload,
    BaseMsgCode.GetCal: NoPayload,
    BaseMsgCode.SetTime: SetTime,
    BaseMsgCode.Ack: Ack,
    BaseMsgCode.GetBitReply: Bit,
    BaseMsgCode.GetCmdsReply: GetCmds,
    BaseMsgCode.GetModelReply: GetString,
    BaseMsgCode.GetSnReply: GetString,
    BaseMsgCode.GetFwReply: GetString,
    BaseMsgCode.GetCalReply: GetString,
}


def create_packet(data):
    payload_size = data[3]
    msg_type = MsgType(data[2])
    packet = Packet(msg_type)
    sub_start = 4

    while payload_size > 0:
        sub_size = data[sub_start + 1] + 2
        packet.add_subpacket(
            create_sub_packet(msg_type, data[sub_start : sub_start + sub_size])
        )
        payload_size -= sub_size
        sub_start += sub_size
    return packet


def create_packet_from_hex(hex_data):
    return create_packet(bytearray.fromhex(hex_data))


def create_sub_packet(msg_type, data):
    if msg_type == MsgType.Base:
        code = BaseMsgCode(data[0])
        return base_lookup[code].from_bytes(data)
    if msg_type == MsgType.Imu:
        code = ImuMsgCode(data[0])
        return imu_lookup[code].from_bytes(data)
    elif msg_type == MsgType.ImuOutput:
        code = ImuOutputCode(data[0])
        return imu_output_lookup[code].from_bytes(data)
    else:
        raise ValueError(f"Unknown message type: {msg_type}")


def create_sub_packet_from_hex(msg_type, hex_data):
    return create_sub_packet(msg_type, bytearray.fromhex(hex_data))


# if __name__ == "__main__":
# print(create_sub_packet_from_hex(MsgType.Base, "80020200"))
# print(
#     create_sub_packet_from_hex(MsgType.Base, "85102020202020204D535F494D5533303230")
# )
# print(create_packet_from_hex("A5A501020500522B"))
# print(
#     create_packet_from_hex(
#         "A5A501168002050085102020202020204D535F494D5533303230EC54"
#     )
# )
# print(create_packet_from_hex("A5A5010E80020300830801020103010401057B57"))
# print(create_packet_from_hex("A5A501080906072F000002FF99AF"))
# print(create_packet_from_hex("A5A501098002010081030000005BAA"))
# print(create_packet_from_hex("A5A5A20E810C37A7C5AC377BA8823F800065D61A"))
# print(create_packet_from_hex("A5A5A20E820C37A7C5AC377BA8823749539C2240"))
# print(create_packet_from_hex("A5A5A20E830C37A7C5AC377BA8823749539C234E"))
# print(create_packet_from_hex("A5A5A20E840C37A7C5AC377BA8823749539C245C"))
# print(create_packet_from_hex("A5A5A20E850C37A7C5AC377BA8823749539C256A"))
# print(create_packet_from_hex("A5A5A2068604000003FD7CB4"))
# print(create_packet_from_hex("A5A5A20E880C410944c000000000072F00081A32"))
# x = "A5A5A22A810C37A7C5AC377BA8823F800065820C37A7C5AC377BA8823749539C32333435363738394041424344453AB9"
# print(
#     create_packet_from_hex(
#         "A5 A5 A2 22 82 0C BD 9D EC 5B 3D 6F 71 4B BD 4C 13 85 81 0C 38 AD C5 C0 BC 40 19 71 BF 7E C9 0F 87 04 41 DC D5 53 A8 60"
#     )
# )
print(create_packet_from_hex("A5A502030C01025E9F"))
# print(len(x))
# print(create_packet_from_hex(x))
