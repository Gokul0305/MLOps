from box import Box
from pymodbus.client.tcp import ModbusTcpClient
import logging
from PLCConnect.communication import ModbusConnection
from PLCConnect.entity import TcpConnectionParams
from PLCConnect.core.modbus_operation import ModbusOperations


class ModbusTCPConnection(ModbusConnection):
    """Modbus TCP Connection class used to communicate with
       PLC via tcp communication."""

    def __init__(self, bit_operations: ModbusOperations):
        """
        Initialize ModbusTCPConnection object.

        Args:
            bit_operations (ModbusOperations): Object for performing Modbus
                                               bit operations.
        """
        self._is_connected = False
        self.client = None
        self._bit_operations = bit_operations(self)

    def connect(self, settings: Box):
        """
        Connect to the PLC using TCP communication.

        Args:
            settings (Box): Configuration settings for tcp connection.
        """
        if isinstance(settings, Box):
            params = TcpConnectionParams(**dict(settings.tcp_connection))
            if not self._is_connected:
                self.client = ModbusTcpClient(host=params.host,
                                              port=params.port)
                self._is_connected = self.client.connect()
            else:
                logging.warning("Connection already established")
        else:
            logging.warning(f"Expected type Box class, Got {type(settings)}")

    def disconnect(self):

        """ Disconnect from the PLC. """
        if self._is_connected:
            self.client.close()
            self._is_connected = False
            logging.info("PLC Successfully Disconnected")
        else:
            logging.warning("Connection is not established")

    @property
    def is_open(self) -> bool:
        return self._is_connected

    def read_bit(self, address: int, index: int) -> bool:

        """
        Read a bit from the PLC.

        Args:
            address (int): Address of the bit to read.
            index (int): Index of the bit within the address.

        Returns:
            bool: Value of the bit (True for 1, False for 0).
        """
        if self._bit_operations is not None:
            return self._bit_operations.get(address=address, index=index)
        else:
            logging.warning("Modbus Operation not found")
            return None

    def write_bit(self, address: int, value: int):

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
