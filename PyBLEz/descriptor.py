import dbus.service
from .logger import logger

class Desctiptor(dbus.service.Object):
    def __init__(self, bus, index, uuid, flags, characteristic):
        self.path = f"{characteristic.get_path()}/desk{index}"
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        self.characteristic = characteristic
        dbus.service.Object.__init__(self, bus, self.path)
        logger.debug(f"Descriptor created with UUID {uuid}")

    def get_properties(self):
        logger.debug(f"GetProperties called for descriptor with UUID {self.uuid}")
        return {
            "org.bluez.GattDescriptor1": {
                "Characteristic": self.characteristic.get_path(),
                "UUID": self.uuid,
                "Flags": self.flags,
            }
        }
    
    def get_path(self):
        logger.debug(f"Descriptor path requested: {self.path}") 
        return dbus.ObjectPath(self.path)

    @dbus.service.method("org.freedesktop.DBus.Properties", in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        logger.debug(f"GetAll called for descriptor with UUID {self.uuid}")
        return self.get_properties()[interface]

    @dbus.service.method("org.bluez.GattDescriptor1", in_signature="a{sv}", out_signature="ay")
    def ReadValue(self, options):
        logger.debug(f"Read request received for descriptor with UUID {self.uuid}")
        return self.value

    @dbus.service.method("org.bluez.GattDescriptor1", in_signature="aya{sv}")
    def WriteValue(self, value, options):
        logger.debug(f"Write request received for descriptor with UUID {self.uuid} with value {value}")
        self.value = value
        