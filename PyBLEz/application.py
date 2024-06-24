import dbus.service
from .logger import logger

class Application(dbus.service.Object):
    def __init__(self, bus):
        self.path = "/"
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)
        logger.debug("Application created")


    def get_path(self):
        logger.debug(f"Application path requested: {self.path}")    
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        logger.debug(f"Added service with UUID {service.uuid}")
        self.services.append(service)

    @dbus.service.method("org.freedesktop.DBus.ObjectManager", out_signature="a{oa{sa{sv}}}")
    def GetManagedObjects(self):
        response = {}
        for service in self.services:
            response[service.get_path()] = service.get_properties()
            for chrc in service.characteristics:
                response[chrc.get_path()] = chrc.get_properties()
        logger.debug("GetManagedObjects called")
        return response
