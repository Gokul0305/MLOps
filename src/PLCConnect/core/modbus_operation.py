from PLCConnect.communication import ModbusConnection
import logging


class ModbusOperations:
    """
    Class to perform Modbus operations such as reading and writing bits.

    Args:
        connection (ModbusConnection): Connection object for communicating
                                       with the PLC.
    """

    def __init__(self, connection: ModbusConnection) -> None:
        """
        Initialize ModbusOperations with a Modbus connection.

        Args:
            connection (ModbusConnection): Connection object for communicating
                                           with the PLC.
        """
        if isinstance(connection, ModbusConnection):
            self._connection = connection
        else:
            self._connection = None
            logging.error(f"Expected ModbusConnection Object, \
                          but got {type(connection)}")

    def get(self, address: int) -> list:
        """
        Read a bit or a set of bits from the PLC.

        Args:
            address (int): Address of the bit(s) to read.
            index (int): Index of the bit within the address.

        Returns:
            list: List of bits read from the PLC.
        """
        if self._connection is not None:
            if isinstance(address, int):
                result = self._connection.client. \
                         read_discrete_inputs(address=address, count=8)
                return result.bits
            else:
                logging.warning(f"Invalid Data, address - {address}")
                return None
        else:
            logging.warning("Please make ensure connection")
            return None

    def set(self, address: int, value: int):
        """
        Write a bit to the PLC.

        Args:
            address (int): Address of the bit to write.
            value (int): Value to write (0 or 1).

        Returns:
            bool: True if the write operation is successful, False otherwise.
        """
        if self._connection is not None:
            if isinstance(address, int) and isinstance(value, int):
                return self._connection.client.write_coil(address, value)
            else:
                logging.warning(f"Invalid Data, address - {address} \
                                 , value - {value}")
                return None
        else:
            logging.warning("Please make ensure connection")
            return None
