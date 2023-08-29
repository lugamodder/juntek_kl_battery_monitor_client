
def calculate_checksum(data):
    checksum = (sum(data) % 255) + 1
    return checksum


def parse_response(response, parse_function):
    response_parts = response.strip().split(",")

    parse_function_code = parse_function.__name__[7:-9]
    if len(response_parts) >= 5 and response_parts[0].lower().startswith(":r{}=".format(parse_function_code)):
        try:
            communication_address = int(response_parts[0][5:])
            received_checksum = int(response_parts[1])
            data = response_parts[2:][:-1]

            calculated_checksum = calculate_checksum([int(value) for value in data])

            if received_checksum != calculated_checksum:
                print("Контрольная сумма не совпадает. Ответ может быть поврежден.")
                return None
            if parse_function_code == "00":
                parsed_response = parse_r00_response(data)
            elif parse_function_code == "50":
                parsed_response = parse_r50_response(data)
            elif parse_function_code == "51":
                parsed_response = parse_r51_response(data)
            else:
                parsed_response = None
                print("Неизвестная команда")

            if parsed_response:
                return parsed_response
            else:
                print("Не удалось распарсировать ответ.")

        except (ValueError, IndexError):
            return None
    else:
        return None


def parse_r00_response(data):
    current_sensor_value = int(data[0][0])
    current_sensor = "Hall-sensor" if current_sensor_value == 1 else "Sampler"
    data_value = int(data[0][1])
    max_voltage = data_value * 100
    max_current = int(data[0][2:]) * 10
    version = int(data[1])
    serial_number = int(data[2])

    result = {
        "current_sensor": current_sensor,
        "max_voltage": max_voltage,
        "max_current": max_current,
        "version": version,
        "serial_number": serial_number
    }
    return result


def parse_r50_response(data):
    voltage = float(data[0]) / 100
    current = float(data[1]) / 100
    remaining_battery_capacity = float(data[2]) / 1000
    cumulative_capacity = float(data[3]) / 1000
    watt_hour = float(data[4]) / 100000
    running_time = int(data[5])

    ambient_temp_sign = int(data[6][0])
    ambient_temp_value = int(data[6][1:])
    ambient_temperature = ambient_temp_value * (-1 if ambient_temp_sign == 0 else 1)

    output_status = int(data[8])
    current_direction = int(data[9])
    battery_life = int(data[10])
    internal_resistance = float(data[11]) / 100
    current_signed = current * (-1 if current_direction == 0 else 1)

    result = {
        "voltage": voltage,
        "current": current,
        "current_signed": current_signed,
        "remaining_battery_capacity": remaining_battery_capacity,
        "cumulative_capacity": cumulative_capacity,
        "watt_hour": watt_hour,
        "running_time": running_time,
        "ambient_temperature": ambient_temperature,
        "output_status": output_status,
        "current_direction": current_direction,
        "battery_life": battery_life,
        "internal_resistance": internal_resistance,
    }
    return result


def parse_r51_response(data):
    overvoltage_protection = float(data[0]) / 100
    undervoltage_protection = float(data[1]) / 100
    forward_overcurrent_protection = float(data[2]) / 100
    negative_overcurrent_protection = -float(data[3]) / 100
    over_power_protection = float(data[4]) / 100

    temp_over_temperature_protection = int(data[5][0])
    over_temperature_value = int(data[5][1:])
    over_temperature_protection = over_temperature_value * (-1 if temp_over_temperature_protection == 0 else 1)

    protection_recovery_time = int(data[6])
    delay_time = int(data[7])
    preset_battery_capacity = float(data[8]) / 10
    fine_tuning_voltage = int(data[9])
    fine_tuning_current = int(data[10])
    temperature_calibration = int(data[11])
    relay_type = int(data[12])
    current_multipler = int(data[13])

    voltage_curve_scale = int(data[14]) if len(data) > 14 else None
    current_curve_scale = int(data[15]) if len(data) > 15 else None

    result = {
        "overvoltage_protection": overvoltage_protection,
        "undervoltage_protection": undervoltage_protection,
        "forward_overcurrent_protection": forward_overcurrent_protection,
        "negative_overcurrent_protection": negative_overcurrent_protection,
        "over_power_protection": over_power_protection,
        "over_temperature_protection": over_temperature_protection,
        "protection_recovery_time": protection_recovery_time,
        "delay_time": delay_time,
        "preset_battery_capacity": preset_battery_capacity,
        "fine_tuning_voltage": fine_tuning_voltage,
        "fine_tuning_current": fine_tuning_current,
        "temperature_calibration": temperature_calibration,
        "relay_type": relay_type,
        "current_multipler": current_multipler,
    }

    if voltage_curve_scale is not None:
        result["voltage_curve_scale"] = voltage_curve_scale

    if current_curve_scale is not None:
        result["current_curve_scale"] = current_curve_scale

    return result

def main():
    print("Hello work")

if __name__ == "__main__":
    main()
