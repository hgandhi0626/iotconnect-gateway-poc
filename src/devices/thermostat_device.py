class ThermostatDevice(BaseDevice):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.attributes = {
            "genBasic": {},
            "hvacFanCtrl": {},
            "hvacThermostat": {},
            "hvacUserInterfaceCfg": {},
            "linkquality": 0,
            "relative_humidity": 0,
            "msOccupancySensing": False,
            "schedule_active": False,
            "manuSpecificUniversalElectronics": {}
        }

    def update_attributes(self, temperature, humidity, occupancy):
        self.attributes["hvacThermostat"]["temperature"] = temperature
        self.attributes["relative_humidity"] = humidity
        self.attributes["msOccupancySensing"] = occupancy

    def get_telemetry_data(self):
        return {
            "uniqueId": self.unique_id,
            "model": self.model,
            "attributes": self.attributes
        }