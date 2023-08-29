#!/usr/bin/python3
import json
import argparse
import serial
import sys
from kl_junctek import calculate_checksum, parse_response, parse_r00_response, parse_r50_response, parse_r51_response

# Создаем парсер аргументов командной строки
parser = argparse.ArgumentParser(description="Serial Client for JUNCTEK KL-F device")
parser.add_argument("-p", "--port", type=str, help="COM port name")
parser.add_argument("-b", "--baudrate", type=int, default=115200, help="Baud rate")
parser.add_argument("-a", "--address", type=int, default=1, help="Communication address")
parser.add_argument("-c", "--command", type=str, help="Commands to run")

args = parser.parse_args()

if args.command:
    commands = filter(None, args.command.split(','))


class DeviceClient:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=2)
        except serial.serialutil.SerialException as e:
            error_message = str(e).split(":")[0].strip()
            print(f"Ошибка при открытии COM-порта: {error_message}")
            sys.exit(1)

    def send_command(self, function_number, address, data_field):
        try:
            calculated_checksum = calculate_checksum([data_field])

            command = f":R{function_number:02d}={address},{calculated_checksum},{data_field},\r\n"
            self.serial_port.write(command.encode())
            response = self.serial_port.read(1024).decode()
            parsed_response = {}

            if function_number == 0:
                parsed_response = parse_response(response, parse_r00_response)
            elif function_number == 50:
                parsed_response = parse_response(response, parse_r50_response)
            elif function_number == 51:
                parsed_response = parse_response(response, parse_r51_response)
            else:
                print("Неизвестная команда")

            if parsed_response:
                return parsed_response
            else:
                print("Нет ответа от устройства ", response)

        except serial.SerialTimeoutException:
            print("Превышено время ожидания ответа.")
        except Exception as e:
            print("Произошла ошибка при отправке или приеме:", e)

    def disconnect(self):
        self.serial_port.close()


def main():
    device_client = DeviceClient(args.port, args.baudrate)
    address = args.address
    command_results = {}

    command_function_mapping = {
        "info": 00,
        "measured": 50,
        "configured": 51
    }

    for command in commands:
        function_number = command_function_mapping.get(command)
        if function_number is not None:
            response = device_client.send_command(function_number, address, 1)
            if response:
                command_results[command] = response
        else:
            print(f"Неизвестная команда: {command}")

    device_client.disconnect()
    result_json = json.dumps(command_results, indent=4)
    print(result_json) if len(result_json) > 2 else None


if __name__ == "__main__":
    main()
