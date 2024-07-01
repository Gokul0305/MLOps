from enum import Enum
from PLCConnect.communication.serial_communication import (
    ModbusSerialConnection
)
from PLCConnect.utils.common import read_toml_to_box
from PLCConnect.utils.enums import EdgeType
from PLCConnect.core.modbus_operation import ModbusOperations
from PLCConnect.communication.tcp_communication import ModbusTCPConnection


class InteractionMode(Enum):
    RTU = ModbusSerialConnection
    TCP = ModbusTCPConnection


def initialize_plc(connection_mode: InteractionMode):
    """
    Initializes a connection to a PLC based on the specified interaction mode
    and configuration path.

    Args:
        connection_mode (InteractionMode): The interaction mode for
        the PLC connection.
        config_path (Path): The path to the configuration file.

    Returns:
        ModbusConnection: A Modbus connection object representing the
        initialized PLC connection.

    Raises:
        ValueError: If an invalid connection type or configuration is provided.
    """
    try:
        return connection_mode.value(bit_operations=ModbusOperations)
    except AttributeError:
        msg = f"Invalid connection type {connection_mode} of type \
               {type(connection_mode)}"
        raise ValueError(msg)


__all__ = ["PlcIoManager",
           "read_toml_to_box",
           "EdgeType",
           "InteractionMode",
           "initialize_plc"
           ]

__version__ = "1.0.0"
