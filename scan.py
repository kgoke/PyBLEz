# main file for the BLE Peripheral
from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
    print("{} - {}".format(name, address))
