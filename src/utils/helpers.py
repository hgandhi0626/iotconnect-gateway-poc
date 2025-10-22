def format_timestamp(timestamp):
    from datetime import datetime
    return datetime.utcfromtimestamp(timestamp).isoformat() + 'Z'

def validate_device_id(device_id):
    if not isinstance(device_id, str) or len(device_id) == 0:
        raise ValueError("Device ID must be a non-empty string.")

def format_humidity(humidity):
    if not (0 <= humidity <= 100):
        raise ValueError("Humidity must be between 0 and 100.")
    return round(humidity, 2)

def generate_device_payload(device_id, temperature, humidity, occupancy):
    validate_device_id(device_id)
    formatted_humidity = format_humidity(humidity)
    
    return {
        "device_id": device_id,
        "temperature": temperature,
        "humidity": formatted_humidity,
        "occupancy": occupancy
    }