from abc import ABC, abstractmethod
from pymodbus.framer import Framer
from box import Box

framer_mode = {"RTU": Framer.RTU, "ASCII": Framer.ASCII}


class ModbusConnection(ABC):
    """
    Abstract base class representing a Modbus connection.

    This class defines methods for establishing and terminating a connection
    to a Modbus server.
    """
    def __init__(self, bit_operation) -> None:
        self._is_connected = False
        self._bit_operations = None

    @abstractmethod
    def connect(self, settings: Box):
        """Abstract method to connect to the Modbus server."""
        pass

    @abstractmethod
    def disconnect(self):
        """Abstract method to disconnect from the Modbus server."""
        ...
