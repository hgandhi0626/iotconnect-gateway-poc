import unittest
from src.devices.gateway_device import GatewayDevice
from src.devices.thermostat_device import ThermostatDevice

class TestDevices(unittest.TestCase):

    def setUp(self):
        self.gateway_device = GatewayDevice(name="Gateway-v3", unique_id="GW-20001448", tag="gateway")
        self.thermostat_device = ThermostatDevice(name="Thermostat-504112112200301", unique_id="Stat-1", tag="thermostat")

    def test_gateway_device_initialization(self):
        self.assertEqual(self.gateway_device.name, "Gateway-v3")
        self.assertEqual(self.gateway_device.unique_id, "GW-20001448")
        self.assertEqual(self.gateway_device.tag, "gateway")

    def test_thermostat_device_initialization(self):
        self.assertEqual(self.thermostat_device.name, "Thermostat-504112112200301")
        self.assertEqual(self.thermostat_device.unique_id, "Stat-1")
        self.assertEqual(self.thermostat_device.tag, "thermostat")

    def test_gateway_send_heartbeat(self):
        heartbeat_data = self.gateway_device.send_heartbeat()
        self.assertIn("hb", heartbeat_data)

    def test_thermostat_send_data(self):
        thermostat_data = self.thermostat_device.send_data()
        self.assertIn("genBasic", thermostat_data)
        self.assertIn("hvacThermostat", thermostat_data)

if __name__ == '__main__':
    unittest.main()