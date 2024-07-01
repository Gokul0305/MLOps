from enum import Enum
from PLCConnect.core.edge_type import RisingEdgeDetection, FallingEdgeDetection


class EdgeType(Enum):
    RISING = RisingEdgeDetection()
    FALLING = FallingEdgeDetection()
