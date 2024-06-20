import dbus.service

class Desctiptor(dbus.service.Object):
    def __init__(self, bus, index, uuid, flags, characteristic):
        self.path = f"{characteristic.get_path()}/desk{index}"
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        self.characteristic = characteristic
        dubs.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
            "org.bluez.GattDescriptor1": {
                "Characteristic": self.characteristic.get_path(),
                "UUID": self.uuid,
                "Flags": self.flags,
            }
        }
    
    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method("org.freedesktop.DBus.Properties", in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        return self.get_properties()[interface]

    @dbus.service.method("org.bluez.GattDescriptor1", in_signature="a{sv}", out_signature="ay")
    def ReadValue(self, options):
        return self.value

    @dbus.service.method("org.bluez.GattDescriptor1", in_signature="aya{sv}")
    def WriteValue(self, value, options):
        self.value = value
        