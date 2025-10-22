"""
Data Generation Functions for IoTConnect Gateway
Contains functions to generate simulated telemetry data for different device types
"""

import random
from datetime import datetime


def generate_gateway_data():
    """Generate gateway heartbeat and network data"""
    return {
        "hb": {
            "net_address_ip_v4": "192.168.68.123",
            "net_address_ip_v6": "fe80::3868:668e:93b4:9c1f",
            "hostname": "raspberrypi",
            "gateway_version": "3.2.40",
            "ota_version": "3.2.13",
            "configured": True,
            "fixed_id": "2941008C7954",
            "serial_id": "20002330",
            "mac_address": "b8:27:eb:3f:f0:11",
            "download_config_success": True,
            "download_firmware_success": True,
            "ota_success": True,
            "reason": "periodic",
            "ota_firmware_timestamp": "2024-09-06T15:57:02.070944Z",
            "gateway_firmware_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "gateway_start_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "gateway_stop_timestamp": "",
            "config_file_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "gateway_reboot_success": True
        },
        "zigbee_network": {
            "channel": 11,
            "extended_pan_id": "0x00124b0024cbee5f",
            "pan_id": 55363
        }
    }


def generate_pct504e_data():
    """Generate data for PCT504-E thermostat model"""
    base_temp = random.uniform(72.0, 78.0)
    
    return {
        "genBasic": {
            "appVersion": 1,
            "dateCode": "20200513",
            "hwVersion": 4,
            "manufacturerName": "OWON Technology Inc.",
            "modelId": "PCT504-E",
            "powerSource_primary": "dc source",
            "powerSource_secondary": False,
            "stackVersion": 0,
            "zclVersion": 3
        },
        "hvacFanCtrl": {
            "fanMode": random.choice(["auto", "on"]),
            "fanModeSequence": "low/med/high/auto"
        },
        "hvacThermostat": {
            "absMaxCoolSetpointLimit": 95.0,
            "absMaxHeatSetpointLimit": 86.0,
            "absMinCoolSetpointLimit": 44.6,
            "absMinHeatSetpointLimit": 41.0,
            "controlSequenceOfOperation": "cooling with heating 4-pipes",
            "localTemperature": round(base_temp, 1),
            "maxCoolSetpointLimit": 95.0,
            "maxHeatSetpointLimit": 86.0,
            "minCoolSetpointLimit": 44.6,
            "minHeatSetpointLimit": 41.0,
            "minSetpointDeadBand": 2.7,
            "occupancy": random.choice([True, False]),
            "occupiedCoolingSetpoint": 69.8,
            "occupiedHeatingSetpoint": 62.6,
            "runningMode": random.choice(["cool", "heat", "auto"]),
            "runningState_cool2ndStageStateOn": False,
            "runningState_coolStateOn": random.choice([True, False]),
            "runningState_fan2ndStageStateOn": False,
            "runningState_fan3rdStageStateOn": random.choice([True, False]),
            "runningState_fanStateOn": False,
            "runningState_heat2ndStageStateOn": False,
            "runningState_heatStateOn": False,
            "systemMode": random.choice(["cool", "heat", "auto", "off"]),
            "unoccupiedCoolingSetpoint": 69.8,
            "unoccupiedHeatingSetpoint": 62.6,
            "programingOperMode_auto_recovery_mode": "off",
            "programingOperMode_economy_energy_star_mode": "off",
            "programingOperMode_mode": "simple/setpoint mode",
            "systemTypeConfig_coolingSystemStage": "cool stage 1",
            "systemTypeConfig_heatingFuelSource": "electric / B",
            "systemTypeConfig_heatingSystemStage": "heat stage 1",
            "systemTypeConfig_heatingSystemType": "conventional"
        },
        "occupied_heating_setphvacUserInterfaceCfgoint": {
            "keypadLockout": "no lockout",
            "tempDisplayMode": random.choice(["temperature in Celsius", "temperature in Fahrenheit"])
        },
        "linkquality": random.randint(150, 255),
        "relative_humidity": {
            "maxMeasuredValue": 100.0,
            "measuredValue": round(random.uniform(25.0, 45.0), 1),
            "minMeasuredValue": 0.0
        },
        "msOccupancySensing": {
            "occupancy": random.choice([True, False]),
            "occupancySensorType": "ultrasonic",
            "pirOToUDelay": 60
        },
        "schedule_active": False
    }


def generate_tbh300_data():
    """Generate data for TBH300 thermostat model (UEI)"""
    base_temp = random.uniform(75.0, 82.0)
    
    return {
        "genBasic": {
            "appVersion": 10,
            "dateCode": "20210915-DE-FB1",
            "hwVersion": 0,
            "manufacturerName": "Universal Electronics Inc.",
            "modelId": "TBH300",
            "powerSource_primary": "mains (single phase)",
            "powerSource_secondary": False,
            "stackVersion": 0,
            "zclVersion": 8
        },
        "hvacFanCtrl": {
            "fanMode": random.choice(["on", "auto"]),
            "fanModeSequence": "on/auto"
        },
        "hvacThermostat": {
            "absMaxCoolSetpointLimit": 112.01,
            "absMaxHeatSetpointLimit": 97.02,
            "absMinCoolSetpointLimit": 44.98,
            "absMinHeatSetpointLimit": 29.98,
            "controlSequenceOfOperation": "cooling with heating 4-pipes",
            "localTemperature": round(base_temp, 1),
            "maxCoolSetpointLimit": 93.0,
            "maxHeatSetpointLimit": 90.05,
            "minCoolSetpointLimit": 60.01,
            "minHeatSetpointLimit": 55.96,
            "minSetpointDeadBand": 3.6,
            "occupancy": random.choice([True, False]),
            "occupiedCoolingSetpoint": 71.01,
            "occupiedHeatingSetpoint": 68.0,
            "runningMode": random.choice(["cool", "heat", "auto"]),
            "runningState_cool2ndStageStateOn": random.choice([True, False]),
            "runningState_coolStateOn": random.choice([True, False]),
            "runningState_fan2ndStageStateOn": False,
            "runningState_fan3rdStageStateOn": False,
            "runningState_fanStateOn": random.choice([True, False]),
            "runningState_heat2ndStageStateOn": False,
            "runningState_heatStateOn": False,
            "systemMode": random.choice(["auto", "cool", "heat"]),
            "unoccupiedCoolingSetpoint": 75.0,
            "unoccupiedHeatingSetpoint": 61.0,
            "programingOperMode_auto_recovery_mode": "off",
            "programingOperMode_economy_energy_star_mode": "off",
            "programingOperMode_mode": "simple/setpoint mode",
            "systemTypeConfig_coolingSystemStage": "cool stage 1",
            "systemTypeConfig_heatingFuelSource": "electric / B",
            "systemTypeConfig_heatingSystemStage": "heat stage 1",
            "systemTypeConfig_heatingSystemType": "conventional"
        },
        "occupied_heating_setphvacUserInterfaceCfgoint": {
            "keypadLockout": "no lockout",
            "tempDisplayMode": "temperature in Fahrenheit"
        },
        "linkquality": random.randint(150, 200),
        "relative_humidity": {
            "maxMeasuredValue": 100.0,
            "measuredValue": round(random.uniform(25.0, 40.0), 2),
            "minMeasuredValue": 0.0
        },
        "msOccupancySensing": {
            "occupancy": random.choice([True, False]),
            "occupancySensorType": "ultrasonic",
            "pirOToUDelay": 60
        },
        "schedule_active": False,
        "manuSpecificUniversalElectronics": {
            "temperature": round(base_temp, 1),
            "lowBattery": False,
            "installed": True,
            "online": True,
            "sensorType": "indoor",
            "systemState_autoModeOn": random.choice([True, False]),
            "systemState_coolModeOn": random.choice([True, False]),
            "systemState_fanModeOn": random.choice([True, False]),
            "systemState_heatModeOn": False,
            "systemState_occupied": random.choice([True, False]),
            "systemState_overrideHospitalityLogicOn": False,
            "systemState_systemStateOn": True,
            "tempSource_sensorSource": "remote"
        },
        "manuSpecific_remote_temperature_sensor": {
            "remTempSensor1": {
                "deviceId": "uei-temp1-6888a100002cd9ed",
                "installed": True,
                "lowBattery": False,
                "name": "Remote Sensor",
                "online": True,
                "sensorType": "indoor",
                "temperature": 81.0
            },
            "remTempSensor2": {
                "deviceId": "uei-temp2-6888a100002cd9ed",
                "installed": True,
                "lowBattery": False,
                "name": "Discharge Sensor",
                "online": True,
                "sensorType": "supply air",
                "temperature": 81.07
            },
            "remTempSensor3": {
                "deviceId": "uei-temp3-6888a100002cd9ed",
                "installed": False,
                "lowBattery": False,
                "name": "Averaging Sensor",
                "online": False,
                "sensorType": "indoor",
                "temperature": 32.0
            }
        }
    }


def generate_gesysense_receiver_data():
    """Generate data for gesySense receiver device (tag: gesysense)"""
    return {
        "receiver": {
            "serial_number": "8.000.020.436",
            "label_id": "8000020436", 
            "firmware_version": "1.07",
            "hardware_version": "0.02",
            "error_status": 0
        }
    }


def generate_gesysense_temperature_data():
    """Generate data for gesySense temperature module device (tag: temperature_gesysense)"""
    # Generate realistic temperature reading around 42°C (similar to sample)
    base_temp = random.uniform(40.0, 45.0)
    
    # Random device name selection
    device_names = ["19728 Cooler", "Kitchen Fridge"]
    device_name = random.choice(device_names)
    
    # Generate label_id based on device name
    if "Cooler" in device_name:
        label_id = "19728"
        serial_number = "0.000.019.728"
    else:
        label_id = "22602" 
        serial_number = "0.000.022.602"
    
    return {
        "registered_temperature_modules": {
            "model_id": "P.W01101-2",
            "serial_number": serial_number,
            "label_id": label_id,
            "signal_quality": random.randint(80, 95),
            "transmission_quality": 100,
            "battery_status": 100,
            "temperature": round(base_temp, 3)
        }
    }


def generate_energy_data():
    """Generate data for WattNode energy device (tag: energy)"""
    # Generate realistic energy readings for a 3-phase system
    base_voltage = random.uniform(208, 240)  # 3-phase voltage range
    total_power = random.uniform(5000, 15000)  # Total power in watts
    
    return {
        "wattnode_modbus_device_info": {
            "firmware_version": "1.23",
            "model_id": "WNC-3Y-208-MB",
            "serial_number": "WN2024001234",
            "modbus_address": 50
        },
        "total_energy_sum": round(random.uniform(1000, 5000), 2),  # kWh
        "power_sum": round(total_power, 1),  # Total power
        "ct_amps": random.randint(100, 400),  # CT rated current
        "ct_amps_a": random.randint(100, 150),
        "ct_amps_b": random.randint(100, 150), 
        "ct_amps_c": random.randint(100, 150),
        "ct_directions": "all normal",
        "phase_adjust_a": 0,
        "phase_adjust_b": 120,
        "phase_adjust_c": 240,
        "zero_energy": 0,
        "real_power_a": round(total_power * 0.33, 1),
        "real_power_b": round(total_power * 0.33, 1),
        "real_power_c": round(total_power * 0.34, 1),
        "voltage_a": round(base_voltage + random.uniform(-5, 5), 1),
        "voltage_b": round(base_voltage + random.uniform(-5, 5), 1),
        "voltage_c": round(base_voltage + random.uniform(-5, 5), 1),
        "voltage_avg": round(base_voltage, 1)
    }


def generate_lighting_data():
    """Generate data for lighting controller device (tag: lighting)"""
    # Generate 8 zones as shown in sample
    zones = {}
    zone_names = ["kitchen", "living room", "bathroom", "bedroom", "garage", "", "", ""]
    
    for i in range(1, 9):
        zone_id = f"zone_id_{i}"
        zones[zone_id] = {
            "id": f"Lighting-21-20002330_{zone_id}",
            "name": zone_names[i-1] if i <= 5 else "",
            "is_enabled": True,
            "relay_value": random.choice(["on", "off"]),
            "schedule_active": random.choice([True, False])
        }
    
    return {
        "lighting_modbus_device_info": {
            "version": 1.0,
            "model_id": "CONMOD1.0-ZG",
            "firmware_version": "2.1.3",
            "modbus_address": 21
        },
        "zone_id_def": zones
    }


def generate_refrigeration_data():
    """Generate data for KE2 refrigeration device (tag: refrigeration)"""
    # Generate realistic refrigeration temperatures (cooler/freezer range)
    room_temp = random.uniform(32, 40)  # Fahrenheit for refrigeration
    coil_temp = random.uniform(25, 35)  # Coil typically cooler than room
    setpoint = random.uniform(35, 38)
    
    return {
        "ke2_modbus_device_info": {
            "firmware_version": "3.2.1",
            "model_id": "21263",
            "firmware_part_number": 21263.0,
            "modbus_address": 31
        },
        "controller_modbus_address": "31",
        "type_of_3rd_input": "temperature",
        "fan_mode_during_refrigeration_mode": "auto",
        "minimum_compressor_run_time": 5.0,
        "minimum_compressor_off_time": 3.0,
        "temperature_differential": 2.0,
        "defrost_time": 30.0,
        "digital_input_active_state_for_3rd_input": "high",
        "number_of_defrosts_per_day": 4.0,
        "type_of_defrost": "electric",
        "temperature_setpoint": round(setpoint, 1),
        "drain_time": 5.0,
        "high_and_low_alarm_delay": 10,
        "low_alarm_temperature_offset": 5.0,
        "high_alarm_temperature_offset": 5.0,
        "defrost_initiate_type": 1,
        "type_of_4th_input": "none",
        "digital_input_active_state_for_4th_input": "low",
        "second_room_temperature_set_point": round(setpoint + 2, 1),
        "start_time_of_defrost_1": 6.0,
        "start_time_of_defrost_2": 12.0,
        "start_time_of_defrost_3": 18.0,
        "start_time_of_defrost_4": 24.0,
        "start_time_of_defrost_5": 0.0,
        "start_time_of_defrost_6": 0.0,
        "start_time_of_defrost_7": 0.0,
        "start_time_of_defrost_8": 0.0,
        "start_time_of_defrost_9": 0.0,
        "start_time_of_defrost_10": 0.0,
        "start_time_of_defrost_11": 0.0,
        "start_time_of_defrost_12": 0,
        "time_of_day": round(random.uniform(0, 24), 1),
        "extreme_differential": 1.0,
        "defrost_heater_mode": 1,
        "defrost_parameter": 1,
        "defrost_pump_down_time": 2.0,
        "fan_state_during_defrost": "off",
        "max_fan_delay_time": 10.0,
        "fan_delay_temperature": round(room_temp - 5, 1),
        "defrost_termination_temperature_setpoint": 45.0,
        "alarms": random.choice(["none", "high_temp", "low_temp"]),
        "coil_temperature_1": round(coil_temp, 1),
        "coil_temperature_2": round(coil_temp + random.uniform(-2, 2), 1),
        "current_temperature": round(room_temp, 1),
        "compressor_relay": random.choice(["on", "off"]),
        "defrost_relay": "off",
        "fan_relay": random.choice(["on", "off"]),
        "system_status": random.choice(["cooling", "idle", "defrost"]),
        "high_alarm_offset": 5.0,
        "low_alarm_offset": 5.0,
        "minimum_comp_off_time": 3,
        "minimum_comp_run_time": 5,
        "room_temp": int(room_temp),
        "coil_temp": int(coil_temp),
        "temp_3_temp": int(random.uniform(30, 40)),
        "temp_4_temp": int(random.uniform(30, 40))
    }


def generate_temperature_zigbee_data():
    """Generate data for temperature_zigbee devices (ZigBee temperature sensors)"""
    return {
        "link_quality": random.randint(85, 100),
        "battery_percentage_remaining": random.randint(90, 100),
        "battery_voltage": round(random.uniform(9.5, 11.0), 1),
        "measure_temperature_value": round(random.uniform(68.0, 80.0), 1)
    }