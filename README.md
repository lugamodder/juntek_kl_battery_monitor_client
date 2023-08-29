

## Клиенты для получения данных с кулонометра (батарейного монитора) Junktel KL/KG.

**[serial_client.py](https://github.com/lugamodder/juntek_kl_battery_monitor_client/blob/master/serial_client.py "serial_client.py")** предназначен для работы через UART интерфейс напрямую. Возвращает JSON c данными, полученными от устройства функциями R00, R50, R51 (см. описание протокола устройства). Может использоватся в качестве источника данных для Zabbix.

Со стороны устройства - интерфейс RS485, разъем RJ-10 ближе к клеммам.

Распиновка:

 | Пин    | Назначение |
 |--------|:----------:|
 | 1      | RS485 -    |
 | 2      | RS485 +    |
 | 3      | GND        |
 | 4      | NC         |

Клиент запускается со следующим параметрами:

 `serial_client.py -p <com_port> -b <baudrate> -a <address> -c info,measured,configured`
 
где:
 *  *com_port* - пусть к com-порту;
 *  *baudrate*  -скорость com-порта, обычно 115200;
 *  *address* - собственный адрес устройства, обычно 1;
 *  *info,measured,configured* - набор функций, по которым запрашивать данные, соответствуют R00, R50, R51 из документации. можно использовать или все, или частично. От этого будет зависеть что возвращает устройство.

Пример использования:
```python
python3 serial_client.py -p COM4 -b 115200 -a 1 -c info,configured
```
---


**[tcp_client.py](https://github.com/lugamodder/juntek_kl_battery_monitor_client/blob/master/tcp_client.py "tcp_client.py")** предназначен для работы через TCP/IP - UART конвертер, например Elfin-EE11A. Подключение к батарейному монитору аналогичное, по RS485.
TCP-клиент запускается со следующим параметрами:

 `tcp_client.py -s <server_ip> -p <server_port> -a <address> -c info,measured,configured`
 
где:

 *  *server_ip* - IP TCP/IP - UART конвертера;
 *  *server_port*  - номер TCP-порт TCP/IP - UART конвертера;
 *  *address* - собственный адрес устройства, обычно 1;
 *  *info,measured,configured* - набор функций, по которым запрашивать данные, соответствуют R00, R50, R51 из документации. можно использовать или все, или частично. От этого будет зависеть что возвращает устройство.
 
Пример использования:
```python
python3 tcp_client.py -s 192.168.2.22 -p 9999 -a 1 -c measured,info,configured
```
Пример вывода JSON:
```json
{
    "info": {
        "current_sensor": "Sampler",
        "max_voltage": 100,
        "max_current": 100,
        "version": 110,
        "serial_number": 6
    },
    "measured": {
        "voltage": 13.78,
        "current": 0.03,
        "current_signed": -0.03,
        "remaining_battery_capacity": 27.728,
        "cumulative_capacity": 40.412,
        "watt_hour": 0.55726,
        "running_time": 419234,
        "ambient_temperature": 30,
        "output_status": 0,
        "current_direction": 0,
        "battery_life": 55456,
        "internal_resistance": 0.0
    },
    "configured": {
        "overvoltage_protection": 0.0,
        "undervoltage_protection": 0.0,
        "forward_overcurrent_protection": 0.0,
        "negative_overcurrent_protection": -0.0,
        "over_power_protection": 0.0,
        "over_temperature_protection": 0,
        "protection_recovery_time": 0,
        "delay_time": 0,
        "preset_battery_capacity": 30.0,
        "fine_tuning_voltage": 100,
        "fine_tuning_current": 100,
        "temperature_calibration": 100,
        "relay_type": 0,
        "current_multipler": 0,
        "voltage_curve_scale": 1
    }
}
```
