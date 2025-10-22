import json
import time
from iotconnect.client import IoTConnectClient
from gateway.config import load_config
from gateway.data_simulator import DataSimulator
from utils.logger import setup_logger

def main():
    # Setup logger
    logger = setup_logger()

    # Load configurations
    device_config, iotconnect_config = load_config()

    # Initialize IoTConnect client
    client = IoTConnectClient(iotconnect_config)

    # Initialize data simulator
    data_simulator = DataSimulator(device_config)

    logger.info("Starting the IoTConnect Gateway application...")

    try:
        while True:
            # Generate telemetry data
            telemetry_data = data_simulator.generate_data()

            # Send data to IoTConnect
            client.send_data(telemetry_data)

            logger.info("Telemetry data sent successfully.")
            time.sleep(60)  # Wait for 60 seconds before the next cycle

    except KeyboardInterrupt:
        logger.info("Gateway application stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()