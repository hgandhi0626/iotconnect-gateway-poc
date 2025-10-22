import unittest
from src.gateway.main import GatewayApplication

class TestGatewayApplication(unittest.TestCase):

    def setUp(self):
        self.app = GatewayApplication()

    def test_initialization(self):
        self.assertIsNotNone(self.app.client)
        self.assertIsNotNone(self.app.data_simulator)

    def test_start_simulation(self):
        self.app.start_simulation()
        self.assertTrue(self.app.simulation_running)

    def test_send_telemetry(self):
        telemetry_data = self.app.generate_telemetry_data()
        response = self.app.send_telemetry(telemetry_data)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.app.stop_simulation()

if __name__ == '__main__':
    unittest.main()