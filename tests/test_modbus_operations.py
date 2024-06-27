from pathlib import Path
import unittest
from PLCConnect.communication.serial_communication import (
    ModbusSerialConnection
)
from HtmlTestRunner import HTMLTestRunner
from PLCConnect.core.modbus_operation import ModbusOperations
from PLCConnect.utils.common import read_toml_to_box


TEST_PLC_SETTINGS = Path("tests/delta_dvp_14SS2.toml")


class ModbusOperationsTest(unittest.TestCase):
    def setUp(self):
        self.connection = ModbusSerialConnection(ModbusOperations)
        self.settings = read_toml_to_box(TEST_PLC_SETTINGS)
        self.connection.connect(settings=self.settings)
        self.modbus_op = ModbusOperations(self.connection)

    def test_init_valid_connection(self):
        self.assertEqual(self.modbus_op._connection, self.connection)


    def tearDown(self) -> None:
        self.connection.disconnect()
    

if __name__ == '__main__':
    unittest.main()
