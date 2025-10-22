import json
import os

class Config:
    def __init__(self):
        self.device_config = self.load_device_config()
        self.iotconnect_config = self.load_iotconnect_config()

    def load_device_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '../../config/device_config.json')
        with open(config_path, 'r') as file:
            return json.load(file)

    def load_iotconnect_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '../../config/iotconnect_config.json')
        with open(config_path, 'r') as file:
            return json.load(file)