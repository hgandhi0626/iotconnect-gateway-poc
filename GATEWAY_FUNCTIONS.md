# IoTConnect Gateway Application - Function Documentation

## Overview
This document provides a comprehensive overview of all functions in the `gateway_app.py` file, their purposes, parameters, and return values.

## Configuration Constants

### Global Variables
- **UNIQUE_ID**: Gateway device unique identifier (`"GW-20001448"`)
- **INTERVAL**: Data transmission frequency in seconds (60)
- **CERT_DIR**: Directory containing SSL certificates
- **SDK_OPTIONS**: Configuration dictionary for IoTConnect SDK
- **CHILD_DEVICES**: List of 11 child thermostat devices

## Data Simulation Functions

### `generate_gateway_data()`
**Purpose**: Generates simulated gateway heartbeat and network status data

**Parameters**: None

**Returns**: Dictionary containing:
- `hb`: Heartbeat data with network info, versions, timestamps
- `zigbee_network`: ZigBee network configuration (channel, PAN ID, extended PAN ID)

**Data Structure**:
```json
{
  "hb": {
    "net_address_ip_v4": "192.168.68.123",
    "net_address_ip_v6": "fe80::3868:668e:93b4:9c1f",
    "hostname": "raspberrypi",
    "gateway_version": "3.2.40",
    "ota_version": "3.2.13",
    "configured": true,
    "fixed_id": "2941008C7954",
    "serial_id": "20002330",
    "mac_address": "b8:27:eb:3f:f0:11",
    "download_config_success": true,
    "download_firmware_success": true,
    "ota_success": true,
    "reason": "periodic",
    "ota_firmware_timestamp": "2024-09-06T15:57:02.070944Z",
    "gateway_firmware_timestamp": "<current_timestamp>",
    "gateway_start_timestamp": "<current_timestamp>",
    "gateway_stop_timestamp": "",
    "config_file_timestamp": "<current_timestamp>",
    "gateway_reboot_success": true
  },
  "zigbee_network": {
    "channel": 11,
    "extended_pan_id": "0x00124b0024cbee5f",
    "pan_id": 55363
  }
}
```

### `generate_pct504e_data()`
**Purpose**: Generates simulated data for PCT504-E thermostat model devices

**Parameters**: None

**Returns**: Dictionary containing comprehensive thermostat data:
- `genBasic`: Basic device information (manufacturer, model, versions)
- `hvacFanCtrl`: Fan control settings
- `hvacThermostat`: Temperature control and status data
- `occupied_heating_setphvacUserInterfaceCfgoint`: User interface configuration
- `linkquality`: ZigBee signal quality (150-255)
- `relative_humidity`: Humidity sensor data
- `msOccupancySensing`: Occupancy detection data
- `schedule_active`: Schedule status (always false)

**Key Features**:
- Randomized temperature readings (72.0°F - 78.0°F)
- Random system states (cool/heat/auto)
- Random occupancy detection
- Variable humidity readings (25% - 45%)

### `generate_tbh300_data()`
**Purpose**: Generates simulated data for TBH300 thermostat model (UEI device)

**Parameters**: None

**Returns**: Similar structure to PCT504-E but with TBH300-specific values:
- Higher temperature range (75.0°F - 82.0°F)
- Different manufacturer (Universal Electronics Inc.)
- Additional `manuSpecificUniversalElectronics` section
- Different humidity range (25% - 40%)

**Key Differences from PCT504-E**:
- More advanced system state reporting
- Manufacturer-specific attributes
- Different operating ranges
- Enhanced sensor capabilities

## Callback Functions (IoTConnect SDK Event Handlers)

### `DeviceCallback(msg)`
**Purpose**: Handles device commands received from the IoTConnect cloud platform

**Parameters**:
- `msg`: Command message dictionary from cloud

**Message Types Handled**:
- Command Type 0: Device commands
- Processes acknowledgment requests
- Sends success acknowledgments back to cloud

**Flow**:
1. Logs received command message
2. Checks command type (`ct` field)
3. For device commands (ct=0), sends acknowledgment
4. Handles both ID-based and general acknowledgments

### `DeviceFirmwareCallback(msg)`
**Purpose**: Handles Over-The-Air (OTA) firmware update commands

**Parameters**:
- `msg`: Firmware update command message

**Message Types Handled**:
- Command Type 1: Firmware OTA commands
- Processes firmware URLs for different device tags
- Manages firmware update acknowledgments

**Flow**:
1. Logs firmware command
2. Checks for URLs in message
3. Matches URLs to device tags
4. Sends OTA acknowledgments for applicable devices

### `DeviceConectionCallback(msg)`
**Purpose**: Handles device connection status updates

**Parameters**:
- `msg`: Connection status message

**Message Types Handled**:
- Command Type 116: Connection status updates
- Reports device online/offline status

**Note**: Function name retains original SDK typo "Conection" for consistency

### `TwinUpdateCallback(msg)`
**Purpose**: Handles device twin (digital shadow) property updates

**Parameters**:
- `msg`: Twin update message containing desired/reported properties

**Flow**:
1. Logs twin update message
2. Checks for desired properties (without reported properties)
3. Updates twin reported properties for each desired property
4. Skips system properties like "version" and "uniqueId"

### `InitCallback(response)`
**Purpose**: Handles SDK initialization response (currently logging only)

**Parameters**:
- `response`: Initialization response from SDK

**Usage**: Debugging and monitoring SDK initialization status

## Main Application Functions

### `send_telemetry()`
**Purpose**: Orchestrates sending telemetry data for gateway and all child devices

**Parameters**: None

**Process**:
1. Generates current timestamp in ISO format
2. Creates data array with gateway data first
3. Generates data for each child device based on model type
4. Sends complete data array via SDK
5. Logs transmission status

**Data Volume**: Sends data for 12 devices total (1 gateway + 11 child devices)

### `main()`
**Purpose**: Main application entry point and control loop

**Process**:
1. **Initialization Phase**:
   - Displays application banner and configuration
   - Verifies SSL certificate files exist
   - Initializes IoTConnect SDK with configuration

2. **Setup Phase**:
   - Registers all callback functions
   - Retrieves device list from cloud
   - Displays connection status

3. **Main Loop**:
   - Continuously sends telemetry every 60 seconds
   - Handles transmission errors with retry logic
   - Graceful shutdown on Ctrl+C

**Error Handling**:
- Certificate file validation
- SDK initialization errors
- Telemetry transmission errors
- Graceful keyboard interrupt handling

## Data Flow Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gateway App   │───▶│   IoTConnect SDK │───▶│  AWS IoT Core   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Data Generators │    │ MQTT Client      │    │ IoTConnect      │
│ - Gateway       │    │ - SSL/TLS        │    │ Platform        │
│ - PCT504-E      │    │ - Certificates   │    │                 │
│ - TBH300        │    │ - Message Queue  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Certificate Requirements

### Required Files
- `pk_Gateway-v3.pem`: Private key file
- `cert_Gateway-v3.crt`: Device certificate
- `AmazonRootCA1.pem`: Amazon Root CA certificate

### Security Features
- X.509 certificate authentication
- TLS 1.2+ encryption
- AWS IoT Core endpoint validation

## Error Handling Strategy

1. **Startup Validation**: Certificate file existence check
2. **SDK Initialization**: Comprehensive error logging
3. **Runtime Errors**: Retry logic with delays
4. **Graceful Shutdown**: Clean resource cleanup

## Performance Considerations

- **Memory Efficiency**: Single SDK instance, reused data structures
- **Network Optimization**: Batch sending of all device data
- **Error Recovery**: Automatic retry on transmission failures
- **Resource Management**: Context manager for SDK lifecycle

## Monitoring and Debugging

- **Verbose Logging**: All SDK operations logged
- **Debug Mode**: Enabled in SDK options
- **Status Reporting**: Real-time transmission status
- **Error Tracking**: Detailed exception handling and reporting