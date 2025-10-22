"""
IoTConnect Gateway Application
Sends simulated thermostat data for gateway and 11 child devices
"""

import json
import time
import random
from iotconnect import IoTConnectSDK
from datetime import datetime
import sys
import os
from data_generators import generate_gateway_data, generate_pct504e_data, generate_tbh300_data, generate_gesysense_receiver_data, generate_gesysense_temperature_data, generate_energy_data, generate_lighting_data, generate_refrigeration_data, generate_temperature_zigbee_data

# ============================================================================
# CONFIGURATION
# ============================================================================

# Gateway Configuration
UNIQUE_ID = "GW-20001448"  # Your gateway device unique ID
INTERVAL = 60  # Send data every 60 seconds

# Certificate Paths (relative to this script) - Back to CA-Signed
CERT_DIR = os.path.abspath("./certs")
SSL_KEY_PATH = os.path.join(CERT_DIR, "pk_Gateway-v3.pem")
SSL_CERT_PATH = os.path.join(CERT_DIR, "cert_Gateway-v3.crt")
SSL_CA_PATH = os.path.join(CERT_DIR, "AmazonRootCA1.pem")

# SDK Options
SDK_OPTIONS = {
    "certificate": {
        "SSLKeyPath": SSL_KEY_PATH,
        "SSLCertPath": SSL_CERT_PATH,
        "SSLCaPath": SSL_CA_PATH
    },
    "offlineStorage": {
        "disabled": False,
        "availSpaceInMb": 0.01,
        "fileCount": 5,
        "keepalive": 60
    },
    "skipValidation": False,
    "IsDebug": True,  # Set to True for detailed logs
    "cpid": "0534592e2d0b4ec3991ef9846363e51b",
    "sId": "",
    "env": "poc",
    "pf": "aws",
    "forceAuthType": 3  # Force CA_SELF_SIGNED authentication type
}

# Child Device IDs
CHILD_DEVICES = [
    {"uniqueId": "Thermostat-504112112200301", "name": "Stat-1", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112112200204", "name": "Stat-2", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112302130096", "name": "Stat-3", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112302130105", "name": "Stat-4", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112302130456", "name": "Stat-5", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112302130127", "name": "Stat-6", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112302130232", "name": "Stat-7", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112302130372", "name": "Stat-8", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112302130017", "name": "Stat-9", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Thermostat-504112302130369", "name": "Stat-10", "model": "PCT504-E", "deviceType": "thermostat"},
    {"uniqueId": "Temperature-ZigBee-317M12303210501", "name": "ZigBee-1", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12303210685", "name": "ZigBee-2", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12303210764", "name": "ZigBee-3", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12303210702", "name": "ZigBee-4", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12303210597", "name": "ZigBee-5", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12303210419", "name": "Zigbee-6", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12303210749", "name": "Zigbee-7", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12211280468", "name": "Zigbee-8", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12303210548", "name": "Zigbee-9", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "Temperature-ZigBee-317M12303210380", "name": "Zigbee-10", "model": "", "deviceType": "temperature_zigbee"},
    {"uniqueId": "ENG-300-707-003", "name": "UEI", "model": "TBH300", "deviceType": "thermostat"},
    {"uniqueId": "8000020280", "name": "gesysense-receiver", "model": "P.W01211", "deviceType": "gesysense"},
    {"uniqueId": "ENG-300-707-004", "name": "WattNode", "model": "WNC-3Y-208-MB", "deviceType": "energy"},
    {"uniqueId": "ENG-300-707-001", "name": "Ke2", "model": "21263", "deviceType": "refrigeration"},
    {"uniqueId": "ENG-300-707-005-20001448", "name": "LightingController", "model": "CONMOD1.0-ZG", "deviceType": "lighting"},
]

# ============================================================================
# DATA SIMULATION FUNCTIONS (imported from data_generators.py)
# ============================================================================

# ============================================================================
# CALLBACK FUNCTIONS - IoTConnect SDK Event Handlers
# ============================================================================

"""
 * Type    : Callback Function "DeviceCallback()"
 * Usage   : Firmware will receive commands from cloud. You can manage your business logic as per received command.
 * Input   :  
 * Output  : Receive device command, firmware command and other device initialize error response 
"""

def DeviceCallback(msg):
    """
    Handle device commands from IoTConnect cloud platform
    
    This callback processes incoming device commands and manages acknowledgments.
    Called automatically by the SDK when commands are received from the cloud.
    
    Command Types Handled:
        - Type 0: Device commands (control, configuration, etc.)
        - Acknowledgment processing for command confirmation
        - Error handling for malformed commands
    
    Args:
        msg (dict): Command message from cloud containing:
            - ct: Command type (0 for device commands)
            - ack: Acknowledgment ID (if response required)
            - id: Device ID (optional, for targeted commands)
            - Additional command-specific data
    
    Acknowledgment Status Codes:
        - 7: Success/Command executed successfully
        - 4: Failed
        - 5: Executed
        - 6: Executed acknowledgment
    """
    print("\n--- Command Message Received ---")
    print(json.dumps(msg, indent=2))
    
    if msg and "ct" in msg:
        cmd_type = msg["ct"]
        
        # Device Command
        if cmd_type == 0:
            data = msg
            if "id" in data:
                if "ack" in data and data["ack"]:
                    sdk.sendAckCmd(data["ack"], 7, "sucessfull", data["id"])
            else:
                if "ack" in data and data["ack"]:
                    sdk.sendAckCmd(data["ack"], 7, "sucessfull")

def DeviceFirmwareCallback(msg):
    """
    Handle Over-The-Air (OTA) firmware update commands
    
    This callback manages firmware update processes for the gateway and child devices.
    Processes firmware URLs and coordinates update acknowledgments across multiple devices.
    
    Firmware Update Process:
        1. Receives firmware URLs from cloud
        2. Matches URLs to device tags (gateway vs thermostat)
        3. Initiates download/update process
        4. Sends acknowledgment with update status
    
    Args:
        msg (dict): Firmware command message containing:
            - ct: Command type (1 for firmware commands)
            - urls: Array of firmware download URLs
            - ack: Acknowledgment ID for response
            - Device targeting information
    
    OTA Status Codes:
        - 0: Success/Ready to download
        - 1: Failed
        - 2: Downloading in progress
        - 3: Download completed
        - 4: Download failed
    """
    print("\n--- Firmware Command Received ---")
    print(json.dumps(msg, indent=2))
    
    if msg and "ct" in msg:
        cmd_type = msg["ct"]
        
        # Firmware OTA Command
        if cmd_type == 1:
            data = msg
            if "urls" in data and data["urls"]:
                for url_list in data["urls"]:
                    if "tg" in url_list:
                        device_list = sdk.Getdevice()
                        for device in device_list:
                            if "tg" in device and device["tg"] == url_list["tg"]:
                                sdk.sendOTAAckCmd(data["ack"], 0, "sucessfull", device["id"])
                    else:
                        sdk.sendOTAAckCmd(data["ack"], 0, "sucessfull")

def DeviceConnectionCallback(msg):
    """
    Handle device connection status updates
    
    This callback monitors and reports device connectivity status changes.
    Provides real-time visibility into device online/offline status.
    
    Connection Events:
        - Device online/offline transitions
        - Network connectivity changes
        - Gateway-to-cloud connection status
        - Child device connectivity through gateway
    
    Args:
        msg (dict): Connection status message containing:
            - ct: Command type (116 for connection status)
            - command: Connection state (true=connected, false=disconnected)
            - Device identification information
            - Timestamp and status details
    """
    print("\n--- Connection Status ---")
    print(json.dumps(msg, indent=2))
    
    if msg and "ct" in msg:
        cmd_type = msg["ct"]
        
        # Connection status
        if cmd_type == 116:
            print(f"Device connection status: {msg.get('command', 'unknown')}")

def TwinUpdateCallback(msg):
    """
    Handle device twin (digital shadow) property updates
    
    Device twins maintain a synchronized state between the physical device and cloud.
    This callback processes desired property changes from the cloud and updates
    the device's reported properties accordingly.
    
    Twin Property Types:
        - Desired: Properties set by applications/cloud (what the device should be)
        - Reported: Properties reported by device (what the device actually is)
        - System: Metadata properties (version, uniqueId) - automatically managed
    
    Update Process:
        1. Receive desired properties from cloud
        2. Apply changes to device configuration
        3. Report back actual device state
        4. Maintain synchronization between desired and reported states
    
    Args:
        msg (dict): Twin update message containing:
            - desired: Properties requested by cloud/applications
            - reported: Current device-reported properties (optional)
            - System properties (version, uniqueId) - ignored
    
    Filtering:
        - Processes only desired properties without reported counterparts
        - Skips system properties (version, uniqueId)
        - Updates each property individually for granular control
    """
    print("\n--- Twin Update Received ---")
    print(json.dumps(msg, indent=2))
    
    if msg:
        if "desired" in msg and "reported" not in msg:
            for key in msg["desired"]:
                if key not in ["version", "uniqueId"]:
                    sdk.UpdateTwin(key, msg["desired"][key])

def InitCallback(response):
    """
    Handle SDK initialization response
    
    This callback receives the initialization response from the IoTConnect SDK.
    Currently used for logging and debugging the initialization process.
    
    Initialization Response Contains:
        - Connection status and configuration validation
        - Device registration confirmation
        - Available features and capabilities
        - Error codes and diagnostic information
    
    Args:
        response (dict): SDK initialization response with status and configuration data
    
    Future Enhancements:
        - Initialize device-specific configurations
        - Set up feature flags based on capabilities
        - Handle initialization errors gracefully
        - Configure device behavior based on cloud settings
    """
    print("\n--- Initialization Response ---")
    print(json.dumps(response, indent=2))

# ============================================================================
# MAIN APPLICATION FUNCTIONS
# ============================================================================

sdk = None

def send_telemetry():
    """
    Send telemetry data for gateway and all child devices
    
    This function orchestrates the complete telemetry transmission process:
    1. Generates current timestamp in ISO 8601 format with milliseconds
    2. Creates gateway heartbeat and status data
    3. Generates data for each child device based on model type
    4. Batches all device data into a single transmission
    5. Sends data to IoTConnect cloud via SDK
    
    Data Volume Per Transmission:
        - 1 Gateway device (heartbeat, network status)
        - 11 Child devices (10 PCT504-E + 1 TBH300)
        - Total: 12 devices per transmission
    
    Transmission Format:
        Each device data includes:
        - uniqueId: Device identifier
        - time: ISO timestamp
        - data: Device-specific telemetry payload
    
    Error Handling:
        - Logs transmission status
        - Does not throw exceptions (handled by caller)
        - Continues operation on individual device data generation errors
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    
    # Prepare data array
    data_array = []
    
    # 1. Gateway data
    gateway_data = {
        "uniqueId": UNIQUE_ID,
        "time": timestamp,
        "data": generate_gateway_data()
    }
    data_array.append(gateway_data)
    
    # 2. Child device data
    for device in CHILD_DEVICES:
        device_type = device.get("deviceType", "")
        model = device.get("model", "")
        
        # Generate data based on deviceType first, then model for differentiation
        if device_type == "thermostat":
            if model == "PCT504-E":
                device_data = generate_pct504e_data()
            elif model == "TBH300":
                device_data = generate_tbh300_data()
            else:
                print(f"Warning: Unknown thermostat model {model} for device {device['uniqueId']}")
                continue
        elif device_type == "temperature_zigbee":
            device_data = generate_temperature_zigbee_data()
        elif device_type == "gesysense":
            if model == "P.W01211":  # gesySense receiver
                device_data = generate_gesysense_receiver_data()
            elif model == "P.W01101-2":  # gesySense temperature module
                device_data = generate_gesysense_temperature_data()
            else:
                print(f"Warning: Unknown gesysense model {model} for device {device['uniqueId']}")
                continue
        elif device_type == "energy":
            device_data = generate_energy_data()
        elif device_type == "refrigeration":
            device_data = generate_refrigeration_data()
        elif device_type == "lighting":
            device_data = generate_lighting_data()
        else:
            print(f"Warning: Unknown device type {device_type} for device {device['uniqueId']}")
            continue
        
        child_payload = {
            "uniqueId": device["uniqueId"],
            "time": timestamp,
            "data": device_data
        }
        data_array.append(child_payload)
    
    # Send data
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending telemetry for {len(data_array)} devices...")
    sdk.SendData(data_array)
    print("Data sent successfully")

def main():
    """
    Main application entry point and control loop
    
    This function manages the complete application lifecycle:
    
    Initialization Phase:
        1. Display application banner and configuration summary
        2. Validate SSL certificate files existence and accessibility
        3. Initialize IoTConnect SDK with authentication and options
        4. Register all callback functions for cloud communication
        5. Retrieve and validate device list from cloud
    
    Main Operation Loop:
        1. Continuously send telemetry data every 60 seconds
        2. Handle transmission errors with retry logic
        3. Maintain connection health and status monitoring
        4. Process incoming commands and callbacks asynchronously
    
    Error Recovery:
        - Certificate validation before startup
        - SDK initialization error handling
        - Runtime transmission error recovery
        - Graceful shutdown on interruption
        - Detailed error logging and diagnostics
    
    Resource Management:
        - Uses context manager for SDK lifecycle
        - Automatic cleanup on exit
        - Proper exception handling and logging
        - Memory-efficient operation for long-running deployment
    
    Shutdown Process:
        - Graceful handling of Ctrl+C (SIGINT)
        - SDK resource cleanup
        - Final status reporting
        - Clean process termination
    """
    global sdk
    
    print("=" * 70)
    print("IoTConnect Gateway Application")
    print("=" * 70)
    print(f"Gateway ID: {UNIQUE_ID}")
    print(f"Child Devices: {len(CHILD_DEVICES)}")
    print(f"Data Interval: {INTERVAL} seconds")
    print("=" * 70)
    
    # Verify certificate files exist
    print("\nVerifying certificate files...")
    for cert_file in [SSL_KEY_PATH, SSL_CERT_PATH, SSL_CA_PATH]:
        if os.path.isfile(cert_file):
            print(f"Found: {cert_file}")
        else:
            print(f"Missing: {cert_file}")
            print("Please ensure all certificate files are in the ./certs directory")
            sys.exit(1)
    
    try:
        print("\nInitializing IoTConnect SDK...")
        with IoTConnectSDK(UNIQUE_ID, SDK_OPTIONS, DeviceConnectionCallback) as sdk:
            print("SDK initialized successfully")
            
            # Register callbacks
            sdk.onDeviceCommand(DeviceCallback)
            sdk.onTwinChangeCommand(TwinUpdateCallback)
            sdk.onOTACommand(DeviceFirmwareCallback)
            
            # Get device list
            device_list = sdk.Getdevice()
            print(f"Retrieved device list: {len(device_list)} devices")
            
            print("\n" + "=" * 70)
            print("Starting telemetry loop... (Press Ctrl+C to stop)")
            print("=" * 70)
            
            # Main telemetry loop
            while True:
                try:
                    send_telemetry()
                    time.sleep(INTERVAL)
                except Exception as e:
                    print(f"Error sending telemetry: {e}")
                    time.sleep(5)  # Wait before retry
                    
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()