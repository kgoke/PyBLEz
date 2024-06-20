import dbus.service
from .characteristic import Characteristic

class Service(dbus.service.Object):
    PATH_BASE = "/org/bluez/example/service"

    def __init__(self, bus, index, uuid, primary):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.uuid = uuid
        self.primary = primary  
        self.characteristics = []
        dbus.service.Object.__init__(self, bus, self.path)

    def add_characteristic(self, uuid, flags, value=b""):
        characteristic = Characteristic(self.bus, len(self.characteristics), uuid, flags, self, value)
        self.characteristics.append(characteristic)
        return characteristic

    def get_properties(self):
        return {
            "org.bluez.GattService1": {
                "UUID": self.uuid,
                "Primary": self.primary,
                "Characteristics": dbus.Array([chrc.get_path() for chrc in self.characteristics], signature="o"),
            }
        }

    @dbus.service.method("org.freedesktop.DBus.Properties", in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        return self.get_properties()[interface]

    def get_path(self):
        return dbus.ObjectPath(self.path)