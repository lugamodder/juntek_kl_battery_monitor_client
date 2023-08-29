import socket
import json
import argparse
import sys
from kl_junctek import calculate_checksum, parse_response, parse_r00_response, parse_r50_response, parse_r51_response

# Создаем парсер аргументов командной строки
parser = argparse.ArgumentParser(description="TCP Client for JUNCTEK KL-F device")
parser.add_argument("server_host", type=str, help="Server host IP")
parser.add_argument("server_port", type=int, help="Server port number")
parser.add_argument("communication_address", type=int, help="Communication address")
parser.add_argument("commands", nargs="+", choices=["info", "measured", "configured"], help="Commands to run")

# Получаем аргументы из командной строки
args = parser.parse_args()

# Используем аргументы для установки соединения
server_host = args.server_host
server_port = args.server_port


class DeviceClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.settimeout(3)
            self.client_socket.connect((self.server_host, self.server_port))
        except TimeoutError:
            print("Не удалось установить соединение с сервером. Проверьте параметры и доступность сервера.")
            sys.exit(1)
        except socket.timeout:
            print("Превышено время ожидания при установке соединения.")
            sys.exit(1)

    def send_command(self, function_number, communication_address, data_field):
        try:
            calculated_checksum = calculate_checksum([data_field])

            command = f":R{function_number:02d}={communication_address},{calculated_checksum},{data_field},\r\n"
            self.client_socket.sendall(command.encode())
            response = self.client_socket.recv(1024).decode()
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
                print("Не удалось распарсировать ответ.")

        except socket.timeout:
            pass
            print("Превышено время ожидания ответа.")
        except Exception as e:
            print("Произошла ошибка при отправке или приеме:", e)

    def disconnect(self):
        self.client_socket.close()


def main():
    device_client = DeviceClient(server_host, server_port)
    device_client.connect()
    communication_address = args.communication_address
    command_results = {}

    command_function_mapping = {
        "info": 00,
        "measured": 50,
        "configured": 51
    }

    for command in args.commands:
        function_number = command_function_mapping.get(command)
        if function_number is not None:
            response = device_client.send_command(function_number, communication_address, 1)
            if response:
                command_results[command] = response
        else:
            print(f"Неизвестная команда: {command}")

    device_client.disconnect()
    result_json = json.dumps(command_results, indent=4)
    print(result_json) if len(result_json) > 2 else None


if __name__ == "__main__":
    main()
