from py_mscip.interfaces.imu import IMU
from py_mscip.interfaces.conn import Conn
import json


class Config:
    """ 
    Handles saving and loading configurations from an IMU. 
    """

    #  Stores the device's configuration settings
    _config = {}

    def __init__(self, sn=None, model=None, fw=None):
        """
        Creates object with initial settings.

        Args:
            sn (str, optional): IMU device serial number.
            model (str, optional): IMU model. 
            fw (str, optional): IMU firmware version.
        """
        self._config["sn"] = sn
        self._config["model"] = model
        self._config["fw"] = fw

    def __str__(self):
        """ 
        Converts the current settings to a JSON string. 

        Returns:
            str: Settings as a JSON string
        """
        return json.dumps(self._config, indent=4)

    def write(self, imu):
        """
        Writes the configs to the connected IMU. 

        Args:
            imu (IMU): The connected IMU.
        """
        if "accel" in self._config:
            imu.set_accel(int(self._config["accel"], 16))
        if "filter" in self._config:
            imu.set_filter(int(self._config["filter"], 16))
        if "gyro" in self._config:
            imu.set_gyro(int(self._config["gyro"], 16))
        if "decimation" in self._config:
            imu.set_decimation(int(self._config["decimation"], 16))

    def read(self, imu):
        """ 
        Reads the configs from the connected IMU. 

        Args:
            imu (IMU): The connected IMU.
        """
        self._config["sn"] = imu.get_sn()
        self._config["model"] = imu.get_model()
        self._config["fw"] = imu.get_fw()

    def save(self, filename):
        """ 
        Saves the configs to a JSON file.

        Args:
            filename (str): JSON Filename to save settings to.
        """
        with open(filename, "w") as file:
            json.dump(self._config, file, indent=4)

    def load(self, filename):
        """ 
        Loads the config from a JSON file.

        Args:
            filename (str): JSON filename to load settings from.
        """
        with open(filename, "r") as file:
            self._config = json.load(file)
