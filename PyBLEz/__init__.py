from .core import BLEPeripheral
from .logger import enable_logs, disable_logs

def create_ble_peripheral():
    return BLEPeripheral()

__all__ = ["BLEPeripheral", "create_ble_peripheral", "enable_logs", "disable_logs"] 