#!/user/bin/env python3

from PyBLEz import create_ble_peripheral
import logging

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
fileLogHandler = logging.FileHandler("logs.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
logHandler.setFormatter(formatter)
fileLogHandler.setFormatter(formatter)
logger.addHandler(fileLogHandler)
logger.addHandler(logHandler)

def main():
    # Create  BLE peripheral instance
    ble_peripheral = create_ble_peripheral()
    ble_peripheral.power_on_adapter()

    # Add a service
    service = ble_peripheral.add_service("12345678-1234-5678-1234-56789abcdef0")

    # Add a read characteristic
    read_characteristic = service.add_characteristic("12345678-1234-5678-1234-56789abcdef1", ["read"], bytearray("hello", "utf-8"))

    def read_value(options):
        return read_characteristic.value

    read_characteristic.ReadValue = read_value

    # Add a write characteristic
    write_characteristic = service.add_characteristic("12345678-1234-5678-1234-56789abcdef2", ["write"], b"")

    def write_value(value, options):
        data = bytes(value).decode("utf-8")
        print(f"Recieved from BLE: {data}")

    write_characteristic.WriteValue = write_value

    # Register GATT application
    ble_peripheral.register_application()

    # Start Advertising
    ble_peripheral.start_advertising("SimpleBLE", [service.uuid])

    # Run the main loop
    ble_peripheral.run()


if __name__ == "__main__":
    main()
