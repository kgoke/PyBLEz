import dbus.service
import dbus
from .logger import logger

class Characteristic(dbus.service.Object):
    def __init__(self, bus, index, uuid, flags, service, value):
        self.path = f"{service.get_path()}/char{index}"
        self.bus = bus
        self.uuid = uuid
        self.flags = flags      
        self.service = service
        self.value = value
        self.notifying = False
        self.Write = None
        self.Read = None
        dbus.service.Object.__init__(self, bus, self.path)
        logger.debug(f"Characteristic created with UUID {uuid}")

    def get_properties(self):
        return {
            "org.bluez.GattCharacteristic1": {
                "Service": self.service.get_path(),
                "UUID": self.uuid,
                "Flags": self.flags,
                "Notifying": self.notifying,
            }
        }

    @dbus.service.method("org.freedesktop.DBus.Properties", in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        logger.debug(f"GetAll called for characteristic with UUID {self.uuid}")
        return self.get_properties()[interface]

    def get_path(self):
        logger.debug(f"Characteristic path requested: {self.path}")
        return dbus.ObjectPath(self.path)

    @dbus.service.method("org.bluez.GattCharacteristic1", in_signature="a{sv}", out_signature="ay")
    def ReadValue(self, options):
        if self.Read:
            logger.debug(f"Custom read function called for characteristic with UUID {self.uuid}")
            return self.Read(options)
        else:
            logger.debug(f"Read request received for characteristic with UUID {self.uuid}, reading value {self.value}")
            return self.value

    @dbus.service.method("org.bluez.GattCharacteristic1", in_signature="aya{sv}")
    def WriteValue(self, value, options):
        if self.Write:
            logger.debug(f"Custom write function called for characteristic with UUID {self.uuid} with value {value}")
            self.Write(value, options)
        else:
            logger.debug(f"Write request received for characteristic with UUID {self.uuid} with value {value}")  
            self.value = value

    @dbus.service.method("org.bluez.GattCharacteristic1")
    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
        self.PropertiesChanged("org.bluez.GattCharacteristic1", {"Notifying": self.notifying}, [])

    @dbus.service.method("org.bluez.GattCharacteristic1")
    def StopNotifying(self):
        if not self.notifying:
            return
        self.notifying = False
        self.PropertiesChanged("org.bluez.GattCharacteristic1", {"Notifying": self.notifying}, [])

    def send_notification(self, value):
        if not self.notifying:
            return
        self.value = value  
        self.PropertiesChanged("org.bluez.GattCharacteristic1", {"Value": self.value}, [])
