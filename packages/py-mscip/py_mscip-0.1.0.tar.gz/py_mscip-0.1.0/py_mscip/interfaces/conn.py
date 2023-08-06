from serial import SerialException, Serial
from datetime import datetime
import sys
from py_mscip.packets.cip_parser import Parser
from py_mscip.packets import cip
from py_mscip.packets import packet_factory as pf


class Conn:
    """ 
    Creates and manages a serial connection with an IMU device.
    """

    def __init__(self, ser, format="info"):
        """ 
        Initializes a connection with the desired settings. 

        Args:
            ser (serial): Serial class for connected IMU.
            format (str, optional): Output format of the parsed packages.
        """
        self.ser = ser
        self.format = format

        self.parser = Parser()

    def read(self):
        """ 
        Reads and formats packets from the serial connection.

        Returns:
            list(packets): A list of formatted packets.
        """
        try:
            if self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting)
                packets = self.parser.parse(data)
                formatted_packets = []
                for packet in packets:
                    if self.verify_checksum(packet):
                        if "hex" in self.format:
                            formatted_packet = self.format_hex(packet)
                            formatted_packets.append(formatted_packet)
                        if "info" in self.format:
                            formatted_packet = pf.create_packet(bytearray(packet))
                            formatted_packets.append(formatted_packet)
                        return formatted_packets
                    else:
                        sys.stderr.write("CS - ERROR: ")
                        sys.stderr.write(self.format_hex(packet) + "\n")
        except SerialException:
            sys.stderr.write(f"Error: Couldn't open {self.comport}\n")
        except Exception as e:
            sys.stderr.write(f"{e}\n")

    def write(self, bytes):
        """ 
        Writes a packet to the serial connection.

        Args:
            bytes (str): Bytes to be written to the serial connection.
        """
        self.ser.write(bytes)

    def format_hex(self, raw_data):
        """ 
        Formats raw data into hex values.

        Args:
            raw_data (str): Raw message to be formatted.

        Returns:
            float: Converted hex value.
        """
        return " ".join(format(p, "02x") for p in raw_data)

    def format_floats(self, raw_data):
        """
        Formats data into float values.

        Args:
            raw_data (str): Raw message to be formatted.

        Returns:
            float: Converted float value.
        """
        return " ".join(format(p, "f") for p in raw_data)

    def verify_checksum(self, raw_data):
        """ 
        Compute and verify the checksum of a packet.

        Args:
            raw_data (str): Raw message to be verified.

        Returns:
            bool: True if a valid data, False otherwise.
        """
        computed_fletcher = cip.compute_fletcher(raw_data[:-2])
        raw_data_fletcher = (raw_data[-2] << 8) + raw_data[-1]
        return computed_fletcher == raw_data_fletcher
