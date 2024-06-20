import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import logging

from .service import Service
from .advertisement import Advertisement
from .agent import Agent
from .application import Application

logger = logging.getLogger(__name__)

class BLEPeripheral:
    def __init__(self):
        # set up the main loop
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.bus = dbus.SystemBus()
        self.adapter = self.find_adapter()
        if not self.adapter:
            raise Exception("Bluetooth adapter not found")
        self.services = []
        self.mainloop = GLib.MainLoop()

    def find_adapter(self):
        remote_om = dbus.Interface(self.bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
        objects = remote_om.GetManagedObjects()
        for path, interfaces in objects.items():
            if "org.bluez.GattManager1" in interfaces:
                return path
        return None

    def add_service(self, uuid, primary=True):
        service = Service(self.bus, len(self.services), uuid, primary)
        self.services.append(service)
        return service

    def start_advertising(self, local_name, service_uuids):
        ad_manager = dbus.Interface(self.bus.get_object("org.bluez", self.adapter), "org.bluez.LEAdvertisingManager1")
        advertisement = Advertisement(self.bus, 0, "peripheral", local_name, service_uuids)
        ad_manager.RegisterAdvertisement(
            advertisement.get_path(),
            {},
            reply_handler=self.advertisement_registered,
            error_handler=self.advertisement_error
        )

    def advertisement_registered(self):
        logger.info("Advertisement registered")

    def advertisement_error(self, error):
        logger.error(f"Failed to register advertisement: {error}")
        self.mainloop.quit()

    def run(self):
        self.mainloop.run()

    def power_on_adapter(self):
        adapter_props = dbus.Interface(self.bus.get_object("org.bluez", self.adapter), "org.freedesktop.DBus.Properties")
        adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))
        logger.info("Adapter powered on")

    def register_application(self):
        app = Application(self.bus)
        for service in self.services:
            app.add_service(service)
        service_manager = dbus.Interface(self.bus.get_object("org.bluez", self.adapter), "org.bluez.GattManager1")
        service_manager.RegisterApplication(
            app.get_path(),
            {},
            reply_handler=self.application_registered,
            error_handler=self.application_error
        )

    def application_registered(self):
        logger.info("GATT application registered")

    def application_error(self, error):
        logger.error(f"Failed to register applicaiton: {error}")
        self.mainloop.quit()
