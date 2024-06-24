import dbus.service
from .logger import logger

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
        logger.debug(f"Advertisement created with type {ad_type}")

    def get_properties(self):
        properties = {
            "Type": self.ad_type,
            "LocalName": dbus.String(self.local_name),
            "ServiceUUIDs": dbus.Array(self.service_uuids, signature="s"),
            "IncludeTxPower": dbus.Boolean(self.include_tx_power)
        }
        logger.debug(f"GetProperties called for advertisement with type {self.ad_type}")
        return {"org.bluez.LEAdvertisement1": properties}

    def get_path(self):
        logger.debug(f"Advertisement path requested: {self.path}")
        return dbus.ObjectPath(self.path)

    @dbus.service.method("org.freedesktop.DBus.Properties", in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        logger.debug(f"GetAll called for advertisement with type {self.ad_type}")
        return self.get_properties()[interface]

    @dbus.service.method("org.bluez.LEAdvertisement1", in_signature="", out_signature="")
    def Release(self):
        logger.debug(f"Release called for advertisement with type {self.ad_type}")
        pass