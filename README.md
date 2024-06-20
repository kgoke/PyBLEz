# PyBLEz

PyBLEz is a Python library for creating BLE peripherals using BlueZ and D-Bus. This library allows you to easily set up BLE services and characteristics, handle read and write operations, and send notifications to connected devices.

## Installation

```Bash
pip install PyBLEz
```

## Usage

### Creating a Simple BLE Peripheral

```Python
#!/usr/bin/env python3

import logging
from PyBLE import create_ble_peripheral

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

def main():
    # Create the BLE peripheral instance
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
        print(f"Received from BLE: {data}")

    write_characteristic.WriteValue = write_value

    # Register GATT application
    ble_peripheral.register_application()

    # Start advertising
    ble_peripheral.start_advertising("SimpleBLE", [service.uuid])

    # Run the main loop
    ble_peripheral.run()

if __name__ == "__main__":
    main()

```

### Detailed Explanation

#### Read Characteristic:

- `read_characteristic` is created with the UUID `12345678-1234-5678-1234-56789abcdef1` and is set to return the value "hello".
- The `read_value` function is assigned to the characteristic's `ReadValue` method.

#### Write Characteristic:

- `write_characteristic` is created with the UUID `12345678-1234-5678-1234-56789abcdef2` and allows writing data.
- The `write_value` function is assigned to the characteristic's `WriteValue method`, which prints the received data to the screen.

#### Advertising:

- The peripheral advertises with the local name "SimpleBLE" and includes the service UUID.

#### Running the Peripheral:

- The `run` method starts the main loop to keep the application running and responsive to BLE interactions.

## Requirements

- Python 3.6 or later
- BlueZ (5.41 or later)
- D-Bus (python-dbus)
- GLib
- Logging

## Conrtibuting

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact `goecke.dev@gmail.com`.
