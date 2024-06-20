import dbus.service

class Advertisement(dbus.service.Object):
    PATH_BASE = "/org/bluez/example/Advertisement"

    def __init__(self, bus, index, ad_type, local_name, service_uuids):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.ad_type = ad_type
        self.local_name = local_name
        self.service_uuids = service_uuids      
        self.include_tx_power = True
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        properties = {
            "Type": self.ad_type,
            "LocalName": dbus.String(self.local_name),
            "ServiceUUIDs": dbus.Array(self.service_uuids, signature="s"),
            "IncludeTxPower": dbus.Boolean(self.include_tx_power)
        }
        return {"org.bluez.LEAdvertisement1": properties}

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method("org.freedesktop.DBus.Properties", in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        return self.get_properties()[interface]

    @dbus.service.method("org.bluez.LEAdvertisement1", in_signature="", out_signature="")
    def Release(self):
        pass