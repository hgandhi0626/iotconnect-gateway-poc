import json
import time
import random
from datetime import datetime
from src.devices.gateway_device import GatewayDevice
from src.devices.thermostat_device import ThermostatDevice

class DataSimulator:
    def __init__(self, gateway_device, thermostat_devices, frequency=60):
        self.gateway_device = gateway_device
        self.thermostat_devices = thermostat_devices
        self.frequency = frequency

    def generate_gateway_data(self):
        return {
            "hb": {
                "timestamp": self.get_current_time(),
                "network_info": self.gateway_device.get_network_info(),
                "version": "1.0"
            },
            "zigbee_network": self.gateway_device.get_zigbee_network(),
            "zigbee_devices": self.gateway_device.get_zigbee_devices_status()
        }

    def generate_thermostat_data(self):
        data = []
        for thermostat in self.thermostat_devices:
            data.append(thermostat.get_telemetry_data())
        return data

    def get_current_time(self):
        return datetime.utcnow().isoformat() + 'Z'

    def run(self):
        while True:
            gateway_data = self.generate_gateway_data()
            thermostat_data = self.generate_thermostat_data()

            telemetry_data = {
                "gateway": gateway_data,
                "thermostats": thermostat_data
            }

            self.send_data(telemetry_data)
            time.sleep(self.frequency)

    def send_data(self, data):
        # Placeholder for sending data to IoTConnect
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    gateway_device = GatewayDevice("GW-20001448")
    thermostat_devices = [ThermostatDevice(f"Stat-{i}") for i in range(1, 12)]
    simulator = DataSimulator(gateway_device, thermostat_devices)
    simulator.run()