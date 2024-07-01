from box import Box
from pymodbus.client.serial import ModbusSerialClient
from PLCConnect.communication import framer_mode, ModbusConnection
from PLCConnect.entity import SerialConnectionParams
from PLCConnect.core.modbus_operation import ModbusOperations
import logging


class ModbusSerialConnection(ModbusConnection):
    """Modbus Serial Connection class used to communicate with
       PLC via serial communication."""

    def __init__(self, bit_operations=ModbusOperations):
        """
        Initialize ModbusSerialConnection object.

        Args:
            bit_operations (ModbusOperations): Object for performing Modbus
                                               bit operations.
        """
        self._is_connected = False
        self.client = None
        self._bit_operations = bit_operations(self)

    def connect(self, settings: Box):
        """
        Connect to the PLC using serial communication.

        Args:
            settings (dynaconf.utils.boxing.DynaBox): Configuration settings
                                                      for serial connection.
        """
        if isinstance(settings, Box):
            params = SerialConnectionParams(**dict(settings.serial_connection))
            if not self._is_connected:
                self.client = ModbusSerialClient(port=params.port,
                                                 framer=framer_mode[params.
                                                                    framer],
                                                 baudrate=params.baudrate,
                                                 bytesize=params.bytesize,
                                                 parity=params.parity,
                                                 stopbits=params.stopbits)
                self._is_connected = self.client.connect()
            else:
                logging.warning("Connection already established")
        else:
            logging.warning(f"Expected type Box class, Got {type(settings)}")

    @property
    def is_open(self) -> bool:
        return self._is_connected

    def disconnect(self):

        """Disconnect from the PLC."""

        if self._is_connected:
            self.client.close()
            self._is_connected = False
            logging.info("PLC Successfully Disconnected")
        else:
            logging.warning("Connection is not established")

    def read_bit(self, address: int) -> bool:

        """
        Read a bit from the PLC.

        Args:
            address (int): Address of the bit to read.

        Returns:
            bool: Value of the bit (True for 1, False for 0).
        """
        if self._bit_operations is not None:
            return self._bit_operations.get(address=address)
        else:
            logging.warning("Modbus Operation not found")
            return None

    def write_bit(self, address: int, value: int) -> bool:

        """
        Write a bit to the PLC.

        Args:
            address (int): Address of the bit to write.
            value (int): Value to write (0 or 1).
        """
        if self._bit_operations is not None:
            return self._bit_operations.set(address, value)
        else:
            logging.warning("Modbus Operation not found")
            return None
