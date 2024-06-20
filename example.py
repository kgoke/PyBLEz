#!/user/bin/env python3

from PyBLEz import create_ble_peripheral
import logging

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

def main():
    ble_peripheral = create_ble_peripheral()
    ble_peripheral.power_on_adapter()

    service = ble_peripheral.add_service("12345678-1234-5678-1234-56789abcdef0")

    characteristic = service.add_characteristic("12345678-1234-5689-1234-56789abcdef1", ["read", "write", "notify"], b"")

    def read_value(options):
        return characteristic.value

    def write_value(value, options):
        data = bytes(value).decode('utf-8')
        print(f"Recived from BLE: {data}")
        processed_value = str(data).upper()
        characteristic.send_notification(processed_value)

    characteristic.ReadValue = read_value
    characteristic.WriteValue = write_value

    ble_peripheral.start_advertising("LabelScanner", [service.uuid])
    ble_peripheral.run()

if __name__ == "__main__":
    main()
