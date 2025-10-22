# IoTConnect Gateway Project

## Overview
The IoTConnect Gateway Project is a Python-based application designed to connect to the IoTConnect platform (AWS backend) and simulate telemetry data from a gateway device and multiple child thermostat devices. The application is structured to facilitate easy development, testing, and deployment.

## Project Structure
The project is organized into several directories and files:

- **src/**: Contains the main application code.
  - **gateway/**: Implements the gateway logic.
    - `__init__.py`: Initializes the gateway module.
    - `main.py`: Entry point for the gateway application.
    - `config.py`: Configuration settings for the gateway.
    - `data_simulator.py`: Simulates telemetry data.
  - **devices/**: Contains device-related classes.
    - `__init__.py`: Initializes the devices module.
    - `base_device.py`: Base class for devices.
    - `gateway_device.py`: Class for the gateway device.
    - `thermostat_device.py`: Class for thermostat devices.
  - **iotconnect/**: Handles communication with the IoTConnect platform.
    - `__init__.py`: Initializes the IoTConnect module.
    - `client.py`: Manages IoTConnect client operations.
    - `message_builder.py`: Builds message payloads for IoTConnect.
  - **utils/**: Contains utility functions and logging.
    - `__init__.py`: Initializes the utils module.
    - `logger.py`: Provides logging functionality.
    - `helpers.py`: Utility functions for various tasks.

- **certs/**: Contains certificate files for secure connections.
  - `AmazonRootCA1.cer`: Root CA certificate.
  - `cert_Gateway-v3.crt`: Device certificate for the gateway.
  - `pk_Gateway-v3.pem`: Private key for the gateway device.

- **config/**: Configuration files for devices and IoTConnect.
  - `device_config.json`: Device-specific configuration settings.
  - `iotconnect_config.json`: IoTConnect connection settings.

- **data/**: Contains sample data structures.
  - `sample-file.json`: Sample data for reference.

- **tests/**: Contains unit tests for the application.
  - `__init__.py`: Initializes the tests module.
  - `test_devices.py`: Unit tests for device classes.
  - `test_gateway.py`: Unit tests for the gateway application.

- **requirements.txt**: Lists project dependencies.

- **setup.py**: Used for packaging and installation.

- **.gitignore**: Specifies files to ignore in version control.

## Setup Instructions
1. Clone the repository from GitHub.
2. Navigate to the project directory.
3. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```
4. Configure the device and IoTConnect settings in the respective JSON files located in the `config/` directory.
5. Place the certificate files in the `certs/` directory.
6. Run the application using:
   ```
   python src/gateway/main.py
   ```

## Usage
The application will connect to the IoTConnect platform and start sending simulated telemetry data from the gateway and child thermostat devices every 60 seconds. Ensure that the device configurations and certificates are correctly set up before running the application.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.