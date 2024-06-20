import dbus
import dbus.service
import logging

AGENT_INTERFACE = "org.bluez.Agent1"

class Agent(dbus.service.Object):
    exit_on_release = True

    def __init__(self,bus, path):
        dbus.service.Object.__init__(self, bus, path)

    def set_exit_on_release(self, exit_on_release):
        self.exit_on_release = exit_on_release

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        logging.info("Release")
        if self.exit_on_release:
            mainloop.quit()

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        logging.info(f"AuthorizeService ({device}, {uuid})")
        authorize = input("Authorize connection (yes/no): ")
        if authorize == "yes":
            return
        raise Rejected("Connection rejected by user")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        logging.info(f"RequestPinCode: ")
        set_trusted(device)
        return input("Enter PIN Code: ")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        logging.info(f"Request Passkey ({device})")
        set_trusted(device)
        passkey = input("Enter passkey: ")
        return dbus.UInt32(passkey)

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def DisplayPinCode(self, device, pincode):
        logging.info(f"DisplayPinCode ({device}, {pincode})")

    @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        logging.info(f"RequestConfirmation ({device}, {passkey:06d})")
        confirm = input("Confirm passkey (yes/no): ")
        if confirm == "yes":
            set_trusted(device)
            return
        raise Rejected("Passkey doesn't match")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        logging.info(f"RequestAuthorization ({device})")
        auth = input("Authorize? (yes/no): ")
        if auth == "yes":
            return
        raise Rejected("Pairing rejected")

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        logging.info("Cancel")

def set_trusted(device_path):
    props = dbus.Interface(
        bus.get_object("org.bluez", device_path), "org.freedesktop.DBus.Properties"
    )
    props.Set("org.bluez.Device1", "Trusted", True)

# custom exception classes
class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"