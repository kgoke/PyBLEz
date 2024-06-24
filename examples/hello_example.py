#!/user/bin/env python3
import logging
from PyBLEz import create_ble_peripheral, enable_logs, disable_logs

# Enable debug logs
enable_logs()

def main():
    # create a BLE peripheral instance
    ble = create_ble_peripheral()
    ble.power_on_adapter()

    # Add a service
    service = ble.add_service("12345678-1234-5678-1234-56789abcdef0")

    # Add a characteristic to the service
    char = service.add_characteristic("12345678-1234-5678-1234-56789abcdef1", ["read", "write"], bytearray("Hello", "utf-8"))

    # Defind the read_value function
    def read_value(options):
        return char.value
    
    char.ReadValue = read_value

    # Define the write_value function
    def write_value(value, options):
        data = bytes(value).decode("utf-8")
        print(f"Received: {data}")
        processed = data.upper()
        char.value = bytearray(processed, "utf-8")
        print(f"Processed: {processed}")

    char.custom_write = write_value

    # Register the GATT application
    ble.register_application()

    # Start advertising
    ble.start_advertising("HelloBLE", [service.uuid])

    # Run the main loop
    ble.run()

if __name__ == "__main__":
    main()