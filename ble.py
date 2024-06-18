import time
from bluetooth.ble import BeaconService
from uuid import uuid1
import dbus

class BLEPeripheral:
	def __init__(self, uuid, major, minor, tx_power, interval, local_name):
		self.service = BeaconService()
		self.uuid = uuid
		self.major = major
		self.minor = minor
		self.tx_power = tx_power
		self.interval = interval
		self.local_name = local_name
		self.characteristics = {}
		self.advertising = False
		
	def add_characteristics(self, uuid, initial_value, properties):
		self.characteristics[uuid] = {
			'value': initial_value,
			'properties': properties
		}
		
	def start_advertising(self):
		self.service.start_advertising(self.uuid, self.major, self.minor, self.tx_power, self.interval)
		self.advertising = True
		print(f"Started advertising with UUID: {self.uuid}, Local Name: {self.local_name}")
		
	def stop_advertising(self):
		self.service.stop_advertising()
		self.advertising = False
		print("Stopped advertising")
		
	def handle_read(self, uuid):
		if uuid in self.characteristics:
			return self.characteristics[uuid]['value']
		return None
		
	def handle_write(self, uuid, value):
		if uuid in self.characteristics and 'write' in self.characteristics[uuid]['properties']:
			self.characteristics[uuid]['value'] = value
			return True
		return False
		
	def advertise_for(self, duration):
		self.start_advertising()
		time.sleep(duration)
		self.stop_advertising()
		
if __name__ == "__main__":
	service_uuid = str(uuid1()).upper()
	major = 1
	minor = 1
	tx_power = 1
	interval = 200
	local_name = "raspberrypi"
	
	ble_peripheral = BLEPeripheral(service_uuid, major, minor, tx_power, interval, local_name)
	
	# add characteristics
	char_
	initial_value = "Hello BLE"
	properties = ['read', 'write']
	ble_peripheral.add_characteristics(char_uuid, initial_value, properties)
	
	
	# advertise for 60 seconds
	ble_peripheral.advertise_for(30)
	
	print("Done.")
