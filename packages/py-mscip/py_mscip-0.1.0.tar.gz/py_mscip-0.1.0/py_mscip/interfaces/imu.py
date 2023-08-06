from py_mscip.interfaces.conn import Conn
from py_mscip.commands import base_commands as bc
from py_mscip.commands import imu_commands as ic
from py_mscip.packets.cip import MsgType, AckCode
from py_mscip.packets import cip
import concurrent.futures
import time


class IMU:
    """ 
    Acts as an interface for communicating with an IMU. 
    """

    def __init__(self, ser):
        self.conn = Conn(ser)

    def ping(self):
        """
        Pings the connected IMU.

        Returns:
            bool: True on success, false otherwise.
        """
        return self._get(bc.ping)

    def reset(self):
        """
        Resets the connected IMU.

        Returns:
            None
        """
        return self._get(bc.reset)

    ####################################
    #              Getters             #
    ####################################

    def get_bit(self):
        """
        Requests the time data bit value for the connected IMU.

        Returns:
            int: Currently set bits.
        """
        return self._get(bc.get_bit)

    def get_cmds(self):
        """ 
        Requests available commands for the connected IMU.

        Returns:
            int: Available commands for the IMU.
        """
        return self._get(bc.get_cmds)

    def get_model(self):
        """ 
        Requests the model of the connected IMU.

        Returns:
            str: Model of IMU. 
        """
        return self._get(bc.get_model)

    def get_sn(self):
        """ 
        Requests the serial number of the connected IMU.
        
        Returns:
            str: Serial number of IMU. 
        """
        return self._get(bc.get_sn)

    def get_fw(self):
        """ 
        Requests the firmware version of the connected IMU. 
        
        Returns:
            str: Firmware version of IMU. 
        """
        return self._get(bc.get_fw)

    def get_cal_date(self):
        """
        Requests the calibration date of the connected IMU.
        
        Returns:
            str: Calibration date of IMU. 
        """
        return self._get(bc.get_cal)

    def get_isr(self):
        """
        Requests the internal sample rate of the connected IMU.
        
        Returns:
            str: Internal sample rate of IMU. 
        """
        return self._get(ic.get_isr)

    def get_select_sensors(self):
        """
        Requests the selected sensors of the connected IMU.
        
        Returns:
            str: Enabled sensors of of IMU. 
        """
        return self._get(ic.get_select_sensors)

    ####################################
    #              Setters             #
    ####################################

    def set_baudrate(self, baudrate):
        """ 
        Sets the baudrate on the connected IMU. 

        Args:
            baudrate (int): Desired baud rate value.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_baudrate, baudrate)

    def set_filter(self, filter):
        """ 
        Sets the filter value on the connected IMU.

        Args:
            filter (FilterCode): Desired filter code.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_filter, filter)

    def set_accel(self, accel):
        """ 
        Sets the accel value on the connected IMU. 

        Args:
            accel (AccelCode): Desired accel code.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_accel, accel)

    def set_gyro(self, gyro):
        """ 
        Sets the gyro value on the connected IMU.

        Args:
            gyro (GyroCode): Desired gyro code.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_gyro, gyro)

    def set_decimation(self, decimation):
        """ 
        Sets the decimation on the connected IMU

        Args:
            decimation (int): Desired decimation value.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_decimation, decimation)

    def set_select_sensors(self, sensors):
        """ 
        Sets the selected sensors on the connected IMU.

        Args:
            sensors (list[ImuOutputCode]): Desired enabled sensors.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_select_sensors, sensors)

    def save_startup_settings(self):
        """ 
        Saves the current settings as the startup settings the connected IMU.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.config_all, cip.FunctionCode.Save)

    def load_startup_settings(self):
        """ 
        Loads the startup settings as the current settings the connected IMU.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.config_all, cip.FunctionCode.Load)

    def reset_startup_settings(self):
        """ 
        Resets the startup settings on the connected IMU.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.config_all, cip.FunctionCode.Reset)

    def enable_data(self):
        """ 
        Enables the data output on the connected IMU.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_data_on_off, 1)

    def disable_data(self):
        """ 
        Disables the data output on the connected IMU.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_data_on_off, 0)

    def enable_trigger(self):
        """ 
        Enables the trigger output on the connected IMU.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_trigger_on_off, 1)

    def disable_trigger(self):
        """ 
        Disables the trigger output on the connected IMU.

        Returns:
            bool: True on success, False otherwise.
        """
        return self._set(ic.configure_trigger_on_off, 0)

    ####################################
    #              Private             #
    ####################################

    def _get(self, request):
        """ 
        Generic method for getting a value and acknowledging response.

        Args:
            request (function): Function to generate a request packet.

        Returns:
            Result of request
        """
        requestPacket = request()
        packet_type = requestPacket.packet_type
        message_code = requestPacket.sub_packets[0].message_code

        with concurrent.futures.ThreadPoolExecutor() as executor:
            read = executor.submit(self._read, packet_type, message_code)
            self.conn.write(requestPacket.bytes)
            data = read.result()

        if message_code == cip.BaseMsgCode.Ping:
            data = True
        elif message_code == cip.BaseMsgCode.Reset:
            return
        elif message_code == cip.BaseMsgCode.GetCmds:
            data = data.sub_packets[1].payload
        elif message_code == cip.ImuMsgCode.GetInternalSampleRate:
            data = data.sub_packets[1].value
        elif message_code == cip.BaseMsgCode.GetBit:
            data = data.sub_packets[0].payload
        else:
            data = data.sub_packets[1].payload.decode("utf-8").strip()

        return data

    def _set(self, request, value):
        """
        Generic method for setting a value and acknowledging response.

        Args:
            request (function): Function to generate a request packet.

        Returns:
            bool: True on success, False otherwise
        """
        requestPacket = request(value)
        packet_type = requestPacket.packet_type
        message_code = requestPacket.sub_packets[0].message_code

        with concurrent.futures.ThreadPoolExecutor() as executor:
            read = executor.submit(self._read, packet_type, message_code)
            self.conn.write(requestPacket.bytes)
            data = read.result()

        return data.sub_packets[0].error_code.value == AckCode.OK.value

    def _read(self, packet_type, message_code):
        """ 
        Reads from the IMU until a specific type is received.

        Args:
            packet_type: Type of packet to wait for.
            message_code: Message code to wait for.

        Returns:
            bool: True on success, False otherwise
        """
        timeout = time.time() + 2
        while time.time() < timeout:
            packets = self.conn.read()
            if packets:
                for packet in packets:
                    if packet.packet_type.value == packet_type.value:
                        if (
                            packet.sub_packets[0].message_echo.value
                            == message_code.value
                        ):
                            return packet

        return []
