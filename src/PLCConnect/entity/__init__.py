from pydantic import BaseModel


class TcpConnectionParams(BaseModel):
    """
    Model representing TCP connection parameters.

    Attributes:
        host (str): The host address of the TCP server.
        port (int): The port number of the TCP server.
    """
    host: str
    port: int


class SerialConnectionParams(BaseModel):
    """
    Model representing serial connection parameters.

    Attributes:
        port (str): The serial port name.
        baudrate (int): The baud rate of the serial connection.
        parity (str): The parity setting of the serial connection
                      (e.g., 'N', 'E', 'O').
        stopbits (int): The number of stop bits used in the serial connection.
        bytesize (int): The number of data bits used in the serial connection.
        framer (str): The framer mode used in the serial connection
                      (e.g., 'RTU', 'ASCII').
    """
    port: str
    baudrate: int
    parity: str
    stopbits: int
    bytesize: int
    framer: str
