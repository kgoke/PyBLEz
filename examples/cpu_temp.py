#!/user/bin/env python3
import os
from PyBLEz import create_ble_peripheral, enable_logs, disable_logs

# Enable debug logs
enable_logs()

def get_cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp.replace("temp=", "").replace("'C\n", "")

def main():
    # create a BLE peripheral instance
    ble = create_ble_peripheral()
    ble.power_on_adapter()

    # Add a service
    service = ble.add_service("12634d89-d598-4874-8e86-7d042ee07ba7")

    # Add a characteristic to the service
    char = service.add_characteristic("12634d89-d598-4874-8e86-7d042ee07ba8", ["read"], bytearray("0 deg", "utf-8"))

    # read function
    def read_value(options):
        char.value = bytearray(get_cpu_temp() + " deg", "utf-8")
        return char.value
    
    # set read function
    char.Read = read_value

    # Register the GATT application
    ble.register_application()

    # Start advertising
    ble.start_advertising("TempSensor", [service.uuid])

    # Run the main loop
    ble.run()

if __name__ == "__main__":
    main()