class BaseDevice:
    def __init__(self, unique_id, device_type, tag):
        self.unique_id = unique_id
        self.device_type = device_type
        self.tag = tag

    def get_device_info(self):
        return {
            "unique_id": self.unique_id,
            "device_type": self.device_type,
            "tag": self.tag
        }

    def send_telemetry(self):
        raise NotImplementedError("This method should be implemented by subclasses")