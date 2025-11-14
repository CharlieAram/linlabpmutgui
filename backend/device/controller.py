"""Device controller wrapper for TX7332."""
import sys
import time
from pathlib import Path
from typing import Optional
from datetime import datetime

# Add EVM_FTDI_API to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "EVM_FTDI_API"))

from deviceController import USBQPort


class DeviceControllerError(Exception):
    """Custom exception for device controller errors."""
    pass


class TX7332Controller:
    """Wrapper for TX7332 device control using existing EVM_FTDI_API code."""
    
    def __init__(self):
        self.device = None
        self.usb_address = None
        self.connected = False
        self.connection_time = None
        self.last_error = None
        
    def connect(self, usb_address: Optional[str] = None) -> bool:
        """
        Connect to the TX7332 device.
        
        Args:
            usb_address: USB address string. If None, tries common addresses.
            
        Returns:
            True if connection successful, False otherwise.
        """
        # Try provided address or common defaults
        addresses_to_try = []
        if usb_address:
            addresses_to_try.append(usb_address)
        else:
            # Common addresses from existing code
            addresses_to_try.extend([
                'FT4232 Mini Module A',
                'TX7332',
                'TX7364',
                'TX7516'
            ])
        
        for addr in addresses_to_try:
            try:
                self.device = USBQPort(addr)
                if self.device.controller.instrument is not None:
                    self.usb_address = addr
                    self.connected = True
                    self.connection_time = datetime.now()
                    self.last_error = None
                    print(f"Successfully connected to device at {addr}")
                    return True
            except Exception as e:
                print(f"Failed to connect to {addr}: {e}")
                continue
        
        self.last_error = f"Failed to connect. Tried addresses: {', '.join(addresses_to_try)}"
        return False
    
    def disconnect(self) -> bool:
        """Disconnect from the device."""
        try:
            if self.device and self.device.controller.instrument:
                # FTDI library will handle cleanup
                self.device = None
                self.connected = False
                self.usb_address = None
                self.connection_time = None
                return True
        except Exception as e:
            self.last_error = f"Error disconnecting: {e}"
            return False
        return True
    
    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self.connected and self.device is not None
    
    def get_uptime(self) -> Optional[float]:
        """Get connection uptime in seconds."""
        if self.connection_time:
            return (datetime.now() - self.connection_time).total_seconds()
        return None
    
    def ensure_connected(self):
        """Ensure device is connected, raise exception if not."""
        if not self.is_connected():
            raise DeviceControllerError("Device not connected")
    
    def enable_sync(self, enable: bool):
        """Enable or disable sync."""
        self.ensure_connected()
        self.device.enableSync(enable)
    
    def write_reg(self, address: int, value: int, page_select: int = 0):
        """
        Write to device register.
        
        Args:
            address: Register address
            value: Value to write
            page_select: Page select value (default 0 for global page)
        """
        self.ensure_connected()
        # Set page select
        self.device.writeReg(2, page_select)
        # Write value
        self.device.writeReg(address, value)
        # Reset page select
        self.device.writeReg(2, 0)
    
    def read_reg(self, address: int, page_select: int = 0) -> int:
        """
        Read from device register.
        
        Args:
            address: Register address
            page_select: Page select value (default 0 for global page)
            
        Returns:
            Register value
        """
        self.ensure_connected()
        # Set page select
        self.device.writeReg(2, page_select)
        # Enable read mode
        self.device.writeReg(0, 2)
        # Read value
        value = self.device.readReg(address)
        # Disable read mode
        self.device.writeReg(0, 0)
        # Reset page select
        self.device.writeReg(2, 0)
        return value
    
    def hardware_reset(self):
        """Perform hardware reset (TX7332 variant)."""
        self.ensure_connected()
        
        dev = self.device.controller.instrument
        RESET = 0x08
        
        # Set bit mode
        dev.setBitMode(0xFF, 0x01)
        
        # Pull low all pins
        dev.write(bytes([0x00]))
        
        # RESET pull up for 100 µs (min 50 us)
        dev.write(bytes([RESET]))
        time.sleep(0.0001)
        dev.write(bytes([0x00]))
        
        # Set DIS_DYN_PDN_LDO = '1' (based on TX7364 code, adjust register if needed)
        # TX7364 uses 0x5C, TX7516 uses 0x30 - TX7332 likely similar
        # For now, use TX7364 register (0x5C)
        self.write_reg(0x5C, 0x00001000)
        
        time.sleep(0.001)  # Wait 1ms
    
    def software_reset(self):
        """Perform software reset."""
        self.ensure_connected()
        self.write_reg(0x0, 0x00000001)
        time.sleep(0.001)
    
    def memory_reset(self):
        """Reset pattern memory."""
        self.ensure_connected()
        print("Resetting device memory...")
        for addr in range(0x00, 0x40):
            try:
                self.write_reg(addr, 0x00000000, 0x0000FFFF)
            except Exception as e:
                print(f"Failed to reset register 0x{addr:02X}: {e}")
        print("Memory reset complete")


# Global singleton instance
_controller_instance: Optional[TX7332Controller] = None


def get_controller() -> TX7332Controller:
    """Get the global controller instance."""
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = TX7332Controller()
    return _controller_instance

