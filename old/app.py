import logging
import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

from ble import (
    Advertisement,
    Characteristic,
    Service,
    Application,
    find_adapter,
    Descriptor,
    Agent,
)
import struct
import array
from enum import Enum
import sys
from uuid import uuid1

#main loop
MainLoop = None
try:
    from gi.repository import GLib
    MainLoop = GLib.MainLoop
except ImportError:
    import gobject as GObject
    MainLoop = GObject.MainLoop

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
filelogHandler = logging.FileHandler("logs.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
logHandler.setFormatter(formatter)
filelogHandler.setFormatter(formatter)
logger.addHandler(filelogHandler)
logger.addHandler(logHandler)

mainloop = None

# dbus/bluez
BLUEZ_SERVICE_NAME = "org.bluez"
GATT_MANAGER_IFACE = "org.bluez.GattManager1"
LE_ADVERTISEMENT_IFACE = "org.bluez.LEAdvertisement1"
LE_ADVERTISING_MANAGER_IFACE = "org.bluez.LEAdvertisingManager1"

class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.freedesktop.DBus.Error.InvalidArgs"

class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.NotSupported"

class NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.NotPermitted"

class InvalidValueLenghtException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.InvalidValueLength"

class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.Failed"

def register_app_cb():
    logger.info("GATT application registered")

def register_app_error_cb(error):
    logger.critical("Failed to register application: " + str(error))
    mainloop.quit()

class HelloWorldService(Service):
    HELLO_SVC_UUID = "12634d89-d598-4874-8e86-7d042ee07ba7" 

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.HELLO_SVC_UUID, True)
        self.add_characteristic(HelloWorldCharacteristic(bus, 0, self))

class HelloWorldCharacteristic(Characteristic):
    HELLO_CHRC_UUID = "4116f8d2-9f66-4f58-a53d-fc7440e7c14e"
    description = b"Hello World Characteristic"

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, self.HELLO_CHRC_UUID, ["read", "write"], service)
        self.value = bytearray("Hello World", "utf-8")
        self.add_descriptor(CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        logger.info("Read Hello World characteristic")
        return self.value

    def WriteValue(self, value, options):
        logger.info(f"Write Hello World characteristic: {bytes(value).decode('utf-8')}")
        self.value = value

class CharacteristicUserDescriptionDescriptor(Descriptor):
    CUD_UUID = "2901"

    def __init__(self, bus, index, characteristic):
        self.value = array.array("B", characteristic.description).tolist()
        Descriptor.__init__(self, bus, index, self.CUD_UUID, ["read"], characteristic)

    def ReadValue(self, options):
        return self.value

class HelloWorldAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, "peripheral")
        self.add_manufacturer_data(0xFFFF, [0x70, 0x74])
        self.add_service_uuid(HelloWorldService.HELLO_SVC_UUID)
        self.add_local_name("VanaPi")
        self.include_tx_power = True

def register_ad_cb():
    logger.info("Advertisement registered")

def register_ad_error_cb(error):
    logger.critical("Failed to register advertisement: " + str(error))
    mainloop.quit()


AGENT_PATH = "/com/vanamatic/agent"


def main():
    print("Starting...")
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    logger.debug("Fiding adapter...")

    adapter = find_adapter(bus)

    if not adapter:
        logger.critical("GattManager1 interface not found")
        return

    logger.debug(f"Adapter found: {adapter}")
    logger.debug(f"Powering on Adapter...")

    adapter_obj = bus.get_object(BLUEZ_SERVICE_NAME, adapter)
    adapter_props = dbus.Interface(adapter_obj, "org.freedesktop.DBus.Properties")
    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    logger.debug("Adapter powered on")

    service_manager = dbus.Interface(adapter_obj, GATT_MANAGER_IFACE)
    ad_manager = dbus.Interface(adapter_obj, LE_ADVERTISING_MANAGER_IFACE)

    advertisement = HelloWorldAdvertisement(bus, 0)
    agent = Agent(bus, AGENT_PATH)

    app = Application(bus)
    app.add_service(HelloWorldService(bus, 0))

    mainloop = MainLoop()

    agent_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez"), "org.bluez.AgentManager1")
    agent_manager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")
    
    logger.debug("Registering Advertisement")

    ad_manager.RegisterAdvertisement(
        advertisement.get_path(),
        {},
        reply_handler=register_ad_cb,
        error_handler=register_ad_error_cb,
    )

    logger.debug("Registering GATT application..")

    service_manager.RegisterApplication(
        app.get_path(),
        {},
        reply_handler=register_app_cb,
        error_handler=register_app_error_cb,
    )

    agent_manager.RequestDefaultAgent(AGENT_PATH)

    mainloop.run()

    print("Done...")

if __name__ == "__main__":
    main()

