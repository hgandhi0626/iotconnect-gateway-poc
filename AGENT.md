# IoTConnect Gateway Project Context

## Project Overview
Implementing a Python-based gateway application that connects to IoTConnect (AWS backend) and sends simulated thermostat telemetry data for a gateway device and 11 child thermostat devices.

## IoTConnect Configuration

### Account Details
- **CPID**: `0534592e2d0b4ec3991ef9846363e51b`
- **Environment**: `poc`
- **Platform**: `aws`
- **Discovery URL**: `https://awsdiscovery.iotconnect.io`
- **Device Broker**: `a110maijzy82z6-ats.iot.us-east-1.amazonaws.com`
- **Message Version**: `2.1`
- **Auth Type**: `3` (X.509 Certificate)

### Device Structure
- **Gateway Device**
  - Name: `Gateway-v3`
  - UniqueId: `GW-20001448`
  - Tag: `gateway`
  
- **Child Devices (11 Total)**
  - 10 thermostats with model `PCT504-E`:
    - Thermostat-504112112200301 (Stat-1)
    - Thermostat-504112112200204 (Stat-2)
    - Thermostat-504112302130096 (Stat-3)
    - Thermostat-504112302130105 (Stat-4)
    - Thermostat-504112302130456 (Stat-5)
    - Thermostat-504112302130127 (Stat-6)
    - Thermostat-504112302130232 (Stat-7)
    - Thermostat-504112302130372 (Stat-8)
    - Thermostat-504112302130017 (Stat-9)
    - Thermostat-504112302130369 (Stat-10)
  - 1 UEI device with model `TBH300`:
    - ENG-300-707-003 (UEI)

### Template Information
Device Template Code: `1000000005`
All devices use tag `thermostat` except gateway which uses tag `gateway`

## Certificate Files
Located in `~/iotconnect-gateway/certs/`:
1. **Root CA**: `AmazonRootCA1.cer`
2. **Device Certificate**: `cert_Gateway-v3.crt`
3. **Private Key**: `pk_Gateway-v3.pem`

## Data Requirements

### Gateway Attributes (tag: gateway)
- `hb` (object): Heartbeat data with network info, versions, timestamps
- `zigbee_network` (object): ZigBee network configuration
- `zigbee_devices` (object): ZigBee device status information

### Thermostat Attributes (tag: thermostat)
All child devices must send:
- `genBasic`: Device basic information
- `hvacFanCtrl`: Fan control data
- `hvacThermostat`: Temperature and setpoint data
- `hvacUserInterfaceCfg`: User interface configuration
- `linkquality`: Link quality metric
- `relative_humidity`: Humidity sensor data
- `msOccupancySensing`: Occupancy detection
- `schedule_active`: Boolean (use `false`)
- `manuSpecificUniversalElectronics`: Manufacturer-specific data (TBH300 model only)

### Data Frequency
Send telemetry every **60 seconds** (as defined in template `dataFrequency`)

## Sample Data Structure
See `sample-file.json` for:
- Gateway heartbeat example
- PCT504-E thermostat data structure
- TBH300 thermostat data structure (with remote sensors)

## Development Environment

### Local (macOS)
- Python: 3.9.6
- IDE: Visual Studio Code
- Git: Installed

### Target (Raspberry Pi Gateway)
- OS: Raspbian GNU/Linux 11 (bullseye)
- Python: 3.9.2
- Internet: Connected

## SDK Information
- Repository: `https://github.com/avnet-iotconnect/iotc-python-sdk`
- Branch: `master-std-21`
- Package: `iotconnect-sdk-1.0.tar.gz`
- Sample File: `iotconnect-sdk-1.0-firmware-python_msg-2_1.py`
- Message Protocol: 2.1

## Implementation Steps

### Completed
1. ✅ IoTConnect account information gathered
2. ✅ Device template and structure understood
3. ✅ Certificates obtained (X.509)
4. ✅ SDK repository cloned (master-std-21 branch)
5. ✅ Sample data structure analyzed

### In Progress
- Installing SDK dependencies
- Creating custom gateway application
- Implementing data simulation logic

### Pending
- Local testing and validation
- Transfer to Raspberry Pi
- Production deployment
- Optional: Setup as systemd service

## Key Technical Notes
- Must send data for ALL devices (gateway + 11 children) in each telemetry cycle
- Ignore attributes in sample-file.json that don't exist in the template
- Use nested object structures as defined in template
- Time format: ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SS.000Z`)
- Gateway uses authentication type 3 (X.509)

## File Locations